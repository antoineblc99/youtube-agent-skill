---
name: yt-comment
description: >-
  Rédige les réponses aux commentaires YouTube dans la voix du créateur,
  triés selon ceux qui valent une réponse. À utiliser pour « réponds à mes
  commentaires », « gère la section commentaires », « quelqu'un a demandé
  X », ou un fil de commentaires collé.
---

# yt-comment

La section commentaires est une surface de rétention, pas une corvée. Ce sont les réponses des
premières heures qui décident si un fil devient une conversation que d'autres lisent.

## Avant d'écrire

1. Lis `~/.claude/youtube/voix.md` s'il existe : c'est la voix de l'utilisateur (comment il parle,
   les mots qu'il n'utilise jamais, à qui il parle, ce qu'il n'affirme pas). S'il n'existe pas,
   demande-lui **trois de ses vidéos**, lis-les ou transcris-les, déduis la voix et écris le fichier
   avec les rubriques de `templates/voix.md` : à qui je parle, comment je parle, mots que je
   n'utilise jamais, mes mots, ce que je n'affirme pas, mon format.
2. N'invente jamais un chiffre, un résultat ou une source.

## Trie d'abord, toujours

Range ce que l'utilisateur colle en quatre piles et dis combien il y en a dans chacune avant
d'écrire quoi que ce soit :

1. **Questions** : réponds-y. Ce sont les sujets de ses prochaines vidéos, alors note celles qui
   reviennent.
2. **Corrections** : si elles ont raison, dis-le simplement et remercie. Ne conteste jamais un fait
   que tu ne peux pas vérifier.
3. **Compliments** : réponds à quelques-uns, brièvement, avec un détail précis de leur commentaire.
   Un mur de « merci ! » identiques se lit comme automatique, parce que ça l'est.
4. **Appâts** : pas de réponse. Dis-le et passe. N'écris jamais de répartie, même méritée.

## Écrire la réponse

- Moins de 30 mots. Une longue réponse dans un fil, c'est un article de blog que personne n'a
  demandé.
- Réponds à la vraie question dans la première phrase.
- Une question en retour, seulement si elle est sincère.
- Pas d'emoji, sauf si les propres réponses de l'utilisateur en ont. Vérifie dans `voix.md`.
- Ne promets jamais une vidéo qu'il n'a pas décidé de faire.
- Passe toutes les réponses dans `python3 ../yt-script/antiia.py` avant de les montrer, et
  réécris chaque tournure signalée.

## Le cœur et l'épingle

Dis quel commentaire épingler, UN seul, et pourquoi. Épingle la question que le plus de gens se
posent aussi, pas le commentaire le plus gentil. Mettre des cœurs ne coûte rien et se voit. Les deux
se font à la main dans Studio ou dans l'appli : aucun outil ne le fait à sa place.

## Avec PlugKit (optionnel)

PlugKit ajoute : Claude lit les commentaires de la chaîne lui-même et publie tes réponses après ton
oui, sans copier-coller. [plugkit.co](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)

Si les outils PlugKit sont branchés :

1. `list_engagement` avec `platform: "youtube"` et `kind: "comment"` : les commentaires qui
   attendent une réponse, chacun avec la vidéo sous laquelle il est. Si la liste est vide alors que
   la vidéo a des commentaires, lance `sync_engagement` (avec le `postId` de la vidéo), puis relis.
   Toujours vide : demande à l'utilisateur de coller les commentaires.
2. Trie et rédige comme ci-dessus.
3. Montre chaque réponse **en entier**, avec le commentaire auquel elle répond. Une réponse est
   publique, signée par la chaîne, et ne se modifie pas après coup. Attends un **oui** explicite.
4. Après le oui, `reply_to_engagement` pour chaque réponse validée, et seulement celles-là.
5. Les appâts : propose de les masquer avec `hide_comment` (réversible, l'auteur n'est pas
   prévenu). Masque seulement après un oui.

Si PlugKit refuse une réponse faute de permission, la chaîne n'a pas donné l'accès aux commentaires
quand elle a été connectée : dis-le à l'utilisateur, ça se règle dans la connexion de sa chaîne sur
le tableau de bord PlugKit. En attendant, donne-lui les réponses à coller. Épingler et mettre un
cœur restent à la main.

## La porte

Rien ne part sans le oui de l'utilisateur. Chaque sortie finit par un bloc à copier (ou par la
liste exacte de ce qui va être publié), et la dernière ligne de chaque passage est la question :
**on y va, ou on change ?**
