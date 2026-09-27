---
type: convention
about: concept
title: An implant is not a brain
description: "Vocabulary rule for this repository and every brain-implant-* repository: a brain is the agent's cortex (the one brainpick repo registered with --cortex) plus the implants mounted beside it; this repository is an implant, its data root is _implant/, and no page, config comment or tool calls it 'the brain'."
tags: [convention, vocabulary, brainpick, naming]
timestamp: 2026-09-27T12:19:44Z
half_life: 0
---

# An implant is not a brain

**The rule.** In brainpick's registry exactly one repository is the
**cortex** (`brainpick register --cortex`: "mark it as the agent's own brain —
at most one"); every other registered repository, or a subfolder of one, is
an **implant** (`--implant`: "mark it as an attached repository bundle — any
number"), per `brainpick register --help` (brainpick 0.8.6). A **brain** is
the cortex plus whatever implants are mounted beside it. So:

- this repository is an *implant*, never "a brain" or "the brain";
- its data root is `_implant/` (`[bundle] root = "_implant"` in
  `brainpick.toml`), never `_brain/`; every repository whose name begins
  with `brain-implant-` uses the same root;
- "cortex" names the agent's own memory, where opinions and conclusions go
  ([Using the brain implant](../skills/using-the-brain-implant.md));
- names fixed by brainpick itself — the `brain_*` MCP tools, the `[brain]`
  table in `brainpick.toml`, the "brain format", `brain://` addresses — are
  kept as they are; they are brainpick's API, not a description of this
  repository.

**Why.** Calling the implant a brain blurs the one boundary the design
depends on: the implant holds what was said, the cortex holds what the agent
concluded. Decided by erkkimon (journal entries of
[2026-09-25](../journals/archive/2026/09/2026-09-25.md) and
[2026-09-27](../journals/2026-09-27.md)).
