import os;HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(HERE+'/../..')+'/'
from playwright.sync_api import sync_playwright
# Default player names ("Player 2") follow the language: tab, name input and stored session all agree.
# Custom names are left alone. Run on the combined page so the shell's language sync is included.
ADD={'forest':'#add-player','moor':'.compact-add','smoky':'#addPlayer'}
STORED={'forest':"state.players.map(p=>p.name)",'smoky':"state.players.map(p=>p.name)",'moor':"forestSession.players.map(p=>p.name)"}
fails=[]
def check(label,got,want):
    ok=got==want;print(('ok  ' if ok else 'FAIL'),label,got,'' if ok else '!= '+str(want))
    if not ok:fails.append(label)
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':1024,'height':900},locale='en-US');pg=ctx.new_page()
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.goto('file://'+ROOT+'index.html');pg.wait_for_timeout(1500)
    def fr(g):return pg.locator('#f-'+g).element_handle().content_frame()
    def stored(g):return fr(g).evaluate(STORED[g])
    def inp(g):return fr(g).evaluate("document.getElementById('player-name').value")
    def setlang(g,l):
        pg.evaluate("g=>location.hash='#'+g",g);pg.wait_for_timeout(300)
        fr(g).select_option('#language-select',l);pg.wait_for_timeout(700)
    for g in ['forest','moor','smoky']:
        pg.evaluate("g=>location.hash='#'+g",g);pg.wait_for_timeout(400)
        f=fr(g)
        f.click(ADD[g]);pg.wait_for_timeout(300)
        f.evaluate("""()=>{const i=document.getElementById('player-name');i.value='Berta';i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}))}""");pg.wait_for_timeout(200)
        f.click(ADD[g]);pg.wait_for_timeout(300)
        check(g+' en stored',stored(g),['Player 1','Berta','Player 3'])
        setlang(g,'fr')
        check(g+' fr stored',stored(g),['Joueur 1','Berta','Joueur 3'])
        check(g+' fr input',inp(g),'Joueur 3')
        f.click(ADD[g]);pg.wait_for_timeout(300)
        check(g+' fr new player',stored(g)[-1],'Joueur 4')
        setlang(g,'de')
        check(g+' de stored',stored(g),['Person 1','Berta','Person 3','Person 4'])
        check(g+' de input',inp(g),'Person 4')
        setlang(g,'en')
        check(g+' en again',stored(g),['Player 1','Berta','Player 3','Player 4'])
    # other games follow a language change made in one game
    setlang('smoky','fr')
    for g in ['forest','moor']:check(g+' follows smoky fr',stored(g)[0],'Joueur 1')
    pg.reload();pg.wait_for_timeout(1500)
    for g in ['forest','moor','smoky']:check(g+' after reload',stored(g)[:2],['Joueur 1','Berta'])
    setlang('forest','en')
    print('errors',errs);b.close()
print('FAILED' if fails or errs else 'ALL OK',fails)
