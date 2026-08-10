# Changelog

All notable changes to this tool are documented in this file, independently of the main
`dudus-app` site's own `CHANGELOG.md` — this tool is never deployed, so it versions on its own
schedule rather than moving in lockstep with site releases. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); [Semantic Versioning](https://semver.org),
pre-1.0. Tags are prefixed `intake-v` to avoid colliding with the site's own `v*` tags.

## [0.2.0] - 2026-08-10

### Added

- Every action (add card, delete card, save/remove photo) now automatically publishes to the
  live site (#34): commits the touched files in an isolated `git worktree`, pushes, opens a PR,
  waits for the required `e2e` check, and squash-merges if green. No VERSION/CHANGELOG/tag bump
  and no separate GitHub issue for these — content-only changes are now explicitly exempt from
  that ceremony (documented in `ONBOARDING.md`/`SKILL.md`). Failed checks leave the PR open
  rather than merging. Runs in a throwaway worktree specifically so it never disrupts whatever
  branch this working directory is actually on. Validated with two real end-to-end publishes
  (a throwaway marker file, created then removed) before wiring it into real content changes.
  Long-term direction (card data out of git entirely, for instant updates) tracked in #33.

tag: `intake-v0.2.0`

## [0.1.0] - 2026-08-09

### Added

- Initial local-only admin intake tool (Streamlit). Scoped in #15, built in #31. "Add new card"
  is exactly three inputs: a lay-report PDF (parsed with PyMuPDF into `common_name`/`id`/
  `sections`/`source_report_ref`, mirroring `md_to_pdf_rl.py`'s own H1/H2/body font styling), an
  optional photo (pad-to-3:2 + EXIF/GPS strip, mirroring `stripPhotoMetadata.ts` from #10 and
  SKILL.md's photo convention), and an order dropdown ("Unknown (fix later)" → `null`, matching
  the site's existing unclassified-order fallback). "Existing cards" lists every card with
  inline photo add/replace/remove, plus a confirm-gated permanent card delete (removes the card
  entry and its photo file together) — added after manual testing found no way back from an
  add-card mistake short of hand-editing `card_index.json`.

tag: `intake-v0.1.0`
