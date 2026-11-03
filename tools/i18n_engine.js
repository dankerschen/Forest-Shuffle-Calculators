(function(){
var D=/*DATA*/null;
var IDX={en:-1,fr:0,de:1},L='en',MOOR=!!document.getElementById('language-select')&&typeof window.applyLanguage==='function';
var SKIP={SCRIPT:1,STYLE:1,TEXTAREA:1,NOSCRIPT:1};
var tOrig=new WeakMap(),tLast=new WeakMap(),aOrig=new WeakMap();
var ATTRS=['aria-label','placeholder','title','alt'];
function norm(s){return s.replace(/\s+/g,' ').trim()}
function pick(v){return v?v[IDX[L]]:null}
function ex(s){var v=D.x[s];return v?v[IDX[L]]:null}
function t(s){var r=T(s);return r==null?s:r}
function pl(n,one,many){return +n===1?one:many}
var R=[
 [/^(Base|Alpine|Woodland Edge|Exploration|Smoky Mountains) · (.+)$/,function(m){return t(m[1])+' · '+t(m[2])}],
 [/^(\d+) points per copy$/,function(m){return L==='fr'?m[1]+' '+pl(m[1],'point','points')+' par exemplaire':m[1]+' '+pl(m[1],'Punkt','Punkte')+' pro Karte'}],
 [/^(\d+) points per qualifying copy$/,function(m){return L==='fr'?m[1]+' '+pl(m[1],'point','points')+' par exemplaire éligible':m[1]+' '+pl(m[1],'Punkt','Punkte')+' pro qualifizierter Karte'}],
 [/^(\d+) × (\w+) cards per copy$/,function(m){var k=D.kind[m[2]];if(!k)return null;return m[1]+' × '+k[IDX[L]]+(L==='fr'?' par exemplaire':' pro Karte')}],
 [/^(\d+) × (.+) symbols per copy$/,function(m){return m[1]+' × '+(L==='fr'?'icônes ':'Symbole ')+t(m[2])+(L==='fr'?' par exemplaire':' pro Karte')}],
 [/^(.+) symbols$/,function(m){var n=ex(m[1]);if(!n)return null;return (L==='fr'?'Icônes ':'Symbole ')+n}],
 [/^(.+) \(×(\d+)\)$/,function(m){var a=T(m[1]);return a==null?null:a+' (×'+m[2]+')'}],
 [/^Add (.+)$/,function(m){var n=T(m[1]);if(n==null)return null;return L==='fr'?'Ajouter '+n:n+' hinzufügen'}],
 [/^Remove (.+)$/,function(m){var n=T(m[1]);if(n==null)return null;return L==='fr'?'Retirer '+n:n+' entfernen'}],
 [/^(.+) — (.+)$/,function(m){var a=T(m[1]),b=T(m[2]);return a==null&&b==null?null:t(m[1])+' — '+t(m[2])}],
 [/^Copy (\d+)$/,function(m){return (L==='fr'?'Exemplaire ':'Karte ')+m[1]}],
 [/^(\d+) (actual trees|real species|deer|hoofed animals)$/,function(m){return m[1]+' '+D.cw[m[2]][IDX[L]]}],
 [/^(fish|insect|amphibian|bird|mouse|paw|tree|river): (\d+)$/,function(m){return D.cw[m[1]][IDX[L]]+' : '+m[2]}],
 [/^#(\d+) (.+)$/,function(m){var r=T(m[2]);return r==null?null:'#'+m[1]+' '+r}],
 [/^Tree #(\d+): attached cards$/,function(m){return L==='fr'?'Arbre n° '+m[1]+' : cartes rattachées':'Baum Nr. '+m[1]+': angelegte Karten'}],
 [/^Bee #(\d+) host$/,function(m){return L==='fr'?'Hôte de l’abeille n° '+m[1]:'Wirt der Biene Nr. '+m[1]}],
 [/^Manual formulas pending verification: (.+)$/,function(m){var l=m[1].split(', ').map(t).join(', ');return (L==='fr'?'Formules manuelles à vérifier : ':'Manuelle Formeln noch zu prüfen: ')+l}],
 [/^(.+) \($/,function(m){var r=T(m[1]);return r==null?null:r+' ('}],
 [/^(.+), (\d+) points$/,function(m){var n=t(m[1]);return n+', '+m[2]+(L==='fr'?' points':' Punkte')}],
 [/^(.+) \((DP\d+)\)$/,function(m){var r=T(m[1]);return r==null?null:r+' ('+m[2]+')'}],
 [/^Total: (\d+)$/,function(m){return (L==='fr'?'Total : ':'Gesamt: ')+m[1]}]
];
function T(s){
 if(!s||!/[A-Za-z]/.test(s))return null;
 var v=ex(s);if(v!=null&&v!==s)return v;if(v!=null)return null;
 for(var i=0;i<R.length;i++){var m=R[i][0].exec(s);if(m){var r=R[i][1](m);if(r!=null)return r}}
 if(s.length>40){var o2=s,c2=false;for(var q=0;q<D.sub.length;q++){var e=D.sub[q];if(o2.indexOf(e[0])>=0){o2=o2.split(e[0]).join(e[1][IDX[L]]);c2=true}}if(c2)return o2}
 if(s.indexOf(' · ')>0){var p=s.split(' · '),ch=false,o=p.map(function(x){var r=T(x);if(r!=null){ch=true;return r}return x});if(ch)return o.join(' · ')}
 return null}
function own(el){return MOOR&&el&&el.closest&&el.closest('#session-status,#bg-status')}
function xt(n){ // text node
 if(own(n.parentNode))return;
 var cur=n.nodeValue;if(tLast.get(n)===cur)return; // our own write
 var orig=cur;tOrig.set(n,orig);
 if(L==='en'){tLast.delete(n);return}
 var lead=orig.match(/^\s*/)[0],trail=orig.match(/\s*$/)[0],k=norm(orig);var r=T(k);
 if(r!=null&&r!==k){var nv=lead+r+trail;tLast.set(n,nv);n.nodeValue=nv}
}
function retextAll(n){ // after language change: redo from stored originals
 var cur=n.nodeValue,o=tOrig.get(n);
 if(o!=null&&tLast.get(n)===cur)n.nodeValue=o;
 tLast.delete(n);tOrig.delete(n);xt(n)}
function xa(el){
 if(own(el))return;
 var rec=aOrig.get(el);if(!rec){rec={};aOrig.set(el,rec)}
 for(var i=0;i<ATTRS.length;i++){var a=ATTRS[i];if(!el.hasAttribute(a))continue;var cur=el.getAttribute(a),r=rec[a];
  if(r&&r.last===cur){if(L==='en'){if(cur!==r.orig){el.setAttribute(a,r.orig)}r.last=r.orig}else{var k=norm(r.orig),tt=T(k);var nv=tt!=null&&tt!==k?tt:r.orig;if(nv!==cur){r.last=nv;el.setAttribute(a,nv)}}continue}
  rec[a]={orig:cur,last:cur};if(L==='en')continue;var k2=norm(cur),t2=T(k2);if(t2!=null&&t2!==k2){rec[a].last=t2;el.setAttribute(a,t2)}}
}
function walk(root,redo){
 if(root.nodeType===3){if(!root.parentNode||!SKIP[root.parentNode.nodeName]){redo?retextAll(root):xt(root)}return}
 if(root.nodeType!==1||SKIP[root.nodeName])return;
 var w=document.createTreeWalker(root,NodeFilter.SHOW_ELEMENT|NodeFilter.SHOW_TEXT,{acceptNode:function(n){return n.nodeType===1&&SKIP[n.nodeName]?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT}});
 var n=root;if(n.nodeType===1)xa(n);
 while(n=w.nextNode()){if(n.nodeType===3){redo?retextAll(n):xt(n)}else xa(n)}
}
var busy=false;
var mo=new MutationObserver(function(recs){
 for(var i=0;i<recs.length;i++){var r=recs[i];
  if(r.type==='characterData'){var p=r.target.parentNode;if(p&&!SKIP[p.nodeName])xt(r.target)}
  else if(r.type==='attributes'){xa(r.target)}
  else for(var j=0;j<r.addedNodes.length;j++)walk(r.addedNodes[j])}
});
function start(){mo.observe(document.documentElement,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:ATTRS})}
function dlg(m){if(L==='en'||typeof m!=='string')return m;return m.split('\n').map(function(l){var k=norm(l),r=T(k)||dlgRe(k);return r!=null?r:l}).join('\n')}
function dlgRe(k){var d=D.dlg;for(var i=0;i<d.length;i++){var m=new RegExp(d[i][0]).exec(k);if(m){var s=d[i][1][IDX[L]];return s.replace(/\$(\d)/g,function(_,x){return m[+x]})}}return null}
['alert','confirm','prompt'].forEach(function(f){var o=window[f];window[f]=function(a,b){return o.call(window,dlg(a),b)}});
var DEFW={en:'Player ',fr:'Joueur ',de:'Person '},DEFRE=/^(?:Player|Joueur|Person) (\d+)$/;
function defName(n){return (DEFW[L]||DEFW.en)+n}
function renameDefaults(){var h=window.__fsPlayers;if(!h)return;try{var ps=h.list()||[],ch=false;
 for(var i=0;i<ps.length;i++){var m=DEFRE.exec(ps[i].name||'');if(m){var nn=defName(m[1]);if(nn!==ps[i].name){ps[i].name=nn;ch=true}}}
 if(ch)h.commit()}catch(e){}}
function setLang(l,user){
 if(!(l in IDX))return;var ch=l!==L;L=l;
 document.documentElement.lang=l;
 var sel=document.getElementById('language-select');
 if(MOOR){try{localStorage.setItem('dartmoor-language',l)}catch(e){}}
 if(sel&&sel.value!==l){sel.value=l;if(MOOR&&document.readyState!=='loading')sel.dispatchEvent(new Event('change',{bubbles:true}))}
 try{localStorage.setItem('fs-lang',l)}catch(e){}
 var nt=document.getElementById('lang-note');if(nt)nt.textContent=l.toUpperCase();
 if(ch)renameDefaults();
 if(ch||user){mo.disconnect();walk(document.body,true);var ti=D.title;if(ti){document.title=(l==='en')?ti.en:ti[l]}start()}
 if(user){try{parent.postMessage({fsLang:l},'*')}catch(e){}}
}
addEventListener('message',function(e){if(e.source!==parent)return;var d=e.data;if(d&&d.fsLang)setLang(d.fsLang,false)});
var sel=document.getElementById('language-select');
if(sel)sel.addEventListener('change',function(){if(sel.value!==L)setLang(sel.value,true)});
var init='en';try{init=localStorage.getItem('fs-lang')||''}catch(e){}
if(!(init in IDX)){var nl=(navigator.language||'en').slice(0,2).toLowerCase();init=nl in IDX?nl:'en'}
window.__fsT=function(s){return dlg(s)};window.__fsDefName=defName;window.__fsLang=function(){return L};
start();setLang(init,false);
if(MOOR&&document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){var l=L;L='';setLang(l,false)});
if(init==='en'&&sel)sel.value='en';
})();
