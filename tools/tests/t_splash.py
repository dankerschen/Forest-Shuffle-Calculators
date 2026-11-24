import os;HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(HERE+'/../..')+'/';WORK=os.path.abspath(HERE+'/../.work')+'/'
from playwright.sync_api import sync_playwright
# Splash game chooser in the combined page: shown without a game in the address, skipped with #forest/#moor/#smoky,
# language buttons set the page language, last played game is marked, choosing a game opens it.
fails=[]
def check(l,got,want):
    ok=got==want;print('ok  ' if ok else 'FAIL',l,got);ok or fails.append(l)
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in [(1280,900),(390,844)]:
        ctx=b.new_context(viewport={'width':w,'height':h},locale='en-US');pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
        U='file://'+ROOT+'index.html'
        pg.goto(U);pg.wait_for_timeout(1200)
        vis=lambda:pg.evaluate("!document.getElementById('splash').hidden")
        check(f'{w} splash shown on plain load',vis(),True)
        check(f'{w} no horizontal scroll',pg.evaluate("document.getElementById('splash').scrollWidth<=innerWidth"),True)
        pg.screenshot(path=WORK+f'splash_{w}_en.png')
        pg.click('.sp-lang button[data-l="de"]');pg.wait_for_timeout(900)
        check(f'{w} DE title',pg.inner_text('#sp-title'),'Mischwald-Punkterechner')
        check(f'{w} DE reaches games',pg.evaluate("['forest','moor','smoky'].map(k=>document.getElementById('f-'+k).contentDocument.getElementById('language-select').value)"),['de','de','de'])
        pg.screenshot(path=WORK+f'splash_{w}_de.png')
        pg.click('.sp-game[data-g="moor"]');pg.wait_for_timeout(600)
        check(f'{w} splash closed',vis(),False)
        check(f'{w} moor shown',pg.evaluate("['forest','moor','smoky'].filter(k=>!document.getElementById('f-'+k).hidden)"),['moor'])
        check(f'{w} hash',pg.evaluate("location.hash"),'#moor')
        pg.goto(U.split('#')[0]+'?again');pg.wait_for_timeout(1200)
        check(f'{w} last played marked',pg.evaluate("[...document.querySelectorAll('.sp-game.last')].map(b=>b.dataset.g)"),['moor'])
        check(f'{w} language remembered',pg.inner_text('#sp-title'),'Mischwald-Punkterechner')
        pg.keyboard.press('Escape');pg.wait_for_timeout(600)
        check(f'{w} Escape opens last game',(vis(),pg.evaluate("location.hash")),(False,'#moor'))
        pg.goto(U+'#smoky');pg.wait_for_timeout(1200)
        check(f'{w} deep link skips splash',(vis(),pg.evaluate("location.hash")),(False,'#smoky'))
        pg.evaluate("localStorage.setItem('fs-lang','en')");ctx.close()
        check(f'{w} errors',errs,[])
    b.close()
print('ALL OK' if not fails else 'FAILED')
