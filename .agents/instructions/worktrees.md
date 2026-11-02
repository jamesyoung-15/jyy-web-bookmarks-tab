<!-- from: agentic-development/instructions/worktrees.md @ 0.4.1+494be6d sha:21d81b2ea213 -->

<!-- load: routed | when: Creating or setting up a git worktree -->

# Worktrees

`git worktree add` carries tracked files only. If any of this project's agent config
is gitignored, a new worktree has none of it, and nothing says so. The agent starts
there with no instructions and no skills, behaving like a project with no setup.

## After creating a worktree

Run this from the main checkout, not from inside the new worktree, since the script
lives in the main checkout's `.agents/bin`:

```bash
git worktree add ../thing-feature -b thing-feature
.agents/bin/link-worktree.sh ../thing-feature
```

It links whatever is missing and leaves whatever is already there, so it is safe to
run on a worktree that is partly set up, and it is a no-op when the project tracks
all of its config.

## Link (do not copy)

Do not set the worktree up as a fresh project with its own copy of the config. Two
copies drift, and then two working trees disagree about the same project while both
look correct. One set of files, shared by link, is the point.

If a worktree really does need a different rule, replace that one link with a real
file and note it in the worktree's `AGENTS.md`.

## Editing config from inside a worktree

The links point back at the main checkout, so editing a fragment under
`.agents/instructions/` from a worktree edits the shared copy and affects every
worktree. That is usually
what you want. When it is not, copy the file in place of the link first and say so.
