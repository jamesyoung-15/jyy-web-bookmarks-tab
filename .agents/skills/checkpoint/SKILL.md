---
name: checkpoint
description: Write the session's durable state to disk so a fresh session can pick it up. Use when the context is filling, after a second compaction, at the end of a work session, when switching tasks, or when the user says "checkpoint", "save state", or "hand this off". Updates STATE.md, appends to JOURNAL.md, and flags decisions that need an ADR.
---

<!-- from: agentic-development/skills/checkpoint/SKILL.md @ 0.4.1+494be6d sha:98159921cfa4 -->

# Checkpoint

Converts what is only in the conversation into files that survive it. Run this before a third compaction, not after.

`STATE.md` and `JOURNAL.md` live at the repo root, one pair per working tree. A worktree keeps its own: state describes one thread of work, so sharing it across two is meaningless.

## Hard rules

1. **Do not summarize the conversation.** A transcript summary is what compaction already produces and it is the wrong artifact. Write state and events, not narrative.
2. **Write what will be needed, not what happened.** Nobody re-reads a checkpoint to relive the session. They read it to start working.
3. **Exact strings survive, paraphrases do not.** Job IDs, error text, file paths, line numbers, command invocations. Copy them, do not describe them.
4. **Never rewrite `JOURNAL.md`.** Append only, even if an earlier line turned out to be wrong. Correct it with a new line.

## Steps

### 1. Append to JOURNAL.md

Walk the session and find every event matching a trigger from `.agents/instructions/context.md`:

- a failure you then explained
- a choice between approaches
- something learned about the system that is not in the code
- an assumption invalidated
- something ruled out

One line each, `YYYY-MM-DD  tag  text`. Create the file from `.agents/templates/journal.md` if it does not exist.

Bias toward the `fail` lines. They are the ones that stop a dead end being walked a second time, and they are the first thing compaction throws away.

### 2. Rewrite STATE.md

In full, from `.agents/templates/state.md`. Not a diff, not an append.

Check each section against reality rather than memory:

- `Done`: verify against `git log` and merged PRs, not recollection.
- `In progress`: name the file and the line where work stops.
- `Next`: specific enough that a fresh session can start without asking a question.
- `Open questions`: what is unresolved and what would resolve it.
- `Landmines`: anything that would cost an hour to rediscover.

If `STATE.md` runs past a page, history has crept in. Move it to `JOURNAL.md` and cut back.

### 3. Flag missing ADRs

List decisions made this session that are not written down anywhere. For each, one line: the decision, and whether it needs an ADR.

A decision needs one when it was not forced, and when someone could reasonably ask later why it went that way. Write them with `.agents/templates/adr.md`. Ask before writing more than two, they are the user's words as much as yours.

### 4. Check the plan landed

If this session involved planning, confirm the plan is on disk. If it only exists in the conversation, write it now.

### 5. Report

```
Journal:  +4 lines
State:    rewritten, next action is <one line>
ADRs:     2 decisions undocumented, listed below
Plan:     on disk at docs/plan-x.md

Start the next session with: read STATE.md and the last 20 lines of JOURNAL.md
```

Then say plainly whether the user should keep going or start fresh. After two compactions, recommend fresh.

## Resuming

A fresh session starts by reading `STATE.md`, then the tail of `JOURNAL.md`, then any ADR named in either.

If that is not enough to start work, the checkpoint was bad. Note what was missing in `JOURNAL.md` so the next one is better.

## Project overrides

<!-- Per-project edits go here. Examples: where STATE.md and JOURNAL.md live,
     extra sections this project needs, systems whose output must be quoted
     exactly. -->
