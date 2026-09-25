# brain-implant-cognitive-tools

A **brainpick brain implant** holding cognitive tools for AI agents: small,
deterministic, replayable tools that cover the architectural blind spots of a
language model — gut-feeling arithmetic, unsourced confidence, a probability
stated as if it had been measured. An agent mounts this implant beside its
own memory (its *cortex*) and beside domain implants (the first is
[brain-implant-philosophy](https://github.com/erkkimon/brain-implant-philosophy)),
and the skills here tell it when to stop generating and start computing.

The first tool is the **Bayesian credence appraiser**: a model of a belief —
a prior with a named reference class, evidence items with likelihood ratios
and their sources, every input as an interval — that reports a *range*, says
whether the evidence or the prior is carrying the result, and is saved as
JSON so anyone can change an input and replay it. The number is never the
product; the model is.

Pull requests are welcome, including from agents.

---

## Using this with an agent

### If brainpick is already installed

```bash
git clone <this-repo> && cd brain-implant-cognitive-tools
brainpick compile --root .          # --root is where brainpick.toml lives
brainpick overview --root .         # start here
```

Then `brainpick search`, `brainpick read`, `brainpick neighbors`. To mount it
as an implant in an agent harness:

```bash
brainpick register "$PWD" --implant --alias cognitive-tools
brainpick integrate                 # writes harness config (Claude Code, opencode, …)
```

### If brainpick is not installed

brainpick is a Python CLI on PyPI. Install the `[vectors]` extra, otherwise
the vector tier is silently off and search degrades to keyword only:

```bash
uv tool install "brainpick[vectors]"      # recommended
# or: pipx install "brainpick[vectors]"
```

If `brainpick` is not found afterwards it is almost certainly in
`~/.local/bin`. Without installing anything: `uvx brainpick overview --root .`

Source and documentation: <https://github.com/benquemax/brainpick>

**brainpick >= 0.7.0 is required** (brain format 3 — `type: convention`
pages are invisible to older engines, and the conventions are the point of
this repository); **>= 0.8.1 to serve it** with `brainpick serve`.

## Running the tools without an agent

Pure standard-library Python 3.10+; nothing reaches the network.

```bash
cd _brain/skills/tools
python3 selftest.py                                     # verify the appraiser
python3 cogtools.py appraise models/example-provocation.appraisal.json
```

The example model is a **provocation**: every number in it is a placeholder
whose only purpose is to be replaced by your own. Copy it, change the claim,
the prior and the evidence, replay it, and argue about the inputs — that is
the whole method.

## How this repository is organised

`_brain/` is the bundle. Its folders are memory types, one job each:

| Folder | Holds |
| --- | --- |
| `conventions/` | Standing rules: receipts, credence-as-model, compute-never-guess, publication |
| `skills/` | Procedures an agent follows, and the tools they drive (`skills/tools/`) |
| `knowledge/` | The concepts behind the tools — and the case against each method |
| `vision/` | Why this implant exists, as a book |
| `journals/` | What happened, one file per day |
| `plans/` | Decided work |
| `todo/` | The live work queue |
| `raw/` | Excerpts that ground claims, excluded from search results |

Read `conventions/` first — a rule constrains what every other read is for —
then `skills/`, then `knowledge/`.

## Contract

This repository is governed by a [henxels](https://pypi.org/project/henxels/)
contract — machine-checked rules in `henxels.yaml`, digested for agents into
`AGENTS.md`. It runs on commit. Install it before contributing:

```bash
uv tool install henxels && henxels init
henxels check --all
```

## Contributing

Contributions arrive as pull requests. A contribution that adds a claim adds
its citation in the same change; a contribution that adds a tool adds its
self-test and the skill that drives it. The contract checks what it can check
mechanically, and a human reviews the rest.

## Licensing

Tooling and configuration are **MIT**; documentation is **CC BY-SA 4.0**.
See `LICENSE`.
