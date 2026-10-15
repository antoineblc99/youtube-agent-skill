---
name: yt-package
description: >-
  Écrit et vérifie le titre et la miniature d'une vidéo YouTube comme une
  seule paire : coupe mobile et ordinateur, doublons, flou. À utiliser pour
  « idées de titre », « comment j'appelle cette vidéo », « texte de
  miniature », « mon CTR est mauvais », le packaging, ou toute demande de
  renommer ou re-packager une vidéo.
---

# yt-package

Le titre et la miniature sont UNE unité. Les écrire séparément, c'est pour ça que la plupart des
packagings ratent : la miniature répète le titre, et la moitié de la surface de clic dit deux fois
la même chose.

```bash
python3 title.py --title "..." --thumb "L'IA A TOUT FAIT"
python3 title.py titres.txt            # un par ligne, classés
```

## Avant d'écrire

1. Lis `~/.claude/youtube/voix.md` s'il existe : c'est la voix de l'utilisateur (comment il parle
   face caméra, les mots qu'il n'utilise jamais, à qui il parle, ce qu'il n'affirme pas). S'il
   n'existe pas, demande-lui **trois de ses vidéos**, lis-les ou transcris-les, déduis la voix et
   écris le fichier avec les rubriques de `templates/voix.md` : à qui je parle, comment je parle,
   mots que je n'utilise jamais, mes mots, ce que je n'affirme pas, mon format.
2. N'invente jamais un chiffre, un résultat ou une source. Si un chiffre renforcerait le titre et
   que tu ne l'as pas, demande-le ou écris le titre sans.

## Les règles que le script applique, et pourquoi

- **60 caractères**, c'est là où la recherche sur ordinateur coupe ; **40**, c'est l'accueil
  mobile. Les deux sont signalés parce qu'ils échouent différemment : sur ordinateur on perd la fin,
  sur mobile on peut perdre le sujet. **100**, c'est la limite dure de YouTube.
- **La miniature ne répète pas le titre.** Des mots différents, la même promesse.
- **Trois mots maximum sur la miniature.** En taille fil, un quatrième mot devient une tache grise.
- **Un chiffre, un nom ou une date** battent tous les adjectifs du dictionnaire.
- **Deux mots en capitales**, c'est le plafond avant que le titre sonne spam.

## Écris-en dix, garde-en deux

Génère dix titres, passe-les tous dans `title.py`, montre à l'utilisateur les trois meilleurs avec
leur score et le problème précis de chacun. Pour le gagnant, écris le brief de miniature :
l'expression, le cadrage, les trois mots, et ce que le fond doit faire pour garder du contraste en
taille fil.

## Avec PlugKit (optionnel)

PlugKit ajoute : le titre et la miniature partent tels quels dans la publication, sans copier-coller
dans Studio. [plugkit.co](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)

C'est `/yt-publier` qui s'en charge, après le oui de l'utilisateur. Renommer ou changer la miniature
d'une vidéo déjà en ligne reste dans Studio : PlugKit ne modifie que les brouillons et les vidéos
programmées.

## La porte

Rien ne part d'ici. Ce skill écrit, l'utilisateur publie (ou `/yt-publier` publie après son oui).
Chaque sortie finit par un bloc à copier, et la dernière ligne de chaque passage est la question :
**on y va, ou on change ?**
