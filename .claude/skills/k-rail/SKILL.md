---
name: k-rail
description: "What K-rail is, its dimensions, where it is used and how it behaves when hit, each with its source, and how to model it in an IFC file as one K-rail type whose sections are its instances. Use this skill whenever the user says K-rail, Krail, Type K, Temporary Railing (Type K), temporary barrier, portable concrete barrier, Jersey barrier or barrier type K; whenever a model, a plan or a schedule needs a temporary barrier for stage construction, traffic handling, falsework, a bridge deck edge or an excavation; and whenever an agent adds, changes or checks a temporary barrier in an IFC file. Use it even when the user does not say K-rail."
---

# K-rail

v0.4, 26 November 2026

K-rail is the common name for Temporary Railing (Type K) of Caltrans, the California Department of Transportation: precast concrete sections of the New Jersey safety shape, joined end to end by a pin through steel loops. A temporary barrier drawn as a plain box, or a K-rail number given without its source, leaves the user a model and a number that cannot be checked. This skill gives each fact with its source, and the one way this repository models K-rail.

## Facts and their sources

Each fact names its source from the list at the end. A number that this skill works out is marked derived. Caltrans's details of K-rail are on its Standard Plan T3A, which was not read for this skill. When T3A is at hand, take the numbers from it and update this skill.

| Fact | Value | Source |
|---|---|---|
| Shape | New Jersey safety shape | 1, 4 |
| Section length | 6,045 mm (19 ft 10 in) | 1 |
| Laying length | 20 ft (6,096 mm); the joint of 51 mm (2 in) is derived | 2, 8 |
| Base width | 610 mm (24 in) | 5 |
| Height | 32 in (813 mm) | 6 |
| Vertical reveal at the base | 3 in (76 mm) | 6, 7 |
| Slope break | 13 in (330 mm) above the pavement | 6, 7 |
| Lower slope | 55 degrees from horizontal, rising 10 in | 6 |
| Upper slope | 84 degrees from horizontal, rising 19 in | 6 |
| Top width | 6 in (152 mm), derived | below |
| Mass | about 3,630 kg (8,000 lb) per section | 2 |
| Connection | pin and loop, with pins 31.8 mm by 660 mm (1.25 in by 26 in) | 1 |
| Stake holes | four per section | 2 |

Derived top width: half the base, 12 in, less the run of the lower slope, 10 in / tan 55 degrees = 7.00 in, less the run of the upper slope, 19 in / tan 84 degrees = 2.00 in, leaves 3.00 in. The top is therefore 6 in wide.

## Where K-rail is used

- K-rail stands between traffic and the work, as a temporary barrier in a work zone: sources 2 and 3.
- K-rail serves as a semi-permanent barrier for two to five years, pinned and staked through its four stake holes: source 2.
- K-rail serves as a median barrier in a narrow median, and beside an excavation, with stakes that limit its movement: source 1.
- At falsework, Caltrans's Standard Specifications require K-rail on both sides of a vehicle opening through the falsework, and wherever falsework stands within 12 ft of the edge of a traffic lane: source 3.
- At a drop-off, such as the edge of a bridge deck, about 2 ft is kept clear from the K-rail to the drop-off. With less than 2 ft, the K-rail is attached to the deck: source 3.
- An end that faces traffic takes a temporary crash cushion. The sloping terminal panel is no longer an accepted end: source 3.
- Bridge Design Memo 13.1 lets projects advertised before 1 January 2027 keep using Temporary Railing (Type K): source 3.

## How K-rail behaves when hit

- K-rail deflects and moves when a vehicle hits it, so the space behind it is kept clear: source 3.
- With four stakes in every section, K-rail held its dynamic deflection to 254 mm and its permanent set to 70 mm in a Caltrans crash test under NCHRP Report 350, the crash-test procedure of the National Cooperative Highway Research Program: source 4.
- Stakes without caps gave no uplift resistance: the sections rotated about the stakes on the side away from the impact, and the vehicle climbed the face. Stakes with caps stopped this: source 1.
- The lower slope of the New Jersey shape lifts a vehicle's tires, which takes up energy and redirects a vehicle that hits at a shallow angle. At a high speed and a large angle, the lift can make the vehicle unstable: source 7.
- No source read for this skill gives the deflection of K-rail without stakes. Give no number for it.

## The K-rail type in an IFC file

Model K-rail as one type with one representative section, and make every section an instance of it. The type then holds the facts once, every section shares its geometry, a change to the type changes every section, and the file stays small.

1. Make an IfcWallType named K-rail, with the predefined type PARAPET and the element type Temporary Railing (Type K). IfcWall with PARAPET is the class that this repository's conversions give a barrier, so K-rail stays with the other barriers in the viewer's IFC Type panel (skill ifc-layer-structure-type).
2. Give the type one representation map: the New Jersey profile in its x-y plane, with x across, y up and the centre of the base at the origin, extruded 6,045 mm along z. In metres, the profile's eight corners are (±0.305, 0), (±0.305, 0.0762), (±0.1272, 0.3302) and (±0.0764, 0.8128). The profile's area is 0.2545 m², and one section's volume is 1.538 m³, both derived.
3. Give the type a property set named K-rail, with the facts of the table and a pointer to this skill.
4. Declare the type in the project, through IfcRelDeclares, so that the type belongs to the project.
5. Type each element that holds a line of K-rail by the K-rail type, through IfcRelDefinesByType. Its body is a mapped representation, with one mapped item for each section. Each mapped item's transformation operator puts the section in the element's own coordinates: Axis3 along the chord, Axis1 across it and horizontal, Axis2 = Axis3 × Axis1, and the local origin at the section's start, less the element's placement.
6. Leave out the pins, the loops, the stake holes, the lifting holes and the scuppers. The model shows where the barrier stands and what space it takes, and these parts change neither.

The script `scripts/lay_k_rail.py` does steps 1 to 5 and the steps of the next section. Run it with `python -I scripts/lay_k_rail.py FILE.ifc --line ID,ID --line ID,ID`, with one `--line` for each line of barrier and the IDs of the elements that hold it. It reads the file with ifcopenshell, edits it as lines, and prints each line's length, its number of sections and how far each end moves. Install ifcopenshell for reading with `pip install ifcopenshell`.

## Laying sections along a line

1. Take the line: the centre line of the barrier's base, with its grade, from the element's own geometry. Take its z values from the model, not from the plans (skill origin-point-ifc). Join pieces of a line that meet end to end into one line, so that no two sections overlap where the pieces meet. Lexocad exports a barrier as a triangulated surface model, a box swept along the line. Its vertices fall in cross-section stations along the element's long axis, and each station gives a point of the line: the mean of its x and y, and its least z.
2. Count whole sections: n = 1 + round((L - 6.045 m) / 6.096 m), where L is the length of the line. Centre the run of n sections, (n - 1) * 6.096 m + 6.045 m long, on the line, so that each end of the line moves by 5 ft or less.
3. Start a section every 6.096 m (20 ft) along the line. Each section is a straight chord, 6,045 mm long, from its start on the line, so the sections follow a curve as chords.
4. Keep each section's cross direction horizontal and its long direction on its chord, so that the section sits on the grade of the line.
5. Give each section to the piece of the line that holds the section's midpoint.

Example: a line 100 m long takes 1 + round((100 - 6.045) / 6.096) = 16 sections. Their run is 15 * 6.096 + 6.045 = 97.49 m long, so each end of the line moves 1.26 m inward.

Example from this repository, measured on 25 November 2026: `merced_sr99_lexo_ifc43_preliminary.ifc`, the file that `merced_sr99_lexo_ifc43_preliminary_r2.ifc` replaced, held four elements named "barrier type K", in two lines. In each line a box 10.56 m long meets a curved run end to end, with a gap of 0.09 m between them. One line is 636.98 m long and takes 104 sections, one in the box #125987 and 103 in the run #92822; each of its ends moves 1.524 m, the most that step 2 allows. The other is 610.42 m long and takes 100 sections, 2 in #287948 and 98 in #288181. The edit replaced 4 lines and added 1,262.

## The K-rail in merced_sr99_lexo_ifc43_preliminary_r2.ifc

`merced_sr99_lexo_ifc43_preliminary_r2.ifc` replaced `merced_sr99_lexo_ifc43_preliminary.ifc` on 26 November 2026, after a round trip through Lexocad (skill ifc-layer-structure-type). Facts measured that day in r2:

- The round trip kept all 204 sections, each at its place, and the four elements kept their GlobalIds, so r2 needs no new K-rail. The elements are #300068 (103 sections), #303081 (98), #305944 (2) and #306023 (1), which were #92822, #288181, #287948 and #125987 in the file r2 replaced.
- Three bodies are still mapped representations. The body of #306023, a single section, became one IfcExtrudedAreaSolid.
- The IfcWallType K-rail still types the four elements, but it holds neither its property set nor its representation map. Each element carries the facts in the property set lx_K-rail instead.
- The four elements are in building "Mainline SR 99", storey "Traffic control".
- The elements that lie over the K-rail's top, named in the facts below, are now in other storeys: G16-02, G03-04, G11-03 and G13-01 in storey "Mainline SR 99 2026"; G39-01 and G40-01 in building "Embankment 2026", storeys "Southbound" and "Northbound"; and G03-16 in building "Bridge_2026", storey "Median" under storey "Falsework".

Facts measured on 25 November 2026 in `merced_sr99_lexo_ifc43_preliminary.ifc`, the file that r2 replaced:

- The K-rail was laid with `python -I scripts/lay_k_rail.py merced_sr99_lexo_ifc43_preliminary.ifc --line 125987,92822 --line 287948,288181`, in pull request #15. A file rebuilt from a new Lexocad export needs the K-rail again: check that the four numbers still name the four elements "barrier type K", then run the same command.
- The 204 sections have no colour. The name "barrier type K test edit", which pull request #11 gave one element as a test, is gone.
- The K-rail runs 4 to 7 m either side of the plans' ROUTE99 line, from station 21+31 to 27+55, in building "Retaining Wall 6 and 7 M", storey "Retaining wall".
- At 109 of the 204 sections, other elements lie over the K-rail's top: elements of building "Mainline SR 99" (G16-02, G03-04, G11-03, G13-01, G39-01, G40-01) and of building "Bridge" (two deck slabs, G03-16), from 21+31 to 22+39 and from 24+48 to 26+75. So when the K-rail does not show in a viewer, look first at those two stretches.
- No cadwork page found says whether the cadwork BIM Viewer draws mapped representations.

## Changing an IFC file

- Edit the file as lines: delete, replace and append whole lines. Do not save it through ifcopenshell, which changes every line (AGENTS.md). Reading the file with ifcopenshell, to find the line and to check the result, changes nothing.
- To give an element its K-rail body, replace its IfcProductDefinitionShape line so that the line points to the new mapped representation. Leave the old geometry lines in the file, unreferenced: their points can be shared with other elements, so deleting them can break another element.
- Before adding a line of K-rail, check that no K-rail line already stands on the same edge. Two lines on one edge overlap.
- Keep each changed element's GlobalId, name, class, floor and property sets.
- Before handing over the file, check that ifcopenshell.validate finds no errors, that no reference points to a deleted line, that each element's volume equals its number of sections times the volume of one section, and that an end view shows the New Jersey shape and a side view shows the joints.
- Do the edit in Claude Code, which has a clone of the repository and git, and push it with git. A chat on claude.ai cannot carry an IFC file of this size (AGENTS.md, section "Where to do the work").

## Check before answering

Before giving a K-rail number, check that it names its source or is marked derived. Before changing K-rail in an IFC file, check that every section is an instance of the one K-rail type, that each line holds whole sections laid every 20 ft, and that the file was edited as lines.

## Sources

1. Caltrans, Roadside Safety Research Group. Development of Staking Configurations for K-Rail. Report. https://dot.ca.gov/-/media/dot-media/programs/research-innovation-system-information/documents/f0017259-staking-k-rail-report-v2.pdf
2. Caltrans. Development of Staking Configurations for K-Rail. Research page. https://dot.ca.gov/programs/research-innovation-system-information/roadside-safety-research-group/staking
3. Caltrans. Bridge Design Memo 13.1, Temporary Barrier Systems. https://dot.ca.gov/-/media/dot-media/programs/engineering/documents/bridgedesignmemos/13/202512bdm1301-a11y.pdf
4. Tie-Downs and Transitions for Temporary Concrete Barriers. Paper. https://www.researchgate.net/publication/325302556_Tie-Downs_and_Transitions_for_Temporary_Concrete_Barriers
5. Compliance Crash Testing of the Type 60K Concrete Barrier. Report. https://wsdot.wa.gov/publications/fulltext/design/roadsidesafety/calfinalreport.pdf
6. The Jersey Barrier. Invention & Technology. https://www.inventionandtech.com/content/jersey-barrier-0
7. Task Force 13. Cast-In-Place Concrete Barriers, 14 May 2021. https://tf13.org/wp-content/uploads/2021/12/MASH-Concrete_May-14-2021.pdf
8. Eiffel Trading, a vendor. What are California Temporary K-Rail Specifications? https://www.eiffeltrading.com/blog/post/what-are-the-california-temporary-k-rail-specifications
