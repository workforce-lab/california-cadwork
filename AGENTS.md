# Agent instructions

The skills for this repository are in `.claude/skills/`. Each skill is a folder with a `SKILL.md` file. Before a task, read the `SKILL.md` of each skill whose description matches the task, and follow it.

## Changing a file in this repository

A change reaches the main branch this way. The user logs the agent in to GitHub. The agent pushes the change to a new branch of this repository, workforce-lab/california-cadwork, and opens a request for review (a pull request) from that branch. An admin of this repository reviews the change and accepts it. Do not make a fork of this repository: students read only the main branch of this repository, and work on a fork does not reach them. Do not ask the user for a token.

The `*.ifc` files in this repository are large text files, and they will change. The login through MCP carries small files only, so a large `*.ifc` file cannot go up through it whole. How an edit to an `*.ifc` file goes up is under test. Two facts are measured on a test file: git merges two edits to different single lines of the file by itself, and a save of the file through the software library ifcopenshell, with no edit, changes every line of the file.

A third fact was measured on November 25, 2026, on `merced_sr99_lexo_ifc43_preliminary.ifc`, a 13.6 MB file. In Claude Code, an edit of one line with `sed`, pushed with `git push`, went up as a diff of one line (1 insertion, 1 deletion). The pack that git builds for that push measures 984 bytes, not the 13.6 MB of the file.

### Give the agent access before the work

An agent pushes to this repository through the Claude GitHub App, not through the user's own GitHub account. So a user can be an admin of this repository and the agent can still be refused. On November 25, 2026, a push from Claude Code was refused with error 403 and the message "Claude doesn't have GitHub access to workforce-lab/california-cadwork for your organization", while the user's account was an admin of this repository.

Before the work, the agent checks that it can push, with `git push --dry-run origin HEAD:refs/heads/BRANCH`. A dry run sends nothing. If the check is refused, the agent stops, tells the user, and asks the user to give it access with these steps:

1. If the user's GitHub account has no write access to this repository, the user asks for it with the issue form "Request write access", and accepts the invitation that GitHub sends after a repo admin approves it.
2. The user connects GitHub to Claude, or connects it again, at https://claude.ai/connect-github, and signs in with that GitHub account.
3. The user gives the Claude GitHub App access to this repository: open https://github.com/apps/claude/installations/select_target, choose workforce-lab, and under "Repository access" choose california-cadwork, or all repositories. Then click Install, or Save if the app is already installed. If the user is not an owner of workforce-lab, GitHub sends the request to an owner, who approves it.
4. The user tells the agent that access is given, and the agent runs the check again before it starts the work.

## Where to do the work

Do an edit to an `*.ifc` file in Claude Code. When the work is an edit to an `*.ifc` file and the agent is in a chat on claude.ai, ask the user to open this repository in Claude Code, at https://claude.ai/code, and to start the task there. In Claude Code, read this file and follow the steps below.

### Why a chat on claude.ai cannot edit an `*.ifc` file

A chat reaches this repository only through the GitHub connection. The chat's code sandbox has no git login to GitHub, so it cannot clone the repository or push a branch. The GitHub connection moves a file whole: a read returns the whole file in one tool result, and a write sends the whole file in one tool call. Every character of that file passes through the agent's context.

An `*.ifc` file is too large for that path:

- `merced_sr99_lexo_ifc43_preliminary.ifc` holds 13,603,032 characters. At about 2.5 characters to a token, that is about 5.4 million tokens. The connection carries a file as Base64, which is a third longer, so about 7.3 million tokens. The largest context window of a Claude model in a chat is 1 million tokens.
- A tool result has its own limit, far below the context window. A tool result of 60,782 characters, three skill files from the lab's skills repository in Base64, was too large for one result in Claude Code on November 25, 2026.
- GitHub's REST API, in the endpoint "Get repository contents," returns the content of a file of up to 1 MB. A file between 1 MB and 100 MB comes back without its content unless it is asked for in the raw format. The three `*.ifc` files here are 1.1 MB, 13.6 MB and 49.1 MB.

Claude Code works on a clone of the repository instead. It reads and edits the file on disk with `grep` and `sed`, so only the lines it reads enter its context. git then sends only the change: the push of a one-line edit to the 13.6 MB file measures 984 bytes.

## How to edit one line of an `*.ifc` file

1. Clone the repository, and make a new branch from main.
2. Find the line by its entity number, for example `grep -n '^#125987=' FILE.ifc`.
3. Edit the line as text, with `sed` or the edit tool, and limit the edit to that line, for example `sed -i "LINE{/^#125987=/s/'OLD'/'NEW'/}" FILE.ifc`. Do not open and save the file through ifcopenshell or another IFC library, because such a save rewrites every line.
4. Check with `git diff --stat main` that one file changed, with one insertion and one deletion for each line edited.
5. Commit, and push the branch with `git push -u origin BRANCH`. Then open a pull request, as the section above says.

## Reading the lab skills

The user's profile says to read the lab's skills from the repository `workforce-lab/cife-research-method-skills` before the work. List a skill's folder through the GitHub connection, then download its `SKILL.md` from the `download_url` in the listing at once with `curl -sS -o NAME.md "DOWNLOAD_URL"`. The token in a `download_url` expires after a few minutes, so a download from an old link returns "404: Not Found". The file `.claude/settings.json` allows that `curl` command, so the permission checker does not block it. If the download is blocked, fetch the file through the GitHub connection, which returns it as Base64, and decode it with `base64 -d`.
