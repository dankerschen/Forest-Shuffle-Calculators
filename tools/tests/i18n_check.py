import os;HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(HERE+'/../..')+'/';WORK=os.path.abspath(HERE+'/../.work')+'/';os.makedirs(WORK,exist_ok=True);URL='file://'+WORK
import sys,json,re
from playwright.sync_api import sync_playwright
JS='''()=>{const out=new Set();const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
while(n=w.nextNode()){const p=n.parentElement;if(!p||['SCRIPT','STYLE'].includes(p.tagName))continue;const t=n.nodeValue.replace(/\\s+/g,' ').trim();if(t)out.add(t)}
document.querySelectorAll('[aria-label],[placeholder],[title]').forEach(e=>{['aria-label','placeholder','title'].forEach(a=>{const v=e.getAttribute(a);if(v)out.add('@'+a+': '+v)})});out.add('@title-tag: '+document.title);return [...out]}'''
def run(pg,game,lang):
    pg.goto(URL+'%s.html'%game)
    pg.evaluate("l=>{try{localStorage.setItem('fs-lang',l);localStorage.setItem('dartmoor-language',l)}catch(e){}}",lang)
    pg.goto(URL+'%s.html'%game);pg.wait_for_timeout(700)
    pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
    # add 2 cards per section
    n=pg.evaluate("document.querySelectorAll('.add-card').length")
    for rnd in range(2):
        pg.evaluate("()=>{const n=document.querySelectorAll('.add-card').length;for(let i=0;i<n;i++){const b=document.querySelectorAll('.add-card')[i];if(b)b.click()}}")
    pg.evaluate("()=>{document.querySelectorAll('.conditions input[type=checkbox]').forEach(c=>{if(!c.checked)c.click()})}")
    pg.evaluate("()=>{document.querySelectorAll('.conditions input[type=number]').forEach(c=>{c.value=1;c.dispatchEvent(new Event('input',{bubbles:true}));c.dispatchEvent(new Event('change',{bubbles:true}))})}")
    for s in ['#solo','#bg-solo-winner']:
        try:pg.check(s,timeout=300)
        except Exception:pass
    pg.wait_for_timeout(400)
    return pg.evaluate(JS)
if __name__=='__main__':
    game=sys.argv[1];out={}
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':1100,'height':900})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        for lang in ['en','fr','de']:out[lang]=run(pg,game,lang)
        print('errors',errs[:3])
        b.close()
    json.dump(out,open(WORK+'chk_%s.json'%game,'w'),ensure_ascii=False)
    en=set(out['en'])
    for lang in ['fr','de']:
        left=[s for s in out[lang] if s in en and re.search(r'[A-Za-z]{3}',s) and not s.startswith('Permission') and not s.startswith('THE SOFTWARE') and not s.startswith('The above')]
        print('=====',game,lang,len(out[lang]),'unchanged',len(left))
        for s in left:print('  ',repr(s)[:150])
