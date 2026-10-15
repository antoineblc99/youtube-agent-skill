---
name: yt-shorts
description: >-
  Trouve les Shorts cachés dans une vidéo longue, les découpe et les écrit, à
  partir du transcript pour choisir les moments qui tiennent seuls. À
  utiliser pour « découpe ça en shorts », « fais des clips », « recycle cette
  vidéo », « qu'est-ce que je devrais extraire ».
---

# yt-shorts

Un Short tiré d'une vidéo longue n'est pas un extrait du meilleur moment. C'est un moment qui
**survit sans la vidéo autour**, et ça fait beaucoup moins de candidats.

## Choisir

Lis le transcript et trouve des passages de 20 à 55 secondes où les trois sont vrais :

1. Ça s'ouvre sur une pensée complète. Si la première phrase a besoin de la minute d'avant, ce n'est
   pas un Short.
2. Il y a un virage dedans : une affirmation, puis quelque chose qui la complique ou la prouve.
3. Ça finit sur une phrase, pas sur une phrase qui traîne.

Classe les candidats et montre les cinq meilleurs avec leurs timecodes et leur première phrase,
pour que l'utilisateur puisse en rejeter un sans relire tout le transcript.

## Écrire chacun

- **Une NOUVELLE première phrase.** Celle de la vidéo longue suppose un contexte que ce viewer n'a
  pas. Écris la remplaçante et passe-la dans `../yt-script/hookscore.py`.
- **Un texte à l'écran pour les deux premières secondes**, avec d'autres mots que la phrase dite.
- **Un point de boucle** : ce que la dernière phrase prépare pour que la première y réponde.
- **Le cadrage vertical** : ce qui sort du cadre quand on passe du 16:9 au 9:16, et si ça compte.

## Découper

Dans Claude Code, si `ffmpeg` est installé, découpe chaque passage validé toi-même, une commande par
Short :

```bash
ffmpeg -ss 00:04:11 -to 00:04:59 -i video.mp4 -c copy short-1.mp4
```

Sans réencodage, la coupe tombe sur l'image clé la plus proche : garde une seconde de marge de
chaque côté. Pour une coupe à l'image près, remplace `-c copy` par `-c:v libx264 -c:a aac`. Sans
ffmpeg, donne les timecodes : l'utilisateur coupe sur son téléphone ou dans son logiciel.

## Avec PlugKit (optionnel)

PlugKit ajoute : chaque passage devient un Short monté (vertical, sous-titres, animations) par Reel
Studio, puis publié sur ta chaîne après ton oui. [plugkit.co](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)

Si les outils PlugKit sont branchés :

1. Envoie le passage découpé : `create_media_upload`, puis `check_media_upload` (ou `list_media` si
   le fichier est déjà dans la bibliothèque). Un passage par projet.
2. Lis `reel_guide` et suis-le : les deux modes (Studio, Express), les questions, les autorisations
   à annoncer, les étapes. Donne-lui le brief : la nouvelle première phrase, le texte à l'écran,
   le point de boucle.
3. Si le passage est filmé en 16:9, dis-le avant de lancer et vérifie le cadrage du visage sur le
   premier brouillon ou la première livraison, avant le rendu final.
4. Prix en crédits annoncé avant, **rien ne démarre sans un oui explicite.**
5. Le Short rendu se publie avec `/yt-publier`.

## La porte

Rien ne part d'ici. Ce skill écrit et découpe, l'utilisateur publie (ou `/yt-publier` publie après
son oui). Chaque sortie finit par un bloc à copier, et la dernière ligne de chaque passage est la
question : **on y va, ou on change ?**
