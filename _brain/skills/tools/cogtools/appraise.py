"""Bayesian appraisal — replayable credence models, not measurements.

Implements conventions/credence-is-a-model-not-a-measurement.md. The unit of
publication is a MODEL: a prior with a named reference class, a list of
evidence items each with a likelihood ratio and a citation, and a report of
how sensitive the result is to those inputs. The number is an output; the
structure and the inputs are the contribution.

Three things this module does that a naive Bayes calculator does not:

1. **Reports a range, never a point.** Every input may be given as an
   interval, and the posterior is reported as a distribution over those
   intervals (Monte Carlo), because multiplying midpoints systematically
   misstates the answer.

2. **Measures prior-sensitivity.** It re-runs the model across a sweep of
   priors and reports how much the posterior moves. That figure — not the
   headline credence — answers "how much of this is evidence and how much is
   faith": a conclusion that survives every defensible prior is carried by
   evidence, one that swings from near-zero to near-certain is carried by the
   assessor.

3. **Refuses certainty.** Cromwell's rule: probabilities are clamped away
   from 0 and 1, and a likelihood ratio of 0 or infinity is rejected. A
   factor at 0 makes all future evidence powerless against it.

Odds form is used throughout:

    posterior_odds = prior_odds * LR_1 * LR_2 * ... * LR_n

and results are also reported in bits (log2 odds), where the evidence
contributions become additive and directly comparable — a ranked list of what
actually moved the belief.

Pure standard library (random, math, json). No numpy required.

Bayes factor interpretation labels follow Kass & Raftery (1995), "Bayes
Factors", J. Amer. Statist. Assoc. 90(430), 773-795, doi:10.1080/01621459.1995.10476572
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass, field

# Cromwell's rule: never 0, never 1.
EPS = 1e-9


def clamp(p: float) -> float:
    return min(1.0 - EPS, max(EPS, p))


def p_to_odds(p: float) -> float:
    p = clamp(p)
    return p / (1.0 - p)


def odds_to_p(o: float) -> float:
    if o <= 0:
        return EPS
    if math.isinf(o):
        return 1.0 - EPS
    return o / (1.0 + o)


def bits(odds_ratio: float) -> float:
    """Log2 of a likelihood ratio — the evidence's weight in bits."""
    return math.log2(odds_ratio) if odds_ratio > 0 else float("-inf")


def kass_raftery(lr: float) -> str:
    """Verbal label for a Bayes factor, per Kass & Raftery (1995) table 1.

    Their scale is stated in terms of 2*ln(B); the equivalent B thresholds
    are 1-3 (not worth more than a bare mention), 3-20 (positive), 20-150
    (strong), >150 (very strong). Labels are symmetric for LR < 1.
    """
    b = lr if lr >= 1 else 1.0 / lr if lr > 0 else float("inf")
    direction = "for" if lr >= 1 else "against"
    if b < 3:
        strength = "not worth more than a bare mention"
    elif b < 20:
        strength = "positive"
    elif b < 150:
        strength = "strong"
    else:
        strength = "very strong"
    return f"{strength} ({direction})"


# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------

@dataclass
class Evidence:
    """One piece of evidence and how much it moves the belief.

    `lr` is the likelihood ratio P(observation | claim true) / P(observation |
    claim false). Give `lr_low`/`lr_high` when the ratio is itself uncertain —
    which it almost always is — and the Monte Carlo samples across that range.

    `kind` says where the likelihood ratio came from:
      cited | derived | elicited | absent
    `cited` is taken from a source that states it; `derived` is computed from
    cited inputs; `elicited` is a judgement (the assessor's or an expert's);
    `absent` is the "we looked and found nothing" case — see `searched`.

    `searched` (0..1) matters only for absent evidence: it is the probability
    we WOULD have found the thing if it were there. Absence of evidence is
    evidence of absence exactly in proportion to how hard we looked, and
    `Evidence.from_absence` computes the LR from it rather than letting an
    assessor guess.
    """

    name: str
    lr: float
    source: str = ""
    kind: str = "cited"
    lr_low: float | None = None
    lr_high: float | None = None
    note: str = ""

    def __post_init__(self):
        if self.lr <= 0 or math.isinf(self.lr):
            raise ValueError(
                f"evidence {self.name!r}: likelihood ratio must be finite and > 0 "
                "(Cromwell's rule — a 0 or infinite LR makes the claim unfalsifiable)"
            )
        if self.lr_low is not None and self.lr_low <= 0:
            raise ValueError(f"evidence {self.name!r}: lr_low must be > 0")

    @staticmethod
    def from_absence(name: str, sensitivity: float, false_alarm: float = 0.0,
                     source: str = "", note: str = "",
                     sensitivity_low: float | None = None,
                     sensitivity_high: float | None = None) -> "Evidence":
        """Evidence from NOT observing something, done correctly.

        `sensitivity` = P(we would have detected it | it is there), i.e. how
        hard and how well we looked. `false_alarm` = P(we would have reported
        it | it is not there). Give `sensitivity_low`/`sensitivity_high` when
        you are unsure how hard the search really was — almost always — and
        the LR interval follows from them, so the Monte Carlo samples it.

            LR = P(no detection | true) / P(no detection | false)
               = (1 - sensitivity) / (1 - false_alarm)

        With sensitivity ~ 0 (we barely looked) the LR is ~1: absence tells
        us essentially nothing — the correct treatment of "absence of evidence
        is not evidence of absence". With sensitivity ~ 1 (an exhaustive
        search that would certainly have found it) the LR approaches 0:
        absence becomes strong evidence of absence. The strength is a
        continuous function of how hard we looked, which is exactly the
        distinction that has to be handled honestly.
        """
        s = clamp(sensitivity)
        f = clamp(false_alarm)
        lr = (1.0 - s) / (1.0 - f)
        lr_low = lr_high = None
        if sensitivity_low is not None and sensitivity_high is not None:
            # a MORE sensitive search gives a SMALLER LR, so the bounds swap
            lr_low = (1.0 - clamp(sensitivity_high)) / (1.0 - f)
            lr_high = (1.0 - clamp(sensitivity_low)) / (1.0 - f)
        return Evidence(name=name, lr=lr, source=source, kind="absent",
                        lr_low=lr_low, lr_high=lr_high,
                        note=note or f"non-detection; search sensitivity {s:.2f}")


@dataclass
class Prior:
    """A prior with its reference class named — a number alone is not a prior."""

    p: float
    reference_class: str
    source: str = ""
    p_low: float | None = None
    p_high: float | None = None

    def __post_init__(self):
        if not self.reference_class:
            raise ValueError(
                "a prior must name its reference class — 'what population is this "
                "claim being drawn from?' An unlabelled number is not inspectable."
            )
        self.p = clamp(self.p)


# --------------------------------------------------------------------------
# The model
# --------------------------------------------------------------------------

@dataclass
class Appraisal:
    """A replayable credence model for one claim."""

    claim: str
    prior: Prior
    evidence: list[Evidence] = field(default_factory=list)
    assessor: str = ""
    date: str = ""
    notes: str = ""

    def add(self, e: Evidence) -> "Appraisal":
        self.evidence.append(e)
        return self

    # -- point estimate -----------------------------------------------------

    def posterior(self, prior_p: float | None = None,
                  lrs: list[float] | None = None) -> float:
        o = p_to_odds(self.prior.p if prior_p is None else prior_p)
        use = lrs if lrs is not None else [e.lr for e in self.evidence]
        for lr in use:
            o *= lr
        return odds_to_p(o)

    # -- Monte Carlo over stated input ranges -------------------------------

    def simulate(self, n: int = 20000, seed: int = 20260924) -> dict:
        """Propagate the stated input RANGES, not the midpoints.

        Multiplying best guesses discards the chance that several factors sit
        at the same end of their ranges at once, which is how naive Drake-style
        products mislead. Sampling log-uniformly over each LR's interval keeps
        the multiplicative structure honest.
        """
        rng = random.Random(seed)
        out = []
        for _ in range(n):
            if self.prior.p_low is not None and self.prior.p_high is not None:
                pp = rng.uniform(self.prior.p_low, self.prior.p_high)
            else:
                pp = self.prior.p
            o = p_to_odds(pp)
            for e in self.evidence:
                if e.lr_low is not None and e.lr_high is not None:
                    lo, hi = math.log(e.lr_low), math.log(e.lr_high)
                    o *= math.exp(rng.uniform(lo, hi))
                else:
                    o *= e.lr
            out.append(odds_to_p(o))
        out.sort()

        def pct(q):
            if not out:
                return float("nan")
            i = min(len(out) - 1, max(0, int(q * len(out))))
            return out[i]

        return {
            "n": n,
            "p05": pct(0.05), "p25": pct(0.25), "median": pct(0.50),
            "p75": pct(0.75), "p95": pct(0.95),
            "mean": sum(out) / len(out),
            "point": self.posterior(),
        }

    # -- sensitivity: the figure that answers "evidence or faith?" ----------

    def prior_sensitivity(self, priors=(0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9)) -> dict:
        """Sweep the prior across defensible values; report how far the
        posterior moves, and whether evidence or prior is carrying it.

        Two measures, because neither alone is honest:

        * `swing` — the spread of posterior PROBABILITY across the sweep.
          This is what matters for a decision, but it compresses near 0 and
          1: three conclusions of 0.001, 0.01 and 0.1 differ by two orders of
          magnitude while showing a swing of only 0.099.

        * `evidence_bits` vs `prior_span_bits` — the principled comparison.
          Evidence weight is |sum log2 LR|; the prior's span is the width of
          the stated prior interval in log-odds. In log-odds the sweep shifts
          the posterior one-for-one, so the question "does the evidence
          outweigh my starting belief?" is exactly the ratio of these two.
          `dominance` is that ratio, and it does not compress at the tails.

        The verdict uses dominance, with the probability table always printed
        so a reader can judge for themselves. Thresholds are this brain's
        stated reporting convention, not a result from the literature.
        """
        rows = [(p, self.posterior(prior_p=p)) for p in priors]
        post = [r[1] for r in rows]
        swing = max(post) - min(post)

        ev_bits = abs(sum(bits(e.lr) for e in self.evidence))
        lo = self.prior.p_low if self.prior.p_low is not None else min(priors)
        hi = self.prior.p_high if self.prior.p_high is not None else max(priors)
        span = abs(math.log2(p_to_odds(hi)) - math.log2(p_to_odds(lo)))
        dominance = ev_bits / span if span > 0 else float("inf")

        if dominance >= 2.0:
            verdict = "evidence-dominated"
        elif dominance >= 0.5:
            verdict = "mixed"
        else:
            verdict = "prior-dominated"
        return {"rows": rows, "swing": swing, "verdict": verdict,
                "evidence_bits": ev_bits, "prior_span_bits": span,
                "dominance": dominance}

    def evidence_sensitivity(self) -> list[dict]:
        """Leave-one-out: how much does each item actually matter?

        Reports the posterior with the item removed, and the item's weight in
        bits. The dominant factor is the real subject of the page.
        """
        base = self.posterior()
        rows = []
        for i, e in enumerate(self.evidence):
            without = self.posterior(lrs=[x.lr for j, x in enumerate(self.evidence) if j != i])
            rows.append({
                "name": e.name, "lr": e.lr, "bits": bits(e.lr),
                "kind": e.kind, "source": e.source,
                "posterior_without": without, "delta": base - without,
                "label": kass_raftery(e.lr),
            })
        rows.sort(key=lambda r: abs(r["bits"]), reverse=True)
        return rows

    def composition(self) -> dict:
        """How much of this model is cited evidence versus judgement?

        A model built from ten cited inputs is a different object from one
        built from ten elicited guesses, and the reader must be able to see
        which they are holding. "Hard" inputs are `cited` and `derived`.
        """
        counts: dict[str, int] = {}
        for e in self.evidence:
            counts[e.kind] = counts.get(e.kind, 0) + 1
        total = max(1, len(self.evidence))
        hard = sum(counts.get(k, 0) for k in ("cited", "derived"))
        return {"counts": counts, "n": len(self.evidence),
                "hard_fraction": hard / total,
                "uncited": sum(1 for e in self.evidence if not e.source)}

    # -- reporting ----------------------------------------------------------

    def report(self, n: int = 20000) -> str:
        sim = self.simulate(n)
        ps = self.prior_sensitivity()
        ev = self.evidence_sensitivity()
        comp = self.composition()

        L = []
        L.append(f"# Appraisal: {self.claim}")
        L.append("")
        if self.assessor or self.date:
            L.append(f"*Assessed by {self.assessor or 'unattributed'}"
                     f"{' on ' + self.date if self.date else ''}.*")
            L.append("")
        L.append(f"**Prior** {self.prior.p:.3g} — reference class: "
                 f"{self.prior.reference_class}"
                 + (f" ({self.prior.source})" if self.prior.source else ""))
        L.append("")
        L.append(f"**Posterior** median **{sim['median']:.3g}**, "
                 f"90 % interval {sim['p05']:.3g}–{sim['p95']:.3g} "
                 f"(point estimate from midpoints: {sim['point']:.3g})")
        L.append("")
        L.append(f"**Prior-sensitivity** → **{ps['verdict']}** "
                 f"(evidence {ps['evidence_bits']:.1f} bits vs prior span "
                 f"{ps['prior_span_bits']:.1f} bits; dominance {ps['dominance']:.2f}× — "
                 f"posterior swing {ps['swing']:.2f} across the sweep)")
        L.append("")
        L.append("| prior | posterior |")
        L.append("|---|---|")
        for p, q in ps["rows"]:
            L.append(f"| {p:.3g} | {q:.3g} |")
        L.append("")
        L.append("## What moved the belief")
        L.append("")
        L.append("| evidence | LR | bits | strength | kind | source |")
        L.append("|---|---|---|---|---|---|")
        for r in ev:
            L.append(f"| {r['name']} | {r['lr']:.3g} | {r['bits']:+.2f} | "
                     f"{r['label']} | {r['kind']} | {r['source'] or '—'} |")
        L.append("")
        L.append(f"**Composition** {comp['n']} items; "
                 f"{comp['hard_fraction'] * 100:.0f} % cited or derived; "
                 f"{comp['uncited']} without a source.")
        if comp["uncited"]:
            L.append("")
            L.append(f"> ⚠ {comp['uncited']} input(s) carry no citation. "
                     "Under conventions/every-claim-carries-its-receipt.md each must be "
                     "labelled an assumption or given a source.")
        if ev and abs(ev[0]["bits"]) > sum(abs(r["bits"]) for r in ev[1:]):
            L.append("")
            L.append(f"> ⚠ **{ev[0]['name']}** outweighs every other input combined. "
                     "That factor is the real subject here; the rest is decoration.")
        if self.notes:
            L.append("")
            L.append(self.notes)
        return "\n".join(L)

    def as_dict(self) -> dict:
        return {
            "claim": self.claim,
            "assessor": self.assessor, "date": self.date,
            "prior": {"p": self.prior.p, "reference_class": self.prior.reference_class,
                      "source": self.prior.source,
                      "p_low": self.prior.p_low, "p_high": self.prior.p_high},
            "evidence": [{"name": e.name, "lr": e.lr, "lr_low": e.lr_low,
                          "lr_high": e.lr_high, "kind": e.kind,
                          "source": e.source, "note": e.note} for e in self.evidence],
            "result": self.simulate(),
            "prior_sensitivity": self.prior_sensitivity(),
            "composition": self.composition(),
            "notes": self.notes,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.as_dict(), indent=indent)

    @staticmethod
    def from_dict(d: dict) -> "Appraisal":
        """Rebuild a model from its record — this is what makes it replayable.

        A reader who disagrees edits the JSON and re-runs; the disagreement is
        then located at a named input rather than spread through prose.
        """
        pr = d["prior"]
        a = Appraisal(
            claim=d["claim"],
            prior=Prior(p=pr["p"], reference_class=pr["reference_class"],
                        source=pr.get("source", ""),
                        p_low=pr.get("p_low"), p_high=pr.get("p_high")),
            assessor=d.get("assessor", ""), date=d.get("date", ""),
            notes=d.get("notes", ""),
        )
        for e in d.get("evidence", []):
            a.add(Evidence(name=e["name"], lr=e["lr"], source=e.get("source", ""),
                           kind=e.get("kind", "cited"), lr_low=e.get("lr_low"),
                           lr_high=e.get("lr_high"), note=e.get("note", "")))
        return a
