# dudu intake tool

Local-only admin tool for adding a new card to `src/data/card_index.json` (with an optional
photo) and for adding/replacing/removing an existing card's photo. Scoped in #15, built in #31.

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
     "Order not yet identified" grouping the site already falls back to for unclassified cards).

  `scientific_name`, `family`, `taxon_rank` (defaults to `"species"`), and `sourcing` (left
  blank) have no edit UI yet — only photos do — so they land as clear placeholders, not guesses.
- **Existing cards**: lists every card with its current photo (or "no photo yet"), with inline
  photo add/replace/remove, plus a confirm-gated "Delete card permanently" that removes the card
  entry and its photo file together.

## After using it

The tool edits `src/data/card_index.json` and `public/photos/` directly in your working tree.
Review the diff (`git status` / `git diff`), then commit and open a PR through the normal
branch → PR → e2e → merge workflow (`ONBOARDING.md`) like any other change — the tool itself
never commits, pushes, or deploys anything.
