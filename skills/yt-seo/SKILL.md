---
name: yt-seo
description: >-
  Écrit la description, les chapitres, les tags et tout le texte vu par la
  recherche d'une vidéo YouTube, visés sur la requête qu'une vraie personne
  tape. À utiliser pour « écris ma description », « tags », « SEO »,
  « chapitres », « timestamps », « découpe la vidéo en parties », « aide
  cette vidéo à être trouvée », « personne ne trouve cette vidéo ».
---

# yt-seo

La recherche est un levier plus petit que le packaging, et plus gros qu'on ne le pense pour les
vidéos intemporelles. Pour une vidéo pensée pour le fil des abonnés, dis-le et mets l'effort dans
`/yt-package`.

```bash
python3 chapters.py transcript.srt --target 8     # chapitres validés
```

## Avant d'écrire

1. Lis `~/.claude/youtube/voix.md` s'il existe : c'est la voix de l'utilisateur (comment il parle,
   les mots qu'il n'utilise jamais, à qui il parle, ce qu'il n'affirme pas). S'il n'existe pas,
   demande-lui **trois de ses vidéos**, lis-les ou transcris-les, déduis la voix et écris le fichier
   avec les rubriques de `templates/voix.md` : à qui je parle, comment je parle, mots que je
   n'utilise jamais, mes mots, ce que je n'affirme pas, mon format.
2. N'invente jamais un chiffre, un résultat ou une source.

## La description

- **Les deux premières lignes sont les seules que les gens lisent.** Elles s'affichent avant
  « ...plus » et servent d'extrait dans la recherche. Dis ce que la vidéo leur donne, avec les mots
  qu'ils auraient tapés.
- Puis le lien ou la ressource, s'il y en a une, pour qu'elle soit au-dessus de la ligne de
  flottaison.
- Puis les chapitres (ci-dessous).
- Puis la version longue : ce qui est couvert, pour qui, ce que la vidéo suppose qu'on sait déjà.

Passe la description finie dans `python3 ../yt-script/antiia.py` et réécris chaque tournure
signalée avant de la montrer.

## Les chapitres

Les règles ne sont pas optionnelles. Une liste qui en casse une ne devient pas des chapitres du tout,
sans message d'erreur : le bloc reste dans la description sans rien faire.

- La première entrée est **0:00**.
- Il en faut **au moins trois**.
- Chacun dure **au moins 10 secondes**.

`chapters.py` vérifie les trois et dit quand une liste est invalide au lieu de la laisser coller.

**Retitre chaque ligne.** Le script trouve bien les COUPURES : il note les pauses que l'utilisateur
a vraiment faites selon le changement de vocabulaire de part et d'autre. Les titres qu'il sort sont
les mots du sujet, un brouillon. Un chapitre qui s'appelle « Miniature Accueil Contraste » est un
bouche-trou. Réécris chacun comme la promesse de sa partie, dans la voix de l'utilisateur, en trois
à cinq mots.

Les chapitres sont aussi un diagnostic de rétention : si une partie ne se nomme pas en cinq mots,
c'est deux parties, ou c'est du remplissage.

## Les tags, honnêtement

Les tags sont un signal faible, et YouTube l'a dit. Sers-t'en pour lever les ambiguïtés :
orthographes, noms d'outils, abréviations que les gens tapent vraiment. Puis arrête-toi. Quinze,
c'est largement assez, et YouTube plafonne le total à 500 caractères, virgules comprises. Un mur de
tags n'est pas une stratégie, et en bourrer qui n'ont rien à voir est contraire aux règles.

## Le test des requêtes

Avant de rendre quoi que ce soit, écris les trois requêtes que cette vidéo doit gagner, en
français, comme on les tape (« comment faire une miniature youtube », pas « optimisation des
miniatures »). Vérifie que le titre et les deux premières lignes de la description contiennent leurs
mots. Sinon, le problème est le titre, pas la description.

## La catégorie

Propose la catégorie YouTube : 22 Personnes et blogs, 27 Éducation, 28 Science et technologie,
26 Vie pratique et style, 24 Divertissement, 20 Jeux vidéo, 10 Musique, 17 Sport, 23 Humour,
25 Actualités et politique.

## Avec PlugKit (optionnel)

PlugKit ajoute : la description, les chapitres, les tags et la catégorie partent directement dans
la publication. [plugkit.co](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)

C'est `/yt-publier` qui s'en charge, après le oui : la description va dans `content`, les tags dans
`youtubeTags`, la catégorie dans `youtubeCategoryId`.

## La porte

Rien ne part d'ici. Ce skill écrit, l'utilisateur publie (ou `/yt-publier` publie après son oui).
Chaque sortie finit par un bloc à copier, et la dernière ligne de chaque passage est la question :
**on y va, ou on change ?**
