<!-- from: agentic-development/instructions/writing-style.md @ 0.4.1+494be6d sha:a070e843cab4 -->

<!-- load: eager | when: Writing any prose, including chat replies -->

<!-- style-check: skip-file (this file quotes the banned patterns on purpose) -->

# Writing Style

Applies to all prose you produce: READMEs, docs, PR descriptions, commit bodies, comments, and chat replies.

## Shape

- Lead with the thing. Command, answer, or conclusion first. Explanation underneath.
- Bullets over paragraphs. If a paragraph runs past 3 sentences, it should probably be a list.
- Intro sections are 2 sentences maximum. No "in this document we will".
- Anything longer than 5 lines of supporting detail goes in a `<details>` block or a link to another page.
- A reader should be able to scroll the page in 10 seconds and know whether it is worth reading closely.
- Define an acronym or term of art the first time it appears, in the same sentence. A reader who does not already know it should not have to search. This applies doubly in a template or instruction, which someone will open cold with no surrounding conversation.
- Reference docs to imitate: Stripe API, FastAPI, Django, MDN.

## Banned

Never use these. Nothing checks them automatically, so this is on you.

- Em dashes. Use a comma, a colon, parentheses, or two sentences.
- Emoji, anywhere, including headings, bullet markers, and commit messages.
- Words: load-bearing, seam, genuinely, delve, powerful, seamless, elegant, kicker, fluff.
- The sentence shapes below. These matter more than the word list.

## Sentence shapes

The vocabulary is a small problem. These structures are the thing that makes writing read as machine-generated, and each one is padding wrapped around a single fact. Write the fact.

**Contrastive parallelism.** Saying what a thing is not, then what it is.

```
Bad:  It's not a config change, it's an architecture change.
Bad:  That's not caching, that's a memory leak.
Bad:  This isn't a small tweak, it's a rewrite.
Bad:  The real bottleneck: connections, not CPU.
Good: This changes the architecture.
Good: That is a memory leak.
Good: Connections are the bottleneck.
```

Plain clarification is fine, so `Report findings, do not fix them` and `comments explain why, not what` both stay. The banned shape repeats the subject to manufacture a reveal.

**The build-up triad.** Two negatives then the payoff.

```
Bad:  No config, no setup, just run it.
Good: Run it. There is nothing to configure.
```

**Rhetorical question you then answer.** Delete the question, keep the answer.

```
Bad:  And the fix? Better briefs. 
Bad:  But why does this matter? Because it compounds.
Bad:  And honestly? That's the whole problem.
Good: The fix is better briefs.
Good: This matters because it compounds.
```

**Not X. But Y.** The setup sentence carries nothing.

```
Bad:  Not because the code is slow. But because the queue is full.
Good: The queue is full.
```

**Staccato triples.** Two-word sentences in a row, for rhythm.

```
Bad:  Fewer questions. Less confusion. Better engagement.
Good: Fewer questions means less confusion.
```

## Rewrites

Filler vocabulary.

```
Bad:  This creates a natural seam for testing.
Good: You can test this part on its own.

Bad:  The retry logic is load-bearing here.
Good: Removing the retry logic breaks reconnection.
```

Narration.

```
Bad:  Now that we've covered installation, let's take a look at how
      configuration works. Configuration is an important part of the
      system and there are several options available to you.
Good: ## Configuration
      - `TIMEOUT` (default 30) seconds before a request is dropped
      - `RETRIES` (default 3) attempts per request
```

Hedging stacked on hedging.

```
Bad:  It's worth noting that this may potentially cause issues in
      some cases.
Good: This fails when the cache is cold.
```

## Honesty

- If something was not tested, say so. Do not describe untested code as working.
- If a step was skipped, say which one and why.
- No "production-ready", "battle-tested", or "enterprise-grade" unless there is evidence.
