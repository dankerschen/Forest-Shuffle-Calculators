import os;HERE=os.path.dirname(os.path.abspath(__file__))+'/'
exec(open(HERE+'b4_forest.py',encoding='utf-8').read())

SMOKY_JS_NEW = r'''
const TITLE={Trees:'Trees',Rivers:'Rivers',Top:'Tops',Bottom:'Bottoms',Sides:'Sides',Squirrels:'Squirrels'};
const IK={Trees:'trees',Rivers:'rivers',Top:'tops',Bottom:'bottoms',Sides:'sides',Squirrels:'squirrels'};
const ic=k=>`<svg class="category-icon" viewBox="0 0 64 64" width="32" height="32" aria-hidden="true"><use href="#icon-${k}"></use></svg>`;
const TYPECAT={bird:'Birds',insect:'Insects',plant:'Plants',paw:'Paws',hoof:'Hooves',mouse:'Mice and shrews',fish:'Fish',amphibian:'Amphibians (and reptiles)'};
const CATIC={Birds:'birds',Insects:'insects',Plants:'plants',Paws:'paws',Hooves:'hooves','Mice and shrews':'mice',Fish:'fish','Amphibians (and reptiles)':'amphibians'};
const ORDER={Top:['Birds','Insects','Paws','Plants'],Bottom:['Amphibians (and reptiles)','Fish','Plants','Insects'],Sides:['Birds','Paws','Hooves','Mice and shrews','Insects','Plants']};
function cardRow(c,p,s){const e=entry(p,c);let ex='';if(c.extra&&e.n){ex='<div class="conditions">'+Array.from({length:e.n},(_,j)=>{const check=['bear','skunk','wasp'].includes(c.rule);return `<label class="option-label">Copy ${j+1} · ${esc(c.extra)} ${check?`<input type="checkbox" data-card="${c.id}" data-copy="${j}" ${e.x[j]?'checked':''}>`:`<input type="number" min="0" max="${c.name==='Virginia Opossum'?8:1000}" inputmode="numeric" data-card="${c.id}" data-copy="${j}" value="${e.x[j]||0}">`}</label>`;}).join('')+'</div>';}
return `<div class="entity-card ${e.n?'selected':''} ${ex?'conditions-open':''} ${c.rule==='manual'?'pending':''}"><div class="row card-row"><span class="number">${e.n}</span><button class="add-card" type="button" data-id="${c.id}" data-delta="1" aria-label="Add ${esc(c.name)}"><span class="card-name">${esc(c.name)}</span><span class="rule-note">Smoky Mountains · ${esc(c.summary)}</span></button><button class="remove" type="button" data-id="${c.id}" data-delta="-1" aria-label="Remove ${esc(c.name)}">−</button><span class="score" id="point-${c.id}">${c.rule==='squirrel'?'set':s.result[c.id]}</span></div>${ex}</div>`;}
function sectionHtml(g,p,s){const list=CARDS.filter(c=>c.group===g);let body;
 if(!ORDER[g])body=list.map(c=>cardRow(c,p,s)).join('');
 else{const by={};list.forEach(c=>{(by[TYPECAT[c.type]]=by[TYPECAT[c.type]]||[]).push(c)});const o=ORDER[g].concat(Object.keys(by).filter(k=>!ORDER[g].includes(k)));
  body=o.filter(k=>by[k]).map(k=>`<div class="card-group"><div class="row row-heading"><h3>${ic(CATIC[k]||'other')}${k}</h3></div>${by[k].sort((a,b)=>a.name.localeCompare(b.name)).map(c=>cardRow(c,p,s)).join('')}</div>`).join('');}
 return `<section class="score-section" id="${g}"><div class="row row-heading"><h2>${ic(IK[g])}${TITLE[g]}</h2></div>${g==='Squirrels'?'<p class="hint">All four species score together once. Individual rows show “set”.</p>':''}<div class="column-guide"><span>Qty</span><span>Tap a card to add</span><span>−</span><span>Pts</span></div>${body}<div class="section-total"><span class="section-total-label">${ic(IK[g])}${TITLE[g]} points</span><span class="section-total-number" id="subtotal-${g}">${s.sections[g]}</span></div></section>`;}
function caveHtml(p){return `<section class="score-section" id="Cave"><div class="row row-heading"><h2>${ic('cave')}Cave &amp; global conditions</h2></div><p class="hint">Count only visible card halves. Universal rivers have no visible tree symbol. Symbol quantities below are totals, not additions.</p>${[['cave','Cards stored in cave · 1 point each'],['emptyRivers','Rivers with NO fish below them · Brook Trout condition'],['buckeye','Total visible Buckeye symbols · include Buckeye trees themselves']].map(([k,l])=>`<div class="entity-card"><div class="global"><label for="${k}">${l}</label><button class="remove" type="button" data-global="${k}" data-delta="-1" aria-label="Decrease">−</button><input id="${k}" data-field="${k}" type="number" min="0" max="1000" inputmode="numeric" value="${p[k]}"><button class="remove" type="button" data-global="${k}" data-delta="1" aria-label="Increase">＋</button></div></div>`).join('')}<div class="section-total"><span class="section-total-label">${ic('cave')}Cave points</span><span class="section-total-number" id="caveTotal">${p.cave}</span></div></section>`;}
function renderSummary(){const p=state.players[state.active],s=score(p);
 document.getElementById('total').textContent=s.total;document.getElementById('dashboard-label').textContent=p.name;document.getElementById('bottom-name').textContent=p.name;document.getElementById('bottom-score').textContent=s.total;
 document.getElementById('player-tabs').innerHTML=state.players.map((q,j)=>`<button class="player-tab" type="button" data-player="${j}" aria-pressed="${j===state.active}"><span class="player-tab-name">${esc(q.name)}</span><strong>${score(q).total}</strong></button>`).join('');
 const cnt=g=>CARDS.filter(c=>c.group===g).reduce((n,c)=>n+entry(p,c).n,0);
 document.getElementById('score-overview').innerHTML=GROUPS.map(g=>`<div class="row row-score"><span>${ic(IK[g])}${TITLE[g]}${g==='Squirrels'?'':' (×'+cnt(g)+')'}</span><span>${s.sections[g]}</span></div>`).join('')+`<div class="row row-score"><span>${ic('cave')}Cave</span><span>${p.cave}</span></div>`;
 document.getElementById('overview-total').textContent=s.total;
 document.getElementById('summary').innerHTML=state.players.map((q,j)=>{const t=score(q);return `<tr class="${j===state.active?'active':''}"><td><button type="button" data-player="${j}">${esc(q.name)}</button></td>${GROUPS.map(g=>`<td>${t.sections[g]}</td>`).join('')}<td>${q.cave}</td><td>${t.total}</td></tr>`}).join('');
 const bs=document.getElementById('bg-start'),cur=bs.value;bs.innerHTML='<option value="">Not specified</option>'+state.players.map((q,j)=>`<option value="${j}">${esc(q.name)}</option>`).join('');if(cur!==''&&+cur<state.players.length)bs.value=cur;
 const pn=document.getElementById('player-name');if(document.activeElement!==pn)pn.value=p.name;document.getElementById('remove-player').disabled=state.players.length===1;}
'''
SMOKY_RENDER_MAIN = r'''document.getElementById('main').innerHTML=GROUPS.map(g=>sectionHtml(g,p,s)).join('')+caveHtml(p);
 updateWarnings();renderSummary();save();}'''

SMOKY_JS_TAIL = r'''
document.getElementById('player-tabs').onclick=e=>{const b=e.target.closest('[data-player]');if(b){state.active=+b.dataset.player;render();}};
document.getElementById('summary').addEventListener('click',e=>{const b=e.target.closest('button[data-player]');if(b){state.active=+b.dataset.player;render();setTimeout(()=>document.getElementById('player-management').scrollIntoView({behavior:'smooth'}),50);}});
document.getElementById('player-name').oninput=e=>{state.players[state.active].name=e.target.value.slice(0,60);render();};
document.getElementById('remove-player').onclick=()=>{if(state.players.length>1&&confirm('Remove this player and their forest?')){state.players.splice(state.active,1);state.active=Math.max(0,Math.min(state.active,state.players.length-1));render();}};
let playId=(window.crypto&&crypto.randomUUID)?crypto.randomUUID():String(Date.now())+Math.random();
(function(){const d=new Date();document.getElementById('date').value=new Date(d-d.getTimezoneOffset()*60000).toISOString().slice(0,16);})();
function bgPayload(){if(!document.getElementById('review').checked)throw Error('Review counts, symbols and placements, then tick the review checkbox.');const names=state.players.map(q=>q.name.trim().normalize('NFC').toLowerCase());if(names.some(n=>!n)||new Set(names).size!==names.length)throw Error('Use unique, non-empty player names.');const d=new Date(document.getElementById('date').value);if(!Number.isFinite(d.getTime()))throw Error('Choose a valid play date.');const sc=state.players.map(q=>score(q).total),hi=Math.max(...sc),start=document.getElementById('bg-start').value,loc=document.getElementById('location').value.trim(),dur=document.getElementById('duration').value;
 const data={sourceName:'Smoky Mountains Forest Score Companion',sourcePlayId:playId,playDate:d.toISOString().slice(0,19).replace('T',' '),game:{name:'Forest Shuffle: Smoky Mountains',sourceGameId:'forest-shuffle-smoky-mountains',highestWins:true,noPoints:false},players:state.players.map((q,i)=>({name:q.name.trim(),sourcePlayerId:'name:'+names[i],score:sc[i],rank:1+sc.filter(x=>x>sc[i]).length,winner:state.players.length===1?document.getElementById('soloWin').checked:sc[i]===hi,startPlayer:start===String(i)}))};
 if(loc)data.location=loc;if(dur!=='')data.durationMin=Number(dur);return data;}
const bgLink=d=>'https://app.bgstatsapp.com/createPlay.html?data='+encodeURIComponent(JSON.stringify(d));
document.getElementById('send').onclick=()=>{try{const data=bgPayload();if(confirm('Open BG Stats with:\n'+data.players.map(q=>q.name+': '+q.score).join('\n')))location.href=bgLink(data);}catch(e){alert(e.message);}};
document.getElementById('copy').onclick=async()=>{try{const url=bgLink(bgPayload());try{await navigator.clipboard.writeText(url);alert('Import link copied');}catch(e){prompt('Copy import link',url);}}catch(e){alert(e.message);}};
document.getElementById('new-game').onclick=()=>{if(confirm('Clear all forests and start a new play?')){state.players=state.players.map(q=>fresh(q.name));state.active=0;playId=(window.crypto&&crypto.randomUUID)?crypto.randomUUID():String(Date.now())+Math.random();document.getElementById('review').checked=false;render();}};
let showRules=true;try{showRules=localStorage.getItem(KEY+'-rules')!=='off';}catch(e){}
function syncRules(){document.documentElement.classList.toggle('rules-hidden',!showRules);document.documentElement.dataset.rules=showRules?'on':'off';document.getElementById('rules-toggle').setAttribute('aria-pressed',String(showRules));}
document.getElementById('rules-toggle').onclick=()=>{showRules=!showRules;try{localStorage.setItem(KEY+'-rules',showRules?'on':'off');}catch(e){}syncRules();};syncRules();
'''

def build_smoky(s, forest_style_src, moor_src):
    # --- script (original logic, patched)
    scripts=[m for m in re.finditer(r'<script[^>]*>(.*?)</script>',s,re.S)]
    js=scripts[0].group(1);extra_js=scripts[-1].group(0)   # [0]=app logic, last=build2 helper (rules/theme/norm)
    js=once(js,"document.getElementById('addPlayer').onclick=()=>{if(state.players.length>=5)return alert('Maximum 5 players.');const name=prompt('Player name',`Player ${state.players.length+1}`);if(name!==null){state.players.push(fresh(name.trim()||'Player'));state.active=state.players.length-1;render();}};",
      "document.getElementById('addPlayer').onclick=()=>{if(state.players.length>=5)return;state.players.push(fresh('Player '+(state.players.length+1)));state.active=state.players.length-1;render();const pm=document.getElementById('player-management'),pn=document.getElementById('player-name');if(pm)pm.scrollIntoView({behavior:'smooth'});if(pn){pn.focus({preventScroll:true});pn.select();}};",'s addplayer')
    js=once(js,"warnings').textContent=warnings.join(' ')","warnings').textContent=warnings.join(' · ')",'warnjoin')
    js=once(js,"const GROUPS=['Trees','Rivers','Top','Sides','Bottom','Squirrels'];","const GROUPS=['Trees','Rivers','Top','Bottom','Sides','Squirrels'];",'s groups')
    # render(): drop select + old total; swap the whole main/summary block
    js=sub1(js,r"document\.getElementById\('players'\)\.innerHTML=.*?\.join\(''\);\n","",'s players sel')
    js=sub1(js,r"document\.getElementById\('total'\)\.textContent=s\.total;\n document\.getElementById\('counts'\)","document.getElementById('counts')",'s total1')
    js=sub1(js,r"document\.getElementById\('main'\)\.innerHTML=GROUPS\.map.*?\n updateWarnings\(\);document\.getElementById\('summary'\)\.innerHTML=.*?\.join\(''\);save\(\);\}",lambda m:SMOKY_RENDER_MAIN,'s main')
    js=sub1(js,r"document\.getElementById\('caveTotal'\)\.textContent=p\.cave;document\.getElementById\('summary'\)\.innerHTML=.*?\.join\(''\);updateWarnings\(\);save\(\);\}",lambda m:"document.getElementById('caveTotal').textContent=p.cave;renderSummary();updateWarnings();save();}",'s refresh')
    js=js.replace("function updateWarnings()",SMOKY_JS_NEW+"function updateWarnings()",1)
    # old handlers for removed elements
    js=sub1(js,r"document\.getElementById\('players'\)\.onchange=.*?\n","",'s onchange')
    js=sub1(js,r"document\.getElementById\('rename'\)\.onclick=.*?\n","",'s rename')
    js=sub1(js,r"document\.getElementById\('export'\)\.onclick=.*?\n","",'s export')
    js=sub1(js,r"document\.getElementById\('reset'\)\.onclick=.*?\n",lambda m:'','s reset')
    js=re.sub(r"\nrender\(\);\s*$",lambda m:"\n"+SMOKY_JS_TAIL+"\nrender();\n",js)
    assert 'new-game' in js
    # --- page parts to keep
    audit=re.search(r'<details><summary>Scoring audit and limitations</summary>.*?</details>',s,re.S).group(0)
    foot=re.search(r'<footer>(.*?)</footer>',s,re.S).group(1)
    notice='English scoring preview · Tap a card name to add a copy; use − to remove. Amber-marked entries require manual points until their formulas are verified. This version does not validate legal forest placement.'
    # --- style: Forest's stylesheet (so everything is laid out identically) with Smoky's own hero image
    st=re.search(r'<style>(.*?)</style>',forest_style_src,re.S).group(1)
    smoky_img=re.search(r':root\{--hero-img:url\([^)]*\)\}',s).group(0)
    st=sub1(st,r':root\{--hero-img:url\([^)]*\)\}',lambda m:smoky_img,'s style img')
    st+='''
.entity-card.pending{border-left:4px solid #b7822c}
.entity-card .global{display:grid;grid-template-columns:minmax(0,1fr) 44px 76px 44px;gap:8px;align-items:center;padding:10px 12px}
.entity-card .global label{font-size:16px;line-height:1.4}
.entity-card .global input{min-height:44px;text-align:center;box-sizing:border-box;font:400 16px system-ui,sans-serif;color:var(--ink);background:var(--soft);border:1px solid var(--line);border-radius:5px}
.entity-card .global button.remove{width:100%;min-height:44px;font-size:22px;color:var(--accent)}
.conditions .option-label input[type=number]{width:84px;min-height:40px;margin-left:8px;box-sizing:border-box;font:400 16px system-ui,sans-serif;background:var(--soft);border:1px solid var(--line);border-radius:5px;color:var(--ink);padding:4px 8px}
#warnings{color:var(--warn,#805213);font-size:15px}
'''
    head=s[:s.index('<style>')]
    head=head.replace('<meta name="viewport" content="width=device-width,initial-scale=1">','<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">')
    sprite=re.search(r'<svg aria-hidden="true" height="0" style="position:absolute;overflow:hidden" width="0"[^>]*>.*?</svg>',moor_src,re.S);assert sprite
    hero=('<header class="hero"><div class="hero-copy"><div class="eyebrow">FOREST SHUFFLE · SMOKY MOUNTAINS</div><h1>Mist over<br/>the ridgeline.</h1><p>Count your cards, mark their conditions, and gather every player\'s score.</p></div>'
      '<div class="hero-score"><span>ACTIVE FOREST</span><strong><output id="total">0</output></strong><div id="dashboard-label"></div><small>points</small></div>'
      '<div class="hero-settings"><div class="view-controls">'+LANG_SELECT+'<button aria-pressed="true" id="rules-toggle" type="button">Rules</button><button aria-pressed="false" class="switch" id="theme" type="button">Dark mode</button></div>'+SESSION.replace('<small id="status" role="status">','<small id="saveState" role="status">')+'</div></header>')
    nav=nav_html([('Trees','Trees','trees'),('Rivers','Rivers','rivers'),('Top','Tops','tops'),('Bottom','Bottoms','bottoms'),('Sides','Sides','sides'),('Squirrels','Squirrels','squirrels'),('Cave','Cave','cave'),('section-summary','Summary','summary'),('section-bgstats','All scores / BG Stats','allscores')])
    sticky=('<div class="sticky-controls" id="sticky-controls"><div class="sticky-content"><div class="player-bar"><div class="player-bar-title"><span>PLAYERS</span><button class="compact-add" id="addPlayer" type="button">＋ Add</button></div>'
      '<div aria-label="Choose a player\'s forest" id="player-tabs" role="group"></div></div>'+nav+'</div></div>')
    settings=('<section class="score-section" id="player-management"><div class="panel-heading"><h2>'+IC('players')+'Forest settings</h2><span class="section-tag">ACTIVE PLAYER</span></div>'
      '<div class="player-settings"><label>Player name<input autocomplete="off" id="player-name" maxlength="60" placeholder="Player name"/></label><button class="switch danger" id="remove-player" type="button">Remove player</button></div>'
      '<p class="hint">Tap a card to add it. Mark conditions per copy; use − and + for symbol totals. The small scoring notes update with your forest.</p>'
      f'<p class="notice">{notice}</p><p class="hint" id="counts"></p><p id="warnings" role="status"></p></section>')
    body=('<body>'+(sprite.group(0) if sprite else '')+EXTRA_SPRITE+hero+sticky+'<main id="calculator">'+settings+'<div id="main"></div>'
      +summary_section()+'\n'+bg_section([('Player','players')]+[(l,i) for l,i in [('Trees','trees'),('Rivers','rivers'),('Tops','tops'),('Bottoms','bottoms'),('Sides','sides'),('Squirrels','squirrels')]]+[('Cave','cave'),('Total','summary')])
      +'</main><footer><p>'+foot+'</p>'+audit+'</footer><div id="bottom-pane"><span id="bottom-name">Player 1</span><span><strong id="bottom-score">0</strong> points</span></div>')
    return head+'<style>'+st+'</style></head>'+body+'<script>'+js+'</script>'+extra_js+'</body></html>'
