---
name: ifc-layer-structure-type
description: "How elements are turned off in the cadwork BIM Viewer through its three panels of lights, IFC Structure, IFC Type and IFC Layer, and what to tell a user whose IFC Layer lights do nothing. Use this skill whenever the user says the layer lights or lamps in the cadwork BIM Viewer do not turn elements off, asks whether that is a bug, or calls a file broken or corrupted because of it; whenever the user wants to turn elements on or off in the viewer; whenever an IFC 4.3 file is made or changed for the viewer, such as a Civil 3D or Lexocad export; before changing a file's spatial structure, classes or layers for the viewer; and whenever an IFC file is to go into Lexocad and back out, imported, edited and exported again. Use it even when the user does not name the panels."
---

# IFC Layer, IFC Structure and IFC Type in the cadwork BIM Viewer

v0.4, 25 November 2026

The cadwork BIM Viewer has three panels with a light beside each line: IFC Structure, IFC Layer and IFC Type. cadwork's manual calls the lights lamps. A light turns off the elements of its line.

## When a user says the IFC Layer lights do not work

Tell the user, in these words or close to them: "In the cadwork BIM Viewer, the IFC Layer lights do not turn elements off in an IFC 4.3 file. This is known, and it is not a bug in the file. Turn elements off with the IFC Structure lights and the IFC Type lights."

Then stop. Do not change the file's layers, its spatial structure or its schema to make the IFC Layer lights work (the instructor, 24 November 2026).

## How we turn off elements

In an IFC 4.3 file, we turn elements off with the IFC Structure lights and the IFC Type lights (the instructor, 24 November 2026). So an IFC 4.3 file made for the viewer needs two things:

- **A spatial structure that the IFC Structure panel lists.** The panel lists the project, the sites, the buildings and the storeys. It did not list the IfcRoad and the two IfcBridge of `MERCED_SR99_ifc43_mapped.ifc`, so the elements in them could not be turned off there. Put the elements in buildings and storeys.
- **An IFC class for each element.** The IFC Type panel lists the classes, such as IFCWALL, IFCFOOTING and IFCEARTHWORKSFILL, with the count of visible elements over the count of all, such as 18/18.

## IFC Layer

- Leave a file's IFC layers where they are. The layers of the C3D file are the 56 layers that Civil 3D wrote into `MERCED_SR99_solid.ifc`, and the conversion to IFC 4.3 carried them over; they stay as the record of the Civil 3D layers, although the viewer cannot switch elements with them.
- In the tests below, the IFC Layer lights turned elements off in an IFC2X3 file and did not in IFC4 or IFC 4.3 files. In those files the light changed colour and the elements stayed visible.
- Lexocad 31's own IFC4.3 export writes no IFC layer. `merced_safe_test_IFC4.ifc`, exported from `merced_safe.lxz` with the IFC4.3 option and the other settings as the dialog showed them, has no IfcPresentationLayerAssignment, and its IFC Layer panel is empty.
- In IFC 4.3 these changes did not make the IFC Layer lights work: the elements in the site or in a building storey; IfcPresentationLayerWithStyle or a plain IfcPresentationLayerAssignment; the layer on the shape representation or on its geometric items.
- The repository's files are IFC 4.3. Do not convert a file to IFC2X3 or IFC4 for the IFC Layer lights.

## Layer 2d

With the option Export Layer 2D on, Lexocad's IFC4.3 export wrote a second site and a building, both named Layer 2d. They hold no elements, so their lights in the IFC Structure panel turn nothing off. On 24 November 2026 the instructor had a copy of the export made without Layer 2d.

## The tests

The instructor opened these files in the viewer on 24 November 2026 and turned off IFC Layer lights. The test files hold the same four elements, three curbs and an approach slab, each on its own layer.

| File | Schema | Written by | IFC Layer lights |
|---|---|---|---|
| `MERCED_SR99_ifc43_mapped.ifc` and the C3D files made from it | IFC4X3_ADD2 | IfcOpenShell | Elements stayed on |
| Test file, elements in the site, IfcPresentationLayerWithStyle | IFC4X3_ADD2 | IfcOpenShell | Elements stayed on |
| Test file, elements in a building storey | IFC4X3_ADD2 | IfcOpenShell | Elements stayed on |
| Test file, plain IfcPresentationLayerAssignment | IFC4X3_ADD2 | IfcOpenShell | Elements stayed on |
| Test file, layers on the geometric items | IFC4X3_ADD2 | IfcOpenShell | Elements stayed on |
| Test file exported by Lexocad's scripting interface | IFC4 | Lexocad | Elements stayed on |
| merced.lxz in IFC 4.3 (preliminary) | IFC4X3_ADD2 | Lexocad's IFC 4 export, then IfcOpenShell | Elements stayed on |
| `merced_safe_test_IFC4.ifc` | IFC4X3_ADD2 | Lexocad 31's IFC4.3 export | No IFC layer in the file |
| Test file exported by Lexocad's scripting interface | IFC2X3 | Lexocad | Elements turned off |

## Lexocad's IFC import and the round trip

The IFC has to make a round trip through Lexocad, or content cannot be added in Lexocad (the instructor, 25 November 2026). Facts found that day:

- Lexocad's API guide, Python/Scripts/08_File_IO/README.md, says that IFC import and export carry only the geometry and part of the data and are not a full round trip. Only the .lxz format carries the whole document.
- The instructor imported main's `merced_sr99_lexo_ifc43_preliminary.ifc` into a new document in the Lexocad window and exported it with the IFC4.3 option. The import made one SuperBloc: the saved .lxz held one element, an IfcBuildingElementProxy named "IFC:" and the file's name, and none of the file's 2,203 GlobalIds. The export was 6,620 bytes: an empty project, the site "Site" with "Building 1" and "Storey 1", and an empty site and building "Layer 2d". It held no element and no geometry.
- Lexocad's API has a setting, openIFCWithSuperBloc, and a command that converts a SuperBloc into Lexocad elements, OpenLxCmd.CmdConvertSuperblocToLexocadElements. Run in a hidden Lexocad on that saved .lxz, the command returned False, and the model kept its one SuperBloc.
- In a hidden Lexocad, an import of the whole file with IFC_Importer did not finish within the time limit of the MCP tool run_cad_script_headless.
- Lexocad 31's own IFC4.3 export of merced_safe.lxz, `merced_safe_test_IFC4.ifc`, put every element into "Storey 1" of "Building 1". Lexocad writes only the spatial structure that its model holds, so the 13 buildings and 18 storeys of the preliminary file came from the conversion, not from Lexocad.
- Buildings and storeys made by script, with lx.Building, lx.BuildingStorey and storey.addElement, come out of Lexocad's IFC export with their elements, and a GlobalId set with setGlobalId comes out on its element. This was tested with an IFC4 export.
- Lexocad's scripting exporter wrote IFC4 for setIfcVersion(4) and IFC2X3 for every other value tried: 5, 43, and 9, which is LxIfcModel.IFC4X3. An IFC 4.3 export goes through the export dialog in the Lexocad window.
- A file rebuilt from a Lexocad export loses the work done after the export, and that work has to be done again: the IFC 4.3 classes with the MER99_Conversion property sets, the spatial structure, the SR 99 alignment (skill origin-point-ifc), the K-rail (skill k-rail), the tree ec.iv with the hawk Carls_hawks, and the deletion of the 99 square trees of the layer "2009 tree" in merced.lxz (pull request #16).

## How an agent got confused

On 24 November 2026 an agent spent an evening trying to make the IFC Layer lights work in an IFC 4.3 file. It took over an earlier chat's guess that elements outside a building storey are skipped, and then rewrote the layers in one form after another, asking the instructor to test each file. The instructor said several times that the storey was not the problem. A Lexocad IFC4.3 export, made in a minute from Lexocad's export dialog, showed that Lexocad writes no IFC layer in IFC 4.3, and the instructor said that the IFC Structure and IFC Type lights are how we turn off elements, that the IFC Layer lights not working is known, and that it is not a bug.

## Check before answering

Before answering a user about the IFC Layer lights, check that the answer says the behavior is known and is not a bug, and names the IFC Structure and IFC Type lights. Before changing an IFC 4.3 file so that a user can turn its elements off in the viewer, check that its elements sit in buildings and storeys and carry their IFC classes, and check that the change is not a rework of its layers or its schema.
