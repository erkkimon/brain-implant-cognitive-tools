---
type: convention
about: concept
title: Evidence before authority
description: A claim is weighed by the evidence behind it and never by who made it — a famous author's thesis and an unknown graduate student's paper are appraised on the same scale, criticism lands on the argument rather than the person, and a proposal's authorship is a separate question (whose idea is this, provably) from its soundness (does the evidence hold).
tags: [convention, epistemics, bias, assessment, appraisal]
timestamp: 2026-09-27T12:19:44Z
half_life: 0
---

# Evidence before authority

Decided by erkkimon on 2026-09-25, founding the cognitive-tools implant
([journal](../journals/archive/2026/09/2026-09-25.md)). The tools here exist to appraise
claims *in the light of evidence* — how much of a belief stands on
established fact, how hard that evidence is, and where it becomes faith.
That appraisal is worthless if it flinches when the author is famous, and
equally worthless if it sneers when the author is unfashionable.

## The rule

**Appraise the argument, never the arguer.** The questions this implant's
tools ask are what kind of evidence exists, how direct it is, how well it
was tested, and how far the claim is extrapolated beyond it. None of those
questions has a field for reputation.

Concretely:

1. **Same scale for everyone.** A paper in a peer-reviewed journal, a
   think-tank report, a book chapter, a blog post and a conference talk are
   each appraised by their evidence and their testability. A celebrated
   author's thesis gets no credit for being widely read and no penalty for
   being popular. Reach and funding are evidence about *capability and
   intent*, which is a real and citable thing — they are simply not
   evidence about whether the claim is true.
2. **Credentials are a weak prior, and they are named as one.** That an
   author has spent thirty years on a problem is a legitimate, small reason
   to expect their reasoning to be sound; it is never a reason to skip
   checking it. Where this implant leans on expertise it says so explicitly,
   as a prior, not as a conclusion.
3. **Criticism attaches to the claim.** "This estimate assumes a base rate
   the survey data do not support ([source])" is in scope. "This author is
   a crank" is not, and never appears here — it is unciteable, it is about a
   person, and it survives in a public repository as defamation rather than
   analysis. Where a *published* critique makes a strong claim about an
   author's competence, this implant reports that the critique exists and
   cites it, without adopting its tone.
4. **Consensus is evidence, not proof.** That most of a field believes
   something is real information about the weight of evidence they have
   seen, and it is reported as such — with a citation to where the consensus
   is stated, not asserted from memory. It does not close a question, and a
   well-evidenced minority result is not downgraded for being a minority
   result. The [GRADE](https://www.gradeworkinggroup.org/) approach to
   rating evidence is the model here: what matters is the design, the
   directness and the consistency of the evidence, not the standing of who
   reports it.
5. **Symmetry of scrutiny.** The test: would this claim get the same
   appraisal if the name on it were swapped for an unknown's? If a thesis is
   being treated gently because it is exciting, or harshly because it is
   commercial, the appraisal is wrong. This applies in both directions — the
   reflex to debunk a famous claim is as much a bias as the reflex to
   believe it.

## Authorship and soundness are two separate questions

Conflating them is the most common failure in writing about any influential
idea.

- **"Is this really their claim?"** is a *provenance* question, settled by
  primary sources: what the person actually published, said, or wrote, cited
  to a locator — an edition and page, a timestamp, a dated post — never to a
  journalist's paraphrase of it. It has an answer, and the answer can be
  wrong in checkable ways. A widely attributed idea that traces back to
  nobody is a finding worth recording.
- **"Is it true?"** is a *soundness* question, settled by evidence and
  argument. It is answered the same way whoever turns out to have said it.

Getting the first right is a precondition for the second being fair: it is
not an appraisal of someone's thesis if the thesis being appraised is a
distortion of what they said. Equally, establishing that a claim is
genuinely someone's says nothing whatever about whether it is true.

## Faith is a category, not an insult

Almost every ambitious argument contains steps that nothing yet
demonstrates. Labelling such a step *faith* — a commitment held beyond what
the evidence presently supports — is a neutral, structural observation, and
this implant makes it about steps rather than about people. Naming it is not
debunking: the point of separating the hard-evidence portion from the
faith portion is to show precisely *where* the load is being carried by
assumption, which is exactly the information a reader deciding what to
believe needs.

And the separation cuts the other way too. **Absence of evidence is not
evidence of absence** — when nobody has run the study, the absence of a
result is expected under both "this holds" and "this does not", and
therefore discriminates between them hardly at all. A step is downgraded
when there is evidence *against* it or when the search that should have
found support came up empty; not merely because it has not been tested yet.
The appraiser makes this explicit: an `absent` piece of evidence carries a
`searched` probability — how likely the search was to find the thing if it
existed — and its likelihood ratio is computed from that rather than
guessed (`skills/tools/cogtools/appraise.py`). Treating the untested as the
disproven would be as unscientific as treating the untested as the proven.

## Why it is a standing rule

Because it is easiest to abandon exactly where it matters most: on the small
number of famous, heavily publicised claims that most readers arrive asking
about. A rule written down before those appraisals are drafted is harder to
bend than a judgement made while drafting them.

It works with [Every claim carries its receipt](every-claim-carries-its-receipt.md):
receipts make the evidence checkable, and this rule says the evidence — and
only the evidence — decides.
