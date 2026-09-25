#!/usr/bin/env python3
"""Self-test for the cogtools appraiser — run it before trusting a number.

    python3 selftest.py

Standard library only, no pytest. Each check names what it is checked
against, so a reader can verify the test as well as the code.

Exit status 0 if every check passes, 1 otherwise.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cogtools.appraise import Appraisal, Evidence, Prior, bits, odds_to_p, p_to_odds  # noqa: E402

PASS, FAIL = [], []


def check(name: str, got: float, want: float, tol: float, source: str):
    """Assert |got - want| / |want| <= tol, naming the reference."""
    rel = abs(got - want) / abs(want) if want else abs(got)
    ok = rel <= tol
    (PASS if ok else FAIL).append(
        f"{'ok  ' if ok else 'FAIL'} {name}: got {got:.6g}, want {want:.6g} "
        f"({rel * 100:.2f}% off, tol {tol * 100:.0f}%) — {source}")


def check_true(name: str, cond: bool, detail: str = ""):
    (PASS if cond else FAIL).append(f"{'ok  ' if cond else 'FAIL'} {name} {detail}")


def test_odds():
    """(a) odds/probability round trips."""
    for p in (0.001, 0.3, 0.5, 0.9):
        check(f"odds round trip p={p}", odds_to_p(p_to_odds(p)), p, 1e-9, "algebra")
    check("even odds are p=0.5", odds_to_p(1.0), 0.5, 1e-12, "definition")
    check("LR 2 is one bit", bits(2.0), 1.0, 1e-9, "log2 by definition")
    # A textbook screening case: prevalence 1%, sens 99%, spec 99% -> PPV 50%
    a = Appraisal("disease present", Prior(0.01, "screened population", "textbook"))
    a.add(Evidence("positive test", 99.0, "textbook", "cited"))
    check("classic base-rate example PPV", a.posterior(), 0.5, 0.01,
          "standard Bayes screening example")


def test_refusals():
    """(b) Cromwell's rule and the named-reference-class rule."""
    for bad in (0.0, -1.0, float("inf")):
        try:
            Evidence("impossible", bad)
            check_true(f"LR {bad} refused", False, "(it was accepted!)")
        except ValueError:
            check_true(f"LR {bad} refused", True)
    try:
        Evidence("bad low", 1.0, lr_low=0.0, lr_high=2.0)
        check_true("lr_low 0 refused", False, "(it was accepted!)")
    except ValueError:
        check_true("lr_low 0 refused", True)
    try:
        Prior(0.5, "")
        check_true("prior without reference class refused", False, "(accepted!)")
    except ValueError:
        check_true("prior without reference class refused", True)


def test_absence():
    """(c) absence of evidence weighs exactly as much as the search did."""
    weak = Evidence.from_absence("barely looked", 0.0)
    strong = Evidence.from_absence("exhaustive search", 0.999)
    check("sensitivity 0 gives LR 1", weak.lr, 1.0, 1e-6, "(1-s)/(1-f) with s=f=0")
    check_true("sensitivity -> 1 gives LR -> 0", strong.lr < 0.002,
               f"(LR={strong.lr:.4f}, {bits(strong.lr):+.2f} bits)")
    check_true("absence evidence is kind 'absent'", weak.kind == "absent")
    ranged = Evidence.from_absence("uncertain search", 0.5,
                                   sensitivity_low=0.3, sensitivity_high=0.7)
    check("sensitivity interval: lr_low from the MORE sensitive end", ranged.lr_low, 0.3, 1e-6,
          "(1-0.7)/(1-0)")
    check("sensitivity interval: lr_high from the LESS sensitive end", ranged.lr_high, 0.7, 1e-6,
          "(1-0.3)/(1-0)")
    check_true("sensitivity interval brackets the point LR",
               ranged.lr_low < ranged.lr < ranged.lr_high)


def test_interval_range():
    """(d) interval inputs give a real, ordered range."""
    m = Appraisal("interval", Prior(0.1, "rc", "x", p_low=0.03, p_high=0.25))
    m.add(Evidence("interval lr", 0.05, "x", "cited", lr_low=0.02, lr_high=0.15))
    m.add(Evidence("second lr", 3.0, "x", "elicited", lr_low=1.5, lr_high=6.0))
    sim = m.simulate(n=5000)
    check_true("p05 < median < p95 (a real range)",
               sim["p05"] < sim["median"] < sim["p95"],
               f"(p05={sim['p05']:.4g}, median={sim['median']:.4g}, p95={sim['p95']:.4g})")
    # Point inputs, by contrast, collapse to a degenerate range — the trap.
    pt = Appraisal("point", Prior(0.1, "rc", "x"))
    pt.add(Evidence("point lr", 0.05, "x", "cited"))
    ps = pt.simulate(n=200)
    check_true("point inputs collapse to a degenerate range", ps["p05"] == ps["p95"])


def test_prior_sensitivity():
    """(e) the verdict labels distinguish evidence from faith."""
    weak = Appraisal("weak", Prior(0.5, "rc", "x", p_low=0.05, p_high=0.95))
    weak.add(Evidence("mild hint", 1.3, "x", "elicited"))
    check_true("weak evidence reads as prior-dominated",
               weak.prior_sensitivity()["verdict"] == "prior-dominated")
    mixed = Appraisal("mixed", Prior(0.5, "rc", "x", p_low=0.2, p_high=0.8))
    mixed.add(Evidence("moderate", 8.0, "x", "cited"))  # 3 bits vs 4 bits span
    check_true("moderate evidence reads as mixed",
               mixed.prior_sensitivity()["verdict"] == "mixed")
    strong = Appraisal("strong", Prior(0.5, "rc", "x", p_low=0.4, p_high=0.6))
    strong.add(Evidence("decisive", 1000.0, "doi:x", "cited"))
    check_true("strong evidence reads as evidence-dominated",
               strong.prior_sensitivity()["verdict"] == "evidence-dominated")


def test_round_trip():
    """(f) as_dict -> from_dict -> same posterior; replayability is the point."""
    a = Appraisal("claim", Prior(0.2, "rc", "src", p_low=0.05, p_high=0.5),
                  assessor="selftest", date="2026-01-01", notes="n")
    a.add(Evidence("one", 4.0, "s1", "cited", lr_low=2.0, lr_high=8.0, note="x"))
    a.add(Evidence("two", 0.5, "s2", "elicited"))
    a.add(Evidence.from_absence("three", 0.7, source="s3"))
    back = Appraisal.from_dict(a.as_dict())
    check("posterior survives a round trip", back.posterior(), a.posterior(),
          1e-12, "replayability requirement")
    check_true("record survives a round trip", back.as_dict() == a.as_dict())
    comp = a.composition()
    check_true("composition counts cited+derived as hard",
               comp["hard_fraction"] == 1 / 3 and comp["counts"]["absent"] == 1,
               f"({comp})")


def main():
    for fn in (test_odds, test_refusals, test_absence, test_interval_range,
               test_prior_sensitivity, test_round_trip):
        try:
            fn()
        except Exception as exc:  # a crash is a failure, reported not swallowed
            FAIL.append(f"FAIL {fn.__name__} raised {type(exc).__name__}: {exc}")

    if FAIL:
        for line in PASS:
            print(line)
        print()
        for line in FAIL:
            print(line)
        print()
        print(f"{len(PASS)} passed, {len(FAIL)} failed")
        return 1
    print(f"selftest: all {len(PASS)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
