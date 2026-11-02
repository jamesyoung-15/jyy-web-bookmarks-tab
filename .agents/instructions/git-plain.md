<!-- from: agentic-development/instructions/git-plain.md @ 0.4.1+494be6d sha:02cbbaba9e32 -->

<!-- load: eager | when: Committing, branching, or writing a commit message -->

# Git Standards (Plain Commits)

## Branches

- Conventional branch names: `<type>/<short-description>`, kebab-case.
- Examples: `fix/header-overflow`, `feat/oauth-callback`, `chore/bump-ruff`.
- Include the ticket ID when the project uses one: `feat/PROJ-412-oauth-callback`.

## Commits

- Plain subject lines, no `type:` prefix.
- Imperative mood, lower-case, no trailing period, under 72 characters.
- Example: `add user authentication middleware`
- Body only for changes where the reason is not obvious from the diff. Explain why, not what.
- At most 3 lines of body. If it needs more, the commit is too big. Either reference an existing doc/file or ask user for permission via prompt tool.

## Rules

- Do not add the agent as author, co-author, or trailer. No references to the agent or the tool used, unless explicitly asked.
- One logical change per commit. Do not bundle a refactor with a behavior change.
- Never commit secrets, `.env` files, or local tool state.
- Do not `git add -A` or `git add .`. Stage the files you touched by name.
- Do not amend, rebase, force-push, or reset without being asked.
