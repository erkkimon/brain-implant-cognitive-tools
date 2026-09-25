# Skills

Procedures an agent follows here — the most distilled, tested layer of the
implant. Each is `type: skill`; the dependency tree is in
[skilltree.md](skilltree.md) (generated — never edited by hand). Read the
[conventions](../conventions/index.md) first: a rule constrains what a
procedure is for.

Skills say *brain implant*, not *brain*: a brain is the agent's own cortex
plus the implants mounted beside it, and opinions go to the cortex
([Using the brain implant](using-the-brain-implant.md)).

## Skills

* [Using the brain implant](using-the-brain-implant.md) — pull first, read
  most-distilled-first, ground every claim, route opinions to the cortex.
* [Estimate a credence](estimate-a-credence.md) — turn "probably" into a
  stated, replayable model built with the user: reference-class prior,
  factors, likelihood-ratio intervals, a Monte Carlo range, a verdict on
  whether evidence or prior carries the result; hand the model back.

## Tools

Deterministic scripts the skills drive, in `tools/`: pure
standard-library Python 3.10+, no network, each with a self-test.

* `cogtools.py` — command-line entry: `appraise <model.json> [--json] [--n N]`.
* `cogtools/appraise.py` — the Bayesian credence appraiser (odds form,
  interval likelihood ratios, Monte Carlo, prior-sensitivity verdict,
  Kass–Raftery labels, absence-of-evidence factors).
* `selftest.py` — checks the appraiser against known cases.
* `models/example-provocation.appraisal.json` — a worked model whose
  numbers exist to be overwritten.
