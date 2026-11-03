# -*- coding: utf-8 -*-
# UI / chrome strings shared by all three games.  EN is the key.  Each value = (FR, DE).
import json
_M = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'moor_i18n.json'), encoding='utf-8'))['UI']

UI = {}
# 1) seed from Dartmoor's own (MIT) FR / DE tables so the three games speak the same way
for k, v in _M['fr'].items():
    UI[k] = (v, _M['de'].get(k, k))

def add(en, fr, de):
    UI[en] = (fr, de)

# --- hero ---------------------------------------------------------------------------
add('Forest', 'Forêt', 'Wald')
add('Dartmoor', 'Dartmoor', 'Dartmoor')
add('Smoky', 'Smoky', 'Smoky')
add('Mountains', 'Mountains', 'Mountains')
add('Choose game', 'Choisir le jeu', 'Spiel wählen')
add('FOREST SHUFFLE · BASE GAME', 'FORÊT MIXTE · JEU DE BASE', 'MISCHWALD · GRUNDSPIEL')
add('FOREST SHUFFLE · SMOKY MOUNTAINS', 'FORÊT MIXTE · SMOKY MOUNTAINS', 'MISCHWALD · SMOKY MOUNTAINS')
add('Into the', 'Au cœur de la', 'Mitten im')
add('deep forest.', 'forêt profonde.', 'tiefen Wald.')
add('Across the', 'À travers la', 'Über das')
add('open moor.', 'lande ouverte.', 'offene Moor.')
add('Mist over', 'Brume sur', 'Nebel über')
add('the ridgeline.', 'la ligne de crête.', 'dem Bergkamm.')
add('Rules', 'Règles', 'Regeln')
add('Back to top', 'Haut de page', 'Nach oben')
add('Dark mode', 'Mode sombre', 'Dunkelmodus')
add('Expansion(s)', 'Extension(s)', 'Erweiterung(en)')
add('Alpine cards', 'Cartes Alpin', 'Alpin-Karten')
add('Woodland Edge cards', 'Cartes Lisière', 'Waldrand-Karten')
add('Exploration cards', 'Cartes Exploration', 'Exploration-Karten')
add('Exmoor cards', 'Cartes Exmoor', 'Exmoor-Karten')
add('ACTIVE FOREST', 'FORÊT ACTIVE', 'AKTIVER WALD')
add('POINTS', 'POINTS', 'PUNKTE')
add('points', 'points', 'Punkte')
add('Language', 'Langue', 'Sprache')
add('Session saved on this device.', 'Session enregistrée sur cet appareil.', 'Sitzung auf diesem Gerät gespeichert.')
add('Saved on this browser', 'Enregistré dans ce navigateur', 'In diesem Browser gespeichert')
add('Session tools & backup', 'Session et sauvegarde', 'Sitzung und Sicherung')

# --- player bar / settings ----------------------------------------------------------
add('PLAYERS', 'JOUEURS', 'SPIELENDE')
add('＋ Add', '＋ Ajouter', '＋ Neu')
add('Player 1', 'Joueur 1', 'Person 1')
add('Player 2', 'Joueur 2', 'Person 2')
add('Player 3', 'Joueur 3', 'Person 3')
add('Player 4', 'Joueur 4', 'Person 4')
add('Player 5', 'Joueur 5', 'Person 5')
add('Player name', 'Nom du joueur', 'Spielername')
add('Find a card…', 'Chercher une carte…', 'Karte suchen…')
add('Home', 'Domicile', 'Zuhause')
add("Choose a player's forest", 'Choisir la forêt d’un joueur', 'Wald einer Person wählen')
add('Scoring categories', 'Catégories de score', 'Wertungskategorien')
add('Increase', 'Augmenter', 'Erhöhen')
add('Decrease', 'Diminuer', 'Verringern')
add('Exploration solo thresholds', 'Seuils solo Exploration', 'Exploration: Solo-Schwellen')
add('Expansion visibility is controlled in the title panel. Hidden cards keep their quantities and continue to score; all-player totals always include them.',
    'La visibilité des extensions se règle dans le bandeau du titre. Les cartes masquées conservent leurs quantités et continuent de compter ; les totaux de tous les joueurs les incluent toujours.',
    'Die Sichtbarkeit der Erweiterungen wird im Titelbereich eingestellt. Ausgeblendete Karten behalten ihre Anzahl und zählen weiter; die Gesamtwerte aller Personen enthalten sie immer.')
add('Entering a forest', 'Saisir une forêt', 'Einen Wald eingeben')
add('Count visible halves only. Mark qualifying copies, fully occupied trees, and bee hosts. For Wood Ant, mark every bottom card attached to a tree. Silver Fir uses the number of attached cards, not occupied slots. Mistletoe turns its host into a Sapling: remove the original tree from the entered counts.',
    'Ne comptez que les moitiés visibles. Cochez les exemplaires éligibles, les arbres entièrement occupés et les hôtes des abeilles. Pour la Fourmi rousse, cochez chaque carte du bas rattachée à un arbre. Le Sapin blanc compte le nombre de cartes rattachées, pas les emplacements occupés. Le Gui transforme son hôte en Jeune pousse : retirez l’arbre d’origine des quantités saisies.',
    'Nur sichtbare Kartenhälften zählen. Markiere qualifizierte Karten, vollständig belegte Bäume und Bienenwirte. Bei der Waldameise markierst du jede untere Karte, die an einem Baum liegt. Die Tanne zählt die Anzahl angelegter Karten, nicht die belegten Plätze. Die Mistel macht ihren Wirt zum Setzling: Nimm den ursprünglichen Baum aus den eingegebenen Mengen heraus.')
add('Symbol totals below must be entered manually, including matching dwellers. This quantity-based page does not reconstruct physical placement or enforce every placement rule.',
    'Les totaux d’icônes ci-dessous doivent être saisis à la main, y compris les habitants correspondants. Cette page fonctionne par quantités : elle ne reconstitue pas la disposition réelle et ne contrôle pas toutes les règles de placement.',
    'Die Symbolsummen unten müssen von Hand eingegeben werden, einschließlich passender Bewohner. Diese mengenbasierte Seite bildet die tatsächliche Platzierung nicht nach und prüft nicht jede Platzierungsregel.')

# --- sections / headings ------------------------------------------------------------
add('Trees', 'Arbres', 'Bäume')
add('Rivers', 'Rivières', 'Flüsse')
add('Squirrels', 'Écureuils', 'Hörnchen')
add('Fish', 'Poissons', 'Fische')
add('Mice and shrews', 'Souris et musaraignes', 'Mäuse und Spitzmäuse')
add('Mushrooms', 'Champignons', 'Pilze')
add('Qty', 'Qté', 'Anz.')
add('Tap a card to add', 'Touchez une carte pour l’ajouter', 'Karte antippen zum Hinzufügen')
add('Pts', 'Pts', 'Pkt.')
add('Trees and shrubs points', 'Arbres et arbustes — points', 'Bäume und Sträucher — Punkte')
add('Rivers points', 'Rivières — points', 'Flüsse — Punkte')
add('Squirrels points', 'Écureuils — points', 'Hörnchen — Punkte')
add('Trees points', 'Arbres — points', 'Bäume — Punkte')
add('Cave & global conditions', 'Grotte et conditions globales', 'Höhle und globale Bedingungen')
add('Visible symbols & expansion markers', 'Icônes visibles et marqueurs d’extension', 'Sichtbare Symbole und Erweiterungsmarker')
add('Count printed symbols on all visible cards in your forest, including the scored card itself. Ignore hidden halves, cards in your cave and saplings. Do not add virtual symbols for Violet Carpenter Bees.',
    'Comptez les icônes imprimées sur toutes les cartes visibles de votre forêt, y compris la carte évaluée. Ignorez les moitiés cachées, les cartes de votre grotte et les jeunes pousses. N’ajoutez pas d’icônes virtuelles pour les Xylocopes violets.',
    'Zähle die aufgedruckten Symbole auf allen sichtbaren Karten deines Waldes, auch auf der gewerteten Karte selbst. Verdeckte Hälften, Karten in deiner Höhle und Setzlinge zählen nicht. Für Holzbienen werden keine virtuellen Symbole addiert.')
add('Mixed printing / expansion-marker adjustments', 'Impressions mixtes / ajustements des marqueurs d’extension', 'Gemischte Drucke / Anpassung der Erweiterungsmarker')
add('Some familiar species have additional expansion-marked printings. Adjust the automatically counted marker totals here when your actual visible symbols differ. Positive values add markers; negative values subtract them. These adjustments affect Stone Pine and European Wildcat, not tree species.',
    'Certaines espèces connues existent aussi avec un marqueur d’extension. Corrigez ici les totaux de marqueurs comptés automatiquement si vos icônes visibles diffèrent. Les valeurs positives ajoutent des marqueurs, les valeurs négatives en retirent. Ces ajustements concernent le Pin cembro et le Chat sauvage, pas les essences d’arbres.',
    'Manche bekannte Arten gibt es auch mit Erweiterungsmarker. Passe hier die automatisch gezählten Markersummen an, wenn deine sichtbaren Symbole abweichen. Positive Werte fügen Marker hinzu, negative ziehen sie ab. Diese Anpassungen betreffen Zirbelkiefer und Wildkatze, nicht die Baumarten.')
add('Alpine marker adjustment', 'Ajustement du marqueur Alpin', 'Anpassung Alpin-Marker')
add('Woodland Edge marker adjustment', 'Ajustement du marqueur Lisière', 'Anpassung Waldrand-Marker')
add('Cave type', 'Type de grotte', 'Höhlentyp')
add('Regular', 'Normale', 'Normal')
add('Collectors', 'Collectionneurs', 'Sammler')
add('Bat', 'Chauve-souris', 'Fledermaus')
add('Lonely', 'Solitaire', 'Einsam')
add('Storage', 'Entrepôt', 'Lager')
add('Smugglers', 'Contrebandiers', 'Schmuggler')
add('Stored cards', 'Cartes stockées', 'Gelagerte Karten')
add('Bearded Vultures score the stored card count separately. Collectors’ Cave doubles only the cave’s own points.',
    'Les Gypaètes barbus comptent séparément le nombre de cartes stockées. La grotte des Collectionneurs ne double que les points de la grotte elle-même.',
    'Bartgeier werten die Anzahl gelagerter Karten getrennt. Die Sammlerhöhle verdoppelt nur die Punkte der Höhle selbst.')
add('Cards stored in cave · 1 point each', 'Cartes stockées dans la grotte · 1 point chacune', 'In der Höhle gelagerte Karten · je 1 Punkt')
add('Additional promos / manual correction', 'Promos supplémentaires / correction manuelle', 'Weitere Promos / manuelle Korrektur')
add('This page includes the rules-derived base-game and expansion catalog. Other promos are not certified. Enter independently calculated corrections here, including any dependent scores; a manual adjustment does not add card types or symbols automatically.',
    'Cette page contient le catalogue du jeu de base et des extensions d’après les règles. Les autres promos ne sont pas certifiées. Saisissez ici des corrections calculées séparément, y compris les scores qui en dépendent ; un ajustement manuel n’ajoute pas automatiquement de types de cartes ni d’icônes.',
    'Diese Seite enthält den aus den Regeln abgeleiteten Katalog von Grundspiel und Erweiterungen. Andere Promos sind nicht geprüft. Trage hier separat berechnete Korrekturen ein, auch davon abhängige Wertungen; eine manuelle Anpassung fügt keine Kartentypen oder Symbole automatisch hinzu.')
add('Points adjustment', 'Ajustement de points', 'Punkteanpassung')
add('Explanation', 'Explication', 'Erklärung')
add('Manual', 'Manuel', 'Manuell')
add('BG STATS', 'BG STATS', 'BG STATS')
add('Total Score', 'Score total', 'Gesamtpunktzahl')

# --- smoky specific notes -----------------------------------------------------------
add('English scoring preview · Tap a card name to add a copy; use − to remove. This version does not validate legal forest placement.',
    'Aperçu du score · Touchez le nom d’une carte pour ajouter un exemplaire ; utilisez − pour en retirer. Cette version ne contrôle pas la légalité du placement dans la forêt.',
    'Wertungsvorschau · Tippe auf einen Kartennamen, um ein Exemplar hinzuzufügen; mit − entfernst du eines. Diese Version prüft nicht, ob die Platzierung im Wald zulässig ist.')
add('Smoky Mountains · ', 'Smoky Mountains · ', 'Smoky Mountains · ')
add('Count only visible card halves. Universal rivers have no visible tree symbol. Symbol quantities below are totals, not additions.',
    'Ne comptez que les moitiés de cartes visibles. Les rivières universelles n’ont pas d’icône d’arbre visible. Les quantités d’icônes ci-dessous sont des totaux, pas des ajouts.',
    'Nur sichtbare Kartenhälften zählen. Universelle Flüsse haben kein sichtbares Baumsymbol. Die Symbolmengen unten sind Gesamtwerte, keine Zuschläge.')
add('Total visible Buckeye symbols · include Buckeye trees themselves', 'Total des icônes Marronnier visibles · y compris les arbres Marronnier eux-mêmes', 'Alle sichtbaren Rosskastanien-Symbole · einschließlich der Rosskastanien-Bäume selbst')
add('Rivers with NO fish below them · Brook Trout condition', 'Rivières SANS poisson en dessous · condition de l’Omble de fontaine', 'Flüsse OHNE Fisch darunter · Bedingung des Bachsaiblings')
add('All four species score together once. Individual rows show “set”.', 'Les quatre espèces comptent ensemble une seule fois. Les lignes individuelles affichent « série ».', 'Alle vier Arten werden gemeinsam einmal gewertet. Die einzelnen Zeilen zeigen „Satz“.')
add('set', 'série', 'Satz')
add('Copy 1', 'Exemplaire 1', 'Karte 1')
add('Scoring audit and limitations', 'Contrôle des formules et limites', 'Wertungsprüfung und Einschränkungen')
add('All named and universal rivers count once. Fish below tree-attached rivers count in forest totals. Cave cards score once on the cave and again for each Beaver. Squirrel set points appear once in the Squirrels subtotal. No external libraries, fonts, artwork or remote scripts are required.',
    'Toutes les rivières nommées et universelles comptent une fois. Les poissons sous des rivières rattachées à un arbre comptent dans les totaux de la forêt. Les cartes de la grotte comptent une fois dans la grotte et encore une fois pour chaque Castor. Les points de série des Écureuils apparaissent une seule fois dans le sous-total Écureuils. Aucune bibliothèque, police, illustration ni script externe n’est nécessaire.',
    'Alle benannten und universellen Flüsse zählen einmal. Fische unter an Bäumen liegenden Flüssen zählen für die Waldsumme. Höhlenkarten werden einmal in der Höhle und zusätzlich für jeden Biber gewertet. Die Satzpunkte der Hörnchen erscheinen nur einmal in der Zwischensumme Hörnchen. Es sind keine externen Bibliotheken, Schriften, Bilder oder Skripte nötig.')
add('Basswood and Hickory use per-copy local counts. Opossums use per-copy distinct local symbols. Turkey uses a per-copy matching-symbol count because its variants cannot be identified from extracted icon text. Buckeye uses a forest-wide manually entered visible-symbol total. Rivers without fish require a separate manual count.',
    'Le Tilleul d’Amérique et le Caryer utilisent des comptages locaux par exemplaire. Les Opossums utilisent les icônes locales différentes, par exemplaire. Le Dindon utilise un comptage d’icônes correspondantes par exemplaire, car ses variantes ne peuvent pas être identifiées à partir du texte des icônes. Le Marronnier utilise un total d’icônes visibles saisi à la main pour toute la forêt. Les rivières sans poisson demandent un comptage manuel séparé.',
    'Amerikanische Linde und Hickory nutzen lokale Zählungen pro Karte. Opossums nutzen die verschiedenen lokalen Symbole pro Karte. Der Truthahn nutzt eine Zählung passender Symbole pro Karte, weil sich seine Varianten aus dem Icon-Text nicht unterscheiden lassen. Die Rosskastanie nutzt eine für den ganzen Wald von Hand eingegebene Summe sichtbarer Symbole. Flüsse ohne Fische erfordern eine eigene manuelle Zählung.')
add('Type assignments should be checked against printed symbols; this is a draft card catalog, not a complete symbol-by-symbol audit. Squirrels form their own category, not pawed animals. Common Box Turtle is counted as an amphibian as specified in the appendix example.',
    'Vérifiez les types d’après les icônes imprimées ; il s’agit d’un catalogue provisoire, pas d’un contrôle complet icône par icône. Les Écureuils forment leur propre catégorie, pas celle des plantigrades. La Tortue boîte commune compte comme amphibien, comme indiqué dans l’exemple de l’annexe.',
    'Die Typzuordnung sollte anhand der aufgedruckten Symbole geprüft werden; dies ist ein vorläufiger Katalog, keine vollständige Symbol-für-Symbol-Prüfung. Hörnchen bilden eine eigene Kategorie und gelten nicht als Pfotentiere. Die Carolina-Dosenschildkröte zählt wie im Beispiel des Anhangs als Amphibie.')
SMOKY_LIMIT_EN = 'German card names follow Lookout’s official German appendix; French names are common French species names, because Lookout publishes no French appendix for this game. Browser/device testing remains necessary.'
add(SMOKY_LIMIT_EN,
    'Les noms de cartes allemands suivent l’annexe allemande officielle de Lookout ; les noms français sont des noms usuels d’espèces, car Lookout ne publie pas d’annexe française pour ce jeu. Des tests sur différents navigateurs et appareils restent nécessaires.',
    'Die deutschen Kartennamen folgen dem offiziellen deutschen Anhang von Lookout; die französischen sind gebräuchliche Artnamen, weil Lookout für dieses Spiel keinen französischen Anhang veröffentlicht. Tests mit verschiedenen Browsern und Geräten bleiben nötig.')
add('Formulas follow Lookout’s English appendix and rulebook. The last nine cards (Yellow Birch, White-Footed Mouse, White-Tailed Deer, Wintergreen, Wood Frog, Wood Thrush, Yellow-Bellied Sapsucker, Yellow Bullhead and Yellow Perch) follow Lookout’s German appendix (15.06.2026). No card needs manual points.',
    'Les formules suivent l’annexe et la règle anglaises de Lookout. Les neuf dernières cartes (Bouleau jaune, Souris à pattes blanches, Cerf de Virginie, Gaulthérie couchée, Grenouille des bois, Grive des bois, Pic maculé, Barbotte jaune et Perchaude) suivent l’annexe allemande de Lookout (15.06.2026). Aucune carte ne demande de points manuels.',
    'Die Formeln folgen dem englischen Anhang und der englischen Spielregel von Lookout. Die letzten neun Karten (Gelb-Birke, Weißfußmaus, Weißwedelhirsch, Scheinbeere, Waldfrosch, Walddrossel, Gelbbauch-Saftlecker, Gelber Katzenwels und Amerikanischer Flussbarsch) folgen dem deutschen Anhang von Lookout (15.06.2026). Keine Karte braucht manuelle Punkte.')

# --- BG stats / table results (those not in Dartmoor's table) -------------------------
add('Every forest is included in one play. Tap a player name to revisit their forest.',
    'Toutes les forêts sont incluses dans une seule partie. Touchez le nom d’un joueur pour revoir sa forêt.',
    'Alle Wälder werden in einer Partie erfasst. Tippe auf einen Namen, um den Wald zu öffnen.')
add('I reviewed all counts, symbols, placements, corrections and scores.',
    'J’ai vérifié tous les comptages, icônes, placements, corrections et scores.',
    'Ich habe alle Zählungen, Symbole, Platzierungen, Korrekturen und Wertungen geprüft.')
add('Highest score wins. Tied highest scores are joint winners; adjust a tie-breaker in BG Stats if needed.',
    'Le score le plus élevé gagne. En cas d’égalité en tête, les joueurs gagnent ensemble ; ajustez un départage dans BG Stats si nécessaire.',
    'Die höchste Punktzahl gewinnt. Bei Gleichstand an der Spitze gewinnen die Beteiligten gemeinsam; ein Tie-Break kann bei Bedarf in BG Stats angepasst werden.')

# --- expansions / boxes ---------------------------------------------------------------
BOX = {'Base': ('Base', 'Grundspiel'), 'Alpine': ('Alpin', 'Alpin'), 'Woodland Edge': ('Lisière', 'Waldrand'),
       'Exploration': ('Exploration', 'Exploration'), 'Smoky Mountains': ('Smoky Mountains', 'Smoky Mountains')}

# --- plural helper words used by templates ------------------------------------------------
KIND = {  # "N × <kind> cards per copy"
 'tree': ('cartes Arbre', 'Baumkarten'), 'plant': ('cartes Plante', 'Pflanzenkarten'),
 'paw': ('cartes Plantigrade/Digitigrade', 'Pfotentierkarten'), 'hoof': ('cartes Ongulé', 'Huftierkarten'),
 'deer': ('cartes Cervidé', 'Hirschkarten'), 'bird': ('cartes Oiseau', 'Vogelkarten'),
 'insect': ('cartes Insecte', 'Insektenkarten'), 'amphibian': ('cartes Amphibien', 'Amphibienkarten'),
 'bat': ('cartes Chauve-souris', 'Fledermauskarten'), 'butterfly': ('cartes Papillon', 'Schmetterlingskarten'),
 'hare': ('cartes Lièvre', 'Hasenkarten'), 'alpine': ('cartes Alpin', 'Alpin-Karten'), 'edge': ('cartes Lisière', 'Waldrand-Karten')}

# official French section headings (Forêt Mixte rulebook: "Arbres + En haut + En bas + Côtés + Grotte")
for _en,_fr in [('Tops','En haut'),('Bottoms','En bas'),('Sides','Côtés'),('Top','En haut'),('Bottom','En bas'),('Tops points','En haut — points'),('Bottoms points','En bas — points'),('Sides points','Côtés — points')]:
    UI[_en]=(_fr,UI[_en][1] if _en in UI else {'Top':'Oben','Bottom':'Unten'}[_en])
