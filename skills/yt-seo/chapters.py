#!/usr/bin/env python3
"""chapters.py : les chapitres d'une vidéo YouTube à partir d'un transcript horodaté.

    python3 chapters.py transcript.srt            # ou .vtt / .json de whisper
    python3 chapters.py transcript.srt --target 8 --json

Imprime un bloc à coller tel quel dans la description. Les règles de YouTube sont vérifiées ici,
pas supposées : la liste commence à 0:00, compte au moins trois chapitres, et chacun dure au moins
10 secondes. Un bloc qui casse une de ces règles ne devient pas des chapitres, sans aucun message
d'erreur, d'où la vérification.

Les coupures viennent des pauses que tu as vraiment faites entre deux parties, notées selon la
longueur de la pause et le changement de vocabulaire de part et d'autre. C'est un premier jet que
tu retitres, pas un résumé.
"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
from deadair import load  # noqa: E402  (même lecteur de transcript, une seule implémentation)

STOP = set("""
dans pour avec sans sous sont était étaient être avoir avait aurait cette cela celle celui ceux
mais donc alors aussi très bien tout tous toute toutes fait faire fais comme quand comment pourquoi
parce même encore déjà voilà voila genre truc trucs chose choses vraiment juste enfin après avant
leur leurs notre votre nous vous elle elles quoi peut peux faut veut vais allez aller voir dire
vois sais savoir fois chez entre plus moins beaucoup trop rien quelque quelques autre autres dont
suis sommes êtes avez avons sera serait ensuite maintenant aujourd ouais okay bref deux trois
quatre cinq vraie vrai petit petite grand grande vont font disent mettre met mets prendre prends
donne donner regarde regarder ici là oui non bah euh heu hein tiens attends
that this with from your what which when where there here they them have just really very like
about into over then than will would should could make made going were been does didn
""".split())

def keywords(text):
    toks = re.split(r"[^\w]+", text.lower().replace("’", "'"))
    return {w for w in toks if len(w) >= 4 and not w.isdigit() and w not in STOP}

def mmss(t):
    t = int(t); h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def main():
    ap = argparse.ArgumentParser(description="Chapitres YouTube validés à partir d'un transcript.")
    ap.add_argument("transcript", help=".srt, .vtt ou .json de whisper")
    ap.add_argument("--target", "--chapitres", dest="target", type=int, default=7,
                    help="nombre de chapitres visé (7 par défaut)")
    ap.add_argument("--json", action="store_true", help="sortie JSON")
    args = ap.parse_args()
    if not os.path.exists(args.transcript): print(__doc__); sys.exit(1)
    cues = load(args.transcript)
    if len(cues) < 6: print("trop peu de répliques pour faire des chapitres"); sys.exit(1)
    dur = cues[-1][1]
    cand = []
    for i in range(1, len(cues)):
        gap = cues[i][0] - cues[i - 1][1]
        before = " ".join(c[2] for c in cues[max(0, i - 12):i])
        after = " ".join(c[2] for c in cues[i:i + 12])
        kb, ka = keywords(before), keywords(after)
        shift = 1 - (len(kb & ka) / len(kb | ka)) if (kb | ka) else 0
        cand.append((gap * 1.6 + shift * 3.2, cues[i][0], i))
    cand.sort(reverse=True)
    picked, MIN = [0.0], 10.0
    for _, t, i in cand:
        if len(picked) >= args.target: break
        if all(abs(t - p) >= MIN for p in picked) and dur - t >= MIN:
            picked.append(t)
    picked.sort()
    chapters = []
    for n, t in enumerate(picked):
        end = picked[n + 1] if n + 1 < len(picked) else dur
        text = " ".join(c[2] for c in cues if c[0] >= t and c[1] <= end)
        low = text.lower().replace("’", "'")
        kw = sorted(keywords(text), key=lambda w: (-len(re.findall(rf"\b{re.escape(w)}\b", low)), w))
        title = " ".join(w.capitalize() for w in kw[:3]) or "Partie"
        chapters.append({"debut": round(t, 2), "repere": mmss(t), "titre_brouillon": title,
                         "secondes": round(end - t, 2)})
    ok = len(chapters) >= 3 and chapters[0]["debut"] == 0 and all(c["secondes"] >= MIN for c in chapters)
    if args.json:
        print(json.dumps({"valide": ok, "chapitres": chapters}, ensure_ascii=False, indent=1)); return
    print()
    for c in chapters: print(f"  {c['repere']} {c['titre_brouillon']}")
    print(f"\n  {len(chapters)} chapitres"
          f"{'' if ok else '  -- INVALIDE : YouTube veut 3 chapitres ou plus, un premier à 0:00 et 10 s minimum chacun'}")
    print("  Retitre chaque ligne avant de coller. Ce sont les mots du sujet, pas tes mots.\n")

if __name__ == "__main__":
    main()
