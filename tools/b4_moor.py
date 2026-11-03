import os;HERE=os.path.dirname(os.path.abspath(__file__))+'/'
exec(open(HERE+'b4_common.py',encoding='utf-8').read())
def add_dp04(m):
    """DP04 promo (Dan's handover): Lambs 1 point (hoof), Willow Ptarmigan 3 points (side bird). Effects are not scored."""
    NEW=[('hoof-lambs','Lambs (DP04)',1,'hoof-dartmoorsheep','hoof-exmoorponyfoal'),
         ('bird-side-willowptarmigan','Willow Ptarmigan (DP04)',3,'bird-side-treecreeper','bird-side-treecreeper')]
    ids=''.join('"%s", "score-%s", '%(i,i) for i,*_ in NEW)
    m=once(m,'"mouse-side-shrew", "score-mouse-side-shrew", ',ids+'"mouse-side-shrew", "score-mouse-side-shrew", ','dp04 ids')
    rules=''.join('"%s":{type:"points",args:[\'%s\', %d]},'%(i,i,p) for i,_,p,*_ in NEW)
    m=once(m,'"mouse-side-shrew":{type:"points",args:[\'mouse-side-shrew\', 1]},',rules+'"mouse-side-shrew":{type:"points",args:[\'mouse-side-shrew\', 1]},','dp04 rules')
    meta=''.join('"%s": {"name": "%s", "origin": "Dartmoor"}, '%(i,n) for i,n,*_ in NEW)
    m=once(m,'"mouse-side-shrew": {"name": "Shrew", "origin": "Dartmoor"}, ',meta+'"mouse-side-shrew": {"name": "Shrew", "origin": "Dartmoor"}, ','dp04 meta')
    cases=''.join("case '%s': score = points('%s', %d); break; "%(i,i,p) for i,_,p,*_ in NEW)
    m=once(m,"case 'mouse-side-shrew':",cases+"case 'mouse-side-shrew':",'dp04 switch')
    names=''.join('"%s": "%s", '%(i,n) for i,n,*_ in NEW)
    m=once(m,'"mouse-side-shrew": "Shrew", ',names+'"mouse-side-shrew": "Shrew", ','dp04 en names')
    for i,n,p,tpl,after in NEW:
        bt=re.search(r'<div class="entity-card" data-card-id="'+tpl+r'">.*?</div></div>',m,re.S).group(0)
        tname=re.search(r'<span class="card-name">([^<]*)</span>',bt).group(1)
        blk=bt.replace(tpl,i).replace(tname,n)
        ba=re.search(r'<div class="entity-card" data-card-id="'+after+r'">.*?</div></div>',m,re.S)
        m=m[:ba.end()]+blk+m[ba.end():]
        assert m.count('data-card-id="%s"'%i)==1,i
    return m
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
    m=once(m,"name:'Player '+(forestSession.players.length+1)","name:fsDefName(forestSession.players.length+1)",'m addplayer name')
    m=once(m,"players:[{id,name:'Player 1',state:emptyForest()}]","players:[{id,name:fsDefName(1),state:emptyForest()}]",'m fresh name')
    m=add_dp04(m)
    return m
