import os;HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(HERE+'/../..')+'/';WORK=os.path.abspath(HERE+'/../.work')+'/';os.makedirs(WORK,exist_ok=True);URL='file://'+WORK
import re,html,sys
from playwright.sync_api import sync_playwright
src=open(ROOT+'index.html',encoding='utf-8').read()
tag=sys.argv[1] if len(sys.argv)>1 else 'cur'
games={}
for k in ['forest','moor','smoky']:
    m=re.search(r'<iframe id="f-%s"[^>]*srcdoc="(.*?)" hidden>'%k,src,re.S)
    games[k]=html.unescape(m.group(1));open(WORK+f'{k}.html','w',encoding='utf-8').write(games[k])
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,name in [(1024,'ipad'),(390,'phone')]:
        for k in games:
            pg=b.new_page(viewport={'width':w,'height':900 if w>600 else 800})
            errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto(f'{URL}{k}.html');pg.wait_for_timeout(600)
            pg.screenshot(path=WORK+f'{tag}_{k}_{name}.png')
            if errs:print(k,name,'ERR',errs[:3])
            pg.close()
    b.close()
