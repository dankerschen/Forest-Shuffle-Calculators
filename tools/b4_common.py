import re,html
W=HERE
def once(t,old,new,label):
    assert t.count(old)==1,(label,t.count(old))
    return t.replace(old,new)
def sub1(t,pat,repl,label,flags=re.S):
    ms=list(re.finditer(pat,t,flags));assert len(ms)==1,(label,len(ms))
    m=ms[0];r=repl(m) if callable(repl) else repl;return t[:m.start()]+r+t[m.end():]
def IC(n,cls='category-icon'):
    return f'<svg aria-hidden="true" class="{cls}" focusable="false" height="32" viewBox="0 0 64 64" width="32"><use href="#icon-{n}"></use></svg>'

# ---------------- extra icons (own gradients, same hand-drawn wash style) ----------------
EXTRA_SPRITE='''<svg aria-hidden="true" height="0" style="position:absolute;overflow:hidden" width="0" xmlns="http://www.w3.org/2000/svg"><defs>
<linearGradient id="fx-leaf" x2=".8" y2="1"><stop stop-color="#abb47c"/><stop offset="1" stop-color="#58704a"/></linearGradient>
<linearGradient id="fx-earth" x2="1" y2="1"><stop stop-color="#c8b391"/><stop offset="1" stop-color="#8d795d"/></linearGradient>
<linearGradient id="fx-water" x2="1" y2="1"><stop stop-color="#ccdad0"/><stop offset="1" stop-color="#7e9a91"/></linearGradient>
<linearGradient id="fx-fish" x2="1" y2="1"><stop stop-color="#cdd4a8"/><stop offset="1" stop-color="#7d9371"/></linearGradient>
<linearGradient id="fx-cap" x2="1" y2="1"><stop stop-color="#cdb08a"/><stop offset="1" stop-color="#8d6e4c"/></linearGradient>
<symbol id="icon-rivers" viewBox="0 0 64 64"><path d="M4 20q9-8 14 0t14 0 14 0 14 0v9q-9-8-14 0t-14 0-14 0-14 0Z" fill="url(#fx-water)"/><path d="M4 37q9-8 14 0t14 0 14 0 14 0v9q-9-8-14 0t-14 0-14 0-14 0Z" fill="url(#fx-water)"/><path d="M4 54q9-8 14 0t14 0 14 0 14 0M4 11q9-8 14 0t14 0 14 0 14 0" fill="none" stroke="#6d8b84" stroke-width="2"/></symbol>
<symbol id="icon-squirrels" viewBox="0 0 64 64"><path d="M32 58C18 52 14 38 14 30h36c0 8-4 22-18 28Z" fill="url(#fx-earth)"/><path d="M10 30c0-12 9-20 22-20s22 8 22 20Z" fill="#7d6a4f"/><path d="M32 10V4" stroke="#5c4f3a" stroke-width="3" stroke-linecap="round"/><path d="M20 36q4 14 12 18m-6-18q3 10 6 18" fill="none" stroke="#6f5d43" stroke-width=".8"/><path d="M18 22q6-6 14-6" fill="none" stroke="#a69378" stroke-width="1.2" stroke-linecap="round"/></symbol>
<symbol id="icon-fish" viewBox="0 0 64 64"><path d="M5 33c9-14 24-16 37-7l15-9v32l-15-9C29 49 14 47 5 33Z" fill="url(#fx-fish)"/><path d="M22 22q-5 11 0 22M31 20q-4 12 0 25" fill="none" stroke="#5f7656" stroke-width="1" opacity=".7"/><path d="M18 16q8-6 16 0" fill="none" stroke="#6d8b84" stroke-width="1.5"/><circle cx="14" cy="30" r="2" fill="#3f4a3a"/></symbol>
<symbol id="icon-mice" viewBox="0 0 64 64"><path d="M12 46c-1-13 9-22 22-22 12 0 19 8 18 17-1 9-10 11-22 11-9 0-17 0-18-6Z" fill="url(#fx-earth)"/><circle cx="38" cy="22" r="8" fill="#b9a587"/><circle cx="38" cy="22" r="4" fill="#dbc7b5"/><circle cx="50" cy="40" r="2" fill="#3f3a33"/><path d="M13 47c-8 1-9 9-2 11 5 1 9-3 14-3" fill="none" stroke="#8d795d" stroke-width="2" stroke-linecap="round"/></symbol>
<symbol id="icon-mushrooms" viewBox="0 0 64 64"><path d="M26 58V36h8v22Z" fill="#e4dcc7"/><path d="M8 36C8 20 18 12 30 12s22 8 22 24Z" fill="url(#fx-cap)"/><path d="M44 58V46h6v12Z" fill="#e4dcc7"/><path d="M34 46c0-9 6-14 14-14s13 5 13 14Z" fill="url(#fx-cap)"/><g fill="#efe6d2" opacity=".8"><circle cx="20" cy="26" r="2"/><circle cx="32" cy="22" r="2.4"/><circle cx="40" cy="30" r="1.8"/></g></symbol>
<symbol id="icon-allscores" viewBox="0 0 64 64"><path d="M5 58V40h15v18Z" fill="url(#fx-earth)"/><path d="M24 58V28h16v30Z" fill="url(#fx-leaf)"/><path d="M44 58V45h15v13Z" fill="url(#fx-earth)"/><path d="M3 58.5h58" stroke="#766e4d" stroke-width="2" stroke-linecap="round"/><path d="M32 26c-9-1-11-10-8-15 7 0 11 6 8 15Zm0 0c2-8 8-12 14-11-1 8-6 12-14 11Z" fill="url(#fx-leaf)"/><path d="M32 27V16" stroke="#5f714f" stroke-width="1.2"/><path d="M10 47h5m-5 5h5M29 36h6m-6 6h6m-6 6h6M49 50h5" stroke="#fbf8ef" stroke-width="1.5" stroke-linecap="round" opacity=".8"/></symbol>
</defs></svg>'''

LANG_SELECT='<label class="sr-only" for="language-select">Language</label><select aria-label="Language" id="language-select"><option value="en">English</option><option value="fr">Français</option><option value="de">Deutsch</option></select>'
# ---------------- shared CSS ----------------
CSS='''
html .hero :is(button,select,summary,label,option,input,.switch){font-weight:400!important}
html .hero-score strong,html .player-tab strong{font-variant-numeric:lining-nums}
html .hero .eyebrow,html .hero-score #dashboard-label{font-weight:600!important}
/* hero settings: identical spot + row heights in every game */
html .hero-settings{position:relative;z-index:1;flex:0 0 100%;display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:4px 0 0;padding:15px 0 0;border-top:1px solid #a9a98b66}
html .hero-settings .view-controls,html .hero-settings #buttons,html .hero-settings .hero-expansions{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0}
html .sr-only{position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
html .hero-settings .view-controls{flex:0 0 100%;min-height:44px}
html .hero-settings .exp-group{flex:0 0 100%;box-sizing:border-box;padding:8px 12px;gap:8px 10px;border:1px solid var(--line);border-radius:10px;background:color-mix(in srgb,var(--surface) 84%,transparent);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}
@media(max-width:620px){html .hero-settings .exp-label{flex:0 0 100%;margin:0}}
html .hero-settings .exp-label{font:600 11px/1 system-ui,-apple-system,Segoe UI,sans-serif;letter-spacing:.14em;text-transform:uppercase;margin-right:6px;color:var(--muted)}
html .hero-settings :is(button,select){height:44px;box-sizing:border-box;font:400 15px/1.2 system-ui,-apple-system,Segoe UI,sans-serif}
html .hero :is(.session-tools,.hero-session-tools){flex:1 1 100%;margin:0;padding:0 14px;color:var(--ink)!important;background:var(--surface)!important;border:1px solid var(--line)!important;border-radius:8px}
html .hero :is(.session-tools,.hero-session-tools) summary{display:flex;align-items:center;min-height:46px;margin:0;font-size:16px;line-height:1.2;color:var(--ink)!important;cursor:pointer}
html .hero :is(.session-tools,.hero-session-tools)[open] summary{border-bottom:1px solid var(--line);margin-bottom:12px}
html .hero :is(.session-tools,.hero-session-tools) .export-actions{display:flex;flex-wrap:wrap;gap:9px;margin:0 0 12px}
html .hero :is(.session-tools,.hero-session-tools) .export-actions button{width:auto;min-height:42px;margin:0;padding:8px 14px;font:400 15px/1.2 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:6px;cursor:pointer}
html .hero :is(.session-tools,.hero-session-tools) .export-actions button.danger{color:var(--color-remove,#9c5750)}
html .hero :is(.session-tools,.hero-session-tools) :is(small,p){display:block;margin:0 0 12px;font-size:14px;color:var(--muted)}
html .hero :is(.session-tools,.hero-session-tools) :is(small,p):empty{display:none}
/* sticky row: one design */
html .sticky-controls{position:sticky;top:0;z-index:100;margin:0 -2px 24px!important;padding:12px 12px 0!important;background:var(--surface)!important;border:1px solid var(--line)!important;border-top:0!important;border-radius:0 0 12px 12px!important;box-shadow:0 8px 25px #454e3212;isolation:isolate}
html .sticky-art{display:none!important}
html .sticky-content{position:relative;display:block;padding:0}
html .player-bar{display:flex;align-items:center;gap:10px;margin:0;padding:0 0 10px;border-bottom:1px solid var(--line)}
html .player-bar-title{display:flex;flex-direction:column;align-items:flex-start;gap:5px;flex:none;margin:0}
html .player-bar-title>span{padding:0;background:none;font-size:10px;font-weight:600;letter-spacing:.14em;color:var(--muted)}
html .compact-add{width:auto;min-height:38px;margin:0;padding:6px 12px;font:600 15px/1.2 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:7px;cursor:pointer;white-space:nowrap}
html #player-tabs{display:flex;flex:1;min-width:0;gap:8px;margin:0;padding:2px;overflow-x:auto}
html .player-tab{width:auto;min-height:48px;margin:0;display:flex;flex:none;align-items:center;gap:10px;padding:8px 14px;font:600 15px/1.2 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:7px;cursor:pointer}
html .player-tab[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:var(--surface)}
html .player-tab strong{font:500 22px/1 Georgia,Palatino,serif;color:inherit}
html .player-tab-name{max-width:130px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
html .category-nav{display:flex;gap:6px;margin:0;padding:9px 0 10px;overflow-x:auto;position:static}
html .category-nav a{display:inline-flex;flex:none;align-items:center;gap:8px;min-height:44px;margin:0;padding:5px 13px 5px 8px;font:400 15px/1.2 system-ui,-apple-system,Segoe UI,sans-serif;white-space:nowrap;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px}
html .category-nav a:hover,html .category-nav a[aria-current=true]{background:var(--accent-soft);color:var(--accent);border-color:#a3ad87}
html .category-nav .category-icon{width:28px;height:28px;flex:none;margin:0}
html .compact-add:focus-visible,html .player-tab:focus-visible,html .category-nav a:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
html{scroll-padding-top:0!important}
html section[id]{scroll-margin-top:calc(var(--sticky-height,150px) + 14px)!important}
html #nav-spacer{height:0}
@media(max-width:620px){html .score-section .row-total{margin:22px -12px -20px;padding:18px 15px}html .player-bar{gap:8px}html .player-tab{padding:8px 11px}html .player-tab-name{max-width:96px}html .category-nav a{padding-right:11px}}
/* results / BG Stats (Dartmoor layout) */
html .panel-heading{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:17px}
html .panel-heading h2{display:flex;align-items:center;gap:10px;margin:0}
html .section-tag{font-size:11px;letter-spacing:.8px;color:var(--muted);padding:5px 8px;border:1px solid var(--line);border-radius:4px;text-align:center;white-space:nowrap}
html .hint{font-size:15px;color:var(--muted);line-height:1.6}
html .table-scroll{overflow:auto;margin:20px 0 26px}
html .results-table{width:100%;border-collapse:collapse;font-size:13px;white-space:nowrap}
html .results-table th,html .results-table td{padding:13px 11px;text-align:right;border-bottom:1px solid var(--line)}
html .results-table th{color:var(--muted);font-size:11px;font-weight:500}
html .results-table th:first-child,html .results-table td:first-child{text-align:left}
html .results-table td:last-child{font-weight:650;font-size:20px;color:var(--accent)}
html .results-table tr.active{background:var(--accent-soft)}
html .results-table .category-icon{width:21px;height:21px;margin-right:5px;vertical-align:-5px}
html .results-table button{width:auto;min-height:44px;margin:0;padding:0;font:inherit;font-size:15px;color:var(--ink);background:transparent;border:0;text-decoration:underline;cursor:pointer}
html .field-grid{display:grid;grid-template-columns:1fr 1fr;gap:17px}
html .field-grid label{display:flex;flex-direction:column;gap:6px;font-size:16px;font-weight:600}
html .field-grid :is(input,select){width:100%;min-height:48px;box-sizing:border-box;padding:10px 12px;font:400 16px/1.3 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--soft);border:1px solid var(--line);border-radius:6px}
@media(max-width:620px){html .field-grid{grid-template-columns:1fr}}
html .score-section .option-label{display:flex;align-items:center;gap:10px;font-weight:400;font-size:16px}
html .score-section .option-label input{width:22px;height:22px;flex:none;margin:0}
html .score-section .export-actions{display:flex;flex-wrap:wrap;gap:9px;margin-top:14px}
html .score-section .export-actions button{width:auto;min-height:46px;margin:0;padding:10px 16px;font:600 16px/1.2 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:6px;cursor:pointer}
html .score-section .export-actions button.primary{background:#596c4d;color:#fffcef;border-color:#596c4d}
html .score-overview .row-score{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0;padding:14px 0;font-size:17px;border-bottom:1px solid var(--line)}
html .score-overview .row-score>span:first-child{display:block}
html .score-overview .row-score>span:last-child{font-weight:650;font-size:20px}
html .score-overview .category-icon{width:32px;height:32px;margin:0 8px 0 0;vertical-align:middle}
html .score-section .row-total{display:flex;justify-content:space-between;align-items:center;margin:22px -25px -25px;padding:20px 25px;font:600 31px/1.2 Georgia,serif;color:var(--accent);background:var(--accent-soft);border-top:1px solid var(--line);border-radius:0 0 11px 11px}
html .score-section .row-total>span:first-child{display:flex;align-items:center}
html .score-section .row-total .category-icon{margin:0 8px 0 0}
html .player-settings{display:flex;flex-wrap:wrap;align-items:flex-end;gap:12px}
html .player-settings label{flex:1 1 260px;display:flex;flex-direction:column;gap:6px;font-size:16px;font-weight:600}
html .player-settings input{min-height:48px;box-sizing:border-box;padding:10px 12px;font:400 16px/1.3 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--soft);border:1px solid var(--line);border-radius:6px}
html .player-settings button.danger{min-height:48px;padding:10px 16px;font:600 16px/1.2 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--color-remove,#9c5750);background:var(--surface);border:1px solid var(--line);border-radius:6px;cursor:pointer}
html .player-settings button:disabled{opacity:.45;cursor:default}
'''
# ---------------- shared JS: scroll-spy, sticky height, end spacer ----------------
JS='''<script>(function(){const D=document;let last=null;
function stickyH(sc){return sc.getBoundingClientRect().height+(parseFloat(getComputedStyle(sc).top)||0)}
function items(){return [...D.querySelectorAll('.category-nav a[href^="#"]:not(.nav-top)')].map(a=>({a,el:D.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)))})).filter(x=>x.el)}
function spacer(sc,its){let sp=D.getElementById('nav-spacer');if(!sp){sp=D.createElement('div');sp.id='nav-spacer';D.body.appendChild(sp)}
const lastEl=its[its.length-1].el;sp.style.height='0px';const below=sp.getBoundingClientRect().top-lastEl.getBoundingClientRect().top;
const need=innerHeight-stickyH(sc)-14-below;sp.style.height=Math.max(0,Math.ceil(need))+'px'}
function upd(){const sc=D.querySelector('.sticky-controls'),nav=D.querySelector('.category-nav');if(!sc||!nav)return;
D.documentElement.style.setProperty('--sticky-height',Math.ceil(stickyH(sc))+'px');
const its=items();if(!its.length)return;spacer(sc,its);const off=sc.getBoundingClientRect().bottom+30;let cur=its[0];
for(const i of its)if(i.el.getBoundingClientRect().top<=off)cur=i;
its.forEach(i=>i.a.removeAttribute('aria-current'));cur.a.setAttribute('aria-current','true');
if(last!==cur.a){last=cur.a;const l=cur.a.offsetLeft-(nav.clientWidth-cur.a.offsetWidth)/2;if(nav.scrollWidth>nav.clientWidth)nav.scrollTo({left:Math.max(0,l)})}}
let q=false;const sched=()=>{if(!q){q=true;requestAnimationFrame(()=>{q=false;upd()})}};
addEventListener('scroll',sched,{passive:true});addEventListener('resize',sched);addEventListener('load',sched);
const sc=D.querySelector('.sticky-controls');if(sc&&window.ResizeObserver)new ResizeObserver(sched).observe(sc);
const mn=D.getElementById('calculator')||D.getElementById('main');if(mn&&window.ResizeObserver)new ResizeObserver(sched).observe(mn);
D.addEventListener('click',function(e){const a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a||e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey)return;
if(a.classList.contains('nav-top')){e.preventDefault();scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});return}
const id=decodeURIComponent(a.getAttribute('href').slice(1));if(!id)return;const el=D.getElementById(id);if(!el)return;e.preventDefault();
const rm=matchMedia('(prefers-reduced-motion: reduce)').matches;el.scrollIntoView({behavior:rm?'auto':'smooth',block:'start'});
D.querySelectorAll('.category-nav a[aria-current]').forEach(x=>x.removeAttribute('aria-current'));if(a.closest('.category-nav'))a.setAttribute('aria-current','true')});
(function(){const nav=D.querySelector('.category-nav'),h=D.querySelector('header.hero');if(!nav||!h||nav.querySelector('.nav-top'))return;
if(!h.id)h.id='hero';const a=D.createElement('a');a.className='nav-top';a.href='#'+h.id;a.setAttribute('aria-label','Back to top');a.title='Back to top';
a.innerHTML='<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false"><path d="M3.5 11.2 12 4l8.5 7.2M6 9.8V20h4.5v-5.5h3V20H18V9.8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>';
nav.insertBefore(a,nav.firstChild)})();
setTimeout(upd,150);})()</script>'''


ART_CSS='''
/* ---- hero: let the artwork breathe, keep text legible ---- */
html .hero:after{background:linear-gradient(90deg,color-mix(in srgb,var(--hs) 88%,transparent),color-mix(in srgb,var(--hs) 64%,transparent) 46%,color-mix(in srgb,var(--hs) 3%,transparent))!important}
html .hero :is(h1,p,.eyebrow){text-shadow:0 0 16px color-mix(in srgb,var(--hs) 90%,transparent),0 0 4px color-mix(in srgb,var(--hs) 70%,transparent)}
@media(max-width:620px){html .hero:after{background:linear-gradient(180deg,color-mix(in srgb,var(--hs) 86%,transparent),color-mix(in srgb,var(--hs) 56%,transparent))!important}}
/* ---- floating sticky bar with habitat strip ---- */
html .sticky-controls{top:8px;margin:0 0 24px!important;padding:12px 12px 2px!important;background:linear-gradient(180deg,color-mix(in srgb,var(--surface) 78%,transparent),color-mix(in srgb,var(--surface) 90%,transparent)),var(--strip-img) center bottom/cover no-repeat,var(--surface)!important;border:1px solid color-mix(in srgb,var(--line) 65%,var(--accent))!important;border-radius:16px!important;box-shadow:inset 0 1px 0 #ffffffb8,0 1px 2px #2f3d2a1f,0 14px 28px -14px #2f3d2a70!important}
html .sticky-controls::before{content:"";position:absolute;z-index:-1;left:0;right:0;top:-9px;height:9px;background:var(--page)}
html .player-bar{border-bottom:1px solid color-mix(in srgb,var(--line) 80%,transparent)}
html .category-nav{padding:10px 0 11px}
/* ---- section backgrounds: corner sprig + habitat ground line ---- */
html .score-section{position:relative;isolation:isolate}
html #player-management .solo-option{width:auto;display:inline-flex;margin:2px 0 8px;min-height:46px;padding:6px 14px;border:1px solid var(--line);border-radius:6px;font-weight:600;background:var(--surface)}
html #player-management .player-settings{margin-bottom:6px}
html .score-section::before{content:"";position:absolute;z-index:-1;top:4px;right:4px;width:min(40%,280px);aspect-ratio:1/1;background:var(--m-default,none) no-repeat right top/contain;opacity:.22;pointer-events:none}
html #player-management.score-section::before{background-image:var(--m-player,none)}
html #section-trees.score-section::before,html #Trees.score-section::before{background-image:var(--m-trees,none)}
html #section-moors.score-section::before{background-image:var(--m-moors,none)}
html #Rivers.score-section::before{background-image:var(--m-rivers,none)}
html #section-tops.score-section::before,html #Top.score-section::before{background-image:var(--m-tops,none)}
html #section-bottoms.score-section::before,html #Bottom.score-section::before{background-image:var(--m-bottoms,none)}
html #section-sides.score-section::before,html #Sides.score-section::before{background-image:var(--m-sides,none)}
html #Squirrels.score-section::before{background-image:var(--m-squirrels,none)}
html #section-symbols.score-section::before{background-image:var(--m-symbols,none)}
html #section-cave.score-section::before,html #Cave.score-section::before{background-image:var(--m-cave,none)}
html #section-manual.score-section::before{background-image:var(--m-manual,none)}
html #section-summary.score-section::before{background-image:var(--m-summary,none)}
html #section-bgstats.score-section::before{background-image:var(--m-bgstats,none)}
html .score-section::after{content:"";position:absolute;z-index:-1;left:0;right:0;bottom:0;height:110px;background:var(--strip-img) center bottom/cover no-repeat;opacity:.22;border-radius:0 0 11px 11px;-webkit-mask-image:linear-gradient(to top,#000 15%,transparent);mask-image:linear-gradient(to top,#000 15%,transparent);pointer-events:none}
html:root[data-theme=dark] .score-section::before{opacity:.16}
html:root[data-theme=dark] .score-section::after{opacity:.12}
@media(max-width:620px){html .score-section::before{width:min(52%,230px)}html .score-section::after{height:80px}html .sticky-controls{padding:10px 10px 0!important;border-radius:14px!important}}
'''


LAYOUT_CSS='''
/* ---- hero scrim: soft pool behind the text only, artwork shows everywhere else ---- */
html .hero:after{background:radial-gradient(ellipse 50% 56% at 21% 38%,color-mix(in srgb,var(--hs) 70%,transparent) 0%,color-mix(in srgb,var(--hs) 48%,transparent) 58%,transparent 100%),linear-gradient(180deg,color-mix(in srgb,var(--hs) 10%,transparent),transparent 45%)!important}
@media(max-width:620px){html .hero:after{background:linear-gradient(180deg,color-mix(in srgb,var(--hs) 80%,transparent),color-mix(in srgb,var(--hs) 60%,transparent))!important}}
/* ---- game switcher inside the hero ---- */
html .game-switch{position:relative;z-index:2;flex:0 0 100%;display:flex;gap:8px;margin:0 0 6px;padding:0}
html .game-switch button{flex:1 1 0;min-width:0;min-height:42px;margin:0;padding:6px 10px;font:500 15px/1.2 Georgia,Palatino,serif;color:var(--ink);background:color-mix(in srgb,var(--surface) 90%,transparent);border:1px solid var(--line);border-radius:10px;cursor:pointer;touch-action:manipulation;text-align:center}
html .game-switch button[aria-current=page]{background:var(--accent);border-color:var(--accent);color:#fbf8ef}
html .game-switch button:not([aria-current=page]):hover{border-color:var(--accent)}
html .game-switch button:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
@media(max-width:480px){html .game-switch .long{display:none}html .game-switch button{padding:6px 4px;font-size:14px}}
/* ---- no bottom bar ---- */
html #bottom-pane{display:none!important}
html body{padding-bottom:36px!important}
/* ---- compact sticky bar ---- */
html .sticky-controls{top:6px;padding:7px 10px 0!important;border-radius:14px!important}
html .sticky-controls::before{top:-7px;height:7px}
html .player-bar{gap:8px;padding:0 0 7px}
html .player-bar-title{flex-direction:row;align-items:center}
html .player-bar-title>span{display:none}
html .compact-add{min-height:36px;padding:4px 11px;font-size:14px;border-radius:8px}
html #player-tabs{gap:6px;padding:1px}
html .player-tab{min-height:38px;padding:4px 11px;gap:8px;font-size:14px;border-radius:8px}
html .player-tab strong{font-size:18px}
html .category-nav{gap:5px;padding:7px 0 8px}
html .category-nav a{min-height:36px;gap:6px;padding:3px 11px 3px 6px;font-size:14px;border-radius:8px}
html .category-nav a:not(:has(.category-icon)){padding-left:11px}
html .category-nav .category-icon{width:24px;height:24px}
@media(max-width:620px){html .sticky-controls{padding:6px 8px 0!important;border-radius:12px!important}html .player-tab{padding:4px 9px}html .category-nav a{padding-right:9px}}
'''

_IC=lambda body:"url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E"+body+"%3C/svg%3E\")"
TOOLS_CSS='''
html .category-nav a.nav-top{box-sizing:border-box;position:sticky;left:0;z-index:1;justify-content:center;width:44px;min-width:44px;padding:0!important;color:var(--accent)}
html .category-nav a.nav-top svg{width:22px;height:22px;display:block}
html .category-nav a.nav-top:hover{background:var(--accent-soft);border-color:#a3ad87}
@media(max-width:620px){html .category-nav a.nav-top{width:40px;min-width:40px}}
html{--ic-lang:'''+_IC("%3Ccircle cx='12' cy='12' r='9'/%3E%3Cpath d='M3 12h18M12 3c3.2 3 3.2 15 0 18M12 3c-3.2 3-3.2 15 0 18'/%3E")+''';--ic-rules:'''+_IC("%3Cpath d='M3 5.5c3-1.2 6-1.2 9 .8 3-2 6-2 9-.8V19c-3-1.2-6-1.2-9 .8-3-2-6-2-9-.8Z'/%3E%3Cpath d='M12 6.3v13.5'/%3E")+''';--ic-dark:'''+_IC("%3Cpath d='M20 14.6A8.2 8.2 0 0 1 9.4 4a8.6 8.6 0 1 0 10.6 10.6Z'/%3E")+'''}
html .hero-top{position:relative;z-index:3;flex:0 0 100%;display:flex;align-items:stretch;gap:10px;margin:0 0 6px}
html .hero-top .game-switch{flex:1 1 0;min-width:0;margin:0}
html .hero-top .game-switch button{min-height:54px}
html .hero-tools{display:flex;flex:none;gap:6px}
html .hero .hero-tools .tool{position:relative;box-sizing:border-box;width:72px!important;min-height:54px!important;margin:0!important;padding:6px 2px 4px!important;display:flex!important;flex-direction:column;align-items:center;justify-content:center;gap:3px;text-align:center;font:400 9.5px/1.1 system-ui,-apple-system,Segoe UI,sans-serif!important;letter-spacing:.01em;white-space:nowrap!important;color:var(--muted)!important;background:color-mix(in srgb,var(--surface) 90%,transparent)!important;border:1px solid var(--line)!important;border-radius:10px!important;cursor:pointer;touch-action:manipulation}
html .hero .hero-tools .tool::before,html .hero .hero-tools button.tool[aria-pressed]::before,html .hero .hero-tools button.tool[aria-pressed=true]::before{content:"";display:block;flex:none;width:22px;height:22px;margin:0;padding:0;border:0;border-radius:0;background:var(--ink);-webkit-mask:var(--ic) center/contain no-repeat;mask:var(--ic) center/contain no-repeat}
html .hero .hero-tools .tool-lang{--ic:var(--ic-lang)}
html .hero .hero-tools .tool-rules{--ic:var(--ic-rules)}
html .hero .hero-tools .tool-theme{--ic:var(--ic-dark)}
html .hero .hero-tools .tool-note{font:inherit;color:inherit;text-transform:none}
html .hero .hero-tools .tool-lang select{position:absolute;inset:0;width:100%;height:100%;margin:0;padding:0;opacity:0;cursor:pointer;font-size:16px;-webkit-appearance:none;appearance:none}
html .hero .hero-tools button.tool[aria-pressed=true]{background:var(--accent)!important;border-color:var(--accent)!important;color:var(--surface)!important}
html .hero .hero-tools button.tool[aria-pressed=true]::before{background:var(--surface)}
html .hero .hero-tools .tool:not([aria-pressed=true]):hover,html .hero .hero-tools .tool-lang:hover{border-color:var(--accent)!important}
html .hero .hero-tools .tool:focus-visible,html .hero .hero-tools .tool-lang:focus-within{outline:3px solid var(--accent);outline-offset:2px}
html .hero .hero-settings :is(.session-tools,.hero-session-tools){background:color-mix(in srgb,var(--surface) 84%,transparent)!important;-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);border-radius:10px!important}
html .hero .session-tools :is(#status,#saveState,#session-status){display:block;margin:0 0 12px!important;padding:0!important;font:400 14px/1.4 system-ui,-apple-system,Segoe UI,sans-serif!important;color:var(--muted)!important;opacity:1!important}
html .sticky-tools{display:flex;flex:none;gap:6px;margin:0 0 0 2px}
html .stool{box-sizing:border-box;width:44px;height:44px;min-height:44px;margin:0;padding:0;display:grid;place-items:center;flex:none;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:8px;cursor:pointer;touch-action:manipulation}
html .stool::before{content:"";display:block;width:22px;height:22px;background:var(--ink);-webkit-mask:var(--ic) center/contain no-repeat;mask:var(--ic) center/contain no-repeat}
html .stool-rules{--ic:var(--ic-rules)}html .stool-theme{--ic:var(--ic-dark)}
html .stool[aria-pressed=true]{background:var(--accent);border-color:var(--accent)}
html .stool[aria-pressed=true]::before{background:var(--surface)}
html .stool:hover{border-color:var(--accent)}html .stool:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
@media(max-width:480px){html .stool{width:40px;height:40px;min-height:40px}html .sticky-tools{gap:4px}}
@media(max-width:560px){html .hero-top{flex-wrap:wrap}html .hero-top .game-switch{flex:0 0 100%}html .hero-tools{flex:0 0 100%;justify-content:flex-end}}
'''
