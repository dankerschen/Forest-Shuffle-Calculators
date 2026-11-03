# -*- coding: utf-8 -*-
import json,sys
sys.path.insert(0,HERE)
from i18n_ui import UI,BOX,KIND
from i18n_names import FOREST,SMOKY,MOOR
from i18n_rules import BODIES,CONDITIONS,WARNINGS,FOOTER
EXTRA={
 'Autosave unavailable. Use a session backup.':('Enregistrement automatique indisponible. Utilisez une sauvegarde de session.','Automatisches Speichern nicht verfügbar. Nutze eine Sitzungssicherung.'),
 'Storage unavailable — use Backup':('Stockage indisponible — utilisez la sauvegarde','Speicher nicht verfügbar — bitte Sicherung nutzen'),
 'Choose a valid play date.':('Choisissez une date de partie valide.','Wähle ein gültiges Spieldatum.'),
 'Review counts, symbols and placements, then tick the review checkbox.':('Vérifiez les comptages, icônes et placements, puis cochez la case de vérification.','Prüfe Zählungen, Symbole und Platzierungen und setze dann das Häkchen.'),
 'Use unique, non-empty player names.':('Utilisez des noms de joueurs uniques et non vides.','Verwende eindeutige, nicht leere Spielernamen.'),
 'Backup too large':('Sauvegarde trop volumineuse','Sicherung zu groß'),
 'This is not an Original calculator backup.':('Ce n’est pas une sauvegarde du calculateur du jeu de base.','Das ist keine Sicherung des Rechners für das Grundspiel.'),
 'Invalid backup':('Sauvegarde non valide','Ungültige Sicherung'),
 'Replace this session with the backup?':('Remplacer cette session par la sauvegarde ?','Diese Sitzung durch die Sicherung ersetzen?'),
 'Clear forests and start a new play?':('Effacer les forêts et commencer une nouvelle partie ?','Wälder löschen und eine neue Partie beginnen?'),
 'Clear all forests and start a new play?':('Effacer toutes les forêts et commencer une nouvelle partie ?','Alle Wälder löschen und eine neue Partie beginnen?'),
 'Open BG Stats with:':('Ouvrir BG Stats avec :','BG Stats öffnen mit:'),
 'Import link copied':('Lien d’importation copié','Importlink kopiert'),
 'Copy import link':('Copier le lien d’importation','Importlink kopieren'),
 'Replace all current player forests with this backup?':('Remplacer toutes les forêts actuelles par cette sauvegarde ?','Alle aktuellen Wälder durch diese Sicherung ersetzen?'),
 'Could not restore: invalid or incompatible backup.':('Restauration impossible : sauvegarde non valide ou incompatible.','Wiederherstellung nicht möglich: ungültige oder inkompatible Sicherung.'),
 'Remove this player and their forest?':('Retirer ce joueur et sa forêt ?','Diese Person und ihren Wald entfernen?'),
 'Maximum 5 players.':('5 joueurs au maximum.','Höchstens 5 Personen.'),
 'Expansion card visibility':('Visibilité des cartes d’extension','Sichtbarkeit der Erweiterungskarten'),
 'Exmoor cards':('Cartes Exmoor','Exmoor-Karten'),
}
EXTRA.update({
 'Official documents (Lookout, PDF).':('Documents officiels (Lookout, PDF).','Offizielle Dokumente (Lookout, PDF).'),
 'Rulebook:':('Règle du jeu :','Spielregel:'),'Appendix:':('Annexe :','Anhang:'),'Play aid:':('Aide de jeu :','Spielhilfe:'),
 '— Appendix:':('— Annexe :','— Anhang:'),'— Play aid:':('— Aide de jeu :','— Spielhilfe:'),
 '(the German appendix also covers the expansions).':('(l’annexe allemande couvre aussi les extensions).','(der deutsche Anhang behandelt auch die Erweiterungen).'),
 'Forest Shuffle — game design: Kosch; illustrations: Toni Llobet and Judit Piella; published by':('Forêt Mixte — conception : Kosch ; illustrations : Toni Llobet et Judit Piella ; édité par','Mischwald — Spielautor: Kosch; Illustrationen: Toni Llobet und Judit Piella; erschienen bei'),
 'Forest Shuffle: Dartmoor — game design: Kosch; illustrations: Toni Llobet and Judit Piella; published by':('Forêt Mixte : Dartmoor — conception : Kosch ; illustrations : Toni Llobet et Judit Piella ; édité par','Mischwald: Dartmoor — Spielautor: Kosch; Illustrationen: Toni Llobet und Judit Piella; erschienen bei'),
 'Forest Shuffle: Smoky Mountains — game design: Kosch; illustrations: Toni Llobet and Judit Piella; published by':('Forêt Mixte : Smoky Mountains — conception : Kosch ; illustrations : Toni Llobet et Judit Piella ; édité par','Mischwald: Smoky Mountains — Spielautor: Kosch; Illustrationen: Toni Llobet und Judit Piella; erschienen bei'),
})
EXTRA.update({
 'Choose player\'s forest':('Choisir la forêt d’un joueur','Wald einer Person wählen'),
 'Find a card':('Chercher une carte','Karte suchen'),
 'Check every per-copy condition/count before finalizing.':('Vérifiez chaque condition ou comptage par exemplaire avant de finaliser.','Prüfe vor dem Abschluss jede Bedingung bzw. Zählung pro Karte.'),
 'No-fish river count exceeds total rivers; scoring is capped.':('Le nombre de rivières sans poisson dépasse le total des rivières ; le score est plafonné.','Die Zahl der Flüsse ohne Fisch übersteigt die Gesamtzahl der Flüsse; die Wertung wird begrenzt.'),
 'Buckeye symbol total is below Buckeye tree quantity; the tree quantity is used as a minimum.':('Le total d’icônes Marronnier est inférieur au nombre d’arbres Marronnier ; le nombre d’arbres sert de minimum.','Die Summe der Rosskastanien-Symbole liegt unter der Zahl der Rosskastanien-Bäume; die Baumzahl gilt als Mindestwert.'),
 'Official rulebook':('Règle officielle','Offizielle Spielregel'),'Official appendix':('Annexe officielle','Offizieller Anhang'),
 'River Lyd':('Rivière Lyd','Fluss Lyd'),'Tarr Steps':('Tarr Steps','Tarr Steps'),
 'Hound of the Baskervilles':('Le Chien des Baskerville','Der Hund von Baskerville'),
 'Dartmoor-Rennpferd':('Cheval de course de Dartmoor','Dartmoor-Rennpferd'),
 'Hairy Hands':('Mains velues','Haarige Hände'),'Wolpertinger':('Wolpertinger','Wolpertinger'),
 'Red Ruby Devons':('Vache Devon rouge','Red-Ruby-Devon-Rinder'),'Otter':('Loutre d’Europe','Fischotter'),'Ring Cairn':('Cercle de pierre','Ringcairn'),
 'Check every per-copy condition/count before finalizing':('Vérifiez chaque condition ou comptage par exemplaire avant de finaliser','Prüfe vor dem Abschluss jede Bedingung bzw. Zählung pro Karte'),
})
EXTRA.update({'Exmoor':('Exmoor','Exmoor'),'Alpine':('Alpin','Alpin'),'Woodland Edge':('Lisière','Waldrand')})
EXTRA.update({
 'Translations.':('Traductions.','Übersetzungen.'),
 'The French and German texts were written for this page with Claude. German card names follow Lookout’s official German appendices. French names for the base game and Alpine follow the French rulebook and a French score sheet; the names for the other expansions and for Smoky Mountains are common French species names and may differ from the printed cards. Please report mistakes.':
 ('Les textes français et allemands ont été rédigés pour cette page avec Claude. Les noms de cartes allemands suivent les annexes allemandes officielles de Lookout. Les noms français du jeu de base et d’Alpin suivent la règle française et une feuille de score française ; les noms des autres extensions et de Smoky Mountains sont des noms usuels d’espèces et peuvent différer des cartes imprimées. Merci de signaler les erreurs.',
  'Die französischen und deutschen Texte wurden für diese Seite mit Claude geschrieben. Die deutschen Kartennamen folgen den offiziellen deutschen Anhängen von Lookout. Die französischen Namen für das Grundspiel und Alpin folgen der französischen Spielregel und einem französischen Wertungsbogen; die Namen der anderen Erweiterungen und von Smoky Mountains sind gebräuchliche Artnamen und können von den gedruckten Karten abweichen. Bitte Fehler melden.'),
})
EXTRA.update({'Page settings':('Réglages de la page','Seiteneinstellungen')})
CW={'actual trees':('arbres réels','echte Bäume'),'real species':('essences réelles','echte Arten'),'deer':('cervidés','Hirsche'),'hoofed animals':('ongulés','Huftiere'),
 'fish':('poissons','Fische'),'insect':('insectes','Insekten'),'amphibian':('amphibiens','Amphibien'),'bird':('oiseaux','Vögel'),'mouse':('souris','Mäuse'),'paw':('plantigrades/digitigrades','Pfotentiere'),'tree':('arbres','Bäume'),'river':('rivières','Flüsse')}
DLG=[['^Remove (.+) and their forest\\?$',['Retirer $1 et sa forêt ?','$1 und den Wald entfernen?']]]
TITLE={'forest':{'en':'Forest Shuffle Original Scoring Calculator','fr':'Forêt Mixte — calculateur de score (jeu de base)','de':'Mischwald — Punkterechner (Grundspiel)'},
       'smoky':{'en':'Forest Shuffle: Smoky Mountains — scoring calculator','fr':'Forêt Mixte : Smoky Mountains — calculateur de score','de':'Mischwald: Smoky Mountains — Punkterechner'},
       'moor':None}
def data(game,extra=None):
    x={}
    for d in (UI,BOX,BODIES,CONDITIONS,WARNINGS,FOOTER,{'forest':FOREST,'smoky':SMOKY,'moor':MOOR}[game],EXTRA):
        for k,v in d.items():x[k]=list(v)
    if extra:x.update(extra)
    x={k:v for k,v in x.items() if not (v[0]==k and v[1]==k)}
    sub=[[k,list(v)] for k,v in WARNINGS.items()]
    return {'x':x,'kind':{k:list(v) for k,v in KIND.items()},'cw':{k:list(v) for k,v in CW.items()},'dlg':DLG,'sub':sub,'title':TITLE[game]}
ENGINE=open(HERE+'i18n_engine.js',encoding='utf-8').read()
def i18n_script(game,extra=None):
    d=json.dumps(data(game,extra),ensure_ascii=False,separators=(',',':'))
    return '<script>'+ENGINE.replace('/*DATA*/null',d.replace('</','<\\/'),1)+'</script>'
