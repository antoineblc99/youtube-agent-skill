---
name: yt-viral
description: >-
  Trouve ce qui marche vraiment dans la niche du créateur sur YouTube, le
  classe selon combien chaque vidéo a battu sa propre chaîne, le décortique,
  puis le reconstruit dans sa voix. À utiliser pour « qu'est-ce qui marche en
  ce moment », « trouve les vidéos virales de ma niche », « pourquoi cette
  vidéo a explosé », la veille concurrents, ou un swipe file.
---

# yt-viral

Les vues brutes classent la taille des chaînes, pas les idées. Ce skill classe par **multiple de la
médiane de chaque chaîne**, la seule version de la question qui parle de la vidéo. Trois temps :
**trouve, décortique, reconstruis.**

```bash
python3 swipe.py niche.json --min 2.0
python3 swipe.py chaine1.json chaine2.json chaine3.json    # sorties yt-dlp, une par chaîne
```

## 1. Trouve

Il faut **au moins quatre vidéos par chaîne**, sinon une médiane ne veut rien dire : le script
ignore la chaîne et le dit. Collecte comme l'utilisateur préfère :

- **Les chaînes de sa niche**, s'il les connaît (cinq à dix), une par fichier :

```bash
yt-dlp --flat-playlist --playlist-end 30 --extractor-args "youtube:lang=fr" -J "https://www.youtube.com/@chaine/videos" > chaine.json
```

  Sans `lang=fr`, YouTube peut renvoyer les titres traduits en anglais ; pour une chaîne
  américaine, mets `lang=en`. L'onglet `/videos` ne contient que les vidéos longues, l'onglet
  `/shorts` que les Shorts : ne mélange pas les deux, leurs vues ne sont pas à la même échelle.
- **Une recherche**, s'il ne les connaît pas : elle donne les chaînes qui reviennent, puis collecte
  chacune comme ci-dessus.

```bash
yt-dlp --flat-playlist --extractor-args "youtube:lang=fr" -J "ytsearch30:mot clé de la niche" > recherche.json
```

- **Une liste à la main**, sans yt-dlp :

```json
[{"channel":"...","title":"...","views":412000,"url":"...","duration":613}]
```

**Lecture publique seulement.** Jamais de session connectée, jamais les identifiants de
l'utilisateur. Pas de yt-dlp installé : `brew install yt-dlp` ou `pip install yt-dlp`, sinon la
liste à la main.

## 2. Décortique

Le multiple est le signal. La ligne de formule est un jugement sur le TITRE, reconnu parmi
[les 21 formules](../yt-script/hooks.json) : ce n'est pas une explication de pourquoi la vidéo a
marché, et dis-le quand tu la présentes.

Pour les trois à cinq meilleurs outliers :

1. Les sous-titres automatiques, sans télécharger la vidéo (`en.*` pour une vidéo en anglais) :
   `yt-dlp --skip-download --write-auto-subs --sub-langs "fr.*" -o "decortique/%(id)s" URL`
   Les scripts lisent le `.vtt` tel quel, répétitions des sous-titres automatiques comprises.
2. **Le hook** : les 15 premières secondes, recopiées, passées dans `../yt-script/hookscore.py`.
   Est-ce qu'elles confirment le titre, ouvrent une question, prouvent que la réponse existe ?
3. **La structure** : où arrive la promesse, combien de temps dure la mise en place, où sont les
   relances. `../yt-seo/chapters.py` sur le `.vtt` donne les grandes parties.
4. **Le packaging** : le titre passé dans `../yt-package/title.py`, la miniature regardée
   (`yt-dlp --skip-download --write-thumbnail`) : qu'est-ce qu'elle dit que le titre ne dit pas ?

Rends : les cinq meilleurs avec leur multiple, la formule de chacun, et LA chose structurelle
qu'ils partagent.

## 3. Reconstruis

Puis la ligne plus dure : lequel l'utilisateur peut vraiment faire **cette semaine**, dans sa voix,
avec ce qu'il a. Un seul. Garde le mécanisme (la formule, la structure, la promesse du packaging),
change tout le reste (le sujet, la preuve, les mots).

- `/yt-package` : dix titres sur le même mécanisme, deux gardés, le brief de miniature.
- `/yt-script` : cinq hooks dont au moins deux sur la formule de l'outlier, puis le script.

Ne recopie jamais une phrase, une miniature ou une image de la vidéo d'origine. On reprend la
mécanique, pas le contenu.

## Avec PlugKit (optionnel)

PlugKit ajoute : tes propres outliers, sortis de ta chaîne sans collecte. Ce sont les plus faciles à
reconstruire : même audience, même voix. [plugkit.co](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)

Si les outils PlugKit sont branchés : `get_top_posts` avec `platform: "youtube"`, `sortBy: "views"`
et une fenêtre longue (`from` un an en arrière), puis mets les vidéos au format ci-dessus avec
`"channel": "Ma chaîne"` et passe-les dans `swipe.py`. La niche, elle, reste en lecture publique :
PlugKit ne lit que les chaînes connectées.

## La porte

Rien ne part d'ici. Ce skill écrit, l'utilisateur publie (ou `/yt-publier` publie après son oui).
Chaque sortie finit par un bloc à copier, et la dernière ligne de chaque passage est la question :
**on y va, ou on change ?**
