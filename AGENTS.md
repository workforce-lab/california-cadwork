# Agent instructions

The skills for this repository are in `.claude/skills/`. Each skill is a folder with a `SKILL.md` file. Before a task, read the `SKILL.md` of each skill whose description matches the task, and follow it.

## Changing a file in this repository

A change reaches the main branch this way. The user logs the agent in to GitHub through MCP. The agent pushes the change to the user's own copy of this repository on GitHub (a fork) and opens a request for review (a pull request). An admin of this repository reviews the change and accepts it. Do not ask the user for a token.

The `*.ifc` file in this repository is a large text file, and it will change: the file here now is a test file of 76 MB and 1.47 million lines. The login through MCP carries small files only, so a whole `*.ifc` file of that size cannot go up through it. How an edit to the `*.ifc` file goes up is under test. Two facts are measured on the test file: git merges two edits to different single lines of the file by itself, and a save of the file through the software library ifcopenshell, with no edit, changes every line of the file.

A third fact was measured on November 25, 2026, on `merced_sr99_lexo_ifc43_preliminary.ifc`, a 13.6 MB file. In Claude Code, an edit of one line with `sed`, pushed with `git push`, went up as a diff of one line (1 insertion, 1 deletion). The pack that git builds for that push measures 984 bytes, not the 13.6 MB of the file.

## Where to do the work

Do an edit to an `*.ifc` file in Claude Code, which has a shell and git. A chat on claude.ai has no shell and no git, and its GitHub connection carries small files only. When the work is an edit to an `*.ifc` file and the agent is in a chat on claude.ai, ask the user to open this repository in Claude Code, at https://claude.ai/code, and to start the task there. In Claude Code, read this file and follow the steps below.

## How to edit one line of an `*.ifc` file

1. Clone the repository, and make a new branch from main.
2. Find the line by its entity number, for example `grep -n '^#125987=' FILE.ifc`.
3. Edit the line as text, with `sed` or the edit tool, and limit the edit to that line, for example `sed -i "LINE{/^#125987=/s/'OLD'/'NEW'/}" FILE.ifc`. Do not open and save the file through ifcopenshell or another IFC library, because such a save rewrites every line.
4. Check with `git diff --stat main` that one file changed, with one insertion and one deletion for each line edited.
5. Commit, and push the branch with `git push -u origin BRANCH`. Then open a pull request, as the section above says.

## Reading the lab skills

The user's profile says to read the lab's skills from the repository `workforce-lab/cife-research-method-skills` before the work. List a skill's folder through the GitHub connection, then download its `SKILL.md` from the `download_url` in the listing at once with `curl -sS -o NAME.md "DOWNLOAD_URL"`. The token in a `download_url` expires after a few minutes, so a download from an old link returns "404: Not Found". The file `.claude/settings.json` allows that `curl` command, so the permission checker does not block it. If the download is blocked, fetch the file through the GitHub connection, which returns it as Base64, and decode it with `base64 -d`.
