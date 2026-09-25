# Cognitive Tools Brain Implant for brainpick

**A Bayesian calculator and other reasoning tools for AI agents** — Claude
Code, Codex, OpenCode, Cursor, Gemini CLI, Copilot, or any agent that can
read a folder of markdown and run Python. The tools here are small,
deterministic and replayable, and they cover the architectural blind spots
of a language model: gut-feeling arithmetic, unsourced confidence, a
probability stated as if it had been measured. The skills tell the agent
*when* to stop generating and start computing.

It is a **brain implant**: a shared, version-controlled half of a brain that
an agent plugs in beside its own memory (its *cortex*) and beside domain
implants. It is meant to be mounted together with the
[philosophy brain implant](https://github.com/erkkimon/brain-implant-philosophy),
which supplies what a Bayesian model needs to be *educated* — reference
classes, cited findings, and the catalogue of biases that corrupt a prior —
while this implant supplies the machinery that turns those into a number
with a range and a receipt.

> Pull requests are welcome, including from agents. The rules this
> repository follows are machine-checked on every commit.

## The flagship: a Bayesian calculator for gut feelings

Ask a language model "how likely is it?" and it produces a number that
sounds measured and is not. The **credence appraiser** replaces that number
with a model:

- a **prior** with a named reference class — *what fraction of things like
  this turn out true?* — as an interval, not a point;
- **evidence items**, each with a likelihood ratio, its source, and a kind:
  *cited*, *derived*, *elicited* from the user, or *absent* — the evidence
  that would have been found if the claim were true and was not;
- a **posterior** reported as a median and a 90 % interval by Monte Carlo
  over the input intervals, never a bare point;
- a **prior-sensitivity sweep** that says, in bits, whether the evidence or
  the prior is carrying the result — so a "70 %" that is really a
  restated prior is exposed as one;
- the whole thing **saved as JSON** so anyone can change one input and
  replay it.

The skill [Estimate a credence](_implant/skills/estimate-a-credence.md)
walks the agent through elicitation: it asks the user for the factors, asks
what evidence was looked for, writes the model, runs it, and reports the
range with its composition (*33 % cited, 0 without a source*). The output is
an educated gut feeling — educated because every input is on the table, a
gut feeling because that is all a credence is.

```bash
cd _implant/skills/tools
python3 selftest.py
python3 cogtools.py appraise models/example-provocation.appraisal.json
```

The example model is a **provocation**: every number in it is a placeholder
whose only purpose is to be replaced by yours. Copy it, change the claim,
the prior and the evidence, replay it, and argue about the inputs. That is
the whole method, and it is the reason the number is never the product —
the model is.

## Skills included

| Skill | What it does |
| --- | --- |
| [Estimate a credence](_implant/skills/estimate-a-credence.md) | Turns "probably" into a stated model: elicits the reference class, the evidence and its sources, runs the appraiser, reports a range with what is carrying it. |
| [Using the brain implant](_implant/skills/using-the-brain-implant.md) | How to read and write an implant: consult before answering from memory, ground every claim, keep opinions in the cortex. |

More tools follow the same pattern — a deterministic script, a self-test,
the skill that drives it, and a knowledge page that carries the case
against the method as well as for it. The open list is in
`_implant/todo/open.md`.

## Quick start

### Option A — clone it and point your agent at it

```bash
git clone https://github.com/erkkimon/brain-implant-cognitive-tools
```

Tell your agent to read `_implant/skills/index.md`, then the skill. The
tools are standard-library Python 3.10+ and never reach the network. This
works — and the agent will use the calculator only when it remembers that
it exists.

### Option B — mount it as a brain implant with brainpick

[brainpick](https://github.com/benquemax/brainpick) compiles a folder like
this one into a link graph, a keyword index and a vector index, and exposes
them to your agent as MCP tools — `brain_overview`, `brain_search`,
`brain_read`, `brain_neighbors`. Skills are listed first and boosted in
search, so the moment the agent is about to say "unlikely", a search for
that surfaces the procedure that computes it instead. Several implants and
the agent's own brain federate into one address space, which is how this
implant and the philosophy implant work as one: the philosophy side holds
the factors, this side holds the arithmetic.

```bash
uv tool install "brainpick[vectors]"      # or: pipx install "brainpick[vectors]"
git clone https://github.com/erkkimon/brain-implant-cognitive-tools && cd brain-implant-cognitive-tools
brainpick compile --root .
brainpick register "$PWD" --implant --alias cognitive-tools
brainpick integrate claude-code           # or: opencode | dsh | agents-md
```

`brainpick integrate` writes the Agent Skill into your harness and prints
the MCP snippet to paste. If a brainpick MCP server is already running,
restart it after `brainpick register` — it reads the registry at start-up,
so a freshly registered implant is "unknown" to it until then. Mount the
philosophy implant the same way:

```bash
git clone https://github.com/erkkimon/brain-implant-philosophy
brainpick register "$PWD/brain-implant-philosophy" --implant --alias philosophy
```

Without an agent, the same graph is on the command line:

```bash
brainpick overview --root .
brainpick search --root . "credence"
brainpick read --root . conventions/credence-is-a-model-not-a-measurement.md
```

If `brainpick` is not found after installing, it is in `~/.local/bin`.
brainpick **≥ 0.7.0** is required (brain format 3 — `type: convention`
pages are invisible to older engines, and the conventions are the point);
**≥ 0.8.1** to serve it with `brainpick serve`. No install at all:
`uvx brainpick overview --root .`

## How the repository is organised

`_implant/` is the bundle. Its folders are memory types, one job each:

| Folder | Holds |
| --- | --- |
| `skills/` | The procedures above and the tools they drive (`skills/tools/`) |
| `conventions/` | Standing rules: compute-never-guess, credence-is-a-model-not-a-measurement, every-claim-carries-its-receipt, evidence before authority, publication, excerpts |
| `knowledge/` | The concepts behind the tools — and the case against each method |
| `vision/` | Why this implant exists, as a book |
| `journals/` | What happened, one file per day |
| `plans/` | Decided work |
| `todo/` | The live work queue |
| `raw/` | Citation excerpts, never copies, excluded from search results |

Read `conventions/` first — a rule constrains what every other read is for —
then `skills/`, then `knowledge/`.

## Contract

This repository is governed by a [henxels](https://pypi.org/project/henxels/)
contract — machine-checked rules in `henxels.yaml`, digested for agents into
`AGENTS.md`. It runs on commit: the implant must compile fresh, every link
must land, every page must carry its grounding, the tools must pass their
self-test. Install it before contributing:

```bash
uv tool install henxels && henxels init
henxels check --all
```

## Contributing

Contributions arrive as pull requests. A contribution that adds a claim adds
its citation in the same change; a contribution that adds a tool adds its
self-test and the skill that drives it. The contract checks what it can check
mechanically, and a human reviews the rest.

## How the content is produced — and a disclaimer

All documentation in this repository is **distilled by AI agents** from the
cited sources, under the contract above, and reviewed by humans only to the
extent the maintainers and contributors have had time for. The contract
checks what can be checked mechanically; it cannot check that a source was
read correctly. Errors of transcription, attribution and interpretation are
possible on any page, and every receipt is there so that you can verify the
claim yourself before relying on it.

The tools compute exactly what their inputs say and nothing more: a
credence produced here is the output of a stated model, not a measurement
of anything, and it is only as good as the inputs you gave it. Everything
is provided **as is**, without warranty of any kind, express or implied;
nothing here is professional advice of any kind. If you find an error, open
an issue or a pull request.

## Licensing

Tooling and configuration are **MIT**; documentation is **CC BY-SA 4.0**.
See `LICENSE`.
