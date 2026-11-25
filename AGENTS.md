# Agent instructions

The skills for this repository are in `.claude/skills/`. Each skill is a folder with a `SKILL.md` file. Before a task, read the `SKILL.md` of each skill whose description matches the task, and follow it.

## Changing a file in this repository

A change reaches the main branch this way. The user logs the agent in to GitHub through MCP. The agent pushes the change to the user's own copy of this repository on GitHub (a fork) and opens a request for review (a pull request). An admin of this repository reviews the change and accepts it. Do not ask the user for a token.

The `*.ifc` files in this repository are large text files, and they will change. The login through MCP carries small files only, so a large `*.ifc` file cannot go up through it whole. How an edit to an `*.ifc` file goes up is under test. Two facts are measured on a test file: git merges two edits to different single lines of the file by itself, and a save of the file through the software library ifcopenshell, with no edit, changes every line of the file.
