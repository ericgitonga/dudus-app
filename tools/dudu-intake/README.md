# dudu intake tool

Local-only admin tool for adding a new card to `src/data/card_index.json` (with an optional
photo) and for adding/replacing/removing an existing card's photo. Scoped in #15, built in
#31/#32, connected to the live site in #34.

**Not part of the deployed app.** Nothing under `tools/` is imported by the Next.js app or
referenced by its build config — this only runs when you start it yourself, on your own
machine.

## Run it

From the repo root:

```bash
conda run -n ds streamlit run tools/dudu-intake/app.py
```

Dependencies (`streamlit`, `pillow`, `pymupdf`) live in the `ds` conda environment — install with
`conda run -n ds pip install -r tools/dudu-intake/requirements.txt` if they're ever missing.

## What it does

- **Add new card** — exactly three inputs:
  1. **Lay report PDF** (from an already-completed `/dudus` or `/dudusonline` pass — this tool
     doesn't research anything itself, Constraint 1 on #15). Parsed directly with PyMuPDF: the
     report's own title becomes `common_name`/`id`, each bold heading starts a new section, and
     the regular-weight text under it becomes that section's body — mirroring exactly how
     `md_to_pdf_rl.py` styles H1/H2/body when it originally generated the PDF. A leading "The/A/An"
     is stripped from the title (some reports phrase it as a sentence; no existing common name
     starts with an article). `source_report_ref.lay` is set from the filename; the sibling
     technical PDF (same name minus `-la`) is looked up automatically in `Dudus/<CommonName>/`
     on this machine and used for `source_report_ref.technical` if found.
  2. **Photo** (optional) — unchanged: EXIF/GPS-stripped, orientation-corrected, padded to 3:2.
  3. **Order** — dropdown of orders already in use, plus "Unknown (fix later)" → `null` (same
     "Order not yet identified" grouping the site already falls back to for unclassified cards),
     plus a write-in "Other (type manually)" option for an order not yet in the dropdown. When a
     technical report exists locally (`Dudus/<CommonName>/`), its stated order (every technical
     report says "Order X" somewhere in its Taxonomy and Classification section) is auto-detected
     and pre-selected — or pre-fills the write-in field if it's a genuinely new order.

  `scientific_name`, `family`, `taxon_rank` (defaults to `"species"`), and `sourcing` (left
  blank) have no edit UI yet — only photos do — so they land as clear placeholders, not guesses.
- **Existing cards** (#52): lists every card with its current photo (or "no photo yet"), with a
  photo uploader, a lay-report-replace uploader, and an order picker (same auto-detect/write-in
  as above, defaulting to the card's current order) all behind **one "Update" button** — submit
  any combination and only that combination gets applied, in a single "Update card: X" PR.
  Replacing the lay report re-parses it the same way "Add new card" does (`common_name`/
  `sections`/`source_report_ref`), leaving `id`/`photo_ref`/`order`/other metadata untouched
  unless also changed in the same click, and clears `reviewed_by`/`reviewed_at` since the old
  review no longer describes new content. "Remove photo" and "Delete card permanently" stay as
  their own separate, confirm-gated actions.
- **Batch** (#40): add several cards (multi-file lay-report upload, each with its own order/photo,
  same auto-detection as above) or delete several existing cards (checkboxes) in one queued
  session. The whole batch publishes as a **single combined PR** — one CI run instead of one per
  card, at the cost that a failed check blocks every card in that batch together rather than
  isolating the failure (an explicit preference, after trying one-PR-per-card first).

## Publishing to the live site

Every action (add card, delete card, save/remove photo) edits `src/data/card_index.json` /
`public/photos/` in your working tree for instant local feedback, then automatically publishes:
it creates a real branch, commits just the files that action touched, pushes, opens a PR, waits
for the required `e2e` check, and squash-merges if green — no VERSION/CHANGELOG/tag bump and no
separate GitHub issue for this, since it's content rather than a code release (see
`ONBOARDING.md`'s "automated content publishing" exception). If checks fail, the PR is left open
instead of merged, with the failure shown in the tool.

This runs entirely in a throwaway `git worktree`, never by checking out a different branch in
this working directory — so it can't disrupt whatever this checkout is currently doing (e.g. a
concurrent dev session working on the tool's own code), and it's safe to use even while another
change is mid-publish. Each publish takes roughly as long as CI does (a minute or two), not
instant — the eventual instant-update version (card data out of git entirely) is tracked
separately in #33.
