import os;HERE=os.path.dirname(os.path.abspath(__file__))+'/'
exec(open(HERE+'b4_smoky.py',encoding='utf-8').read())
exec(open(HERE+'b4_moor.py',encoding='utf-8').read())
exec(open(HERE+'b4_credits.py',encoding='utf-8').read())
exec(open(HERE+'i18n_build.py',encoding='utf-8').read())
base={k:open(W+f'base_{k}.html',encoding='utf-8').read() for k in ['forest','moor','smoky']}
f=build_forest(base['forest']);m=build_moor(base['moor']);s=build_smoky(base['smoky'],base['forest'],base['moor'])
def inject(t,sprite=True):
    t=t.replace('</style>',CSS+CREDIT_CSS+ART_CSS+LAYOUT_CSS+TOOLS_CSS+'</style>',1).replace('</body>',JS+'</body>',1)
    if sprite:t=once(t,'<body>','<body>'+EXTRA_SPRITE,'sprite')
    return t
def nocards(x):
    a=".replace(/:\\s*(Hide|Show)\\s+cards$/i,' cards')";b=".replace(/:\\s*(Hide|Show)\\s+cards$/i,'')"
    assert x.count(a)==1,x.count(a);x=x.replace(a,b)
    a="c.textContent='Exmoor cards'";assert x.count(a)==1;return x.replace(a,"c.textContent='Exmoor'")
f=nocards(f);m=nocards(m);s=nocards(s)
SAVED='Saved on this browser. Back up before clearing browser data.'
assert f.count('Session saved on this device.')==1;f=f.replace('Session saved on this device.',SAVED)
assert s.count("Saved on this browser'")==1;s=s.replace("Saved on this browser'",SAVED+"'")
f=inject(apply_credits(f,'forest'));m=inject(apply_credits(m,'moor'));s=inject(apply_credits(s,'smoky'),sprite=False)
import base64
def b64(p,mime):return 'url(data:%s;base64,%s)'%(mime,base64.b64encode(open(HERE+'art/'+p,'rb').read()).decode())
import glob as _g,os as _o
def rootvars(g):
    ms=''.join(';--m-%s:%s'%(_o.path.basename(f)[len('motif_%s_'%g):-5],b64(_o.path.basename(f),'image/webp')) for f in sorted(_g.glob(HERE+'art/motif_%s_*.webp'%g)))
    return ':root{--hero-img:%s;--strip-img:%s%s}'%(b64('hero_%s.jpg'%g,'image/jpeg'),b64('strip_%s.jpg'%g,'image/jpeg'),ms)
import re as _re
def setvars(t,g):
    ms=list(_re.finditer(r':root\{--hero-img:url\([^)]*\)\}',t));assert len(ms)==1,(g,len(ms))
    return t[:ms[0].start()]+rootvars(g)+t[ms[0].end():]
f=setvars(f,'forest');m=setvars(m,'moor');s=setvars(s,'smoky')
THEMEJS="""<script>(function(){var R=document.documentElement;function post(){try{parent.postMessage({fsTheme:R.dataset.theme==='dark'?'dark':'light'},'*')}catch(e){}}
addEventListener('message',function(e){if(e.source!==parent)return;var d=e.data;if(!d||(d.fsTheme!=='dark'&&d.fsTheme!=='light'))return;
 if(R.dataset.theme===d.fsTheme)return;var b=document.getElementById('theme')||document.getElementById('theme-toggle');if(b)b.click();else R.dataset.theme=d.fsTheme});
new MutationObserver(post).observe(R,{attributes:true,attributeFilter:['data-theme']})})()</script>"""
def switch(g):
    items=[('forest','Forest',''),('moor','Dartmoor',''),('smoky','Smoky',' Mountains')]
    return '<nav class="game-switch" aria-label="Choose game">'+''.join('<button type="button" data-g="%s"%s>%s%s</button>'%(k,' aria-current="page"' if k==g else '',n,('<span class="long">%s</span>'%x) if x else '') for k,n,x in items)+'</nav>'
# Default player names ("Player 2") follow the page language; the i18n engine renames them on a language switch.
DEFNAME_JS="<script>function fsDefName(n){return window.__fsDefName?window.__fsDefName(n):'Player '+n}</script>"
PLAYER_HOOK={
 'forest':"{list:function(){return state.players},commit:function(){save();render()}}",
 'smoky':"{list:function(){return state.players},commit:function(){render();var i=document.getElementById('player-name');if(i)i.value=state.players[state.active].name}}",
 'moor':"{list:function(){return typeof forestSession!=='undefined'&&forestSession?forestSession.players:[]},commit:function(){setTimeout(function(){var i=document.getElementById('player-name');if(i)i.value=activePlayer().name;renderPlayers();persistSession()},0)}}",  # deferred: let Moor's own language handler run first
}
def addswitch(t,g):
    assert t.count('<header class="hero">')==1,g
    vc=_re.search(r'<div class="view-controls">(.*?)</div>',t,_re.S);assert vc,g
    inner=vc.group(1);t=t[:vc.start()]+t[vc.end():]
    lab=_re.search(r'<label class="sr-only".*?</label>',inner,_re.S).group(0)
    sel=_re.search(r'<select.*?</select>',inner,_re.S).group(0)
    sel=sel.replace('>EN<','>English<').replace('>FR<','>Fran\u00e7ais<').replace('>DE<','>Deutsch<')
    btns=_re.findall(r'<button.*?</button>',inner,_re.S);assert len(btns)==2,(g,len(btns))
    def addcls(b,c):
        if 'class="' in b.split('>')[0]:return _re.sub(r'class="([^"]*)"',lambda m:'class="'+m.group(1)+' '+c+'"',b,count=1)
        return b.replace('<button','<button class="'+c+'"',1)
    tools=('<div class="hero-tools" role="group" aria-label="Page settings"><span class="tool tool-lang">'+lab+sel+'<span class="tool-note" id="lang-note">EN</span></span>'
           +addcls(btns[0],'tool tool-rules')+addcls(btns[1],'tool tool-theme')+'</div>')
    t=t.replace('<header class="hero">','<header class="hero"><div class="hero-top">'+switch(g)+tools+'</div>',1)
    js="<script>document.querySelectorAll('.game-switch button').forEach(function(b){b.addEventListener('click',function(){if(b.getAttribute('aria-current')==='page')return;try{parent.postMessage({fsGame:b.dataset.g},'*')}catch(e){}})})</script>"
    js+=THEMEJS
    js+="""<script>(function(){var pb=document.querySelector('.player-bar');if(!pb)return;var src={rules:document.querySelector('.hero-tools .tool-rules'),dark:document.querySelector('.hero-tools .tool-theme')};
var w=document.createElement('div');w.className='sticky-tools';
[['rules','Rules','stool-rules'],['dark','Dark mode','stool-theme']].forEach(function(d){var s=src[d[0]];if(!s)return;var b=document.createElement('button');b.type='button';b.className='stool '+d[2];b.setAttribute('aria-label',d[1]);b.title=d[1];
function sync(){b.setAttribute('aria-pressed',s.getAttribute('aria-pressed')==='true'?'true':'false')}
b.addEventListener('click',function(){s.click()});sync();new MutationObserver(sync).observe(s,{attributes:true,attributeFilter:['aria-pressed']});w.appendChild(b)});
pb.appendChild(w)})()</script>"""
    js+='<script>window.__fsPlayers='+PLAYER_HOOK[g]+'</script>'
    js+=i18n_script(g)
    assert t.count('</head>')==1,g
    t=t.replace('</head>',DEFNAME_JS+'</head>',1)
    return t.replace('</body>',js+'</body>',1)
f=addswitch(f,'forest');m=addswitch(m,'moor');s=addswitch(s,'smoky')
shell=open(HERE+'shell_template.html',encoding='utf-8').read()
import re as _r
if '<nav id="games"' in shell:
    shell=_r.sub(r'<nav id="games".*?</nav>\n?','',shell,count=1,flags=_r.S)
    shell=_r.sub(r'#games\{[^}]*\}\n#games button\{[^}]*\}\n#games button\[aria-selected=true\]\{[^}]*\}\n#games button:focus-visible\{[^}]*\}\n','',shell)
    i=shell.index('<script>\nconst KEY');j=shell.index('</script></body></html>')
    shell=shell[:i]+'''<script>
const KEY='fs-last-game',root=document.documentElement,G=['forest','moor','smoky'];
function show(g){G.forEach(k=>document.getElementById('f-'+k).hidden=k!==g);
 try{localStorage.setItem(KEY,g)}catch(e){}try{history.replaceState(null,'','#'+g)}catch(e){}}
addEventListener('message',function(e){const d=e.data;if(!d||G.indexOf(d.fsGame)<0)return;
 if(!G.some(k=>document.getElementById('f-'+k).contentWindow===e.source))return;show(d.fsGame)});
addEventListener('hashchange',function(){const h=location.hash.slice(1);if(G.includes(h))show(h)});
let start='forest';try{start=localStorage.getItem(KEY)||start}catch(e){}
const h=location.hash.slice(1);if(G.includes(h))start=h;show(start);
const dark=matchMedia('(prefers-color-scheme: dark)');
let theme=null;try{theme=localStorage.getItem('fs-theme')}catch(e){}
if(theme!=='dark'&&theme!=='light')theme=dark.matches?'dark':'light';
function setTheme(t,from){theme=t;root.dataset.theme=t;try{localStorage.setItem('fs-theme',t)}catch(e){}
 for(const k of G){const w=document.getElementById('f-'+k).contentWindow;if(w&&w!==from)try{w.postMessage({fsTheme:t},'*')}catch(e){}}}
addEventListener('message',function(e){const d=e.data;if(!d||(d.fsTheme!=='dark'&&d.fsTheme!=='light'))return;
 if(!G.some(k=>document.getElementById('f-'+k).contentWindow===e.source))return;if(d.fsTheme!==theme)setTheme(d.fsTheme,e.source)});
for(const k of G){const f=document.getElementById('f-'+k);f.addEventListener('load',function(){try{f.contentWindow.postMessage({fsTheme:theme},'*')}catch(e){}})}
root.dataset.theme=theme;
'''+shell[j:]

NEWTHEME='''const dark=matchMedia('(prefers-color-scheme: dark)');
let theme=null;try{theme=localStorage.getItem('fs-theme')}catch(e){}
if(theme!=='dark'&&theme!=='light')theme=dark.matches?'dark':'light';
function setTheme(t,from){theme=t;root.dataset.theme=t;try{localStorage.setItem('fs-theme',t)}catch(e){}
 for(const k of G){const w=document.getElementById('f-'+k).contentWindow;if(w&&w!==from)try{w.postMessage({fsTheme:t},'*')}catch(e){}}}
addEventListener('message',function(e){const d=e.data;if(!d||(d.fsTheme!=='dark'&&d.fsTheme!=='light'))return;
 if(!G.some(k=>document.getElementById('f-'+k).contentWindow===e.source))return;if(d.fsTheme!==theme)setTheme(d.fsTheme,e.source)});
for(const k of G){const f=document.getElementById('f-'+k);f.addEventListener('load',function(){try{f.contentWindow.postMessage({fsTheme:theme},'*')}catch(e){}})}
root.dataset.theme=theme;
let lang=null;try{lang=localStorage.getItem('fs-lang')}catch(e){}
if(!['en','fr','de'].includes(lang)){const n=(navigator.language||'en').slice(0,2).toLowerCase();lang=['fr','de'].includes(n)?n:'en'}
root.lang=lang;
function setLang(l,from){lang=l;root.lang=l;try{localStorage.setItem('fs-lang',l)}catch(e){}
 for(const k of G){const w=document.getElementById('f-'+k).contentWindow;if(w&&w!==from)try{w.postMessage({fsLang:l},'*')}catch(e){}}}
addEventListener('message',function(e){const d=e.data;if(!d||['en','fr','de'].indexOf(d.fsLang)<0)return;
 if(!G.some(k=>document.getElementById('f-'+k).contentWindow===e.source))return;if(d.fsLang!==lang)setLang(d.fsLang,e.source)});
for(const k of G){const f=document.getElementById('f-'+k);f.addEventListener('load',function(){try{f.contentWindow.postMessage({fsLang:lang},'*')}catch(e){}})}
'''
if "const dark=matchMedia('(prefers-color-scheme: dark)');" in shell:
    a_=shell.index("const dark=matchMedia('(prefers-color-scheme: dark)');");b_=shell.index('</script></body></html>')
    shell=shell[:a_]+NEWTHEME+shell[b_:]

frames=''.join(f'<iframe id="f-{k}" title="{t}" srcdoc="{html.escape(v,quote=True)}" hidden></iframe>' for k,v,t in
 [('forest',f,'Forest Shuffle base game'),('moor',m,'Forest Shuffle Dartmoor'),('smoky',s,'Forest Shuffle Smoky Mountains')])
a=shell.index('<iframe id="f-forest"');b=shell.rindex('</iframe>')+9
open(HERE+'../index.html','w',encoding='utf-8').write(shell[:a]+frames+shell[b:])
print('built',len(shell[:a]+frames+shell[b:]))
