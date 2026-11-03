import os;HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(HERE+'/../..')+'/';WORK=os.path.abspath(HERE+'/../.work')+'/';os.makedirs(WORK,exist_ok=True);URL='file://'+WORK
import json,urllib.parse
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    # ---------- Smoky logic
    pg=b.new_page(viewport={'width':1024,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    dl=[]
    pg.on('dialog',lambda d:(dl.append(d.message),d.accept('Anna' if 'name' in d.message.lower() else None)))
    pg.goto(URL+'smoky.html');pg.wait_for_timeout(400)
    # add Bald Eagle twice -> score, 'per fish' etc
    pg.click('button.add-card[aria-label="Add Bald Eagle"]');pg.click('button.add-card[aria-label="Add Bald Eagle"]')
    print('eagle qty/pts:',pg.locator('.entity-card:has(button[aria-label="Add Bald Eagle"]) .number').inner_text(),pg.locator('.entity-card:has(button[aria-label="Add Bald Eagle"]) .score').inner_text(),'(expect 2 / 20)')
    print('hero total',pg.inner_text('#total'),'| tab',pg.locator('.player-tab').first.inner_text().replace('\n',' '),'| bottom',pg.inner_text('#bottom-score'))
    pg.click('button.remove[aria-label="Remove Bald Eagle"]');print('after remove qty',pg.locator('.entity-card:has(button[aria-label="Add Bald Eagle"]) .number').inner_text())
    # Basswood extras input
    pg.click('button.add-card[aria-label="Add Basswood"]');pg.fill('.conditions input[data-copy="0"]','3');pg.wait_for_timeout(100)
    print('basswood pts (copy default1 -> set 3 => 6):',pg.locator('.entity-card:has(button[aria-label="Add Basswood"]) .score').inner_text())
    # cave stepper
    pg.click('button[data-global="cave"][data-delta="1"]');pg.click('button[data-global="cave"][data-delta="1"]');print('cave pts',pg.inner_text('#caveTotal'))
    # add player, rename via input, switch, remove
    pg.click('#addPlayer');print('tabs',pg.locator('.player-tab').all_inner_texts())
    pg.fill('#player-name','Berta');print('tabs after rename',[t.replace('\n',' ') for t in pg.locator('.player-tab').all_inner_texts()])
    pg.locator('.player-tab').first.click();print('active name field:',pg.input_value('#player-name'))
    print('results rows',pg.locator('#summary tr').count(),'| start options',pg.locator('#bg-start option').all_inner_texts())
    # BG payload
    pg.check('#review');pg.select_option('#bg-start','1');pg.fill('#location','Luxembourg')
    url=pg.evaluate("(()=>{try{return bgLink(bgPayload())}catch(e){return 'ERR '+e.message}})()")
    d=json.loads(urllib.parse.unquote(url.split('data=')[1]));print('BG:',d['game'],[(x['name'],x['score'],x['winner'],x['startPlayer']) for x in d['players']],d.get('location'))
    pg.click('#remove-player');print('after remove tabs',pg.locator('.player-tab').count())
    # persistence + backup/new game
    pg.reload();pg.wait_for_timeout(300);print('after reload tabs',pg.locator('.player-tab').all_inner_texts())
    pg.click('#hero-session-tools summary');print('session buttons',pg.locator('#hero-session-tools button').all_inner_texts())
    pg.click('#new-game');print('after new game cave',pg.inner_text('#caveTotal'),'| dialogs:',dl[-1])
    print('rules toggle:',end=' ');pg.click('#rules-toggle');print(pg.evaluate("getComputedStyle(document.querySelector('.rule-note')).display"),pg.get_attribute('#rules-toggle','aria-pressed'))
    print('smoky errs',errs)
    # ---------- Forest BG + groups
    pg2=b.new_page(viewport={'width':1024,'height':800});e2=[];pg2.on('pageerror',lambda e:e2.append(str(e)));pg2.on('dialog',lambda d:d.accept())
    pg2.goto(URL+'forest.html');pg2.wait_for_timeout(400)
    pg2.click('button.add-card[aria-label="Add Barn Owl"]');pg2.click('button.add-card[aria-label="Add Beech"]')
    print('forest hero total',pg2.inner_text('#dashboard-score'),'overview',pg2.inner_text('#score-overview').replace('\n',' | ')[:200])
    print('forest groups tops:',pg2.eval_on_selector_all('#section-tops .card-group h3','e=>e.map(x=>x.textContent)'),'bottoms:',pg2.eval_on_selector_all('#section-bottoms .card-group h3','e=>e.map(x=>x.textContent)'),'sides:',pg2.eval_on_selector_all('#section-sides .card-group h3','e=>e.map(x=>x.textContent)'))
    pg2.click('#addPlayer, #add-player') if pg2.locator('#add-player').count() else None
    pg2.wait_for_timeout(200);print('forest players',pg2.locator('.player-tab').count(),'start opts',pg2.locator('#bg-start option').all_inner_texts())
    pg2.check('#review');pg2.select_option('#bg-start','0')
    try:
        url=pg2.evaluate("(()=>{try{return link(payload())}catch(e){return 'ERR '+e.message}})()");d=json.loads(urllib.parse.unquote(url.split('data=')[1]));print('forest BG start:',[(x['name'],x['score'],x['startPlayer']) for x in d['players']])
    except Exception as ex:print('forest bg eval',ex)
    pg2.click('.results-table button[data-player]');print('forest results link switches ok')
    print('forest session buttons',pg2.locator('#hero-session-tools button').all_inner_texts(),'errs',e2)
    # ---------- Dartmoor: language
    pg3=b.new_page(viewport={'width':1024,'height':800});e3=[];pg3.on('pageerror',lambda e:e3.append(str(e)))
    pg3.goto(URL+'moor.html');pg3.wait_for_timeout(400)
    pg3.select_option('#language-select','fr');pg3.wait_for_timeout(300)
    print('moor FR nav:',pg3.locator('.category-nav a').all_inner_texts()[-2:],'errs',e3)
    pg3.select_option('#language-select','de');pg3.wait_for_timeout(300);print('moor DE nav:',pg3.locator('.category-nav a').all_inner_texts()[-2:])
    b.close()
