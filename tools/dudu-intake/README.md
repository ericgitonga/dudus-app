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

Dependencies (`streamlit`, `pillow`) live in the `ds` conda environment — install with
`conda run -n ds pip install -r tools/dudu-intake/requirements.txt` if they're ever missing.

## What it does

- **Add new card**: structured fields matching `Card`/`CardSection` in `src/types/card.ts`,
  plus a repeatable list of section heading/body pairs. Section text is meant to be pasted in
  from an already-completed `/dudus` or `/dudusonline` research pass — this tool doesn't
  research anything itself (Constraint 1 on #15).
- **Existing cards**: lists every card with its current photo (or "no photo yet"), with inline
  add/replace/remove.
- Uploaded photos are stripped of EXIF/GPS metadata and orientation-corrected (mirroring
  `stripPhotoMetadata.ts`, #10), then padded to exact 3:2 if narrower — the same convention
  documented in `SKILL.md`. The tool never crops; if a photo is already wider than 3:2 it warns
  instead of guessing where the subject is.

## After using it

The tool edits `src/data/card_index.json` and `public/photos/` directly in your working tree.
Review the diff (`git status` / `git diff`), then commit and open a PR through the normal
branch → PR → e2e → merge workflow (`ONBOARDING.md`) like any other change — the tool itself
never commits, pushes, or deploys anything.
