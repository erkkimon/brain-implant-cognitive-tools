---
type: skill
title: Using the brain implant
description: "Use when reading from or writing to this brain implant — before answering from memory, before grepping, and before adding or changing any doc in _brain/. Explains what an implant is (one half of a brain, the other half being the agent's own cortex), where opinions go (the cortex, never here), and the read and write discipline the contract enforces."
timestamp: 2026-09-25T18:30:00Z
depends_on: []
export: agent-skill
---

# Using the brain implant

`_brain/` is a **brain implant**: a public, shared knowledge bundle that an
agent mounts beside its own memory. In brainpick's terms a *brain* is a
**cortex** — the agent's own, private memory — plus any number of
**implants** mounted alongside it
([Federation](https://github.com/benquemax/brainpick/blob/main/docs/federation.md)).
The two halves have different jobs and the split is the whole design:

| | cortex | this implant |
| --- | --- | --- |
| whose | the agent's (and its user's) | everyone's — public, shared |
| holds | opinions, decisions, preferences, what *you* concluded | what was said, by whom, where — and tools for thinking |
| writes | freely | under the contract, for a stranger |

An implant can be used without a cortex, and a cortex without an implant;
either works, slightly lobotomized. **Your opinions and interpretations never
go into the implant.** They go into the cortex. The implant gives you the
material and the tools to form them; forming them is your turf, and the
user's ([Written to be public](../conventions/written-to-be-public.md)).

What is here is the **best knowledge available at the moment, not the
truth**: everything is provisional, and when you notice a flaw your job is to
fix the implant, not route around it.

## First: pull

**Before reading anything, pull the implant's latest version** (`git pull`
in the repository that holds it — every brain, if several are mounted). An
implant is shared memory: other agents and people commit to it between your
sessions, and an answer built on a stale checkout is built on knowledge the
implant has already corrected. Pull first, then read; if the pull brings
changes, re-read before acting on what you remembered.

## Reading: most distilled first

1. **The closest brain first.** If several are mounted (your cortex, this
   implant, other implants), the one closest to the task wins when they
   disagree — but only the cortex may hold a *conclusion*; an implant holds
   what was said and the tools to weigh it.
2. **`conventions/`** — standing rules for how things get done, across
   many tasks. brainpick lists them first in `brain_overview` and the
   AGENTS.md report for a reason: a convention can rule out an approach
   outright, so read them before planning anything.
3. **`skills/`** — actionable, tested procedures. The purest layer.
4. **`knowledge/`** — evergreen concepts, for the idea behind a skill or a
   fact no skill covers yet.
5. **`journals/`** — dated episodes, only when nothing distilled exists.
   Today is `journals/YYYY-MM-DD.md`; earlier days are in
   `journals/archive/YYYY/MM/`.
6. **`todo/open.md`** — the implant's open work. Check it before planning:
   it may already flag what you are about to rediscover.
7. **`raw/`** — undistilled source material. Not in search results; grep it
   to ground a claim or to distil something new.

With brainpick: `brain_overview` first, then `brain_search`, then
`brain_read`, then `brain_neighbors`. Grep only after the implant comes up
short.

## Writing: distil upward, point, ground

- **Only two kinds of sentence enter the implant.** Logic or mathematics a
  reader can verify alone, or *someone said X, at location Y* — with the
  receipt attached ([Every claim carries its receipt](../conventions/every-claim-carries-its-receipt.md)).
  Anything else is an opinion, and opinions live in the cortex.
- **Information flows `journals/` → `knowledge/` → `skills/`.** An episode
  becomes a concept when it settles; a concept becomes a skill when it has
  been carried out and works. A decision that settles into a standing rule
  — applied broadly, not just this one time — becomes a `conventions/` page
  instead, `type: convention`, alongside that flow rather than inside it.
- **Journal in today's file.** Write into `journals/YYYY-MM-DD.md` (create
  it on the first entry of the day; headings inside are free — `## HH:MM`
  or a title, newest first). **Before the first entry of a new day, move
  yesterday's file to `journals/archive/YYYY/MM/`**
  (`mkdir -p _brain/journals/archive/YYYY/MM && git mv …`) — the contract
  blocks a commit with two unarchived days.
- **To-dos live in `todo/open.md`.** A task that surfaces mid-work goes
  there as `- [ ] …`. When it is done, tick it `- [x] … (done: YYYY-MM-DD)`
  and move the line to `todo/archive/YYYY-MM-DD.md` (a `type: todo` doc
  for that day; create it on first use) — the same day or the next, the
  contract insists. Never edit the archive afterwards.
- **A procedure that works becomes a skill**: `brainpick skill new <name>`
  scaffolds `skills/<name>.md` as `type: skill` with `depends_on` and
  `tools` (paths to the deterministic scripts it drives — put them in
  `skills/tools/`). A `playbook` is a how-to for humans and is not a skill.
- **DRY by pointer.** When you distil, the less distilled doc gains a
  pointer to the more distilled one ("now covered by [skill]") — never a
  copy. The journal points to what it changed and never restates it.
- **Raw stays clean.** Drop source material into `raw/` with a kebab-case
  name that says what it is, list it in `raw/index.md`, and clean up after
  yourself: prune what you have distilled or found worthless. Only excerpts
  with a pointer to the original, never whole works
  ([Raw holds excerpts, not copies](../conventions/raw-holds-excerpts-not-copies.md)).
- **Ground every claim inline**, Wikipedia-style, with a plain link: a
  journal entry (a decision this implant made), an external page, another
  brain (`brain://slug-id/path`), or say in words that it is an assumption.
- **Reading a less distilled layer is a distillation opportunity.** If the
  answer was in the journal, ask whether it should now be knowledge.
- **Bump `timestamp`** on every change; keep `type`, `title`, `description`.
  The timestamp is also what the half-life reads: memories fade in search
  ranking as they age, slowly by default (`[half_life]` in
  `brainpick.toml`). When you notice the lists silting up with stale
  material, steepen the curve there — shorter days for `journals` or
  `todo`, or a per-page `half_life:` in frontmatter — rather than deleting;
  nothing is ever hidden, it only ranks lower.
- **Leave it committed.** The contract runs on commit and asks the
  maintainer to review and stage; a change that sits on one machine is not
  shared memory. Contributions from outside arrive as pull requests.

## Several brains: subsidiarity

When brains conflict: the closest wins. Update both. Then decide — keep the
information duplicated (readers of the farther brain may not have the
closer one) or replace it with a `brain://` pointer. Record the episode in
the journal of the brain that changed. Never resolve a conflict by writing
your *verdict* into an implant — that is a cortex entry.

## Where this comes from

Evergreen concepts live in [Knowledge](../knowledge/index.md); what happened
and when, in the [Journals](../journals/index.md). The brain format and its
reasoning live in brainpick's wiki:
https://github.com/benquemax/brainpick/blob/main/docs/brain.md — data flow,
grounding, subsidiarity, and what is fixed for life versus cheap to change.
Serve this implant with `brainpick init`, then the `brain_*` MCP tools.
