---
type: convention
about: concept
title: Raw holds excerpts, not copies
description: What may be stored under raw/ — only the minimum excerpt needed to support a citation with enough context to check it, always beside a link to the original source where the full material can be fetched; never a wholesale copy of a copyrighted work, because this repository is public and redistributing source material is a legal exposure the project does not need.
tags: [convention, raw, copyright, legal, sources, public]
timestamp: 2026-09-27T12:19:44Z
half_life: 0
---

# Raw holds excerpts, not copies

`raw/` is where source material grounds the distilled layers. The temptation
is to drop whole papers, whole datasets, whole book chapters into it so that
a future reader has everything to hand. For this repository that is a
mistake, for a plain legal reason:
[this repository is public](written-to-be-public.md), and redistributing a
copyrighted paper, article, chapter or dataset is not something a public
repository should do. The project does not own that right, and it does not
need it.

What the implant actually needs from a source is narrower than the source
itself. It needs **enough of the source to support the specific claim, with
enough surrounding context to check that the claim is fair**, and it needs a
**pointer back to the original** so anyone who wants the rest can fetch it
from the party who is entitled to distribute it. That is what `raw/` stores.
Nothing more.

## The rule

A file under `raw/` is admissible when **both** hold:

1. **It is an excerpt, not the whole work.** Only the passage(s), row(s),
   figure caption or quotation that a claim in this brain implant actually
   relies on, plus the immediate context needed to read them honestly — not
   the full article, not the full chapter, not the full dataset. If a file
   reproduces substantially all of a source, it is a copy and does not
   belong here.

2. **It carries a resolvable pointer to the original.** A DOI, a stable URL,
   a dataset accession, an ISBN with page numbers, a canonical locator such
   as a Stephanus or Bekker number — an identifier that lets a reader
   retrieve the complete source from its rightful home. An excerpt without a
   way back to the original is an orphan: it cannot be checked and cannot be
   updated.

This is a copyright-and-context rule, not a fair-use legal opinion. When in
doubt, store **less** and point **harder**: a one-line quotation with a DOI
beats three paragraphs without one, every time.

## What this looks like in practice

A raw file that grounds a claim reads roughly like this:

```markdown
# Heuristics and biases — the framing sentence

Source: Tversky & Kahneman (1974), Science 185(4157), 1124–1131.
Original: https://doi.org/10.1126/science.185.4157.1124  (paywalled; excerpt only)
Retrieved: 2026-09-25

> "...people rely on a limited number of heuristic principles which reduce
>  the complex tasks of assessing probabilities and predicting values to
>  simpler judgmental operations."  (p. 1124, opening paragraph)

Relied on for: the claim that probability judgements are made by heuristic
substitution rather than by calculation.
Context: the authors then describe three heuristics (representativeness,
availability, anchoring) and the biases each produces; the excerpt is the
thesis sentence, not a result.
```

The quotation is short, its purpose is stated, and the DOI takes a reader to
the whole paper. That is the shape every raw file should have — the same
shape for a passage from a book (ISBN, edition, page), a row from a survey
(the study's accession and the one table used), or a historical document (the
archive's reference number and the lines quoted).

## What must never go in raw/

- A full PDF, HTML dump, or scanned chapter of a copyrighted work.
- A complete dataset that its publisher distributes under its own terms —
  store the accession and the few values used, and let the reader fetch the
  set from its repository.
- Anything whose only pointer is "I found it somewhere" — no resolvable
  original means it cannot be checked and does not belong.

Public-domain and open-licensed material (a text whose author died centuries
ago, a CC-BY dataset) *may* legally be copied in full, but the
excerpt-plus-pointer habit is still the right default: it keeps `raw/` small,
greppable and [orderly](../conventions/index.md) rather than a mirror of the
open web.

## How this is enforced

Two layers, both described in the
[founding of this rule](../journals/archive/2026/09/2026-09-25.md):

- The standing [raw/ is orderly source material](../conventions/index.md)
  henxel keeps `raw/` named and indexed.
- A `make_sure_that` henxel shows each new or changed `raw/` file to the
  contract's judge and asks whether it is an excerpt-with-a-pointer rather
  than a wholesale copy. A judge is fallible, so it only warns unless it is
  confident — but it catches the obvious case of a whole article pasted in,
  which is exactly the case that creates the legal exposure. How such
  natural-language henxels work is documented by
  [henxels](https://github.com/benquemax/henxels) itself.
