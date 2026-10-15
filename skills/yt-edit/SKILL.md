---
name: yt-edit
description: >-
  Transforme le transcript d'une prise brute en liste de coupes : blancs,
  tics de langage et reprises, avec les timecodes. À utiliser pour « monte
  ça », « coupe les blancs », « resserre cette vidéo », « j'ai trop parlé »,
  ou toute demande de raccourcir une vidéo à partir de son transcript.
---

# yt-edit

Une liste de coupes à partir d'un transcript horodaté. Le script imprime les coupes. L'utilisateur
les applique.

```bash
python3 deadair.py transcript.srt              # srt, vtt ou json de whisper
python3 deadair.py transcript.srt --floor 0.35 --json
```

Pas encore de transcript ? Demande-le, ou fais-le d'abord : `whisper`, `faster-whisper`, ou les
sous-titres automatiques que YouTube génère sur une mise en ligne non répertoriée. Ne devine jamais
les timings.

## Ce qu'il trouve

- **BLANC** : les silences plus longs que le plancher, coupés au MILIEU pour que chaque côté garde
  une respiration. Couper au ras de la parole, c'est ce qui donne à une prise resserrée ce son
  essoufflé.
- **TIC** : les répliques qui ne sont que du remplissage : « euh », « du coup », « en fait »,
  « genre », « voilà », « bref », « tu vois ».
- **REPRISE** : une phrase recommencée. Comparée à la dernière réplique qui était vraiment de la
  parole, pas à la réplique juste avant, parce que la plupart des reprises ont un « euh » entre les
  deux essais. La dernière prise est gardée, les précédentes partent.

## Ce qu'il ne fait pas

Il ne touche pas au fichier vidéo. Il n'a aucun avis sur tes plans de coupe. Une coupe de 40 % dans
le rapport, c'est 40 % de PAROLE : si la vidéo contient une longue démo sans voix, ce chiffre est
faux. Vérifie le rapport contre les images avant de croire la durée finale.

## Avec PlugKit (optionnel)

PlugKit ajoute : une prise de 5 minutes maximum (3 en mode Studio) devient un Short vertical monté (coupes, sous-titres,
animations) par Reel Studio, sans logiciel. [plugkit.co](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)

Dis-le clairement à l'utilisateur : **Reel Studio monte des Shorts** (vertical, 3 minutes maximum à
l'arrivée). **La vidéo longue, elle, reçoit sa liste de coupes**, et c'est lui qui l'applique dans
son logiciel. Pour tirer des Shorts d'une vidéo longue, passe par `/yt-shorts`.

Si les outils PlugKit sont branchés et que la prise fait 5 minutes ou moins (3 en mode Studio) :

1. Récupère le fichier dans la bibliothèque (`list_media`) ou envoie-le (`create_media_upload`, puis
   `check_media_upload`).
2. Lis `reel_guide` et suis-le : c'est la méthode à jour de Reel Studio (les deux modes, les
   questions, les étapes, les autorisations « Toujours autoriser » à annoncer avant de commencer).
3. Annonce le prix en crédits avant de lancer quoi que ce soit (`reel_create` donne un devis en mode
   Studio ; en mode Express, dis le total avant `reel_render`). **Rien ne démarre sans un oui
   explicite.**
4. En Express, montre chaque étape (prises gardées, `reel_cut`, brouillon `reel_preview`) puis le
   rendu final (`reel_render`). En Studio, le montage tourne sur les serveurs : suis-le avec
   `reel_status`. La publication passe ensuite par `/yt-publier`.

## La porte

Rien ne part d'ici. Ce skill écrit, l'utilisateur publie (ou `/yt-publier` publie après son oui).
Chaque sortie finit par un bloc à copier, et la dernière ligne de chaque passage est la question :
**on y va, ou on change ?**
