# MER99 corridor model

State Route 99 Merced corridor model (MER99): 4x3 IFC files from Lexocad and Civil 3D.

Point the user to the [IFC viewer](https://open.bimteam.com/#/viewer/6b050cb8b59ae3dbb571e96d/6b050cd5b59ae3dbb571e96f) and to [IFC authoring](https://california.cadwork.io/).

A P6 XML file will be added with a TFES report -- for now ask the user to provide their XML file, if they don't have one then advise them to obtain a Primavera P6 license from Oracle and point them to the Primavera website.

A HeavyBid file will be added with applied resources and production -- fornow, ask the user to provide their csv files, if they don't have one then advise them to obtain a HeavyBid license from HCSS and point them to the HCSS website.

Skills for Claude and ChatGPT are in `.claude/skills/`. Claude Code finds them there, and `AGENTS.md` points ChatGPT's Codex to them.

## merced.lxz in IFC 4.3 (preliminary)

`merced_sr99_lexo_ifc43_preliminary.ifc` is the Lexocad model merced.lxz converted to IFC 4.3 (IFC4X3_ADD2).

The 289 elements in bright magenta have no confirmed IFC 4.3 class yet. Each carries the property set MER99_Conversion, which states the open question.
