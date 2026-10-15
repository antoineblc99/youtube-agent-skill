---
name: yt-script
description: >-
  Écrit le script d'une vidéo YouTube à partir d'une idée brute : des hooks
  sur 21 formules, notés, puis le script parlé complet avec ce qu'on voit à
  l'écran. À utiliser dès que l'utilisateur veut un script, un hook, une
  phrase d'ouverture, « qu'est-ce que je dis », « écris ma prochaine vidéo »,
  ou va tourner sans avoir ses quinze premières secondes.
---

# yt-script

Une idée transformée en script que quelqu'un regarde jusqu'au bout.

Deux outils vivent dans ce dossier et tournent vraiment. Sers-t'en. Ne note pas le hook à l'œil.

```bash
python3 hookscore.py hooks.txt              # classe les hooks
python3 hookscore.py --hook "une phrase"    # note un seul hook
python3 antiia.py script.txt --report       # retire l'empreinte IA, signale les structures
```

## Avant d'écrire

1. Lis `~/.claude/youtube/voix.md` s'il existe : c'est la voix de l'utilisateur (comment il parle
   face caméra, les mots qu'il n'utilise jamais, à qui il parle, ce qu'il n'affirme pas). S'il
   n'existe pas, demande-lui **trois de ses vidéos**, lis-les ou transcris-les, déduis la voix et
   écris le fichier avec les rubriques de `templates/voix.md` : à qui je parle, comment je parle,
   mots que je n'utilise jamais, mes mots, ce que je n'affirme pas, mon format. Un script dans la
   mauvaise voix est pire que pas de script : il faut le dire à voix haute.
2. N'invente jamais un chiffre, un résultat ou une source. Si un chiffre renforcerait la phrase et
   que tu ne l'as pas, demande-le ou écris la phrase sans.

## La forme

**Les 15 premières secondes, c'est tout le travail.** Elles font trois choses ou la vidéo fuit :
confirmer le clic que le titre a promis, ouvrir une question que le viewer ne peut pas refermer, et
prouver que la réponse existe.

1. **Le hook.** Écris-en CINQ sur [les 21 formules](hooks.json), passe-les dans `hookscore.py`,
   garde les deux meilleurs et montre-les tous les deux avec leur panneau. Ne rends jamais un seul
   hook. Le score porte sur la première phrase : c'est elle qui doit tomber tout de suite.
   N'ouvre pas sur « Si tu… », sur une salutation ou sur « dans cette vidéo, je vais te montrer » :
   ce sont les trois ouvertures que le corpus a mesurées comme les plus faibles.
2. **Le virage** (0:15 à 0:45). Dis ce que la vidéo va faire, en une phrase, et commence à le
   faire. Pas d'intro de chaîne, pas de « avant de commencer », pas de « abonne-toi ». C'est la
   cause la plus courante de la falaise à 0:30.
3. **Le corps.** Une idée par temps. Marque chaque temps avec ce qu'on VOIT à l'écran, pas
   seulement ce qui est dit : une tête qui parle sans rien à regarder, c'est un podcast.
4. **La promesse tenue.** Livre ce que le hook a promis, explicitement, et dis que tu le livres :
   « voilà le prompt, il est dans la description ».
5. **La fin.** Une seule demande. Pas trois.

Avant de montrer le script, passe-le dans `antiia.py --report`, garde la version nettoyée et
réécris toi-même chaque structure signalée.

## Ce que tu rends

- les deux meilleurs hooks avec leur panneau de score
- le script, temps par temps, avec `[À L'ÉCRAN : ...]` sur chaque temps
- la durée estimée à 150 mots par minute, ou au débit de l'utilisateur s'il est noté dans
  `voix.md` (mots d'un de ses transcripts divisés par la durée en minutes)
- une ligne qui nomme la formule du hook gagnant et pourquoi elle colle à cette idée

## Ce que vaut le score

Le score est le rang de la première phrase parmi celles de 623 reels français mesurés (le corpus
de calibration, détaillé dans le README). Il sépare les hooks qui ont cartonné des autres un peu
mieux qu'une pièce : il sert à tuer les hooks faibles avant le tournage, pas à choisir entre deux
bons. Une note basse est une raison de relire, une note haute n'est jamais une promesse. Dis-le
quand tu montres les panneaux.

## La porte

Rien ne part d'ici. Ce skill écrit, l'utilisateur tourne et publie (ou `/yt-publier` publie après
son oui). Chaque sortie finit par un bloc à copier, et la dernière ligne de chaque passage est la
question : **on y va, ou on change ?**
