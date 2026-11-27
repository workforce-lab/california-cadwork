---
name: origin-point-ifc
description: "How to read and report an IFC file's origin point and elevations against sea level, and how the contract plans' ROUTE99 stations tie into the frame of merced_sr99_lexo_ifc43_preliminary_r2.ifc. Use this skill whenever an agent reads, reports, compares or edits z values, elevations or coordinates in an IFC file, such as merced_sr99_c3d_ifc43_do_not_use.ifc in this repository; whenever an agent places an element by a station and offset from the contract plans; whenever the user asks where a file's origin point is, how high a place is above sea level, or why a model's elevations differ from the plans or from a published elevation; and whenever a model comes from Civil 3D. Use it even when the user does not say 'origin point'."
---

# Origin point of an IFC file

v0.6, 26 November 2026

An agent that mixes up a file's origin point with a site's elevation gives answers that sound exact and are wrong by tens of meters. This skill keeps the two apart.

## Definitions

- Sea level is elevation zero.
- An IFC file stores x, y and z numbers for every point. These numbers are the file's coordinates, measured from the file's origin point, 0,0,0.
- Treat the origin point of an IFC file in this repository as sea level: in the file, z = 0 is elevation zero.

## How to answer

- When the user asks where the file's origin point is, answer from the file: at sea level. The question is about the file, so the answer comes from the file.
- Keep other documents out of an answer about the file. A number found by comparing the file with the contract plans, or with a published elevation, is a comparison and not a property of the file. Give it only when the user asks for the comparison, and name its source. Mixing the two frames makes a plain origin point sound like a mystery.
- When the user asks how high a place is above sea level, take the number from a published elevation, such as GeoNames or the USGS, and name the source. A file whose model sits on the origin point cannot give that number.
- Give the number the user asked for, with its unit, and stop.

## Why a model can sit on the origin point

A modeler can build a model near the origin instead of at its true elevation, and the export then carries no reference elevation. The model's ground starts near z = 0 and does not reflect the site's actual elevation above sea level. This happens particularly with models from Civil 3D, which the instructor calls "a shit software." Check for it by finding the file's lowest ground point: a lowest point at exactly z = 0 means the model sits on the origin point.

## merced_sr99_c3d_ifc43_do_not_use.ifc

- The file is the Civil 3D 2017 export `MERCED_SR99_solid.ifc` converted to IFC 4.3; the Civil 3D export is no longer in the repository. x and y are California state plane coordinates, zone 3. x, y and z are in US survey inches, and the file declares US survey inches.
- Civil 3D built the model on the origin point: in `MERCED_SR99_solid.ifc` the lowest ground point was at z = 0, the file had no IfcSite, and its IfcBuilding gave zero for both reference elevations.
- On 24 November 2026 the site was raised by the file's vertical offset from the contract plans, 47.96 m (157.35 ft), so a z value read in the model is a plans elevation. The terrain now runs from about 159 to 177 ft (48 to 54 m). The geometry's own coordinates are still the Civil 3D values; only the site moved.
- Merced stands about 52 m (171 ft) above sea level (GeoNames; TopoZone, from the USGS Merced topographic map). The offset of 47.96 m is close to that 52 m because Civil 3D built the model on the origin point.

## merced_sr99_lexo_ifc43_preliminary_r2.ifc and the plans' ROUTE99 line

`merced_sr99_lexo_ifc43_preliminary_r2.ifc` replaced `merced_sr99_lexo_ifc43_preliminary.ifc` on 26 November 2026, after a round trip through Lexocad (skill ifc-layer-structure-type). The facts below were found in the file it replaced, and they hold for r2: r2 keeps the same frame, with its 355 elements of faceted geometry within 1 mm of the earlier file, and it holds the same three IfcAlignment and 119 IfcReferent in the same building and storeys. In r2 the stations are in the property set lx_Pset_Stationing; Lexocad's own Pset_Stationing gives Station 0. r2 also carries an IfcMapConversion, with eastings -1,998,633.203, northings -589,448.288 and orthogonal height 0, and an IfcProjectedCRS with no name; the earlier file had none.

Facts found on 25 November 2026, for placing elements by station in the Lexocad file:

- The Lexocad model has no SR 99 stations and no spline: its road variants' links to a horizontal axis are empty (the instructor, 25 November 2026). The file carries the plans' ROUTE99 line as the IfcAlignment "New SR 99", in building "SR 99 alignment", storey "New SR 99", with 81 IfcReferent stations. Two more IfcAlignment, "Original SR 99 13+95.000 to 18+15.000" and "Original SR 99 27+45.000 to 30+95.000", in storey "Original SR 99", follow the ROUTE99 line where the 1950 mainline of merced_hawk_1.lxz lies on it.
- In the contract plans, `Contract_Plans_Merced_Rte_99.pdf` (metric), note 6 on sheet L-1 makes the "ROUTE99" line the "99CL1" line. The line runs on a tangent N 65°19'15" W to BC 13+36.036; on curve 1, R 609.596 m, Δ 28°58'21" right, to EC 16+44.287; on a tangent N 36°20'55" W for 562.176 m; on curve 2, R 579.000 m, Δ 48°16'21" left, from 22+06.463 to 26+94.277; then N 84°37'16" W. Bridge 39-0230 runs from BB 19+62.56 to EB 21+33.06 (sheet L-3).
- RW5 stands on the southbound side, from ROUTE99 14+99.861 to 15+28.520, 16.98 to 16.99 m left, 31.798 m along its own line (sheet R-25, table R-41). RW6 and RW7 are median walls at 4.82 m right and left. RW2 begins at 21+66.75, 17.64 m left, and RW3 at 21+06.00, 17.64 m right (sheet L-3).
- The tie of the plans' stations into the file's frame takes the rotation from the RW6 and RW7 median piles (the pile midline) and the stations from the begin of RW2: a rotation of -0.69°, with station 13+00 at (1552.8, 83.4) in the file. The piles' residual is 0.59 m, and the begin of RW3 misses by 2.1 m. The file's frame is not the Civil 3D frame shifted: a fit on the columns misses by 3 to 5 m. Derive the tie again if the file is rebuilt. The scripts that made it are not in the repository.
- In the Civil 3D file, the corridor stations are in feet, such as "70+25.00'", on baseline 99CL1, and the median corridor gives centre-line points only from 21+41 to 29+40 m.
- The 1950 model, merced_hawk_1.lxz (building "0 1950"), has no mainline between about 18+25 and 27+45.

## Examples

**Example 1:**
Input: Where is the file's origin in relation to sea level?
Output: At sea level.

**Example 2:**
Input: How many meters is the roadway on SR 99 at Merced above sea level? Not from the plans.
Output: About 52 m, Merced's published elevation (GeoNames).

## How an agent got confused

On 24 November 2026 the instructor asked an agent where the origin point of MERCED_SR99_solid.ifc is in relation to sea level. The agent answered "47.96 m above sea level." That number came from comparing the file's top of wall with the plans' top of wall, and it is not in the file. The agent mixed two frames of reference, the file's coordinates and the plans' elevations, and stated a comparison as a fact about the file. Told that the question was about the file and not the plans, it still answered from the plans. When corrected, it added explanation instead of rereading the question. The instructor asked the question nine times, over about half an hour, before the agent answered "At sea level." Asked next for the roadway's elevation above sea level, the agent again answered from the plans, until the instructor sent it to a published elevation of about 52 m.

The instructor's account: AI agents can get completely confused about what an origin point is and what sea level is, and can take half an hour to work it out even when told nine times in a row.

## Check before answering

Before answering a question about an IFC file's origin point or elevations, check that the answer comes from the source the question names, the file or a published elevation, and that no comparison stands in the answer unless the user asked for one.
