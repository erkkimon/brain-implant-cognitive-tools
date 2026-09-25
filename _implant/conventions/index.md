# Conventions

Standing rules for how work is done here — naming, process, contracts the
brain implant's keepers hold themselves to. One kebab-case page per rule,
`type: convention`, listed here. Not a specific piece of work (that is
`plans/`), not a step-by-step procedure (that is `skills/`), not the record
of choosing (that is a `decision`) — the standing answer, applied broadly.

## Conventions

Read these first — a rule constrains what every other read is for.

* [Compute, never guess](compute-never-guess.md) — every number a deterministic tool could produce comes from that tool, not from the model's head; an LLM's fluent, confident arithmetic is quietly and often wrong, so the tools in `skills/tools/` — today the Bayesian credence appraiser, tomorrow whatever arithmetic a future tool covers — are a correctness control, and a derived number a reader cannot reproduce is a defect.
* [Credence is a model, not a measurement](credence-is-a-model-not-a-measurement.md) — a probability here is the output of a stated, replayable model (decomposition, prior with its reference class, likelihood ratios with citations, every input labelled `cited | derived | elicited | absent`), never a claim to have measured a truth; readers substitute their own inputs and recompute, prior-sensitivity is what separates evidence from faith, and the published example model is a provocation whose numbers exist to be overwritten.
* [Every claim carries its receipt](every-claim-carries-its-receipt.md) — no statement of fact without a resolvable citation attached to that statement; the fact is cheap, the source is the product. Derivations, assumptions and judgements are allowed and labelled; confident unsourced sentences are not.
* [Evidence before authority](evidence-before-authority.md) — claims are appraised by their evidence, never by who made them; criticism lands on the argument; absence of evidence counts only in proportion to how hard the search looked; and "is this really their claim?" (provenance) is a separate question from "is it true?" (soundness).
* [Written to be public](written-to-be-public.md) — the repository is public from its first commit and every page is addressed to a stranger on the open internet: no host names, no internal paths, no personal detail beyond the maintainer's chosen handle, no credentials, no assumption of anyone's infrastructure. Pull requests are welcome.
* [Raw holds excerpts, not copies](raw-holds-excerpts-not-copies.md) — `raw/` stores only the minimum excerpt needed to support a citation, with enough context to check it, always beside a resolvable pointer to the original; never a wholesale copy of a copyrighted work, because the repository is public. Enforced by a `make_sure_that` judge henxel.
