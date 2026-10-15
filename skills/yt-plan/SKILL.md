---
name: yt-plan
description: >-
  Planifie une semaine ou un mois de vidéos YouTube : quoi poster, quand, et
  dans quel ordre, à la taille du temps réel du créateur. À utiliser pour
  « planifie ma semaine », « calendrier de contenu », « qu'est-ce que je
  poste », « je ne sais pas quoi faire ensuite ».
---

# yt-plan

Un plan qui ne tient pas dans la semaine est une liste de regrets. Pose deux questions avant
d'écrire quoi que ce soit : **combien d'heures as-tu vraiment**, et **qu'est-ce qui est déjà à
moitié fait**.

## Avant d'écrire

1. Lis `~/.claude/youtube/voix.md` s'il existe : c'est la voix de l'utilisateur (comment il parle,
   les mots qu'il n'utilise jamais, à qui il parle, ce qu'il n'affirme pas). S'il n'existe pas,
   demande-lui **trois de ses vidéos**, lis-les ou transcris-les, déduis la voix et écris le fichier
   avec les rubriques de `templates/voix.md` : à qui je parle, comment je parle, mots que je
   n'utilise jamais, mes mots, ce que je n'affirme pas, mon format.
2. N'invente jamais un chiffre, un résultat ou une source.

## La forme d'une semaine

- **Une vidéo phare.** Celle pour laquelle la semaine existe. Elle prend le plus de temps et sort le
  jour que les statistiques de la chaîne donnent comme le meilleur : demande-le, ne suppose pas le
  mardi.
- **Une vidéo rapide.** Faite à partir de ce qui existe déjà : un extrait, une réaction, une suite
  au commentaire qui a eu le plus de réponses la semaine passée.
- **Des Shorts tirés de la phare.** Trois, coupés dans la vidéo longue, pas écrits à part.
  `/yt-shorts` les trouve.

Trois mises en ligne sur une semaine de sept jours, pas sept. Un plan qui poste tous les jours n'est
un plan pour personne, et ce sont les jours vides qui permettent aux jours pleins de survivre à une
mauvaise semaine.

## Ce que tu rends

Un tableau : jour, format, titre de travail, la phrase que la vidéo promet, et ce qui existe déjà
pour elle. Puis la ligne honnête en bas : combien d'heures ça coûte, et quoi lâcher en premier si
la semaine déraille.

## Avec PlugKit (optionnel)

PlugKit ajoute : les meilleurs créneaux de ta chaîne et ce qui est déjà programmé, lus directement
au lieu de te les demander. [plugkit.co](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)

Si les outils PlugKit sont branchés :

- `get_best_times_to_post` avec `platform: "youtube"` (dans le fuseau de l'utilisateur) pour les
  jours et heures. Une case portée par deux vidéos, c'est du bruit : dis-le au lieu de recommander
  l'heure.
- `list_posts` avec `platform: "YOUTUBE"` et `status: "SCHEDULED"` pour ce qui est déjà programmé,
  puis `status: "DRAFT"` pour ce qui est à moitié fait.

Ce skill ne programme rien. Chaque vidéo du plan passe par `/yt-publier` le moment venu, avec son
propre oui.

## La porte

Rien ne part d'ici. Ce skill écrit, l'utilisateur publie (ou `/yt-publier` publie après son oui).
Chaque sortie finit par un bloc à copier, et la dernière ligne de chaque passage est la question :
**on y va, ou on change ?**
