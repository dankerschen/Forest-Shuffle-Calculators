import os;HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(HERE+'/../..')+'/';WORK=os.path.abspath(HERE+'/../.work')+'/';os.makedirs(WORK,exist_ok=True);URL='file://'+WORK
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for k in ['forest','moor','smoky']:
      for vw in (1024,390):
        pg=b.new_page(viewport={'width':vw,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.on('dialog',lambda d:d.accept())
        pg.goto(f'{URL}{k}.html');pg.wait_for_timeout(600)
        pg.evaluate('window.scrollTo(0,2500)');pg.wait_for_timeout(500)
        n=pg.locator('.category-nav a.nav-top').count()
        pg.locator('.sticky-controls').screenshot(path=WORK+f'st_{k}_{vw}.png')
        pg.locator('.category-nav a.nav-top').click();pg.wait_for_timeout(1500)
        y=pg.evaluate('scrollY');cur=pg.eval_on_selector_all('.category-nav a[aria-current=true]','e=>e.length')
        print(k,vw,'home links',n,'scrollY after',y,'current count',cur,errs[:2])
        pg.close()
    b.close()
