# Changelog

All notable changes to this tool are documented in this file, independently of the main
`dudus-app` site's own `CHANGELOG.md` — this tool is never deployed, so it versions on its own
schedule rather than moving in lockstep with site releases. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); [Semantic Versioning](https://semver.org),
pre-1.0. Tags are prefixed `intake-v` to avoid colliding with the site's own `v*` tags.

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
