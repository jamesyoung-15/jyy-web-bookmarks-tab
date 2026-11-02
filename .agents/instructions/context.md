<!-- from: agentic-development/instructions/context.md @ 0.4.1+494be6d sha:432cccac27a8 -->

<!-- load: eager | when: Always. Governs what enters the main context -->

# Context

Rules for what enters the main context and what gets written down. Compaction is lossy and the loss compounds, so treat context as a budget and disk as the real memory.

## Sub-agents

Delegate to a sub-agent whenever the raw output is large and the answer is small. The sub-agent reads it, the main context never sees it.

Delegate these by default, without being asked:

- Any CI, deploy, or automation job output.
- Any log search over roughly 200 lines.
- Any search across the whole repo when you do not already know the file.
- Reading a file only to answer one question about it.
- Any exploration where you expect to open more than 3 or 4 files.

Tell the sub-agent exactly what to return. A sub-agent that reports back 2,000 tokens of narration has saved nothing.

```
Return only: status, the failing step, the error line verbatim, and the
identifier needed to fetch it again. No summary of what you read.
```

Do not delegate when you need the detail in front of you for the next several turns, or when the task is a handful of targeted edits.

## Never paste large output back

Write it to a file, then have a sub-agent read the file. This applies to command output, API responses, query results, and anything you are tempted to quote at length.

Quote the specific lines that matter. Reference the file for the rest.

## Write it down as it happens

Append one line to `JOURNAL.md` in the same turn, whenever any of these happen:

- A command or job fails and you work out why.
- You pick between two or more approaches.
- You learn something about this system that is not visible in the code.
- An assumption turns out to be wrong.
- You rule something out.

Format: `YYYY-MM-DD  <one line>`. Append only. Never rewrite or tidy earlier entries.

Negative results matter most. "Tried X, no effect, the real cause was Y" is the line that stops the same approach being proposed again in three weeks.

Do not judge whether something is important enough. The triggers above are the rule.

## Planning ends on disk

A plan that exists only in the conversation is deleted by the first compaction.

Before leaving plan mode, write the plan to a file, and write an ADR for each decision made inside it. If a planning session produced no file, it produced nothing that survives.

## Checkpoint instead of compacting again

One compaction is fine. At the second, stop and run the `checkpoint` skill, then start a fresh session that reads `STATE.md`.

A fresh session with a good state file beats a third compaction every time. A summary of a summary of a summary is not worth defending.

## Keep context clean

- Re-read the specific lines you need, not whole files you have already seen.
- Start a new session between unrelated tasks.
- Trim connected tool servers to the ones this project needs. Every tool definition occupies context permanently, before any work happens.
