#!/usr/bin/env python3
"""swipe.py : classe des vidéos selon combien chacune a battu SA PROPRE chaîne, puis nomme la formule.

    python3 swipe.py niche.json
    python3 swipe.py chaine1.json chaine2.json chaine3.json --min 2.0 --json

Entrée : une liste que tu as collectée, un objet par vidéo :

    [{"channel":"Une chaîne","title":"...","views":412000,"url":"...","duration":613}, ...]

ou directement la sortie de `yt-dlp --flat-playlist -J https://www.youtube.com/@chaine/videos`
(un fichier par chaîne, autant de fichiers que tu veux).

Les vues brutes classent la taille des chaînes, pas les idées. 400 000 vues sur une chaîne de
2 millions d'abonnés, c'est un mardi normal ; 400 000 vues sur une chaîne dont la médiane est à
30 000, c'est ce qu'il faut étudier. Chaque vidéo est donc notée en MULTIPLE DE LA MÉDIANE DE SA
CHAÎNE, ce qui demande au moins quatre vidéos par chaîne pour vouloir dire quelque chose : le script
le dit au lieu de classer du bruit en silence.

La formule vient de skills/yt-script/hooks.json, reconnue sur le TITRE. C'est un jugement sur les
mots affichés, pas une explication de pourquoi la vidéo a marché.
"""
import argparse, json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "..", "yt-script", "hooks.json"), encoding="utf-8"))["hooks"]

def classify(title):
    scored = []
    for i, f in enumerate(FORMULAS):
        n = sum(1 for p in f["match"] if re.search(p, title, re.I))
        if n: scored.append((-n, i, f["name"]))
    scored.sort()
    return scored[0][2] if scored else "Non classé"

def first(d, *keys):
    for k in keys:
        if d.get(k) not in (None, ""): return d[k]
    return None

def flatten(node, channel=None):
    """Aplati une sortie yt-dlp (entries imbriquées) ou une liste maison en vidéos."""
    if isinstance(node, list):
        for x in node: yield from flatten(x, channel)
        return
    if not isinstance(node, dict): return
    ch = first(node, "channel", "chaine", "uploader") or channel
    if isinstance(node.get("entries"), list):
        yield from flatten(node["entries"], ch or node.get("title"))
        return
    if isinstance(node.get("videos"), list):
        yield from flatten(node["videos"], ch)
        return
    views = first(node, "views", "vues", "view_count")
    title = first(node, "title", "titre")
    if title is None or views is None: return
    url = first(node, "url", "webpage_url") or ""
    if url and not url.startswith("http") and node.get("id"):
        url = f"https://www.youtube.com/watch?v={node['id']}"
    yield {"channel": ch or "?", "title": title, "views": float(views or 0), "url": url,
           "duration": first(node, "duration", "duree")}

def main():
    ap = argparse.ArgumentParser(description="Classe les vidéos d'une niche par multiple de la médiane de leur chaîne.")
    ap.add_argument("fichiers", nargs="+", help="un ou plusieurs JSON (liste maison ou sortie yt-dlp)")
    ap.add_argument("--min", dest="lo", type=float, default=1.5, help="multiple minimal affiché (1.5 par défaut)")
    ap.add_argument("--json", action="store_true", help="sortie JSON")
    args = ap.parse_args()
    files = [f for f in args.fichiers if os.path.exists(f)]
    if not files: print(__doc__); sys.exit(1)
    rows = []
    for f in files: rows.extend(flatten(json.load(open(f, encoding="utf-8"))))
    by = {}
    for r in rows: by.setdefault(r["channel"], []).append(r)
    out, thin = [], []
    for ch, vids in by.items():
        views = [v["views"] for v in vids]
        if len(vids) < 4:
            thin.append((ch, len(vids)))
            continue
        med = statistics.median(views)
        for v in vids:
            m = (v["views"] / med) if med else 0
            out.append({"chaine": ch, "titre": v["title"], "vues": int(v["views"]), "mediane": int(med),
                        "multiple": round(m, 2), "formule": classify(v["title"]), "url": v["url"]})
    out = [r for r in out if r["multiple"] >= args.lo]
    out.sort(key=lambda r: -r["multiple"])
    if args.json:
        print(json.dumps({"outliers": out, "chaines_ignorees": thin}, ensure_ascii=False, indent=1)); return
    print(f"\n  {len(rows)} vidéos sur {len(by)} chaînes, outliers à {args.lo}x ou plus\n")
    for r in out[:25]:
        vues = f"{r['vues']:,}".replace(",", " ")
        med = f"{r['mediane']:,}".replace(",", " ")
        print(f"    {r['multiple']:5.2f}x  {vues:>11}  contre {med:>11} de médiane   {r['chaine'][:22]:<22} {r['titre'][:52]}")
        print(f"            {r['formule']}")
    if not out: print("    rien ne passe le seuil : collecte plus de vidéos par chaîne ou baisse --min")
    if thin:
        print(f"\n  {len(thin)} chaîne(s) ignorée(s), moins de 4 vidéos collectées : une médiane sur une")
        print( "  ou deux vidéos n'est pas une médiane : " + ", ".join(f"{c} ({n})" for c, n in thin[:6]))
    counts = {}
    for r in out: counts[r["formule"]] = counts.get(r["formule"], 0) + 1
    if counts:
        print("\n  formules parmi les outliers")
        for f, n in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"    {n:2d}x  {f}")
    print()

if __name__ == "__main__":
    main()
