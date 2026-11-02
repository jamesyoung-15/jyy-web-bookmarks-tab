<!-- from: agentic-development/templates/wiki/index.md @ 0.4.1+494be6d sha:8613aa054b70 -->

<!--
The routing layer. The only wiki file read unconditionally, so keep it under
50 lines. One line per page, grouped. Update it in the same change that adds
or renames a page.

A line here should let an agent decide whether to open the page without
opening it.
-->

# Wiki

Things that are true about how we work here and are not derivable from any
repo. Code is the source of truth for how the system behaves. This is for
everything else.

Every page carries a `Last verified` date. Treat anything older than six
months as a lead, not a fact, and say so when you use it.

## Systems

| Page | What |
|---|---|
| [{{aap}}]({{aap}}.md) | {{One line. What it is and what it is used for here}} |

## Processes

| Page | What |
|---|---|
| [{{deploy}}]({{deploy}}.md) | {{What happens between the button and the result}} |

## Conventions and ownership

| Page | What |
|---|---|
| [{{team}}]({{team}}.md) | {{Who owns what, who to ask}} |

## Maintenance

- [log.md](log.md) is the append-only record of what was added and when.
- A page that only restates code should be deleted. If an agent can learn it
  by reading the code for a minute, it does not belong here.
