"""Lay K-rail sections in an IFC file, by the steps of the skill k-rail.

Usage:
    python -I lay_k_rail.py FILE.ifc --line ID[,ID...] [--line ID[,ID...]] ...

Each --line names the elements that together hold one line of barrier, in any
order: for example a short box and the curved run it meets end to end. The
script reads FILE.ifc with ifcopenshell (read only), works out each line's base
centre line from the elements' own geometry, and then edits FILE.ifc as text:

- it appends one IfcWallType "K-rail" (PARAPET) with one New Jersey section as
  its representation map, a property set "K-rail", an IfcRelDefinesByType and
  an IfcRelDeclares to the project;
- it replaces the IfcProductDefinitionShape line of each element so that its
  body is a mapped representation, one IfcMappedItem per section.

It deletes no line. The old geometry lines stay in the file, unreferenced,
because their points can be shared with other elements. It never saves the file
through ifcopenshell, which would change every line.

The centre line is found from a triangulated body, such as the surface models
that Lexocad exports for a barrier: the vertices are grouped into cross-section
stations along the element's long axis, and each station gives the mean of its
x and y and the least z. This holds for a barrier body that is a swept box. For
another kind of body, check the stations in a plan view before you trust them.
"""
import argparse, math, sys
import numpy as np
import ifcopenshell, ifcopenshell.geom, ifcopenshell.guid
import ifcopenshell.util.placement as P

SEC, LAY = 6.045, 6.096          # section length and laying length, m (skill k-rail)
HALF_BASE, HEIGHT = 0.305, 0.8128
BREAK, REVEAL = 0.3302, 0.0762


def profile():
    xb = HALF_BASE - 0.254 / math.tan(math.radians(55))      # lower slope rises 10 in
    xt = xb - 0.4826 / math.tan(math.radians(84))            # upper slope rises 19 in
    return [(HALF_BASE, 0), (HALF_BASE, REVEAL), (xb, BREAK), (xt, HEIGHT),
            (-xt, HEIGHT), (-xb, BREAK), (-HALF_BASE, REVEAL), (-HALF_BASE, 0)]


def stations(f, s, eid):
    v = np.array(ifcopenshell.geom.create_shape(s, f.by_id(eid)).geometry.verts).reshape(-1, 3)
    v = np.unique(np.round(v, 4), axis=0)
    c = v[:, :2].mean(0)
    a = np.linalg.svd(v[:, :2] - c)[2][0]
    t = (v[:, :2] - c) @ a
    o = np.argsort(t); v, t = v[o], t[o]
    groups, cur = [], [0]
    for i in range(1, len(v)):
        if t[i] - t[i - 1] > 1.0:
            groups.append(cur); cur = [i]
        else:
            cur.append(i)
    groups.append(cur)
    return np.array([[*v[g, :2].mean(0), v[g, 2].min()] for g in groups])


def join(pieces):
    """Join station polylines that meet end to end into one polyline."""
    pts, lab = pieces[0][1], [pieces[0][0]] * (len(pieces[0][1]) - 1)
    rest = pieces[1:]
    while rest:
        best = None
        for k, (eid, q) in enumerate(rest):
            for rev_p in (False, True):
                for rev_q in (False, True):
                    p2 = pts[::-1] if rev_p else pts
                    q2 = q[::-1] if rev_q else q
                    d = np.linalg.norm(p2[-1][:2] - q2[0][:2])
                    if best is None or d < best[0]:
                        best = (d, k, rev_p, rev_q)
        d, k, rev_p, rev_q = best
        eid, q = rest.pop(k)
        if rev_p:
            pts, lab = pts[::-1], lab[::-1]
        q = q[::-1] if rev_q else q
        q = q[1:] if d < 0.5 else q
        pts = np.vstack([pts, q]); lab = lab + [eid] * len(q)
        print(f"  joined #{eid}: gap {d:.3f} m")
    return pts, lab


def at(pts, cum, d):
    i = min(max(np.searchsorted(cum, d) - 1, 0), len(pts) - 2)
    u = (d - cum[i]) / (cum[i + 1] - cum[i])
    return pts[i] + u * (pts[i + 1] - pts[i]), i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ifc")
    ap.add_argument("--line", action="append", required=True)
    args = ap.parse_args()
    lines_ids = [[int(x) for x in l.split(",")] for l in args.line]
    elems = [e for l in lines_ids for e in l]

    f = ifcopenshell.open(args.ifc)
    s = ifcopenshell.geom.settings(); s.set("use-world-coords", True)
    first = f.by_id(elems[0])
    OH = first.OwnerHistory.id() if first.OwnerHistory else None
    body = [r for r in first.Representation.Representations if r.RepresentationIdentifier == "Body"]
    CTX = (body[0] if body else first.Representation.Representations[0]).ContextOfItems.id()
    PROJ = f.by_type("IfcProject")[0].id()
    oh = f"#{OH}" if OH else "$"

    sections = {e: [] for e in elems}
    for ids in lines_ids:
        pts, lab = join([(e, stations(f, s, e)) for e in ids])
        seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
        cum = np.concatenate([[0], np.cumsum(seg)]); L = cum[-1]
        n = 1 + round((L - SEC) / LAY); run = (n - 1) * LAY + SEC; s0 = (L - run) / 2
        print(f"line {ids}: length {L:.3f} m, {n} sections, run {run:.3f} m, each end moves {s0:.3f} m")
        if s0 > 1.524 + 1e-6 or s0 < -1.524 - 1e-6:
            print("  warning: an end moves more than 5 ft")
        for k in range(n):
            d = s0 + k * LAY
            p0, _ = at(pts, cum, d); p1, _ = at(pts, cum, d + SEC); _, im = at(pts, cum, d + SEC / 2)
            z3 = (p1 - p0) / np.linalg.norm(p1 - p0)
            x1 = np.cross([0, 0, 1], z3); x1 /= np.linalg.norm(x1)
            y2 = np.cross(z3, x1)
            sections[lab[im]].append((p0, x1, y2, z3))

    nid = [max(e.id() for e in f) + 1]
    new = []

    def ent(txt):
        i = nid[0]; nid[0] += 1; new.append(f"#{i}={txt};"); return i

    def r(x):
        x = 0.0 if abs(x) < 5e-10 else float(x)
        return ("%.6f" % x).rstrip("0")

    def pt(c): return ent("IFCCARTESIANPOINT((%s))" % ",".join(r(x) for x in c))
    def dr(c): return ent("IFCDIRECTION((%s))" % ",".join(r(x) for x in c))
    g = ifcopenshell.guid.new

    prof = profile()
    pp = [pt(c) for c in prof]
    poly = ent("IFCPOLYLINE((%s))" % ",".join(f"#{i}" for i in pp + [pp[0]]))
    pdef = ent(f"IFCARBITRARYCLOSEDPROFILEDEF(.AREA.,'K-rail New Jersey shape',#{poly})")
    ax = ent(f"IFCAXIS2PLACEMENT3D(#{pt((0, 0, 0))},$,$)")
    solid = ent(f"IFCEXTRUDEDAREASOLID(#{pdef},#{ax},#{dr((0, 0, 1))},{r(SEC)})")
    mrep = ent(f"IFCSHAPEREPRESENTATION(#{CTX},'Body','SweptSolid',(#{solid}))")
    rmap = ent(f"IFCREPRESENTATIONMAP(#{ax},#{mrep})")
    props = [
        ("Name", "IFCTEXT('Temporary Railing (Type K), Caltrans')"),
        ("Shape", "IFCTEXT('New Jersey safety shape')"),
        ("SectionLength", "IFCLENGTHMEASURE(6.045)"),
        ("LayingLength", "IFCLENGTHMEASURE(6.096)"),
        ("BaseWidth", "IFCLENGTHMEASURE(0.61)"),
        ("Height", "IFCLENGTHMEASURE(0.8128)"),
        ("TopWidth", "IFCLENGTHMEASURE(0.1524)"),
        ("MassPerSection", "IFCMASSMEASURE(3630.)"),
        ("Connection", "IFCTEXT('pin and loop, pins 31.8 mm by 660 mm')"),
        ("Source", "IFCTEXT('Skill k-rail; numbers not yet checked against Caltrans Standard Plan T3A')"),
    ]
    pids = [ent(f"IFCPROPERTYSINGLEVALUE('{n}',$,{v},$)") for n, v in props]
    pset = ent(f"IFCPROPERTYSET('{g()}',{oh},'K-rail','Facts from the skill k-rail',({','.join('#%d' % i for i in pids)}))")
    wtype = ent(f"IFCWALLTYPE('{g()}',{oh},'K-rail','Temporary Railing (Type K) of Caltrans, one section',$,(#{pset}),(#{rmap}),$,'Temporary Railing (Type K)',.PARAPET.)")

    replace = {}
    for eid in elems:
        e = f.by_id(eid)
        M = np.array(P.get_local_placement(e.ObjectPlacement)); R, T = M[:3, :3], M[:3, 3]
        items = []
        for p0, x1, y2, z3 in sections[eid]:
            op = ent("IFCCARTESIANTRANSFORMATIONOPERATOR3D(#%d,#%d,#%d,1.,#%d)"
                     % (dr(R.T @ x1), dr(R.T @ y2), pt(R.T @ (p0 - T)), dr(R.T @ z3)))
            items.append(ent(f"IFCMAPPEDITEM(#{rmap},#{op})"))
        if not items:
            print(f"  note: #{eid} holds no section midpoint and keeps its old body")
            continue
        rep = ent(f"IFCSHAPEREPRESENTATION(#{CTX},'Body','MappedRepresentation',({','.join('#%d' % i for i in items)}))")
        pds = e.Representation.id()
        replace[pds] = f"#{pds}=IFCPRODUCTDEFINITIONSHAPE($,$,(#{rep}));"
    typed = [e for e in elems if sections[e]]
    ent(f"IFCRELDEFINESBYTYPE('{g()}',{oh},$,$,({','.join('#%d' % i for i in typed)}),#{wtype})")
    ent(f"IFCRELDECLARES('{g()}',{oh},$,$,#{PROJ},(#{wtype}))")

    raw = open(args.ifc, newline="").read()
    eol = "\r\n" if "\r\n" in raw[:2000] else "\n"
    rows = raw.splitlines()
    endsec = [i for i, l in enumerate(rows) if l == "ENDSEC;"][-1]
    out, hit = [], 0
    for i, l in enumerate(rows):
        if i == endsec:
            out.extend(new)
        k = l.split("=", 1)[0]
        if k.startswith("#") and k[1:].isdigit() and int(k[1:]) in replace:
            out.append(replace[int(k[1:])]); hit += 1
        else:
            out.append(l)
    open(args.ifc, "w", newline="").write(eol.join(out) + eol)
    area = 0.5 * abs(sum(prof[i][0] * prof[(i + 1) % 8][1] - prof[(i + 1) % 8][0] * prof[i][1] for i in range(8)))
    print("sections per element:", {e: len(v) for e, v in sections.items()})
    print(f"one section: area {area:.5f} m2, volume {area * SEC:.5f} m3")
    print(f"replaced {hit} lines, appended {len(new)} lines")


if __name__ == "__main__":
    sys.exit(main())
