# Forest Shuffle scorer: handover for Claude Code

Owner: Dan Kerschen (dan@kerschen.lu), German teacher in Luxembourg. He plays Forest Shuffle and
publishes this on **GitHub Pages**. The deliverable is ONE file, `index.html` (about 3.7 MB,
fully self-contained, no external scripts, fonts or images). He writes in English; the page itself
is English, French and German.

## What it is

An unofficial scoring calculator for three games, in one page: **Forest Shuffle** (base game, plus
Alpine, Woodland Edge, Exploration), **Dartmoor** (plus Exmoor) and **Smoky Mountains**.
Hard rules from Dan:
- Each game keeps its own calculation. **Never mix calculations between games.**
- All three share one layout, one look and one set of tools (language, rules notes, dark mode,
  session backup, BG Stats export).
- Keep it one self-contained file. No CDN, no tracking, no server.

## Repo layout

```
index.html                 BUILT OUTPUT. Never edit by hand; rebuild instead.
README.md LICENSE THIRD-PARTY-NOTICES.md .nojekyll   (.nojekyll = serve files as they are, no Jekyll)
tools/
  build.py                 entry point: `python3 tools/build.py` rewrites ../index.html
  shell_template.html      outer page: game switcher state, theme/lang sync, 3 empty iframes
  base_forest.html  base_moor.html  base_smoky.html   the three upstream-derived calculators (inputs)
  b4_common.py             shared CSS (CSS, LAYOUT_CSS, TOOLS_CSS) and shared JS (scroll-spy, click handler, home link)
  b4_forest.py b4_moor.py b4_smoky.py   per-game patches: hero, groups, nav, save notes, etc.
  b4_credits.py            footer credits and the Lookout PDF links (DOCS dict)
  i18n_build.py            merges the dictionaries and embeds i18n_engine.js per game
  i18n_engine.js           runtime translator (DOM text, attributes, regex rules, dialogs)
  i18n_ui.py  i18n_names.py  i18n_rules.py  moor_i18n.json   EN -> (FR, DE) data
  art/                     hero_*.jpg, strip_*.jpg, motif_*_*.webp (AI-generated, embedded as base64)
  tests/                   Playwright scripts (see below); output goes to tools/.work/ (git-ignored)
```

## Build and test

```
python3 tools/build.py            # prints "built <bytes>"
pip install playwright && playwright install chromium     # once, for the tests
python3 tools/tests/shots.py      # extracts the three games to tools/.work/*.html and takes screenshots
python3 tools/tests/test4.py      # nav links scroll to their section and the highlight follows
python3 tools/tests/test5.py      # functional checks per game, plus FR/DE nav
python3 tools/tests/test6.py      # sticky home icon: scrolls to the top, exists in all games, phone and desktop
python3 tools/tests/t_lang.py     # language sync across the three games in the combined page
python3 tools/tests/t_names.py    # default player names follow the language (tab, name input, stored session)
python3 tools/tests/t_smoky9.py   # the nine late Smoky cards against the German appendix examples
python3 tools/tests/i18n_check.py forest|moor|smoky   # lists strings left untranslated in FR/DE
```
Run `shots.py` first: the other tests open the extracted `tools/.work/<game>.html` files.
The rebuild from a clean checkout was verified byte-identical to the last delivered `index.html`.
`test4.py` prints one harmless "mismatch" per game for the home icon (empty label, current = Trees).

## Architecture in short

- `index.html` is a shell with three `<iframe id="f-forest|f-moor|f-smoky" srcdoc="..." hidden>`.
  The shell shows one at a time and uses the hash `#forest`, `#moor` or `#smoky`.
- Shell and frames talk by `postMessage`: `fsGame` (switch game), `fsTheme` (light/dark), `fsLang`
  (en/fr/de). Shell keeps `fs-last-game`, `fs-theme`, `fs-lang` in localStorage. srcdoc frames share
  the parent origin, so frames read the same localStorage.
- Each game has `<header class="hero">` with `.hero-top` = `nav.game-switch` + `.hero-tools`
  (language select, rules button, dark-mode button as icons with tiny captions). The `.sticky-controls`
  block holds `.player-bar` (player tabs, plus `.sticky-tools` that proxy the hero's rules and dark
  buttons) and `.category-nav` (section links, with a house icon `.nav-top` first that scrolls to the top).
- Shared JS in `b4_common.py` does scroll-spy, sets `--sticky-height`, and intercepts in-page `#` links with
  `scrollIntoView` (browser anchor jumps inside srcdoc frames were unreliable, probably Safari/iPad).
  Sections have `scroll-margin-top: calc(var(--sticky-height) + 14px)`.
- Build style: every patch is a string substitution through `once(t, old, new, label)` or
  `sub1(t, pattern, repl, label)`, which **assert exactly one match**. If an upstream base file changes,
  the build fails loudly instead of silently producing something wrong.

## i18n (EN, FR, DE)

- The engine keys text nodes by their English text and stores originals, so switching back to English is exact.
  It also translates aria-label, placeholder, title and alt, plus regex patterns (for example "N points per copy",
  "Name (DP01)") and wraps alert/confirm/prompt.
- Merge order in `i18n_build.py`: UI, BOX, BODIES, CONDITIONS, WARNINGS, FOOTER, game names, EXTRA. EXTRA wins.
  Identity entries (value equals key) are dropped, otherwise they block the regex rules.
- Dartmoor has its own language machinery; the engine drives it through `#language-select` and `dartmoor-language`,
  and must skip Moor's `#session-status` and `#bg-status` (`own()`), or the two fight and the page hangs.
- Names: German follows Lookout's official appendices. French follows the French Forêt Mixte rulebook, Dan's
  French score sheet, and the Dartmoor French play aid. French for the other Forest expansions and for Smoky
  Mountains uses common species names (flagged to Dan, not official). The Dartmoor promo names DP01 to DP03 are
  my own wording. The Lookout French play aid forbids reproducing its rules, so only names and terms were taken.

## Gotchas learned the hard way

- Moor's ID rules (`#rules-visibility-toggle`) beat class selectors, so `TOOLS_CSS` needs `!important`.
- Game JS rewrites button text itself; `norm()` strips ": On/Off" and ": Hide/Show cards" suffixes.
- Engine attribute translation must not re-set an unchanged attribute (it caused an infinite loop once).
- Shell theme/lang patch in `build.py` (`NEWTHEME`) is keyed on `const dark=matchMedia(`. Keep that anchor.
- The footers link the official Lookout PDFs (`DOCS` in `b4_credits.py`). Don't paste rulebook text.

## Open items (none blocking)

1. ~~Real-device testing~~ Done: Dan tested on his phone, all good (Nov 2026). Dan keeps the home icon.
2. ~~Nine Smoky cards with manual points~~ Done from Lookout's German appendix (15.06.2026): Yellow Birch 1 each,
   Sapsucker and Yellow Perch 2 each, Wood Thrush and Yellow Bullhead 0, Wood Frog 1 per tree, White-Tailed Deer
   2 per tree, White-Footed Mouse 1 per mouse (itself included), Wintergreen 3 per squirrel. No card is manual now.
3. ~~Default player names stay English in the input.~~ Done: `fsDefName(n)` creates "Player/Joueur/Person n"; on a
   language switch the engine renames players whose name is still a default in any language, via the per-game
   `window.__fsPlayers` hook in `build.py` (`PLAYER_HOOK`). Custom names are never touched.
4. Remaining `confirm()`/`alert()` dialogs: Dan is fine with them as they are. No change planned.
5. French names for Smoky Mountains and for the Woodland Edge/Exploration expansions are not official.
6. Base-game promo cards have not been fully audited.

## Working agreement

- Make changes in `tools/*.py`, `tools/i18n_*`, `tools/base_*.html` or `shell_template.html`, rebuild, run the tests, commit
  `index.html` together with the source change.
- Keep the layout identical across the three games. A change in one game's hero, nav, sticky row or tools goes in all three.
- Credits and licences: MIT for our parts; upstream MIT code from Sören Oldag and Mikko Saari (see THIRD-PARTY-NOTICES.md).
  Artwork is AI-generated; game names and rules belong to Lookout GmbH.
