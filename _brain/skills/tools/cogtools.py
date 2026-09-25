#!/usr/bin/env python3
"""cogtools — the brain's cognitive tools, on one command line.

Every subcommand replays a saved model deterministically and prints its
result with the inputs that produced it, so a reader can dispute a named
input rather than the conclusion.

    python3 cogtools.py appraise model.json           # replay a credence model
    python3 cogtools.py appraise model.json --json    # the full record as JSON
    python3 cogtools.py appraise model.json --n 50000 # more Monte Carlo samples

Pure standard library; nothing here reaches the network. Runs from any cwd.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cogtools.appraise import Appraisal  # noqa: E402


def cmd_appraise(a):
    with open(a.model, encoding="utf-8") as fh:
        d = json.load(fh)
    ap = Appraisal.from_dict(d)
    if a.json:
        rec = ap.as_dict()
        rec["result"] = ap.simulate(a.n)
        print(json.dumps(rec, indent=2))
    else:
        print(ap.report(a.n))


def main(argv=None):
    p = argparse.ArgumentParser(prog="cogtools", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("appraise", help="replay a Bayesian credence model")
    q.add_argument("model", help="path to the model JSON")
    q.add_argument("--json", action="store_true", help="machine-readable output")
    q.add_argument("--n", type=int, default=20000,
                   help="Monte Carlo samples over the input ranges (default 20000)")
    q.set_defaults(fn=cmd_appraise)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    main()
