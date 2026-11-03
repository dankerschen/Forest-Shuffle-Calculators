import os;HERE=os.path.dirname(os.path.abspath(__file__))+'/'
exec(open(HERE+'b4_common.py',encoding='utf-8').read())

SESSION='''<details class="session-tools hero-session-tools" id="hero-session-tools"><summary>Session tools &amp; backup</summary><div class="export-actions"><button class="switch" id="backup" type="button">Back up session</button><button class="switch" id="restore-btn" onclick="document.getElementById('restore').click()" type="button">Restore backup</button><button class="switch danger" id="new-game" type="button">New game</button><input accept=".json,application/json" hidden id="restore" type="file"/></div><small id="status" role="status"></small></details>'''

def nav_html(items):
    return '<nav aria-label="Scoring categories" class="category-nav">'+''.join(f'<a href="#{h}">{IC(i)}{l}</a>' for h,l,i in items)+'</nav>'

def bg_section(cols,tbody='summary'):
    ths=''.join(f'<th>{IC(i)}{l}</th>' for l,i in cols)
    return ('<section class="score-section" id="section-bgstats"><div class="panel-heading"><h2>'+IC('allscores')+'The table\'s results</h2><span class="section-tag">BG STATS</span></div>'
     '<p class="hint">Every forest is included in one play. Tap a player name to revisit their forest.</p>'
     f'<div class="table-scroll"><table class="results-table"><thead><tr>{ths}</tr></thead><tbody id="{tbody}"></tbody></table></div>'
     '<div class="field-grid"><label>Play date and time<input id="date" type="datetime-local"/></label><label>Location (optional)<input id="location" maxlength="100" placeholder="Home"/></label>'
     '<label>Duration in minutes (optional)<input id="duration" max="10000" min="0" step="1" type="number"/></label><label>Starting player (optional)<select id="bg-start"><option value="">Not specified</option></select></label></div>'
     '<p><label class="option-label"><input id="soloWin" type="checkbox"/> I won (used only with a single player)</label></p>'
     '<p class="hint">Highest score wins. Tied highest scores are joint winners; adjust a tie-breaker in BG Stats if needed.</p>'
     '<p><label class="option-label"><input id="review" type="checkbox"/> I reviewed all counts, symbols, placements, corrections and scores.</label></p>'
     '<div class="export-actions"><button class="switch primary" id="send" type="button">Send all scores to BG Stats</button><button class="switch" id="copy" type="button">Copy import link</button></div>'
     '<p class="hint">Requires BG Stats. Review and save the play there. A new game creates a new export ID.</p></section>')

def summary_section(extra_rows_js=''):
    return ('<section class="score-section" id="section-summary"><div class="row row-heading"><h2>'+IC('summary')+'Total Score</h2></div>'
     '<div class="score-overview" id="score-overview"></div><div class="row row-total"><span>'+IC('summary')+'Total</span> <span id="overview-total">0</span></div></section>')

def build_forest(f):
    # ---- hero: same structure/spot as Dartmoor
    hero=re.search(r'<header class="hero">.*?</header>',f,re.S).group(0)
    art=re.search(r'<div aria-hidden="true" class="hero-art">.*?</div>(?=<div class="hero-copy">)',hero,re.S).group(0)
    copy=re.search(r'<div class="hero-copy"><div class="eyebrow">.*?</p>',hero,re.S).group(0)+'</div>'
    score=re.search(r'<div class="hero-score">.*?</div></header>',hero,re.S).group(0)[:-len('</header>')]
    settings=('<div class="hero-settings"><div class="view-controls">'+LANG_SELECT+'<button aria-pressed="true" id="rules-toggle" type="button">Rules: On</button><button aria-pressed="false" class="switch" id="theme" type="button">Dark mode: Off</button></div>'
      '<div class="exp-group" id="buttons" role="group" aria-labelledby="exp-label"><span class="exp-label" id="exp-label">Expansion(s)</span><div aria-label="Expansion card visibility" class="hero-expansions" id="boxes" style="display:contents"></div></div>'+SESSION+'</div>')
    f=f.replace(hero,'<header class="hero">'+art+copy+score+settings+'</header>',1)
    # ---- Players & expansions -> "Forest settings" (same layout as Dartmoor / Smoky)
    f=sub1(f,r'<h2>Players &amp; expansions</h2><div class="settings-grid"><label>Active player<input id="player-name" maxlength="100" type="text"/></label><button class="compact-add" id="remove-player">Remove player</button></div><label class="option-label"><input id="solo" type="checkbox"/>Exploration solo thresholds</label><p><small>(.*?)</small></p>',
      lambda m:('<div class="panel-heading"><h2><svg aria-hidden="true" class="category-icon" focusable="false" height="32" viewBox="0 0 64 64" width="32"><use href="#icon-players"></use></svg>Forest settings</h2><span class="section-tag">ACTIVE PLAYER</span></div>'
        '<div class="player-settings"><label>Player name<input autocomplete="off" id="player-name" maxlength="100" placeholder="Player name" type="text"/></label><button class="switch danger" id="remove-player" type="button">Remove player</button></div>'
        '<p class="hint">Tap a card to add it. Mark conditions per copy; use \u2212 and + for symbol totals. The small scoring notes update with your forest.</p>'
        '<label class="option-label solo-option"><input id="solo" type="checkbox"/>Exploration solo thresholds</label>'
        '<p class="hint">'+m.group(1)+'</p>'),'players')
    f=once(f,"document.getElementById('add-player').onclick=()=>{const name=prompt('Player name');if(name?.trim()){state.players.push(player(name.trim().slice(0,100)));state.active=state.players.length-1;update();}};",
      "document.getElementById('add-player').onclick=()=>{state.players.push(player(fsDefName(state.players.length+1)));state.active=state.players.length-1;update();const pm=document.getElementById('player-management'),pn=document.getElementById('player-name');pm.scrollIntoView({behavior:'smooth'});pn.focus({preventScroll:true});pn.select();};",'addplayer')
    # ---- nav
    f=sub1(f,r'<nav aria-label="Scoring categories" class="category-nav">.*?</nav>',
        nav_html([('section-trees','Trees','trees'),('section-tops','Tops','tops'),('section-bottoms','Bottoms','bottoms'),('section-sides','Sides','sides'),('section-cave','Cave','cave'),('section-summary','Summary','summary'),('section-bgstats','All scores / BG Stats','allscores')]),'f nav')
    # ---- Cave heading with icon + icon on its total
    f=once(f,'<h2>Cave</h2><div class="settings-grid">','<div class="row row-heading"><h2>'+IC('cave')+'Cave</h2></div><div class="settings-grid">','f cave h2')
    f=once(f,'<div class="section-total"><span class="section-total-label">Cave points</span>','<div class="section-total"><span class="section-total-label">'+IC('cave')+'Cave points</span>','f cave total')
    # ---- summary -> Total Score + The table's results
    f=sub1(f,r'<section class="score-section" id="section-summary">.*?</section>',
        summary_section()+'\n'+bg_section([('Player','players'),('Trees and shrubs','trees'),('Tops','tops'),('Bottoms','bottoms'),('Sides','sides'),('Cave','cave'),('Manual','other'),('Total','summary')]),'f summary')
    # ---- JS
    # (1) animal category groups
    grp='''const CATN=c=>{const t=c.tags;return t.includes('bat')?'Bats':t.includes('bird')?'Birds':(t.includes('hoof')||t.includes('deer'))?'Hooves':t.includes('amphibian')?'Amphibians (and reptiles)':t.includes('mushroom')?'Mushrooms':t.includes('plant')?'Plants':t.includes('insect')?'Insects':t.includes('paw')?'Paws':'Other';};
const CATI={Bats:'bats',Birds:'birds',Hooves:'hooves','Amphibians (and reptiles)':'amphibians',Mushrooms:'mushrooms',Plants:'plants',Insects:'insects',Paws:'paws',Other:'other'};
const CATO={tops:['Birds','Insects','Paws','Plants'],bottoms:['Amphibians (and reptiles)','Plants','Mushrooms','Paws','Insects'],sides:['Bats','Birds','Paws','Hooves','Insects']};
function groupRows(g,s){const list=CARDS.filter(c=>c.group===g&&state.boxes.includes(c.box)&&(!search||c.name.toLowerCase().includes(search)));if(g==='trees')return list.map(c=>row(c,s)).join('');
const by={};list.forEach(c=>{(by[CATN(c)]=by[CATN(c)]||[]).push(c)});const o=(CATO[g]||[]).concat(Object.keys(by).filter(k=>!(CATO[g]||[]).includes(k)));
return o.filter(k=>by[k]).map(k=>`<div class="card-group"><div class="row row-heading"><h3>${icon(CATI[k])}${k}</h3></div>${by[k].sort((a,b)=>a.name.localeCompare(b.name)).map(c=>row(c,s)).join('')}</div>`).join('');}
'''
    f=once(f,'function render(){',grp+'function render(){','f render hook')
    f=once(f,"${CARDS.filter(c=>c.group===g&&state.boxes.includes(c.box)&&(!search||c.name.toLowerCase().includes(search))).map(c=>row(c,s)).join('')}","${groupRows(g,s)}",'f rows')
    # (2) summary table + overview + start-player select
    f=sub1(f,r"document\.getElementById\('summary'\)\.innerHTML='<table>.*?</tbody></table>';",
r"""document.getElementById('summary').innerHTML=state.players.map((q,i)=>`<tr class="${i===state.active?'active':''}"><td><button type="button" data-player="${i}" data-goto="1">${escape(q.name)}</button></td>${GROUPS.map(g=>`<td>${all[i].groups[g]}</td>`).join('')}<td>${all[i].cave}</td><td>${all[i].manual}</td><td>${all[i].total}</td></tr>`).join('');
{const cnt=g=>CARDS.filter(c=>c.group===g).reduce((n,c)=>n+qty(p(),c.id),0);document.getElementById('score-overview').innerHTML=GROUPS.map(g=>`<div class="row row-score"><span>${icon(g)}${title(g)} (×${cnt(g)})</span><span>${s.groups[g]}</span></div>`).join('')+`<div class="row row-score"><span>${icon('cave')}Cave</span><span>${s.cave}</span></div>`+(s.manual?`<div class="row row-score"><span>${icon('other')}Manual correction</span><span>${s.manual}</span></div>`:'');document.getElementById('overview-total').textContent=s.total;}
{const bs=document.getElementById('bg-start'),cur=bs.value;bs.innerHTML='<option value="">Not specified</option>'+state.players.map((q,i)=>`<option value="${i}">${escape(q.name)}</option>`).join('');if(cur!==''&&+cur<state.players.length)bs.value=cur;}""",'f summary js')
    f=once(f,"startPlayer:i===0","startPlayer:document.getElementById('bg-start').value===String(i)",'f start')
    # (3) clicking a name in the results table also scrolls to the settings
    f=once(f,"document.getElementById('send').onclick=","document.getElementById('summary').addEventListener('click',e=>{if(e.target.closest('[data-goto]')){const pm=document.getElementById('player-management');if(pm)setTimeout(()=>pm.scrollIntoView({behavior:'smooth'}),50)}});document.getElementById('send').onclick=",'f goto')
    f=once(f,"players:[player('Player 1')]","players:[player(fsDefName(1))]",'f fresh name')
    return f
