# Changelog

All notable changes to this tool are documented in this file, independently of the main
`dudus-app` site's own `CHANGELOG.md` — this tool is never deployed, so it versions on its own
schedule rather than moving in lockstep with site releases. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); [Semantic Versioning](https://semver.org),
pre-1.0. Tags are prefixed `intake-v` to avoid colliding with the site's own `v*` tags.

## [0.1.0] - 2026-08-09

### Added

- Initial local-only admin intake tool (Streamlit): add a new card to `card_index.json` with
  structured metadata fields and repeatable sections, matching `Card`/`CardSection` in
  `src/types/card.ts`; list existing cards with inline photo add/replace/remove; pad-to-3:2
  photo handling and EXIF/GPS metadata stripping mirroring the site's own conventions
  (SKILL.md's photo convention, `stripPhotoMetadata.ts` from #10). Scoped in #15, built in #31.

tag: `intake-v0.1.0`
