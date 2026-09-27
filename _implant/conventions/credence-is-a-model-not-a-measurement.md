---
type: convention
about: concept
title: Credence is a model, not a measurement
description: Numeric probabilities attached to hypotheses in this implant are the output of a stated, replayable model — a decomposition into factors, a prior, and explicit likelihood ratios with their justifications — never a claim to have measured a truth; the contribution is the structure and its defensible inputs, so any reader can substitute their own numbers and recompute, and the spread of results across reasonable inputs is itself the report on how much of a belief is evidence and how much is faith.
tags: [convention, bayesian, epistemics, credence, uncertainty, replicability]
timestamp: 2026-09-27T12:19:44Z
half_life: 0
---

# Credence is a model, not a measurement

Decided by erkkimon on 2026-09-25, founding the cognitive-tools implant
([journal](../journals/archive/2026/09/2026-09-25.md)):

> *"It is at least a formal way to systematically get some kind of a number
> for beliefs, and of course, we cannot say exact probabilities for the
> factors, but at least we can give them some numbers that say something […]
> if somebody wants to use different kind of probabilities, there could be a
> tool for that so they can then calculate the probability that they believe
> in based on how good probabilities they give to the factors. So then
> everything is replicable and everybody can use the factors that they think
> are true."*

That is the whole justification, and it survives the usual objection. The
objection — *"you cannot know that this hypothesis is 12 % likely"* — is
correct and beside the point, because the number was never the claim.

## What is actually being published

**The model, not the number.** A credence in this implant is a small,
inspectable artifact with four parts:

1. **A decomposition** — what has to hold for the claim to be true, stated
   as named factors. This is the real intellectual contribution and the part
   that can be wrong in interesting ways.
2. **A prior** — with its reference class named. "Published psychology
   effects of this size, in this subfield, that survived a preregistered
   direct replication" is a reference class; a number alone is not.
3. **Likelihood ratios** — for each piece of evidence, how much more
   expected that observation is if the claim holds than if it does not, with
   the reasoning and a citation.
4. **A provenance record** — who assigned each input, on what date, from
   what source, and of which kind
   ([receipts](every-claim-carries-its-receipt.md)).

A reader who disagrees does not have to argue about the conclusion. They
change the input they object to and recompute. Everything downstream moves
automatically, and the disagreement is now *located* — at factor 3, say,
rather than somewhere in a paragraph of prose. That is a far better
epistemic position than two essays talking past each other, and it is why
this is worth doing even though none of the numbers are measurements.

## The rule

1. **Every credence ships with its model.** A bare probability in prose is
   forbidden. The number appears with, or links to, the decomposition and
   inputs that produced it. A number nobody can replay is decoration.
2. **Every input is labelled by kind** — `cited` (taken from a source that
   states it), `derived` (computed from cited inputs), `elicited` (a
   judgement, this brain implant's or an expert's, with its reasoning
   written out), or `absent` (a search that found nothing, with how hard it
   looked). The proportions of each kind across a model are themselves
   reported: a model built from twelve elicited inputs is a different object
   from one built from ten cited ones, and the reader must be able to see
   which they are holding.
3. **Never a single number.** A credence is reported as a range across
   defensible inputs, with the point estimate as one value inside it.
   Reporting `0.12` invites a precision that does not exist; reporting
   `0.02–0.35, point 0.12 under the default inputs` is honest and just as
   actionable.
4. **Sensitivity is mandatory output.** Every model reports which factor
   dominates the result. If moving one input across its plausible range
   swings the posterior more than all others combined, that factor is the
   real subject and the page says so.
5. **Never assign 0 or 1** (Cromwell's rule). A factor at 0 makes all
   evidence powerless against it; a factor at 1 makes it unfalsifiable.
   Certainty about an empirical claim is not available and the tool refuses
   it.
6. **Do not Bayesianise what is measured.** See below — this is the rule
   most likely to be broken by enthusiasm.

## Bayes is for the joints, not for the facts

The most common abuse of this machinery is applying it to questions that
have answers. What percentage of respondents in a named, published survey
answered "yes" is not a matter of belief: it is a measurement question, and
it has a published answer with a sampling error attached. Wrapping it in a
subjective probability replaces a hard fact with a soft one and makes the
implant *worse* than the literature it was built from.

So: **cited facts go in as facts, with their published uncertainties.**
Credence modelling applies to the joints between them — the extrapolations,
the "does this effect generalise beyond the population it was measured in",
the "will this hold up when someone replicates it", the steps where the
evidence genuinely runs out and judgement begins. Those joints are what this
implant calls *faith*, and putting a number on them is how the faith gets
measured instead of merely admitted.

Where a model assigns a credence to something that has a citable measured
answer, that is a defect in the model.

## Odds form, because it makes disagreement local

Credences here are computed in odds form:

    posterior odds = prior odds × LR₁ × LR₂ × … × LRₙ

and reported in log-odds as well, where the multiplications become
additions. Two reasons, both practical:

- **A likelihood ratio is a local judgement.** "How much more expected is
  this observation if the claim is true than if it is false?" is a question
  about one piece of evidence, answerable by someone who knows that
  evidence. "What is the probability that this whole theory is right?" is a
  question about everything at once, answerable by nobody. Eliciting the
  local quantities honestly is achievable; eliciting the global one is not.
- **In log-odds, the contributions are additive and comparable.** The
  evidence that moved a belief can be shown as a ranked list — this
  replication added +1.2 bits, this failed preregistration subtracted −3.0 —
  which is a far more useful summary than the posterior alone.

## The multiplication trap

A decomposition into many factors that are then multiplied will produce a
tiny number almost regardless of the inputs: ten factors at 0.7 multiply to
0.028. This is a known failure — the same arithmetic that makes naive Drake
equation estimates collapse — and it has two distinct causes, both of which
this implant handles explicitly.

- **Correlation.** Factors are usually not independent, because they share
  hidden causes ("the measurement instrument is valid", "the sample was not
  selected on the outcome"). Multiplying correlated factors double-counts
  the same doubt repeatedly. A model must either state that its factors are
  conditionally independent *and defend it*, or model the shared cause as
  its own node and condition on it.
- **Point estimates instead of distributions.** Multiplying best guesses
  discards the probability that several factors are simultaneously at the
  optimistic end. Propagating distributions — a Monte Carlo over the input
  ranges — gives a different and much wider answer than multiplying the
  midpoints, and the difference is often orders of magnitude.

So the appraiser (`skills/tools/cogtools/appraise.py`, driven by
`skills/tools/cogtools.py`) propagates distributions by default, and a
decomposition with more than a handful of multiplied factors is treated as
a smell to be justified rather than a sign of rigour.

## The payoff: faith and evidence, separated numerically

How much of a belief stands on hard evidence and how much on faith? A
sensitivity analysis answers that *quantitatively*, which prose cannot:

- If the posterior stays within a narrow band across every defensible choice
  of prior and factor, the **evidence is carrying the conclusion**. Readers
  with different starting beliefs converge. That is what a well-evidenced
  claim looks like.
- If the posterior swings from near-zero to near-certain across choices that
  reasonable people would make, the conclusion is **prior-dominated** — it
  is being carried by what the assessor believed before looking. That is
  what faith looks like, stated precisely, without insulting anyone.

Every appraisal in this implant therefore reports its prior-sensitivity, and
that figure — not the headline credence — is the honest summary of how much
is known. A claim whose credibility swings on the assessor's temperament
has been *characterised*, which is the useful result, even though it has not
been settled.

## A worked example is a provocation

The implant ships a published example model
(`skills/tools/models/example-provocation.appraisal.json`), and it is
deliberately called a *provocation*. Its numbers are not this implant's
verdict on anything; they exist to be overwritten by the reader's own. The
point of publishing it is to nudge a person and their agent into doing a
better calculation from their own beliefs — to change a prior, replace a
likelihood ratio they find indefensible, add the evidence the example
missed, and rerun — never to hand them a conclusion. A reader who walks
away quoting the example's posterior has misused it; a reader who walks
away with a different posterior and a clear picture of *which input made
the difference* has used it as intended. This framing is erkkimon's
founding decision for the implant
([journal](../journals/archive/2026/09/2026-09-25.md)), and it is why the file's name says
what it is.

## What this does not claim

It does not claim the numbers are objective, that the decomposition is the
only sensible one, or that a posterior is a forecast anyone should bet on
without reading the model. It claims something narrower and defensible: that
a belief with a stated structure and stated inputs is inspectable,
criticisable and replayable, and a belief expressed as confident prose is
none of those things. The calibrated-language guidance the IPCC gives its
authors makes the same distinction between the *confidence* in a finding and
the *likelihood* it expresses
([IPCC AR5 guidance note](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)),
and this implant keeps the two apart for the same reason.

Calibration is the long-term check — where a model's claims resolve, the
record is kept and scored, because a credence machine that is never scored
against outcomes is a rhetoric machine.
