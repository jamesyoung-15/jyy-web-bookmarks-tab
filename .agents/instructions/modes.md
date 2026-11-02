<!-- from: agentic-development/instructions/modes.md @ 0.4.1+494be6d sha:2556874050ed -->

<!-- load: eager | when: Deciding how much to explain -->

# Working Modes

<!-- "you" is the agent. The human is "the user". -->

Four modes, in order of how involved the user wants to be. Default to `assist` if nothing is declared. Switching mid-session is fine, say which mode you are in when you switch.

Mode governs explanation, when to stop for a decision, and how much may be done to the repository without asking.

## vibe

For spikes, PoCs, demos, throwaway tools.

- Do not explain decisions. Do not ask for approval at decision points.
- Pick reasonable defaults and keep moving.
- Report at the end: what was built, what is obviously fragile.
- No ADRs. No drill.
- Commit, tag, and push as you go. No need to ask.
- Not even approach-level questions. If the user wants direction confirmed before
  building, that is `steer`.

## steer

For work where the user wants the direction but not the implementation. They will
not read the diff.

- Work in long uninterrupted stretches. Do not narrate as you go.
- Stop only at approach-level forks: which library, which data model, which overall
  strategy, anything expensive to undo. Give 2 or 3 options with a one-line tradeoff
  each, then wait.
- Do not stop for implementation choices. Pick a sensible default and keep moving.
- End with a verification list: what to run, what to look at, and what you are least
  confident in. The user checks output and direction, not code.
- Ask before committing, tagging, or pushing, unless the user lifts that when
  declaring the mode. Default to asking: an extra question costs less than an
  unwanted commit.

## assist

Default. For work code and anything that outlives the week.

- One line of justification for each non-obvious decision, inline as you go.
- Stop and ask when a choice is hard to reverse: schema shapes, public API, dependency additions, auth and permissions, data migrations.
- Name alternatives you rejected and why, in one line each.
- Ask before committing, tagging, or pushing. The working tree is the review surface.

## defend

For customer-facing work, or anything the user will have to explain to another person.

- Everything in `assist`, plus:
- Write an ADR (`.agents/templates/adr.md`) for every decision that was not forced. Write it at the moment of the decision, not at the end.
- Run the `whiteboard-defense` skill before opening the PR. Do not open the PR while there are unresolved `fail` answers.

## Signals

If the user says any of these, treat it as a mode switch:

- "just make it work", "I don't care how", "quick and dirty" → `vibe`
- "you decide the details", "don't make me read this" → `steer`
- "explain as you go", "walk me through" → `assist`
- "this is going to prod", "customer-facing", "I need to defend this" → `defend`
