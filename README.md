# YouTube Agent Skill

Onze skills Claude qui font tourner une chaîne YouTube. En français. Gratuit, licence MIT, sans
inscription, sans clé d'API.

Un écrit tes scripts sur 21 formules de hook et note le hook avant que tu grilles une prise dessus.
Un travaille ton titre et ta miniature comme une seule paire. Un te sort la liste des coupes à
faire à partir de ton transcript. Un te montre où tes viewers décrochent. Un autre trouve et
découpe les Shorts cachés dans ta vidéo longue. Et un s'occupe de la viralité : il trouve les
vidéos qui explosent dans ta niche, les décortique, et les reconstruit dans ta voix.

Avec [PlugKit](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)
branché (optionnel), Claude monte aussi tes Shorts et publie tes vidéos à ta place.

**Rien n'est publié sans ton oui.**

## Installation (10 secondes)

Ouvre Claude Code et colle ça :

```
https://github.com/antoineblc99/youtube-agent-skill

Installe ce skill, puis vérifie que /yt-script marche.
```

Ou en plugin, dans Claude Code :

```
/plugin marketplace add antoineblc99/youtube-agent-skill
/plugin install youtube-agent@youtube-agent-skill
```

Ou à la main :

```bash
git clone https://github.com/antoineblc99/youtube-agent-skill.git
cp -r youtube-agent-skill/skills/yt-* ~/.claude/skills/
```

Pour un seul projet au lieu de tous : copie les mêmes dossiers dans le `.claude/skills/` du projet.
Pas de Claude Code ? Sur claude.ai, colle un `SKILL.md` en début de conversation et il tourne comme
un mode. Tu perds les scripts Python, qui font l'essentiel de `/yt-script`, `/yt-retention` et
`/yt-edit`, mais le reste marche.

Ensuite, passe dix minutes sur [`templates/voix.md`](templates/voix.md). Copie-le dans
`~/.claude/youtube/voix.md` et remplis-le, ou envoie trois de tes vidéos à Claude et dis « écris
mon voix.md à partir de ça ». Tous les skills le lisent. Ici plus qu'ailleurs, parce qu'il faut
dire les mots à voix haute.

## Les onze

| Commande | Ce qu'elle fait |
| --- | --- |
| `/yt-script` | Une idée devient un script. Cinq hooks sur [21 formules](skills/yt-script/hooks.json), notés, puis le script parlé avec ce qu'on voit à l'écran. |
| `/yt-package` | Le titre et la miniature comme une paire, vérifiés : coupe mobile, doublons, flou. |
| `/yt-edit` | Un transcript devient une liste de coupes : blancs, tics, reprises, avec les timecodes. |
| `/yt-comment` | Les commentaires triés en quatre piles, puis des réponses dans ta voix. Dit lequel épingler. |
| `/yt-plan` | Une semaine qui tient dans tes heures réelles. Une vidéo phare, une rapide, trois Shorts. |
| `/yt-viral` | Ce qui explose dans ta niche, classé par multiple de la médiane de chaque chaîne. Trouve, décortique, reconstruit. |
| `/yt-retention` | Ton export de rétention bien lu : fuite du hook, falaises, glissade, et quoi changer. |
| `/yt-shorts` | Les Shorts déjà cachés dans une vidéo longue, découpés, avec une nouvelle première phrase pour chacun. |
| `/yt-seo` | La description, les chapitres validés, les tags qui servent, et les trois requêtes à gagner. |
| `/yt-audit` | Toute la chaîne, et à la fin UNE correction, pas vingt. |
| `/yt-publier` | Tout ce qui part, montré en entier, puis publié ou programmé après ton oui. Sans PlugKit, la fiche à coller dans Studio. |

## Les outils

Ils tournent sur un Python 3 propre, sans aucune dépendance. C'est eux qui font que ces skills ne
sont pas que des prompts.

```bash
python3 skills/yt-script/hookscore.py --hook "une phrase"       # score du hook, calibré
python3 skills/yt-script/antiia.py brouillon.txt --report       # empreinte IA retirée
python3 skills/yt-package/title.py --title "..." --thumb "..."  # paire titre + miniature
python3 skills/yt-edit/deadair.py transcript.srt                # liste de coupes
python3 skills/yt-seo/chapters.py transcript.srt                # chapitres validés
python3 skills/yt-retention/retention.py retention.csv          # où ils sont partis, et pourquoi
python3 skills/yt-viral/swipe.py niche.json --min 2.0           # outliers par multiple de leur chaîne
```

Des exemples en français pour chacun sont dans [`exemples/`](exemples/), et
`python3 -m unittest discover tests` vérifie que tout tourne.

## Avec PlugKit (optionnel)

Les onze marchent sans. [PlugKit](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)
est un serveur MCP qui laisse Claude piloter tes réseaux, YouTube compris. Branché, il débloque
quatre choses :

- **Le montage de tes Shorts.** Reel Studio monte un passage de 5 minutes maximum (3 en mode Studio) en
  Short vertical (coupes, sous-titres, animations). La vidéo longue, elle, reçoit sa liste de coupes : c'est toi
  qui l'appliques.
- **La publication.** Titre, miniature, description, chapitres, tags, catégorie, date : `/yt-publier`
  montre tout, puis publie ou programme après ton oui.
- **Les stats.** Tes dernières vidéos, leurs vues, tes abonnés et tes meilleurs créneaux, lus
  directement au lieu d'être copiés-collés.
- **Les commentaires.** Claude les lit, rédige les réponses, et les publie après ton oui.

Ce qu'il ne fait pas, le branchement en deux minutes et la liste des outils :
[`docs/plugkit.md`](docs/plugkit.md).

## Le score des hooks, calibré sur des reels français

Le score de Jake était calibré sur 74 hooks anglais. Celui-ci a été recalibré sur **623 reels
français** d'Antoine Blanco (2020 à 2026, transcrits). La méthode, le fichier de poids et le
résultat sont publiés ; les transcripts, non.

- **Ce qu'on mesure.** La première phrase dite, notée sur cinq mesures (longueur, précision,
  enjeu, attaque, adresse) et trois pièges. Un « hit » = un reel qui fait au moins 2 fois la
  médiane des 50 reels publiés autour de lui : 112 sur 623, soit 18 %.
- **Le modèle.** Une régression logistique. Une mesure ne peut que monter le score, un piège que le
  baisser. Deux mesures allaient à contresens sur ce corpus et ont été retirées (poids 0) :
  l'attaque et l'adresse. Le « tu » en ouverture, que la formule d'origine récompensait, ne
  rapporte rien ici. Ce qui pèse le plus : la précision, puis la longueur, puis l'enjeu.
- **Le résultat, modeste.** L'AUC dit à quelle fréquence le score place un hit au-dessus d'un
  reel qui n'a pas cartonné : 0,50, c'est pile ou face, 1, c'est parfait. Ici, 0,59 en validation croisée (de
  0,576 à 0,606), contre 0,57 pour la formule d'origine sur les mêmes mesures. Appris jusqu'en 2023
  et testé sur les 146 reels d'après : 0,52, presque pile ou face. Taux de hits par tiers de score :
  12,6 %, 19,2 %, 22,1 %.
- **Les pièges, eux, sont nets.** Ouvrir sur « Si tu… » : 7 % de hits (43 reels) contre 18,8 %
  sans. Une salutation : 0 % (16 reels). Un préambule (« dans cette vidéo, je vais te montrer ») :
  9,1 % (11 reels). Quatre autres pièges ont une pénalité fixée à la main, pas mesurée : « arrête de
  scroller », un hashtag, un emoji, un adjectif creux (« incroyable », « ultime »).

Ce que ça veut dire : le score tue les hooks faibles, il ne choisit pas entre deux bons. Il a été
calibré sur des reels, pas sur des vidéos longues : c'est pour ça qu'il note la première phrase
du hook, la plus proche de ce que le corpus a mesuré. Pour le recalibrer sur ta propre chaîne
(100 vidéos au moins) : [`skills/yt-script/calibration/calibrer.py`](skills/yt-script/calibration/calibrer.py).

## Les petites lignes

La partie que la plupart des packs oublient.

**Rien n'est publié sans ton oui.** Sans PlugKit, chaque skill finit sur un bloc à copier et une
question : on y va, ou on change ? Avec PlugKit, `/yt-publier` montre tout ce qui va partir et
attend un oui explicite. Pareil pour une réponse à un commentaire, un commentaire masqué ou un
montage payé en crédits.

**PlugKit ne lit pas ta rétention.** Ni CTR, ni impressions : il n'a pas accès à YouTube Analytics.
`/yt-retention` demande l'export de Studio.

**Le montage PlugKit, ce sont des Shorts.** Pas ta vidéo longue : celle-ci reçoit sa liste de
coupes.

**Le score des hooks est une heuristique**, calibrée et modeste (voir plus haut). Une note basse est
une raison de relire, une note haute n'est jamais une promesse.

**La formule parle des mots, pas du résultat.** Quand `/yt-viral` dit qu'un titre utilise La
Statistique, c'est un jugement sur le titre affiché, pas une explication de ses vues.

**`/yt-viral` lit, il ne scrape pas.** Des pages publiques seulement. Jamais connecté à ta place,
jamais tes identifiants.

**Les tags comptent peu**, et ce pack le dit au lieu de te vendre un générateur de tags.

**Rien n'invente un chiffre.** Si un skill veut un chiffre qu'il n'a pas, il te le demande ou
écrit la phrase sans.

## Crédits

Ce pack est la version française de
[youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) de
[Jake Schincariol](https://opusjake.ai), sous licence MIT. Les onze skills, les 21 formules, les
six outils d'origine et la méthode de calibration viennent de lui. Ce qui change ici : tout en
français (formules, listes de mots, motifs, exemples, accents, virgule décimale), le score de hook
recalibré sur des reels français, l'outil anti-IA français partagé avec le pack Instagram
jumeau (insta-kit), `/yt-publier` ajouté, `/yt-chapters` fusionné dans
`/yt-seo`, et PlugKit en option.

## Licence

MIT. Utilise-le, modifie-le, partage-le. Garde les deux notices de [`LICENSE`](LICENSE).
