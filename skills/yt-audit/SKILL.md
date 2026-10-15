---
name: yt-audit
description: >-
  Audite une chaîne YouTube de bout en bout : packaging, régularité, les
  quinze premières secondes, et quoi corriger en premier. À utiliser pour
  « audite ma chaîne », « pourquoi ma chaîne ne grandit pas », « regarde mes
  vidéos », ou un lien de chaîne collé.
---

# yt-audit

Un audit qui liste vingt problèmes est une façon d'éviter celui qui compte. Celui-ci finit sur UNE
correction.

## Avant d'écrire

1. Lis `~/.claude/youtube/voix.md` s'il existe : c'est la voix de l'utilisateur (comment il parle,
   les mots qu'il n'utilise jamais, à qui il parle, ce qu'il n'affirme pas). S'il n'existe pas,
   demande-lui **trois de ses vidéos**, lis-les ou transcris-les, déduis la voix et écris le fichier
   avec les rubriques de `templates/voix.md` : à qui je parle, comment je parle, mots que je
   n'utilise jamais, mes mots, ce que je n'affirme pas, mon format.
2. N'invente jamais un chiffre, un résultat ou une source.

## Quoi regarder, dans cet ordre

1. **Les dix derniers titres, comme un ensemble.** Lis-les en liste, comme la page de la chaîne les
   montre. Promettent-ils des choses différentes ? Passe-les dans `../yt-package/title.py`. Une
   chaîne où tous les titres ont la même forme a un problème de format, pas de titre.
2. **Les miniatures, en taille fil.** Réduis-les. Qu'est-ce qui survit ? Si trois sont illisibles à
   cette taille, c'est ça la correction, et rien d'autre ne compte encore.
3. **Les quinze premières secondes des trois plus récentes.** Transcris-les et note-les avec
   `../yt-script/hookscore.py`. C'est là que la plupart des chaînes perdent.
4. **Le rythme de mise en ligne.** Pas la fréquence : la RÉGULARITÉ. Six vidéos une semaine puis
   rien pendant un mois, c'est pire qu'une tous les quinze jours pour toujours.
5. **La forme de la rétention**, s'il peut l'exporter : `/yt-retention`.

Sans PlugKit, la chaîne se lit en public, ou l'utilisateur colle sa liste :

```bash
yt-dlp --flat-playlist --playlist-end 10 --extractor-args "youtube:lang=fr" -J "https://www.youtube.com/@chaine/videos"
```

## Ce que tu rends

- La correction la plus importante, nommée, avec ce qu'il faut faire cette semaine.
- Trois choses qui marchent déjà, pour ne pas les casser. Sois précis : « ton énergie est bonne »
  n'est pas une observation.
- Ce qu'il ne faut PAS faire tout de suite, et pourquoi.

N'ouvre jamais un audit par un compliment que tu ne penses pas, et ne le finis jamais par une liste
de vingt choses.

## Avec PlugKit (optionnel)

PlugKit ajoute : les derniers titres, miniatures, vues, dates de mise en ligne et abonnés de ta
chaîne, lus directement, sans copier-coller. [plugkit.co](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)

Si les outils PlugKit sont branchés :

- `get_top_posts` avec `platform: "youtube"`, `sortBy: "date"`, `limit: 10` et une fenêtre longue
  (`from` six mois en arrière) : les dix dernières vidéos, avec leurs vues et leurs dates. Le
  rythme se lit dans les dates.
- `get_follower_stats` avec `platform: "youtube"` : les abonnés dans le temps (la courbe commence le
  jour où la chaîne a été connectée à PlugKit).

Le CTR, les impressions et la rétention ne passent pas par PlugKit : ils restent dans Studio
(l'export pour `/yt-retention`).

## La porte

Rien ne part d'ici. Ce skill écrit, l'utilisateur décide. Chaque sortie finit par un bloc à copier,
et la dernière ligne de chaque passage est la question : **on y va, ou on change ?**
