import os;HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(HERE+'/../..')+'/';WORK=os.path.abspath(HERE+'/../.work')+'/';os.makedirs(WORK,exist_ok=True);URL='file://'+WORK
from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':1024,'height':900},locale='en-US');pg=ctx.new_page()
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]));pg.on('console',lambda m:m.type=='error' and errs.append(m.text[:200]))
    pg.goto('file://'+ROOT+'index.html');pg.wait_for_timeout(1500)
    fr={k:pg.frame_locator('#f-'+k) for k in ['forest','moor','smoky']}
    print('init sel',[pg.evaluate("k=>document.getElementById('f-'+k).contentDocument.getElementById('language-select').value",k) for k in fr])
    fr['forest'].locator('#language-select').select_option('fr');pg.wait_for_timeout(800)
    print('after fr',[pg.evaluate("k=>document.getElementById('f-'+k).contentDocument.getElementById('language-select').value",k) for k in fr], pg.evaluate("document.documentElement.lang"))
    pg.screenshot(path='L_forest_fr.png')
    pg.evaluate("location.hash='#moor'");pg.wait_for_timeout(500);pg.screenshot(path='L_moor_fr.png')
    pg.evaluate("location.hash='#smoky'");pg.wait_for_timeout(500);pg.screenshot(path='L_smoky_fr.png')
    fr['smoky'].locator('#language-select').select_option('de');pg.wait_for_timeout(800)
    print('after de',[pg.evaluate("k=>document.getElementById('f-'+k).contentDocument.getElementById('language-select').value",k) for k in fr])
    pg.screenshot(path='L_smoky_de.png')
    pg.evaluate("location.hash='#moor'");pg.wait_for_timeout(500);pg.screenshot(path='L_moor_de.png')
    pg.evaluate("location.hash='#forest'");pg.wait_for_timeout(500);pg.screenshot(path='L_forest_de.png')
    # back to en from moor
    pg.evaluate("location.hash='#moor'");pg.wait_for_timeout(300)
    fr['moor'].locator('#language-select').select_option('en');pg.wait_for_timeout(800)
    print('after en',[pg.evaluate("k=>document.getElementById('f-'+k).contentDocument.getElementById('language-select').value",k) for k in fr],pg.evaluate("localStorage.getItem('fs-lang')"))
    pg.screenshot(path='L_moor_en.png')
    pg.evaluate("location.hash='#forest'");pg.wait_for_timeout(500);pg.screenshot(path='L_forest_en.png')
    print('errors',errs)
