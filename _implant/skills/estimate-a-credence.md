---
type: skill
title: Estimate a credence
description: "Use whenever you or the user are about to say how likely something is — 'probably', 'unlikely', 'I'd say 30 %' — and the question is genuinely one of belief under uncertainty rather than a fact that can be looked up. Turns the gut feeling into a stated, replayable model built with the user: reference class, factors, likelihood ratios as intervals, a Monte Carlo range, and a verdict on whether evidence or prior is carrying the result — then hands the model back so the user can change the inputs."
timestamp: 2026-09-25T18:30:00Z
depends_on: [using-the-brain-implant.md]
tools:
  - skills/tools/cogtools.py
  - skills/tools/cogtools/appraise.py
  - skills/tools/selftest.py
  - skills/tools/models/example-provocation.appraisal.json
export: agent-skill
---

# Estimate a credence

A language model states probabilities the way it states everything: fluently,
confidently, and from nowhere. "Probably", "unlikely", "maybe 30 %" arrive
with no structure behind them, so nobody — not the user, not the model — can
say *which* belief did the work. This skill replaces that with a model the
user can argue with. It implements
[Credence is a model, not a measurement](../conventions/credence-is-a-model-not-a-measurement.md)
and [Compute, never guess](../conventions/compute-never-guess.md).

The aim is not to tell anyone what is true. It is to make the gut feeling
**educated**: decomposed, sourced where it can be, and replayable by someone
who disagrees. The decision stays with the user.

## When to use it — and when not

Use it when a question is a genuine matter of belief under uncertainty: an
extrapolation, a contested interpretation, a prediction, a "which of these
is more defensible".

**Do not** use it on a question that has a checkable answer. Whether a text
says X is settled by reading the text; whether an experiment found an effect
is settled by the paper. Wrapping a fact in a probability replaces a hard
thing with a soft one. Bayes is for the joints between facts, not for the
facts ([Credence is a model, not a measurement](../conventions/credence-is-a-model-not-a-measurement.md)).

## The steps

### 1. State the proposition so that it could be false

Write the claim as one sentence with a truth value. "Is compatibilism
right?" is not a proposition; "the majority of professional philosophers
surveyed in 2020 accept or lean toward compatibilism" is, and it is also a
fact you should look up rather than model. Find the version of the question
that is really uncertain. If a domain implant is mounted, use its vocabulary
so that every term has a fixed sense.

### 2. Name the reference class, then the prior — as an interval

Ask: *of what population is this claim one instance, and how often are
claims in that population true?* That is the prior, and the population is
the reference class. The tool refuses a prior without one. Give it as a
range (`p_low`, `p_high`) — a point prior produces a fake range downstream.

Tell the user the reference class you chose and ask whether they would pick
another. Reference-class choice is usually where honest disagreement lives.

### 3. List the factors with the user

Ask the user what considerations bear on the question; add your own; look
for what a mounted domain implant already holds (a bias page, an argument
page, a survey). Each factor becomes one evidence item with a `kind`:

| kind | meaning |
| --- | --- |
| `cited` | a published finding, with its source |
| `derived` | computed from cited inputs, saying how |
| `elicited` | a judgement — yours or the user's — with its reasoning written out |
| `absent` | something that would have been found if the claim were true, and was not |

Before going on, check the list for **correlated factors**: two items that
share a hidden cause double-count the same doubt. Merge them or say
explicitly that they are conditionally independent and why.

### 4. Elicit each likelihood ratio — as an interval, with anchors

For each factor ask the local question: *how much more expected is this
observation if the claim is true than if it is false?* Anchor the answer
with the Kass & Raftery labels the tool prints
([doi:10.1080/01621459.1995.10476572](https://doi.org/10.1080/01621459.1995.10476572)):
LR 1–3 barely worth mentioning, 3–20 positive, 20–150 strong, over 150 very
strong; below 1 the same in reverse. Give `lr_low`/`lr_high`. For an
`absent` item do not guess the ratio — give the search sensitivity
(`Evidence.from_absence`, with `sensitivity_low`/`sensitivity_high`) and let
the tool derive it: barely looking yields LR ≈ 1, an exhaustive search
yields LR → 0.

Ask the user whether they accept each ratio. Record whose number each one is.

### 5. Run the tool — never the arithmetic in your head

```python
import sys; sys.path.insert(0, "_implant/skills/tools")
from cogtools.appraise import Appraisal, Prior, Evidence
ap = Appraisal(
    claim="…",
    prior=Prior(p=0.2, p_low=0.05, p_high=0.5, reference_class="…", source="user"),
    evidence=[
        Evidence("…", lr=4, lr_low=2, lr_high=8, kind="cited", source="doi:…"),
        Evidence("…", lr=0.6, lr_low=0.3, lr_high=0.9, kind="elicited", source="user, 2026-09-25"),
        Evidence.from_absence("…", sensitivity=0.5, sensitivity_low=0.3, sensitivity_high=0.7, source="…"),
    ],
    assessor="…", date="…",
)
print(ap.report())
open("model.json", "w").write(ap.to_json())
```

Replay any saved model with `python3 _implant/skills/tools/cogtools.py appraise model.json`.

### 6. Read the report the right way round

- **The range, not the point.** Report the median and the 90 % interval.
  A single number invites a precision that does not exist.
- **The prior-sensitivity verdict is the headline.** *Evidence-dominated*
  means the factors carry the conclusion and readers with different priors
  converge. *Prior-dominated* means the result is mostly the starting
  belief read back — say so plainly; it is the honest finding, not a
  failure.
- **The dominant factor is the real subject.** If one item outweighs all
  the others combined, the tool says so; the conversation should move to
  that item.
- **Composition.** How much of the model is cited versus elicited is
  reported; a model of pure judgement is a different object from one built
  on sources, and the user must see which they hold.

### 7. Hand the model back

Give the user the JSON and invite them to change any input and replay. End
with the substitution offer explicitly: *"These are the numbers I used;
which would you set differently?"* Then recompute with theirs. A credence
nobody can push back on has missed the point.

### 8. Check the elicitation itself

Before closing, look at how the numbers were produced: was the first number
mentioned an anchor for the rest? Were vivid factors weighted over dull
ones? If a domain implant holds bias pages, consult them here — the
appraisal is itself a piece of reasoning that can be biased, and the user
should know where.

## The provocation

The example model, `tools/models/example-provocation.appraisal.json`, shipped
with the tool is deliberately called a *provocation*: every number in it is
a placeholder, and its only purpose is to nudge a reader and their agent
into replacing it with a better model built from their own beliefs
([journal](../journals/2026-09-25.md)). Never cite it as a result. Copy it,
overwrite it, argue about it.

## What never happens here

- A bare probability in prose, from you, without a model behind it. If you
  would not build the model, say "I have no basis for a number" instead.
- A probability of 0 or 1 (the tool refuses them — Cromwell's rule).
- A credence on a question that has a citable answer.
- A model whose inputs the user was not shown and asked about.
