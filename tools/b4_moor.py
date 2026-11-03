import os;HERE=os.path.dirname(os.path.abspath(__file__))+'/'
exec(open(HERE+'b4_common.py',encoding='utf-8').read())
def build_moor(m):
    # nav: last link -> All scores / BG Stats with its own icon
    m=sub1(m,r'<a href="#section-bgstats"><svg[^>]*><use href="#icon-bgstats"></use></svg>All scores</a>',
           '<a href="#section-bgstats">'+IC('allscores')+'All scores / BG Stats</a>','m nav')
    # results heading icon
    i=m.index('id="section-bgstats"');j=m.index('<h2>',i);k=m.index('</svg>',j)+6
    m=m[:j+4]+IC('allscores')+m[k:]
    # translations for the new label
    n=0
    for en,fr in [('"All scores": "Tous les scores"','"All scores / BG Stats": "Tous les scores / BG Stats"'),('"All scores": "Alle Ergebnisse"','"All scores / BG Stats": "Alle Ergebnisse / BG Stats"')]:
        c=m.count(en);n+=c
        if c:m=m.replace(en,en+', '+fr)
    assert n>=2,n
    # hero: language + rules + dark mode in one row; Exmoor in an "Expansion(s)" group
    def regroup(mm):
        vc,btns=mm.group(1),mm.group(2)
        th=re.search(r'<button[^>]*id="theme-toggle".*?</button>\s*',btns,re.S);assert th
        btns=btns.replace(th.group(0),'')
        return '<div class="view-controls">'+vc+th.group(0).strip()+'</div><div class="exp-group" id="buttons" role="group" aria-labelledby="exp-label"><span class="exp-label" id="exp-label">Expansion(s)</span>'+btns+'</div>'
    m=sub1(m,r'<div class="view-controls">(.*?)</div>\s*<div id="buttons">(.*?)</div>(?=\s*<details)',regroup,'m hero')
    # official French section headings (rulebook: En haut / En bas / Côtés)
    for a,b in [('"Tops": "Haut"','"Tops": "En haut"'),('"Bottoms": "Bas"','"Bottoms": "En bas"'),('"Sides": "Gauche / droite"','"Sides": "Côtés"'),
                ('"Tops points": "Haut — points"','"Tops points": "En haut — points"'),('"Bottoms points": "Bas — points"','"Bottoms points": "En bas — points"'),('"Sides points": "Gauche / droite — points"','"Sides points": "Côtés — points"')]:
        m=once(m,a,b,'m fr '+a)
    return m
