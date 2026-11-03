import os;HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(HERE+'/../..')+'/';WORK=os.path.abspath(HERE+'/../.work')+'/';os.makedirs(WORK,exist_ok=True);URL='file://'+WORK
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for k in ['forest','moor','smoky']:
        pg=b.new_page(viewport={'width':1024,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.on('dialog',lambda d:d.accept())
        pg.goto(f'{URL}{k}.html');pg.wait_for_timeout(500)
        pg.add_style_tag(content='html{scroll-behavior:auto!important}')
        n=pg.locator('.category-nav a').count();bad=[]
        for i in range(n):
            a=pg.locator('.category-nav a').nth(i);label=a.inner_text().strip()
            pg.evaluate('window.scrollTo(0,0)');pg.wait_for_timeout(120)
            a.click();pg.wait_for_timeout(1500)
            cur=pg.eval_on_selector_all('.category-nav a','els=>els.filter(e=>e.getAttribute("aria-current")==="true").map(e=>e.textContent.trim())')
            if cur!=[label]:bad.append((label,cur))
        print(k,'nav links',n,'highlight mismatches:',bad)
        m=pg.evaluate("""()=>{const r=s=>{const e=document.querySelector(s);return e?Math.round(e.getBoundingClientRect().height):null};
          window.scrollTo(0,0);return {hero:r('.hero'),settings:r('.hero-settings'),summary:r('.hero-session-tools summary, .session-tools summary'),sticky:r('.sticky-controls'),playerbar:r('.player-bar'),nav:r('.category-nav'),
          settingsTop:Math.round(document.querySelector('.hero-settings').getBoundingClientRect().top-document.querySelector('.hero').getBoundingClientRect().top)}}""")
        print('   heights',m)
        if errs:print(k,'ERR',errs[:3])
        pg.close()
    b.close()
