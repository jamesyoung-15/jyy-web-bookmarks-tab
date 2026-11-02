<!-- from: agentic-development/templates/wiki/log.md @ 0.4.1+494be6d sha:f9c2aa9a3789 -->

<!--
Append only, newest at the bottom. The record of how the wiki got this way.

Separate from a project JOURNAL.md: this tracks the wiki itself, not the work.
-->

# Wiki Log

Format: `## [YYYY-MM-DD] <verb> | <page or source>`

Verbs: `add`, `update`, `verify` (re-checked, still true), `contradict`
(a source disagreed with a page), `retire`.

```
## [2026-10-20] add | aap.md
Source: internal runbook plus a walkthrough with {{person}}.
Open: nobody could say who owns the staging inventory.

## [2026-10-21] contradict | deploy.md
The runbook says the gate is manual. It has been automatic since the
pipeline change. Page now records both, trusting observed behavior.
```

Why this file exists: the date on a page tells you when it was checked, this
tells you what it was checked against.
