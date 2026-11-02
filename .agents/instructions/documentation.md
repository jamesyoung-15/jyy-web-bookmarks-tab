<!-- from: agentic-development/instructions/documentation.md @ 0.4.1+494be6d sha:f34ce3197e6b -->

<!-- load: routed | when: Writing a README, docs, or a wiki page -->

# Documentation

Follow `.agents/instructions/writing-style.md` for prose. This file covers structure.

## README

Order matters. A reader stops as soon as they have what they came for.

1. One sentence on what this is and who it is for.
2. Install, as copy-pasteable commands.
3. Minimal working example. Runnable as written, no placeholders the reader has to guess.
4. Common tasks, one section each, command first.
5. Configuration, as a table or definition list.
6. Links to deeper docs.

Do not include: a feature bullet list that repeats the sentence above, a badge wall, a roadmap, a philosophy section, or an "About" that restates the title.

## Code examples

- Must run as written. If a value is a placeholder, make it obviously fake (`sk_test_xxx`, `example.com`).
- Show the output when the output is the point.
- One concept per example. Do not demonstrate four features in one snippet.

## Structure

- Long explanations live behind `<details><summary>`, or in a separate page linked from the short version.
- Tables for anything with more than 3 parallel items (flags, env vars, error codes).
- Headings are noun phrases, not sentences. "Configuration" not "How to configure the thing".

## Maintenance

- When you change behavior, update the docs in the same change. A doc that lies is worse than a missing doc.
- Do not write docs for code that does not exist yet.
