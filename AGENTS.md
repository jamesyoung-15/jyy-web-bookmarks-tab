# Agent Instructions

This project is a static bookmark/shortcust website meant to replace landing pages like [nightTab](https://github.com/zombieFox/nightTab) for work. Work has a strict whilelist of extensions so nightTab isn't an option, we can only use Chrome/Edge, and I personally don't like the default chrome homepage shortcuts nor do I like using bookmarks via the top tab.

Project should use `steer` mode, where I direct high-level direction but agent does low-level implementation without much input from user.

## Always

<!-- install:eager -->
@.agents/instructions/context.md
@.agents/instructions/writing-style.md
@.agents/instructions/modes.md
@.agents/instructions/git-plain.md

## Never

- Commit secrets, credentials, or `.env` contents.
- `git add -A`. Stage files by name.
- Describe untested code as working.

## Where to look

Read these when the task calls for it, not before.

| When you are | Read |
|---|---|
| Picking up work after a break | `STATE.md`, then the tail of `JOURNAL.md` |
<!-- install:routed -->
| Creating or setting up a git worktree | `.agents/instructions/worktrees.md` |
| Writing a README, docs, or a wiki page | `.agents/instructions/documentation.md` |

## Project notes
