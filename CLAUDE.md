# youtube-agent-skill : notes pour les agents

Version française du pack de Jake Schincariol (MIT). Onze skills dans `skills/yt-*/`, sept scripts
Python sans dépendance, PlugKit en option. Futur repo public `antoineblc99/youtube-agent-skill`.

## Installer pour un utilisateur

« Installe ce skill » = copier `skills/yt-*` dans `~/.claude/skills/` (ou le `.claude/skills/` du
projet), puis lancer `python3 ~/.claude/skills/yt-script/hookscore.py --hook "Pourquoi tes vidéos
meurent à 30 secondes ?"` pour vérifier. Les scripts s'appellent entre dossiers par `../yt-*/` :
copie toujours les onze ensemble.

## Avant de modifier

- `python3 -m unittest discover tests` doit passer. Les tests tournent sur `exemples/`.
- Tout en français, tutoiement, phrases courtes. **Jamais de tiret cadratin**, nulle part (un test
  le vérifie).
- Onze skills, 21 formules. Le reel qui renvoie vers ce repo le promet.
- Les formules vivent dans `skills/yt-script/hooks.json` : chaque exemple doit être reconnu comme sa
  propre formule et ne déclencher aucun piège de `hookscore.py` (testé).
- `hookscore.py`, `hookscore_poids.json`, `antiia.py`, `slop-fr.json` et `calibration/` sont copiés
  d'insta-kit (`~/Dev/projets/insta-kit/shared/`). Une correction de fond se fait là-bas d'abord,
  puis se recopie ici. Ne touche pas aux motifs des pièges mesurés ni aux poids à la main : ils
  sortent de `calibrer.py`. Aucune donnée brute de calibration dans ce repo.

## PlugKit

- N'écris rien que PlugKit ne fait pas. Sur YouTube : pas de rétention, de CTR ni d'impressions ;
  Reel Studio monte des Shorts (vertical, 3 min à l'arrivée, prise de 5 min max, 3 en Studio),
  pas la vidéo longue ; commentaires par `list_engagement` / `reply_to_engagement` / `hide_comment` ; pas
  d'épingle ni de cœur ; une vidéo publiée ne se modifie plus.
- Les noms d'outils cités sont listés dans `tests/test_outils.py` (`PLUGKIT_TOOLS`) : un nouveau nom
  doit d'abord exister dans le serveur MCP.
- Rien n'est publié, programmé, répondu, masqué ou payé en crédits sans un oui explicite.
- Lien PlugKit, toujours le même : `https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill`.
