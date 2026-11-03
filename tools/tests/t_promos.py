import os;HERE=os.path.dirname(os.path.abspath(__file__));WORK=os.path.abspath(HERE+'/../.work')+'/'
from playwright.sync_api import sync_playwright
# Forest promo cards (box "Promos"): scoring per card, box toggle, FR/DE names. Run shots.py first.
CASES=[  # (forest {card id: copies or (copies, qual list)}, symbols, card id, expected)
 ({'pamatna_lipa':1},{'Linden':3},'pamatna_lipa',3),
 ({'lookout_tower':1,'little_red_riding_hood':1,'dracula':1},{},'lookout_tower',2),
 ({'maple_promo':1,'guarana':1,'paeonia_peregrina':1,'blackthorn':1},{},'maple_promo',3),
 ({'dracula':1,'little_red_riding_hood':1,'big_bad_wolf':1,'short_beaked_echidna':1},{},'dracula',8),
 ({'paeonia_peregrina':1,'great_spotted_woodpecker':1},{},'paeonia_peregrina',10),
 ({'paeonia_peregrina':1},{},'paeonia_peregrina',0),
 ({'little_red_riding_hood':1,'chanterelle':2},{},'little_red_riding_hood',20),
 ({'big_bad_wolf':1,'little_red_riding_hood':1,'dracula':1},{},'big_bad_wolf',10),
 ({'roseate_spoonbill':1,'australian_magpie':1},{},'roseate_spoonbill',2),
 ({'american_alligator':1,'short_beaked_echidna':1,'australian_magpie':1,'sheep_promo':1,'little_red_riding_hood':1},{},'american_alligator',5),
 ({'australian_magpie':1,'birch':6},{},'australian_magpie',7),
 ({'australian_magpie':1,'birch':7},{},'australian_magpie',0),
 ({'gibbon':1,'guarana':1,'paeonia_peregrina':1,'maple_promo':0},{},'gibbon',5),
 ({'gibbon':1,'guarana':1,'paeonia_peregrina':1,'mistletoe':1},{},'gibbon',15),
 ({'pitta':1,'cicada':1,'american_alligator':1},{},'pitta',2),
 ({'black_stork':(2,[True,False])},{},'black_stork',7),
 ({'cicada':(1,[True])},{},'cicada',10),
 ({'short_beaked_echidna':2},{},'short_beaked_echidna',10),
 ({'hyacinth_macaw':1,'guarana':1,'blue_jay':1,'robber':1},{},'hyacinth_macaw',7),
 ({'sheep_promo':1,'roe_linden':2},{},'sheep_promo',9),
 ({'durer_bat':1,'barbastelle_bat':1,'bechstein_s_bat':1},{},'durer_bat',5),
 ({'chinese_hare':2,'european_hare':1},{},'chinese_hare',6),
]
fails=0
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1024,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.goto('file://'+WORK+'forest.html');pg.wait_for_timeout(800)
    for forest,sym,card,want in CASES:
        got=pg.evaluate("""([forest,sym,card])=>{const q=player('T');for(const [id,v] of Object.entries(forest)){if(!CARDS.find(c=>c.id===id))throw Error('no card '+id);
          const [n,qual]=Array.isArray(v)?v:[v,[]];q.cards[id]={n,qual};}q.symbols=sym;return calculate(q,[q]).rows[card]}""",[forest,sym,card])
        ok=got==want;fails+=not ok;print('ok  ' if ok else 'FAIL',card,got,'' if ok else '!= %d'%want)
    # box toggle: hidden by default, shown after clicking the Promos button
    vis=lambda:pg.locator('text=Big Bad Wolf').count()
    before=vis();pg.click('[data-visibility="Promos"]');pg.wait_for_timeout(300);after=vis()
    ok=before==0 and after>0;fails+=not ok;print('ok  ' if ok else 'FAIL','promo box toggle',before,after)
    pg.select_option('#language-select','de');pg.wait_for_timeout(600)
    de=[pg.locator('text='+s).count()>0 for s in ['Großer, böser Wolf','Rotkäppchen','Gedenklinde (Památná lípa)']]
    ok=all(de);fails+=not ok;print('ok  ' if ok else 'FAIL','German promo names',de)
    pg.select_option('#language-select','en');pg.wait_for_timeout(300)
    print('errors',errs);b.close()
print('ALL OK' if not fails and not errs else 'FAILED')
