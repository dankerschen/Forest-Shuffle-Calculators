import re
LOOKOUT='<a href="https://www.lookout-spiele.de/en/games/{p}.html" rel="noopener">Lookout Games</a>'
def credits(game, keep_details=''):
    names={'forest':('Forest Shuffle','forrestshuffle'),'moor':('Forest Shuffle: Dartmoor','dartmoor'),'smoky':('Forest Shuffle: Smoky Mountains','smoky')}
    title,page=names[game]
    lookout=f'<a href="https://www.lookout-spiele.de/en/games/{page}.html" rel="noopener">Lookout Games</a>'
    specific={
     'forest':('<p><strong>This calculator.</strong> Design idea: Dan Kerschen. Scoring logic informed by the Lookout rules and by '
               '<a href="https://github.com/soldag/forest-shuffle-scoring" rel="noopener">Sören Oldag’s Forest Shuffle scoring project</a>, an independent quantity-based implementation. '
               'Promo cards (box “Promos”) come from card photos and a fan-compiled list; check them against your printed cards.</p>',
               '<p><strong>Licence.</strong> Code and scoring logic derived from Sören Oldag’s project are used under the MIT licence, © 2023 Sören Oldag. Interface parts shared with the Dartmoor tool (results layout, icon set) derive from Mikko Saari’s MIT-licensed code, © 2025 msaari. Both notices are reproduced below. Game name, rules and artwork remain © Lookout GmbH.</p>'),
     'moor':('<p><strong>This calculator.</strong> Design idea: Dan Kerschen. Calculator developed by Mikko Saari, expanded for Exmoor by nils-codes (version 1.28, 13.10.2026; <a href="https://codeberg.org/msaari/forestshuffle-dartmoor" rel="noopener">source on Codeberg</a>); inspiration drawn from '
             '<a href="https://forestshuffle.app/" rel="noopener">ForestShuffle.app</a>.</p>',
             '<p><strong>Licence.</strong> Code derived from Mikko Saari’s Dartmoor scoring tool is used under the MIT licence, © 2025 msaari. Shared page styling derives from Sören Oldag’s MIT-licensed project, © 2023 Sören Oldag. Both notices are reproduced below. Game name, rules and artwork remain © Lookout GmbH.</p>'),
     'smoky':('<p><strong>This calculator.</strong> Design idea: Dan Kerschen. Scoring formulas follow the Lookout English rulebook and appendix and were written for this page; see the scoring audit below for sources and limits. Page layout and styling build on <a href="https://github.com/soldag/forest-shuffle-scoring" rel="noopener">Sören Oldag’s Forest Shuffle scoring project</a> and on Mikko Saari’s Dartmoor tool.</p>',
              '<p><strong>Licence.</strong> The layout, stylesheet and icon set derive from MIT-licensed code by Sören Oldag (© 2023) and Mikko Saari (© 2025 msaari); both notices are reproduced below. The Smoky Mountains scoring logic is original to this page and uses no external libraries, fonts or remote scripts. Game name, rules and artwork remain © Lookout GmbH.</p>'),
    }[game]
    return ('<footer class="site-credits"><h2>Credits &amp; licence</h2>'
      f'<p><strong>The game.</strong> {title} — game design: Kosch; illustrations: Toni Llobet and Judit Piella; published by {lookout} (Lookout GmbH). '
      'This calculator is an independent, unofficial scoring aid. It is not affiliated with or endorsed by the publisher and contains no official game artwork.</p>'
      '<p><strong>Illustrations.</strong> The habitat banners, the top-bar strip and the section decorations are AI-generated watercolour-and-ink illustrations made for this calculator with <a href="https://deepmind.google/models/gemini-image/" rel="noopener">Nano Banana 2</a> (Google), from image prompts written with Claude (Anthropic), then cropped and compressed for the web. They are new compositions, not copies of any card, board or official illustration. The small category icons were originally drawn with Perplexity (AI) for the first versions of these calculators; the Dartmoor tool’s icon set is also covered by Mikko Saari’s MIT notice below, and a few more icons were added with Claude.</p>'
      +specific[0]+
      '<p><strong>Made with AI.</strong> This calculator was developed with the help of AI tools, notably <a href="https://www.perplexity.ai/" rel="noopener">Perplexity</a> and <a href="https://claude.ai/" rel="noopener">Claude</a> (Anthropic), '
      'for research, code, text, interface design, image prompts and the original icons. The combined three-game page was assembled and styled with Claude. AI-assisted work can contain mistakes: please check scores against the official rulebook and appendix.</p>'
      '<p><strong>Translations.</strong> The French and German texts were written for this page with Claude. German card names follow Lookout’s official German appendices. French names for the base game and Alpine follow the French rulebook and a French score sheet; the names for the other expansions and for Smoky Mountains are common French species names and may differ from the printed cards. Please report mistakes.</p>'
      +DOCS[game]+
      '<p><strong>Privacy.</strong> Scores are stored only in this browser (local storage) and are sent nowhere unless you choose Back up, Copy or Send to BG Stats.</p>'
      +specific[1]+keep_details+'</footer>')

U='https://www.lookout-spiele.de/upload/'
DOCS={
 'forest':'<p><strong>Official documents (Lookout, PDF).</strong> Rulebook: <a href="'+U+'en_forrestshuffle.html_Forest_Shuffle_175_Rules_EN_WEB_260209.pdf" rel="noopener">English</a> · <a href="'+U+'de_mischwald.html_Forest_Shuffle_175_Rules_DE_WEB_260209.pdf" rel="noopener">Deutsch</a> — Appendix: <a href="'+U+'en_forrestshuffle.html_Forest_Shuffle_175_Appendix_EN_WEB_260518.pdf" rel="noopener">English</a> · <a href="'+U+'de_mischwald.html_Forest_Shuffle_175_Appendix_DE_WEB_260518.pdf" rel="noopener">Deutsch</a> (the German appendix also covers the expansions).</p>',
 'moor':'<p><strong>Official documents (Lookout, PDF).</strong> Rulebook: <a href="'+U+'en_dartmoor.html_ForestShuffeDartmoor_0156_Rules_EN_WEB_250922.pdf" rel="noopener">English</a> · <a href="'+U+'de_dartmmor.html_ForestShuffeDartmoor_0156_Rules_DE_WEB_250922.pdf" rel="noopener">Deutsch</a> — Appendix: <a href="'+U+'en_dartmoor.html_ForestShuffeDartmoor_0156_Appendix_EN_DSV9.pdf" rel="noopener">English</a> · <a href="'+U+'de_dartmmor.html_ForestShuffeDartmoor_0156_Appendix_DE_DSV7.pdf" rel="noopener">Deutsch</a> — Play aid: <a href="'+U+'en_dartmoor.html_FR%20-%20Dartmoor%20-%20Exmoor_Aide%20de%20jeu%20%5BDLC%5D.pdf" rel="noopener">Français</a>.</p>',
 'smoky':'<p><strong>Official documents (Lookout, PDF).</strong> Rulebook: <a href="'+U+'en_smoky.html_SmokyMountains_0195_Rules_EN_WEB_260518.pdf" rel="noopener">English</a> · <a href="'+U+'de_smoky.html_SmokyMountains_0195_Rules_DE_WEB_260518.pdf" rel="noopener">Deutsch</a> — Appendix: <a href="'+U+'en_smoky.html_SmokyMountains_0195_Appendix_EN_WEB_260521.pdf" rel="noopener">English</a> · <a href="'+U+'de_smoky.html_SmokyMountains_0195_Appendix_DE_WEB_260615.pdf" rel="noopener">Deutsch</a>.</p>',
}
CREDIT_CSS='''
html footer.site-credits{margin:34px 0 0;padding:22px 2px 8px;border-top:1px solid var(--line);color:var(--muted);font-size:14px;line-height:1.6}
html footer.site-credits h2{margin:0 0 10px;font:600 11px/1.2 system-ui,-apple-system,Segoe UI,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
html footer.site-credits p{margin:0 0 10px;font-size:14px}
html footer.site-credits strong{color:var(--ink);font-weight:600}
html footer.site-credits a{color:var(--accent);text-decoration:underline}
html footer.site-credits details{margin-top:10px}
html footer.site-credits summary{min-height:44px;display:flex;align-items:center;gap:8px;cursor:pointer;color:var(--ink);list-style:none}
html footer.site-credits summary::-webkit-details-marker{display:none}
html footer.site-credits summary::before{content:"\\25B8";color:var(--accent);font-size:13px;transition:transform .15s}
html footer.site-credits details[open]>summary::before{transform:rotate(90deg)}
'''
MOOR_MIT='<details><summary>MIT notice: Dartmoor scoring tool (Mikko Saari)</summary><p>MIT License</p><p>Copyright (c) 2025 msaari</p><p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p><p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p><p>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p></details>'
OLDAG=None
def apply_credits(t, game):
    global OLDAG
    m=re.search(r'<footer[^>]*>.*?</footer>',t,re.S);assert m,game
    old=m.group(0)
    if game=='forest':
        d=re.search(r'<details><summary>Upstream MIT notice</summary>.*?</details>',old,re.S);assert d
        OLDAG=d.group(0).replace('Upstream MIT notice','MIT notice: Forest Shuffle scoring project (Sören Oldag)')
    assert OLDAG
    keep=OLDAG+MOOR_MIT
    if game=='smoky':
        d=re.search(r'<details><summary>Scoring audit and limitations</summary>.*?</details>',old,re.S);assert d
        dd=re.sub(r'<p>French/German official card terminology.*?</details>','<p>German card names follow Lookout’s official German appendix; French names are common French species names, because Lookout publishes no French appendix for this game. Browser/device testing remains necessary.</p></details>',d.group(0),flags=re.S);assert dd!=d.group(0)
        keep=dd+keep
    return t[:m.start()]+credits(game,keep)+t[m.end():]
