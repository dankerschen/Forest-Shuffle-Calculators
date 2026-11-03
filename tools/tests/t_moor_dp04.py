import os;HERE=os.path.dirname(os.path.abspath(__file__));WORK=os.path.abspath(HERE+'/../.work')+'/'
from playwright.sync_api import sync_playwright
# Dartmoor promo DP04: Lambs 1 point (counts as hoof), Willow Ptarmigan 3 points. Run shots.py first.
fails=[]
def check(l,got,want):
    ok=got==want;print('ok  ' if ok else 'FAIL',l,got);ok or fails.append(l)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]));pg.goto('file://'+WORK+'moor.html');pg.wait_for_timeout(1000)
    inc=lambda i:pg.click("button[onclick=\"increment('%s')\"]"%i)
    inc('hoof-lambs');inc('hoof-lambs');inc('bird-side-willowptarmigan');inc('hoof-dartmoorsheep');pg.wait_for_timeout(300)
    g=lambda i:pg.inner_text('#'+i)
    check('lambs 2 copies',g('score-hoof-lambs'),'2');check('ptarmigan',g('score-bird-side-willowptarmigan'),'3')
    check('sheep counts lambs as hooves',g('score-hoof-dartmoorsheep'),'6')
    pg.reload();pg.wait_for_timeout(1000);check('kept after reload',g('hoof-lambs'),'2')
    for l,names in [('de',['Lämmer (DP04)','Moorschneehuhn (DP04)']),('fr',['Agneaux (DP04)','Lagopède des saules (DP04)'])]:
        pg.select_option('#language-select',l);pg.wait_for_timeout(800);check(l+' names',[pg.locator('text='+s).count() for s in names],[1,1])
    pg.select_option('#language-select','en');pg.wait_for_timeout(300);b.close()
print('errors',errs);print('ALL OK' if not fails and not errs else 'FAILED')
