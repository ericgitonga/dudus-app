# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org) (pre-1.0: MINOR = new features/user-facing
behaviour, PATCH = fixes/docs/housekeeping — see `SKILL.md`).

## [0.3.0] - 2026-08-07

### Added

- Card detail view: `/species/[id]` statically renders a species' taxonomy and its full,
  unmodified list of sections exactly as they exist in the card index — no compression, no
  fixed field set. All sections shown at once (no accordion/progressive disclosure): verified
  against the richest 9-section card and it reads comfortably as a single scroll, so the extra
  interaction cost of collapsing sections wasn't justified. Card browser list items now link to
  their detail page. Unknown ids 404 cleanly. Covered by `e2e/test_species_detail.py` (closes #5)

tag: `v0.3.0`

## [0.2.0] - 2026-08-07

### Added

- Card browser: the home page now lists all 31 species from the bundled card index, sorted
  alphabetically, with a live search box that filters by common name and an explicit empty
  state when nothing matches. Works fully offline (the index is imported at build time, no
  fetch). Covered by `e2e/test_card_browser.py` (closes #4)

tag: `v0.2.0`

## [0.1.1] - 2026-08-07

### Added

- Reviewed card index (`src/data/card_index.json`, 31 species) bundled into the app repo: fixed
  Orchard Orbweaver's missing family/order, spot-checked 7 of 31 cards directly against source
  reports (including the most complex dual-source merge case) with zero fabrication found, and
  stamped every card `reviewed_by`/`reviewed_at` (closes #3)

tag: `v0.1.1`

## [0.1.0] - 2026-08-07

### Added

- Initial project scaffold: repo, branch protection, CI (e2e gate on every PR), versioning and
  issue-first workflow (closes #1)

tag: `v0.1.0`
