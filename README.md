# Forest Shuffle scoring: three games in one page

An unofficial, offline-friendly scoring calculator for the card game **Forest Shuffle**
(Lookout Games), in a single `index.html`:

| Game | Scoring |
|------|---------|
| **Forest Shuffle** (base game) | with the Alpine, Woodland Edge and Exploration expansions |
| **Forest Shuffle: Dartmoor** | with the Exmoor expansion |
| **Forest Shuffle: Smoky Mountains** | |

Each game keeps its own calculation (nothing is mixed between games), but they share one
layout, one look and one set of tools. Switch games with the buttons in the banner
(`#forest`, `#moor` and `#smoky` in the URL open a game directly).

## Features

- Tap a card to add it, set per-copy conditions and symbol counts; the small scoring
  notes explain each card's points.
- Several players, a live score banner, sticky player and section navigation.
- Expansion groups you can switch on and off per game.
- **English, French and German**, switchable from any game and shared by all three. It
  follows the browser language on the first visit and is remembered afterwards.
- Light and dark mode, shared by all three games.
- Rules notes on or off; session backup and restore (JSON); send results to
  [BG Stats](https://www.bgstatsapp.com/) or copy the import link.
- Everything is stored in your browser (local storage). No server, no account, no
  tracking, no external scripts, fonts or images.

## Use it

Open `index.html` in a browser, or host the repository with GitHub Pages
(Settings, Pages, deploy from the `main` branch, root folder). The `.nojekyll` file is
only there so Pages serves the file as it is.

## Languages and sources

German card names follow Lookout's official German appendices; Dartmoor's French and German
texts build on Mikko Saari's tool. French names for the base game and Alpine follow the
French rulebook and a French score sheet. The other expansions and Smoky Mountains use
common French species names, because no French appendix exists, so they may differ from the
printed cards. Please open an issue for any wrong name or term.

Official documents (PDF, Lookout): see the footer of each game in the page, or
[Forest Shuffle](https://www.lookout-spiele.de/en/games/forrestshuffle.html),
[Dartmoor](https://www.lookout-spiele.de/en/games/dartmoor.html),
[Smoky Mountains](https://www.lookout-spiele.de/en/games/smoky.html).

## Known limitations

- Nine Smoky Mountains cards still use manual points (Yellow Birch, White-Footed Mouse,
  White-Tailed Deer, Wintergreen, Wood Frog, Wood Thrush, Yellow-Bellied Sapsucker,
  Yellow Bullhead, Yellow Perch).
- The base game's promo cards have not been fully audited.
- Browser and device testing is limited. Always check important scores against the
  official rulebook and appendix.
- AI-assisted work can contain mistakes (see below).

## Credits

- Game: Forest Shuffle, Forest Shuffle: Dartmoor and Smoky Mountains, design Kosch,
  illustrations Toni Llobet and Judit Piella, published by Lookout Games (Lookout GmbH).
  This project is independent and unofficial and contains no official artwork.
- Design idea: Dan Kerschen.
- Code and layout build on [Sören Oldag's Forest Shuffle scoring project](https://github.com/soldag/forest-shuffle-scoring)
  (MIT) and [Mikko Saari's Dartmoor scoring tool](https://codeberg.org/msaari/forestshuffle-dartmoor)
  (MIT, Exmoor expansion by nils-codes).
- Illustrations: AI-generated watercolour-and-ink pictures made for this page with
  Nano Banana 2 (Google), from prompts written with Claude (Anthropic).
- Made with AI: developed with help from Perplexity and Claude (Anthropic) for research, code,
  text, interface design and translation.

## Licence

MIT for the original parts, see [LICENSE](LICENSE). Third-party code, translation
sources and the AI-image terms are listed in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
Game names, rules and artwork remain the property of Lookout GmbH.

## Development

`index.html` is generated. Sources and the build live in `tools/`; see [CLAUDE.md](CLAUDE.md).

```
python3 tools/build.py        # rebuilds index.html
```
