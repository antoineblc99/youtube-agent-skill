---
name: yt-retention
description: >-
  Lit l'export de fidélisation de l'audience de YouTube Studio, trouve où les
  viewers décrochent vraiment, puis dit quoi changer. À utiliser pour
  « pourquoi les gens arrêtent de regarder », « ma rétention est mauvaise »,
  un graphique ou un CSV de rétention collé, ou « corrige mon rythme ».
---

# yt-retention

Le graphique de rétention est le seul retour honnête que YouTube te donne. Presque personne ne
l'exporte.

```bash
python3 retention.py retention.csv --duration 600
python3 retention.py retention.csv --transcript transcript.srt
```

Récupérer le fichier : Studio > la vidéo > Statistiques > Engagement > le graphique « Fidélisation
de l'audience » > l'icône de téléchargement. Le script lit les exports français comme anglais
(point-virgule ou virgule, « 45,3 » ou « 45.3 », positions en pourcentage, en secondes ou en
« 1:30 »). Pas d'export, seulement une capture du graphique : lis-la à l'œil, dis que c'est moins
précis, et demande l'export pour la prochaine fois.

## Trois problèmes différents

- **FUITE DU HOOK** : ce qui est perdu dans les 30 premières secondes. Sous 25 %, c'est sain. C'est
  toujours la première chose à corriger, et c'est toujours les quinze premières secondes du script,
  jamais le montage.
- **FALAISES** : des chutes raides d'un seul coup. Une falaise, c'est un moment : un changement de
  sujet sans annonce, une lecture de sponsor, une mise en place trop longue. Avec `--transcript`, le
  script imprime ce qui se disait à cet endroit, et c'est ça qui rend le rapport utile au lieu
  d'intéressant.
- **GLISSADE** : la perte régulière sur le milieu. Une glissade plate, c'est le rythme. La
  correction, c'est couper, pas réécrire (`/yt-edit`).

## Ce que tu rends

Nomme la plus grosse fuite et UNE correction pour elle. Pas une liste de cinq. Puis, seulement si
on te le demande, le reste. Et si la fuite du hook est saine et la glissade plate, dis que la vidéo
va bien et que le problème est le packaging : envoie vers `/yt-package`.

## PlugKit ne lit pas la rétention

PlugKit n'a pas accès à YouTube Analytics : ni rétention, ni CTR, ni impressions. Même avec PlugKit
branché, l'export Studio reste obligatoire pour ce skill.

## La porte

Rien ne part d'ici. Ce skill écrit, l'utilisateur corrige. Chaque sortie finit par un bloc à
copier, et la dernière ligne de chaque passage est la question : **on y va, ou on change ?**
