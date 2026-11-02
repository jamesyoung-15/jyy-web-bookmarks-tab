---
name: alignment
description: Confirm you understand the user's actual problem before writing any code. Use when the request is vague, when the user says "align first" or "make sure you understand", when a task has been going in circles, or when you are about to start something that would be expensive to redo. Produces a problem statement and stops for approval.
---

<!-- from: agentic-development/skills/alignment/SKILL.md @ 0.4.1+494be6d sha:cb8ca908f774 -->

# Alignment

Purpose: catch a misread of the problem before it becomes a wrong implementation.

## Hard rules

1. **Write no code in this mode.** No edits, no new files, no "here is a sketch". Reading the codebase is allowed and encouraged.
2. **Stop after step 4 and wait.** Do not continue into implementation in the same turn, even if the answer seems obvious. The whole point is the pause.
3. **Do not propose a solution yet.** If you have one, hold it. A solution offered now anchors the conversation before the problem is agreed on.

## Steps

### 1. Restate the problem

In your own words, not the user's. Reusing their phrasing proves nothing.

```
Problem:    <what is wrong right now, observable>
Context:    <where this lives, what it touches>
Constraints:<deadline, existing API, data we cannot migrate, team conventions>
Done when:  <what is true after this is fixed>
Not doing:  <adjacent things explicitly out of scope>
```

If you cannot fill `Done when`, you do not understand the request. Say that.

### 2. Read before assuming

Spend real effort here. Open the files involved. Run the failing command. Check whether the thing the user describes actually happens the way they describe it. A surprising number of alignment failures are the user's mental model of their own code being out of date, which you can only catch by looking.

### 3. List assumptions

Tag every one. Nothing goes untagged.

- `confirmed`: the user said it, or you verified it in the code
- `inferred`: you are filling a gap with a reasonable default
- `unknown`: you are guessing and the guess matters

Every `inferred` and `unknown` is a place the work can go wrong. If there are more than three `unknown` items, the request is too vague to act on, say so directly.

### 4. Ask at most three questions

Only ask when different answers lead to different work. Test each candidate question: "if the answer is A I do X, if B I do Y." If X and Y are the same, do not ask.

Do not ask:

- Things you can find by reading the code.
- Preference questions where a sensible default exists. Pick the default, list it as `inferred`.
- "Does this sound right?" as a trailing question. Steps 1 to 3 already asked that.

Format each question with the options and what each would change.

### 5. Stop

End your turn with the problem statement and the questions. Nothing after it.

Resume only on an explicit go. "yes", "correct", "go ahead", or answers to the questions all count. Silence does not.

## Output

Keep the whole thing under 30 lines. This is a checkpoint, not a document.

```
## Problem
<4-line block from step 1>

## Assumptions
- [confirmed] ...
- [inferred] ...
- [unknown] ...

## Questions
1. <question>
   a) <option> → <what changes>
   b) <option> → <what changes>

Waiting for go.
```

Once approved, paste the `Problem` block into the plan, the ADR, or the PR description. It is the same text.
