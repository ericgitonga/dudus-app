# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org) (pre-1.0: MINOR = new features/user-facing
behaviour, PATCH = fixes/docs/housekeeping — see `SKILL.md`).

## [0.11.0] - 2026-08-10

### Added

- Unit test suite (Vitest, `.test.ts` colocated with the module it covers) for the card-index
  lookup/filter logic (extracted out of `CardBrowser.tsx` into `src/lib/cardIndex.ts` to make it
  directly testable), alongside — not instead of — the existing `e2e/` Playwright suite. Gated
  in CI via a new required check, `.github/workflows/unit.yml` (closes #57)

tag: `v0.11.0`

## [0.10.0] - 2026-08-10

### Removed

- "Identify a dudu" homepage link — the underlying capture flow (`/identify`, `PhotoCapture`)
  isn't a working identification feature yet (taxon-guessing #8 and index-matching #9 are still
  unbuilt), so it's misleading to link to it as if it were. Search remains the only homepage
  link. The `/identify` route, `PhotoCapture` component, and its EXIF-stripping regression test
  (`e2e/test_photo_capture.py`, #10) are all left in place — this only removes the entry point,
  not the feature's progress. Re-add the link once #8/#9 land and `/identify` is actually usable
  (closes #61)

tag: `v0.10.0`

## [0.9.0] - 2026-08-09

### Added

- New card: White-Ringed Atlas Moth (*Epiphora mythimnia*), the site's first Lepidoptera entry
  — sourced from an existing `/dudusonline` research pass in `Dudus/White-Ringed Atlas Moth/`.
  Added a "moths and butterflies" tagline for Lepidoptera to the order buttons (closes #29)

tag: `v0.9.0`

## [0.8.0] - 2026-08-09

### Changed

- Replaced the single "back" link on `/dudus/[id]` and `/orders/[order]` with a full breadcrumb
  trail (`Dudus / <Order> / <Dudu>` and `Dudus / <Order>`), matching the convention already used
  on `umoja-voices` — earlier segments are links, the current page is plain bold text. Built as
  a reusable `src/components/Breadcrumb.tsx`, now also carried into the `/newproject` scaffold
  template for future Next.js projects. Covered by new cases in `e2e/test_dudu_detail.py` and
  `e2e/test_browse_by_order.py` (closes #27)

tag: `v0.8.0`

## [0.7.1] - 2026-08-09

### Fixed

- The dudu detail page's breadcrumb now takes you back to that dudu's own order page
  (`/orders/[order]`) instead of the homepage, matching the order-buttons browse flow from #23.
  Covered by two new cases in `e2e/test_dudu_detail.py` (closes #25)

tag: `v0.7.1`

## [0.7.0] - 2026-08-09

### Changed

- Home page now shows one button per taxonomic order (plus a fallback button for any dudu whose
  order isn't yet identified) instead of inline per-order grids, each with a small tagline of
  example dudus in that order (e.g. "bees, wasps and ants" for Hymenoptera). Clicking a button
  opens a new dedicated `/orders/[order]` page with that order's dudus, at roughly half the
  thumbnail size of the old inline grid. Covered by `e2e/test_browse_by_order.py` (closes #23)

tag: `v0.7.0`

## [0.6.1] - 2026-08-08

### Security

- Every photo captured via `/identify` is now decoded and re-encoded onto a canvas before it's
  held as state or previewed, stripping all EXIF metadata — including any GPS geotag — since
  canvas output carries no metadata channel. Applies regardless of what tags the original photo
  carried; nothing about the original file is kept around after capture (closes #10)

tag: `v0.6.1`

## [0.6.0] - 2026-08-08

### Added

- Browse-by-order grid view is now the home page (`/`): dudus grouped by taxonomic order, each
  order's dudus in their own responsive photo grid, modelled on `umoja-voices`' songs grid.
  Orders are derived from the bundled card index at render time — only orders with at least one
  dudu appear, and a new order shows up automatically the moment a dudu with that order is
  added, no code change needed. A fallback "Order not yet identified" bucket exists for any card
  missing an `order` value, though none currently need it (closes #19)
- The former home page's search/flat-list view moved to `/search`, with a breadcrumb back to
  home, so browse-by-order and search-by-name are now two distinct, equally-reachable ways to
  find a dudu rather than one replacing the other

### Changed

- The whole site now has one consistent, always-light look (matching the browse-by-order page's
  styling) instead of switching to a dark theme under the OS's `prefers-color-scheme` — the
  entomology-report imagery and taxonomy text read better against a fixed light background than
  adapting per visitor

### Fixed

- Aedes Mosquitoes and Crane Flies were missing an `order` value in the card index; both are
  Diptera. Fixing this in the source library removed the last 2 cards that would have needed
  the "Order not yet identified" fallback bucket above

tag: `v0.6.0`

## [0.5.0] - 2026-08-08

### Added

- In-app photo capture (`/identify`): `<input capture="environment">` so mobile browsers open
  the camera directly rather than the gallery, with a local preview once a photo's taken. No
  upload, no network call — nothing leaves the device yet. Deliberately does nothing with the
  photo beyond proving capture works: taxon-guessing (#8) and index-matching (#9) are separate
  tickets, and geotag/EXIF handling (#10) has to be settled before this photo is ever processed.
  Desktop browsers fall back to a normal file picker (gallery included) since `capture` is
  mobile-only — a known, discussed tradeoff of the simpler option over a full custom
  getUserMedia viewfinder (closes #7)
- Existing reference photos wired up for the dudus that had one (folded in per the user):
  copied into `public/photos/`, rendered on the detail page and as a browser-list thumbnail.
  `photo_ref` now points at the app-servable path rather than the old source-library path. The
  user has since photographed the remaining dudus too, so all 11 now have one (closes #7)

### Removed

- Robber Flies and Whirligig Beetles withdrawn from the site (moved to `Dudus/Not to use/` in
  the source library, alongside the earlier round of 18). 11 dudus remain

tag: `v0.5.0`

### Added

- "Not yet researched" empty state (`NotYetResearched` component): when a search matches no
  dudu, the app now says so with copy distinct from a dead end — "isn't in the library yet... the
  library is still growing" — rather than a generic "no results," plus a working "Browse all
  dudus" fallback that clears the search. Built as a reusable component so the future
  photo-based lookup (#7-#9) can reuse the same messaging rather than duplicating it. Covered by
  two new e2e specs (closes #6)

### Changed

- Site terminology changed from "species" to "dudu"/"dudus" throughout (result count, search
  label, detail-page route `/dudus/[id]`, link text) — the card index can't always identify down
  to species level (several entries are family/genus/order-confirmed only), and "dudu" doesn't
  carry that implied claim the way "species" does. `taxon_rank`'s `"species"` value is unchanged
  — it's the honest technical description of ID confidence, not a user-facing claim (closes #6)

tag: `v0.4.0`

### Removed

- 18 species withdrawn from the site (moved to `Dudus/Not to use/` in the source library):
  Amegilla Bee (card: Blue-Banded Bee), Antlions, Banana Fly, Biting Midges, Fringed-Sucker
  Clinger, Giant Water Bugs, Marsh Beetles, Mealybugs, Pond Skaters, Saucer Bug, Stout
  Backswimmer, Tiger Crane Flies, True Stoneflies, Water Boatman, Water-penny Beetles, Water
  Scavenger Beetles, Water Scorpions, Wheel Bug. 13 species remain (closes #14)

### Changed

- e2e suite no longer hardcodes a total species count or specific species names — every
  assertion is now derived from the actual bundled `card_index.json` at test time, so the suite
  survives future species being added or withdrawn without needing hand-editing

tag: `v0.3.1`

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
