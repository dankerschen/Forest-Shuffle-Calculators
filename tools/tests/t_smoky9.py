import os;HERE=os.path.dirname(os.path.abspath(__file__));WORK=os.path.abspath(HERE+'/../.work')+'/'
from playwright.sync_api import sync_playwright
# The nine Smoky Mountains cards that used to need manual points, checked against the worked examples
# in Lookout's German appendix (15.06.2026). Run shots.py first.
CASES=[  # (forest as {card name: copies}, card to check, expected points for all its copies)
 ({'Yellow Birch':2},'Yellow Birch',2),
 ({'Yellow-Bellied Sapsucker':2},'Yellow-Bellied Sapsucker',4),
 ({'Yellow Perch':2},'Yellow Perch',4),
 ({'Wood Thrush':2},'Wood Thrush',0),
 ({'Yellow Bullhead':2},'Yellow Bullhead',0),
 ({'Wintergreen':2,'Gray Squirrel':1,'Red Squirrel':1,'Flying Squirrel':1},'Wintergreen',18),
 ({'Wood Frog':2,'Fraser Fir':2,'Yellow Birch':1},'Wood Frog',6),
 ({'White-Footed Mouse':2,'Masked Shrew':2,'Rock Vole':1},'White-Footed Mouse',10),
 ({'White-Tailed Deer':2,'Fraser Fir':3},'White-Tailed Deer',12),
 ({'White-Tailed Deer':1},'White-Tailed Deer',0),
]
fails=0
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.goto('file://'+WORK+'smoky.html');pg.wait_for_timeout(800)
    print('manual cards left:',pg.evaluate("CARDS.filter(c=>c.rule==='manual').map(c=>c.name)"))
    for forest,card,want in CASES:
        got=pg.evaluate("""([forest,card])=>{const p=fresh('T');for(const [n,k] of Object.entries(forest)){const c=CARDS.find(c=>c.name===n);if(!c)throw Error('no card '+n);p.cards[c.id]={n:k,x:[]}}
          return score(p).result[CARDS.find(c=>c.name===card).id]}""",[forest,card])
        ok=got==want;fails+=not ok;print('ok  ' if ok else 'FAIL',card,forest,got,'' if ok else '!= %d'%want)
    print('errors',errs);b.close()
print('ALL OK' if not fails and not errs else 'FAILED')
