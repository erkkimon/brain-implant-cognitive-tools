---
type: article
about: concept
title: "Manifest: tools for the blind spots of a language model"
description: "Why this implant exists and what it may hold — small, deterministic, replayable tools that cover the things a language model's architecture does badly: arithmetic it emits instead of computing, probabilities it states as if measured, confidence without a source; each tool ships with its self-test, the skill that drives it, and the documented case against its method. Everything else in the implant should be derivable from this page."
tags: [vision, manifest, cognitive-tools, bayesian, llm, blind-spots]
timestamp: 2026-09-27T12:19:44Z
half_life: 0
---

# Manifest: tools for the blind spots of a language model

Founded by erkkimon on 2026-09-25 ([journal](../journals/archive/2026/09/2026-09-25.md)).

## The problem

A large language model is an engine that emits the most plausible next
token. That makes it fluent and broad, and it makes it systematically bad at
a short list of things that plausibility cannot do:

- **Arithmetic.** It produces confident numbers it did not compute.
- **Calibration.** It says "about 30 %" with no model behind the number,
  and the number moves with the phrasing of the question.
- **Systematicity.** Asked to find every instance of something, it finds
  the instances that came to mind.
- **Provenance.** It knows a fact and not where the fact came from.
- **Sensitivity.** It cannot say which of its inputs is carrying its
  conclusion, because it has no inputs — only a prompt.

These are not knowledge gaps; a bigger model does not close them. They are
properties of the architecture, and the remedy is the one a careful human
uses: stop generating and use a tool.

## What this implant is

A public brainpick brain implant holding **cognitive tools** — scripts an
agent runs instead of guessing, together with the skill that says when to
run each and the knowledge that says what the method assumes. Every tool
here is:

1. **Deterministic and replayable** — same inputs, same output, saved as a
   file anyone can change and rerun ([Compute, never guess](../conventions/compute-never-guess.md)).
2. **Honest about its inputs** — each labelled by kind, `cited | derived |
   elicited | absent`, so a reader sees how much of a result is evidence and
   how much is judgement ([Credence is a model, not a measurement](../conventions/credence-is-a-model-not-a-measurement.md)).
3. **Self-tested** — `skills/tools/selftest.py` must pass before a commit.
4. **Documented with its case against** — the objections to the method
   live in `knowledge/` beside the method, with receipts
   ([Every claim carries its receipt](../conventions/every-claim-carries-its-receipt.md)).
   A tool offered as a truth rather than as a tool is a bias with a
   command line.

## What it is not

It holds no domain knowledge and no opinions. Domain implants (philosophy
first) supply the factors, the base rates and the bias catalogues; the
agent's own cortex holds its conclusions
([Using the brain implant](../skills/using-the-brain-implant.md)). A worked
example shipped here is a **provocation** — numbers that exist to be
overwritten by the reader's own.

## The first tool, and the next

The first is the Bayesian credence appraiser, driven by
[Estimate a credence](../skills/estimate-a-credence.md). Candidates that
fit the same test — a blind spot, a deterministic remedy, a self-test, a
case against: a calibration ledger that scores resolved credences against
outcomes; a reference-class finder; a systematic-checklist runner that
walks a catalogue instead of memory. Each is a todo ([open work](../todo/open.md)) until it has all four.
