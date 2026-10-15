# PlugKit avec ce pack

PlugKit est optionnel. Les onze skills marchent sans : ils écrivent, et tu publies à la main. Avec
PlugKit branché, Claude fait en plus quatre choses sur ta chaîne : **monter tes Shorts, publier,
lire tes stats, gérer tes commentaires**. Toujours après ton oui.

[Essayer PlugKit](https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill)

## Brancher PlugKit (2 minutes)

1. Crée ton compte sur PlugKit et connecte ta chaîne YouTube depuis le tableau de bord. Accepte
   l'accès aux commentaires si tu veux que Claude y réponde.
2. Branche le connecteur :
   - **Claude (app ou claude.ai)** : Personnaliser > Connecteurs > Ajouter un connecteur
     personnalisé, colle `https://api.plugkit.co/mcp`, puis clique Autoriser.
   - **Claude Code** : `claude mcp add --transport http plugkit https://api.plugkit.co/mcp`, puis
     `/mcp` pour te connecter.
3. Vérifie : demande à Claude « appelle whoami sur PlugKit ». Ta chaîne doit apparaître.

Pendant un montage ou une publication, Claude te demande d'autoriser des outils PlugKit. Clique
« Toujours autoriser », sinon tout s'arrête à chaque étape.

## Ce que PlugKit fait sur YouTube

| Quoi | Outils | Dans quel skill |
| --- | --- | --- |
| Publier une vidéo ou un Short, ou le programmer : titre (100 caractères), description, tags, catégorie, miniature, visibilité, « conçu pour les enfants » | `create_post`, `publish_post`, `list_posts` | `/yt-publier` |
| Modifier une vidéo programmée, ou la remettre en brouillon | `update_post` | `/yt-publier` |
| Envoyer un fichier (vidéo, miniature) | `list_media`, `create_media_upload`, `check_media_upload`, `upload_media` | `/yt-publier`, `/yt-shorts`, `/yt-edit` |
| Monter un Short vertical (3 minutes maximum à l'arrivée, prise de 5 minutes maximum, 3 en mode Studio) | `reel_guide`, `reel_create`, `reel_status`, `reel_cut`, `reel_preview`, `reel_render`, `reel_revise` | `/yt-shorts`, `/yt-edit` |
| Lire les vues, likes et commentaires de tes vidéos, et tes meilleures vidéos | `get_top_posts` | `/yt-viral`, `/yt-audit` |
| Abonnés dans le temps | `get_follower_stats` | `/yt-audit` |
| Meilleurs créneaux de ta chaîne | `get_best_times_to_post` | `/yt-plan`, `/yt-publier` |
| Lire les commentaires, y répondre, masquer un appât | `list_engagement`, `sync_engagement`, `reply_to_engagement`, `hide_comment` | `/yt-comment` |

## Ce que PlugKit ne fait pas sur YouTube

- **Pas de rétention, pas de CTR, pas d'impressions.** PlugKit n'a pas accès à YouTube Analytics.
  `/yt-retention` demande l'export de Studio, avec ou sans PlugKit.
- **Pas de montage de vidéo longue.** Reel Studio monte des Shorts. La vidéo longue reçoit sa liste
  de coupes (`/yt-edit`) et tu l'appliques dans ton logiciel.
- **Pas de modification d'une vidéo déjà en ligne.** Titre, miniature ou description d'une vidéo
  publiée : c'est dans Studio.
- **Pas d'épingle ni de cœur sur un commentaire.** L'API de YouTube ne le permet pas : à la main.
- **Pas de lecture des autres chaînes.** La veille de `/yt-viral` reste en lecture publique.

## La règle

Rien n'est publié, programmé, répondu ou masqué sans un **oui** explicite, après que Claude t'a
montré exactement ce qui va partir. Un montage Reel Studio ne démarre pas sans ton oui sur le prix
en crédits.
