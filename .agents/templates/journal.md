<!-- from: agentic-development/templates/journal.md @ 0.4.1+494be6d sha:60b02ebdf483 -->

<!--
Append only. Newest at the bottom. Never edit or tidy an earlier entry, even
a wrong one. Correct it with a new line that says it was wrong.

One line per event. If an entry needs a paragraph, it needs an ADR instead,
and the line here should link to it.

Triggers are in .agents/instructions/context.md. Do not judge importance, follow the
triggers.
-->

# Journal

Format: `YYYY-MM-DD  tag  one line`

Tags: `fail` (tried, did not work), `why` (decision made), `found` (learned
something not in the code), `wrong` (an assumption was invalid).

```
2026-10-20  found  Inventory plugin caches for 15 min, explains the stale host list
2026-10-20  fail   Raising forks to 50 changed nothing, bottleneck is the plugin not parallelism
2026-10-20  why    Pinned the collection instead of patching upstream, see adr 0003
2026-10-21  wrong  The retry wrapper does not cover timeouts, only non-2xx
```

Negative results are the point. The `fail` lines are what stop the same dead
end being walked twice.
