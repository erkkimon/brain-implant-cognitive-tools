---
type: convention
about: concept
title: Written to be public
description: This implant is public from its first commit and written for the open internet — every page is addressed to a stranger with no access to the machine it was written on, so no host names, internal paths, personal details or credentials ever enter it; pull requests are welcome, and the only handle that appears is the maintainer's chosen public one.
tags: [convention, publishing, privacy, scope]
timestamp: 2026-09-25T18:30:00Z
half_life: 0
---

# Written to be public

Decided by erkkimon on 2026-09-25, founding the cognitive-tools implant
([journal](../journals/2026-09-25.md)): this repository is public from its
first commit, and every agent that writes into it must know that — now and
in the future.

So it is recorded here — in the brain implant, where an agent reads before
it writes — rather than only in a README. It is also what `brainpick.toml`
declares in `[brain] audience`, the field brainpick reports in
`brain_overview`.

## The rule

**Write every page as if a stranger is reading it today.** Not a colleague,
not a future teammate, not an agent running on the maintainer's hardware:
someone who found this repository on the internet, knows nothing about how
it was made, and cannot reach anything it mentions.

That is not a hypothetical reader. The repository has been public since its
first commit, so there was never a private phase, no grace period, and no
"we will clean it up before publishing" pass — by design. A page that would
need cleaning before a stranger saw it is a page that should not have been
written that way.

**Pull requests are welcome.** A public implant is meant to be improved by
people who are not its maintainer, which is one more reason every page must
stand on its own: a contributor cannot ask the conversation the page came
from what it meant.

### Never in this repository

1. **No machine or network identity** — no internal host names, LAN
   addresses, private URLs, user accounts, or SSH remotes in any page.
   (`brainpick.toml` may name the git origin because that is what the field
   is for; prose does not repeat it.)
2. **No filesystem paths outside the repository** — paths are
   repository-relative. A reader clones this and the paths work. `/home/…`,
   `~/Brain`, or a path on a specific machine do not appear.
3. **No personal data** — no names of people who did not choose to appear in
   a public document, no e-mail addresses, no schedules or locations.
   `erkkimon` is the maintainer's chosen public handle and the only handle
   that appears; decisions are attributed to it, and nobody else is named
   without making the same choice.
4. **No credentials, tokens or keys** — the contract enforces this
   mechanically (`no_secrets` in `henxels.yaml`), but the rule is wider than
   what a scanner catches: not even an example key, not even a revoked one.
5. **No assumption of the maintainer's infrastructure** — a skill says how
   to do the thing with ordinary, publicly available tools. Where a step
   needs a local model, an API token or a specific service, it says so as a
   *requirement the reader must supply*, with a documented free alternative
   where one exists, and degrades gracefully when it is absent. A tool that
   only runs on one machine is a tool this implant does not have.
6. **No private reasoning about third parties** — assessments are about
   published claims and their evidence, never about the people who made
   them. Criticism lands on the argument, with a citation, as
   [Evidence before authority](evidence-before-authority.md) requires.

### Always in this repository

- **Every external dependency is named and free to obtain**, or the page
  says plainly what it costs and what happens without it.
- **Every citation resolves for a stranger** — a public DOI, URL or
  identifier, never a file only the maintainer holds. This is the same
  requirement [Every claim carries its receipt](every-claim-carries-its-receipt.md)
  makes for a different reason; here it is also what makes the implant
  usable by someone who is not its author.
- **Terms are defined before they are used**, because the reader did not sit
  in the conversation where they were coined.

## Why this is a convention and not a task

A one-time cleanup is a task; this is a property every future page must have,
including pages written by agents that never read this conversation. It is
`type: convention` with `half_life: 0` so it never fades out of
`brain_overview`, and it is the first thing a writer is told to respect
before adding or changing any page of this implant. The reasoning behind
`audience` and the other fields it sits beside is in brainpick's own
documentation of the brain format:
https://github.com/benquemax/brainpick/blob/main/docs/brain.md

## The only checks that are ever needed

Because the rule has held from the first commit, there is no publication
event to prepare for. The checks are mechanical and routine: `henxels check
--all` for the secret scan, and a grep for host names and absolute paths
before any change is proposed. If those come back clean, the page is what
it was always meant to be — readable by anyone.
