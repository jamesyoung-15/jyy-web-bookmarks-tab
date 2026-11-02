<!-- from: agentic-development/templates/wiki/page.md @ 0.4.1+494be6d sha:094f7c5558fb -->

<!--
One page per entity: a system, a service, a process, a convention. Not one
page per document you read.

Under 150 lines. Past that, split by entity rather than adding headings.

Write only what is not in any repo. The test before adding a line: could an
agent learn this by reading the code for a minute? If yes, leave it out.
-->

# {{Entity}}

Last verified: {{YYYY-MM-DD}} by {{who}}
Source of truth: {{link to the console, repo, or runbook that actually governs this}}

## What it is

{{Two or three lines. Assume the reader knows the domain and not this system.}}

## How we use it here

- {{The specific way this org or project uses it, which is rarely the default}}

## Gotchas

- {{The thing that wastes an hour. Caching, silent truncation, a flag that
   does not do what it says}}

## Common tasks

| Task | How |
|---|---|
| {{...}} | {{command, or a link to the runbook}} |

## Open questions and contradictions

- {{Where two sources disagree, say both and which one you trust. Do not
   silently pick one}}

## Related

- {{Other wiki pages, ADRs, tickets}}
