# Forest Shuffle promo cards (box "Promos"). Forest game only: never reuse these rules for Dartmoor or Smoky.
# Sources: Dan's card photos (seen) and Dan's consolidated promo handover (text only, not seen on a card).
# Promos already in the calculator through Exploration (Brimstone, Marsh Cinquefoil, Elk, Troll, ...) are not repeated.
# Left out on purpose: P003 hare (handover says "fixed 1", conflicts with the base European Hare), P021 Iberian Lynx
# (scale unknown), P009 badger (1 point vs base 2), P002 fourth Fire Salamander (scale unknown), P005a, P019.
import json as _json
PROMO_CARDS = [
 # id, name, group, tags, rule, extra, printed number, source
 ('pamatna_lipa','Memorial Linden (Památná lípa)','trees',['tree'],'lipa','Linden','P018','card'),
 ('lookout_tower','Lookout','trees',['tree'],'boot','','P030','card'),
 ('maple_promo','Maple','trees',['tree'],'maple','Sycamore','P025','card+handover'),
 ('dracula','Dracula','tops',['bat','boot'],'dracula','','P023','card'),
 ('paeonia_peregrina','Paeonia peregrina','bottoms',['plant'],'paeonia','','P023','card'),
 ('little_red_riding_hood','Little Red Riding Hood','sides',['boot'],'mushroom10','','PX25','card'),
 ('big_bad_wolf','Big Bad Wolf','sides',['paw'],'boot5','','PX25','card'),
 ('roseate_spoonbill','Roseate Spoonbill','tops',['bird'],'bird','','P027','card'),
 ('american_alligator','American Alligator','bottoms',['amphibian'],'alligator','','P027','card'),
 ('australian_magpie','Australian Magpie','tops',['bird'],'magpie','','P017','card'),
 ('short_beaked_echidna','Short-Beaked Echidna','bottoms',['paw'],'5','','P017','card'),
 ('hyacinth_macaw','Hyacinth Macaw (Arara-Azul)','tops',['bird'],'7','','P020','card'),
 ('guarana','Guaraná','bottoms',['plant'],'2','','P020','card'),
 ('gibbon','Gibbon','tops',['paw'],'gibbon','','P026','card+handover'),
 ('pitta','Pitta','bottoms',['bird'],'stork','','P026','card+handover'),
 ('durer_bat','Dürer Bat','sides',['bat'],'bats','','P003','handover'),
 ('chinese_hare','Chinese Hare','sides',['paw','hare'],'hare','','P005','handover'),
 ('meeps','Meeps','sides',['paw','edge'],'edge','','P013','handover'),
 ('black_stork','Black Stork','sides',['bird'],'check7','Its tree has no pawed or cloven-hoofed animal','P021','handover'),
 ('sheep_promo','Sheep','sides',['hoof'],'hoof3','','P022','handover'),
 ('robber','Robber','sides',[],'7','','P022','handover'),
 ('cicada','Cicada','tops',['insect'],'check10','A plant is on its tree or shrub','P024','handover'),
 ('red_wood_ant','Red Wood Ant','bottoms',['insect'],'woodant','','P024','handover'),
 ('blue_jay','Blue Jay','tops',['bird'],'3','','P029','handover'),
 ('beaver_promo','Beaver','bottoms',['paw'],'cavecards','','P029','handover'),
]
PROMO_CASES=("case 'lipa':v=n*x.sym('Linden');break;case 'maple':v=n*(x.count('plant')+x.count('shrub'));break;"
 "case 'dracula':v=n*2*(x.count('paw')+x.count('boot'));break;case 'paeonia':v=n*(qty(p,'great_spotted_woodpecker')?10:0);break;"
 "case 'alligator':v=n*(x.count('paw')+x.count('amphibian')+x.count('bird')+x.count('hoof')+x.count('boot'));break;"
 "case 'magpie':v=n*(x.trees<=6?7:0);break;case 'gibbon':v=n*(x.different('plant')>=3?15:5);break;")
PROMO_HINTS=("lipa:'1 × Linden symbols per copy',maple:'Plants + shrubs per copy',dracula:'2 × (pawed animals + boot cards) per copy',"
 "paeonia:'10 each if at least one Great Spotted Woodpecker',alligator:'Pawed, amphibian, bird, hoofed and boot cards per copy',"
 "magpie:'7 each with at most 6 trees',gibbon:'5 each, or 15 with at least 3 different plants',")
TAGRE='(tree|plant|paw|hoof|deer|bird|insect|amphibian|bat|butterfly|hare|alpine|edge)'
def apply_promos(f):
    m=re.search(r'const CARDS=(\[.*?\]);',f,re.S);assert m
    cards=_json.loads(m.group(1));ids={c['id'] for c in cards}
    for cid,name,group,tags,rule,extra,_num,_src in PROMO_CARDS:
        assert cid not in ids,cid
        cards.append({'id':cid,'name':name,'group':group,'tags':tags,'rule':rule,'box':'Promos','extra':extra})
    f=f[:m.start(1)]+_json.dumps(cards,ensure_ascii=False)+f[m.end(1):]
    assert f.count(TAGRE)==2;f=f.replace(TAGRE,TAGRE[:-1]+'|boot|mushroom|shrub)')
    f=once(f,"case 'bee':v=0;break;",PROMO_CASES+"case 'bee':v=0;break;",'promo cases')
    f=once(f,"bee:'No points; choose the host for each bee'",PROMO_HINTS+"bee:'No points; choose the host for each bee'",'promo hints')
    assert f.count("['Alpine','Woodland Edge','Exploration']")==2
    f=f.replace("['Alpine','Woodland Edge','Exploration']","['Alpine','Woodland Edge','Exploration','Promos']")
    return f
