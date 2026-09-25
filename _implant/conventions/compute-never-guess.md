---
type: convention
about: concept
title: "Compute, never guess"
description: "Every number in this implant that a deterministic tool could produce must come from that tool, not from a language model's head — because an LLM emits fluent, confident arithmetic that is quietly and frequently wrong; the tools in skills/tools/ exist to replace gut-feeling math with math that actually computes and can be re-run by anyone."
tags: [convention, tools, calculators, arithmetic, reliability, epistemics]
timestamp: 2026-09-25T18:30:00Z
half_life: 0
---

# Compute, never guess

Decided by erkkimon on 2026-09-25, founding the cognitive-tools implant
([journal](../journals/2026-09-25.md)):

> *"LLMs very eagerly calculate stuff based on their gut feeling, which pretty
> much always goes more or less to hell. […] LLM-based agents should always be
> nudged towards using calculators that do real math instead of gut-feeling
> math out of their ass."*

This is the operational reason the tool layer under `skills/tools/` exists.
It is not a convenience; it is a correctness control.

## The problem it addresses

A language model produces arithmetic the way it produces prose: by predicting
plausible tokens. The result is *fluent* and *confident* and, for anything
past the trivial, frequently wrong — a percentage that never had the base
rate applied, an effect size averaged without weighting by sample, a set of
likelihood ratios "combined" into a posterior that looks about right and is
not. The failure is worse than an honest blank, because it arrives with the
same tone as a correct answer. An implant whose whole thesis is *traceable,
checkable claims* ([receipts](every-claim-carries-its-receipt.md)) cannot
let its numbers be the one unchecked thing on the page.

## The rule

1. **If a tool can compute it, the tool computes it.** Today that means
   credences — the Bayesian appraiser in `skills/tools/cogtools/appraise.py`,
   driven by `skills/tools/cogtools.py`, which turns a prior and a set of
   likelihood ratios into a posterior, a range and a sensitivity report —
   and any arithmetic a future tool in this implant covers. Use it. Do not
   do the sum in your head and type the result.
2. **A number in a page names how it was produced.** `cited` (taken from a
   source), `derived` (computed — say by which tool), `elicited` (judgement,
   with reasoning) or `absent` (a search that found nothing, with how hard
   it looked). A `derived` number a reader cannot reproduce with the same
   tool is a defect.
3. **Carry the structure through the calculation, not in your head.** A
   credence is computed in odds and log-odds by the tool, from inputs that
   are each labelled; a probability "combined" mentally from three
   percentages is how the factor-of-ten errors get in.
4. **If no tool exists and the number matters, write the tool** — then it is
   tested, reusable, and every later use is trustworthy — *or* state plainly
   that the figure is an unverified estimate. What is not allowed is a
   confident computed-looking number with no computation behind it.
5. **Reproduce a known answer before trusting the tool, and trust the tool
   over your intuition after.** The self-test (`skills/tools/selftest.py`)
   checks each tool against an independently known value — a textbook
   Bayes' theorem example, a hand-computable odds update — not against its
   own output. Once a tool reproduces the known answer, its result on a new
   input beats any gut feeling about what the answer "should" be — that is
   the entire point of building it.

## Why this is a convention and not just advice

Because the pull to guess is strong and constant. Typing a number is one
token-stream; stopping to call a calculator is a deliberate interruption, and
under time pressure the interruption is what gets skipped. Making it a standing
rule means the skipped step is a *violation*, visible and correctable, rather
than an invisible default. The same discipline, applied to probabilities, is
[Credence is a model, not a measurement](credence-is-a-model-not-a-measurement.md);
this convention is the general case, of which credence is the most dangerous
instance because there the wrong number also *sounds* like humility. The
tools themselves are listed by the skills that drive them, which is how
brainpick's [brain format](https://github.com/benquemax/brainpick/blob/main/docs/brain.md)
makes a tool discoverable before an agent decides to improvise.

## The test of compliance

Read any page's numbers and ask of each: *could I re-run the thing that made
this?* For a cited value, the citation resolves. For a derived value, the
named tool reproduces it. For a credence, the model replays. If the answer is
"no, it was just stated," the number has not earned its place — regardless of
how right it looks.
