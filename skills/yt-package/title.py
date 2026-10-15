#!/usr/bin/env python3
"""title.py : vérifie la paire titre + miniature d'une vidéo YouTube avant de la publier.

    python3 title.py --title "..." --thumb "L'IA A TOUT FAIT"
    python3 title.py titres.txt                 # un titre par ligne, classés
    python3 title.py --title "..." --json

L'unité, c'est la paire, pas le titre. Un titre qui répète le texte de la miniature gâche la moitié
de la surface de clic : c'est l'erreur la plus courante, et la première que ce script cherche.

Longueur : YouTube coupe vers 60 caractères dans la recherche sur ordinateur et vers 40 sur
l'accueil mobile. Les deux limites sont signalées parce que ce sont deux échecs différents : sur
ordinateur on perd la fin, sur mobile on peut perdre le sujet.
"""
import argparse, json, os, re, sys

DESKTOP, MOBILE, HARD = 60, 40, 100
VAGUE = {"incroyable", "dingue", "fou", "folle", "ouf", "énorme", "ultime", "meilleur", "meilleure",
         "puissant", "puissante", "secret", "secrète", "révolutionnaire", "hallucinant", "épique",
         "parfait", "parfaite", "complet", "complète", "extraordinaire", "magique", "génial",
         "amazing", "incredible", "insane", "crazy", "huge", "massive", "ultimate", "best",
         "powerful", "secret", "revolutionary", "mindblowing", "epic", "perfect", "complete",
         "everything"}
STOP = {"le", "la", "les", "l", "un", "une", "des", "de", "du", "d", "à", "au", "aux", "et", "ou",
        "en", "pour", "par", "sur", "dans", "avec", "est", "sont", "ce", "cet", "cette", "ces", "c",
        "ça", "qui", "que", "qu", "quoi", "ton", "ta", "tes", "tu", "te", "t", "vous", "votre", "vos",
        "mon", "ma", "mes", "je", "j", "me", "m", "il", "elle", "on", "nous", "comment", "pourquoi",
        "a", "ai", "as", "ne", "n", "pas", "plus", "se", "s",
        "the", "an", "of", "for", "to", "in", "and", "or", "is", "are", "with", "your", "you",
        "my", "i", "this", "that", "it", "how", "what", "why"}

def words(t):
    return [w for w in re.split(r"[^\w]+", t.lower().replace("’", "'")) if w]

def check(title, thumb=None):
    t = title.strip()
    n = len(t)
    issues, good = [], []
    if n > HARD: issues.append(("longueur", f"{n} caractères : la limite dure de YouTube est {HARD}"))
    elif n > DESKTOP: issues.append(("longueur", f"{n} caractères : la recherche sur ordinateur coupe vers {DESKTOP}"))
    else: good.append(f"{n} caractères, sous la coupe ordinateur de {DESKTOP}")
    if n > MOBILE:
        head = t[:MOBILE].rsplit(" ", 1)[0]
        issues.append(("mobile", f"l'accueil mobile affiche environ « {head}... » : vérifie que le sujet survit"))
    caps = [w for w in t.split() if len(w) > 2 and w.isupper()]
    if len(caps) > 2: issues.append(("majuscules", f"{len(caps)} mots en capitales : deux, c'est le plafond avant que ça sonne spam"))
    elif caps: good.append(f"{len(caps)} mot en capitales pour l'accent" if len(caps) == 1
                           else "2 mots en capitales pour l'accent")
    v = [w for w in words(t) if w in VAGUE]
    if v: issues.append(("flou", f"{', '.join(sorted(set(v)))} : remplace par un chiffre, un nom ou une date"))
    nums = re.findall(r"\d[\d  ,.]*%?", t)
    nums = [x.strip() for x in nums if x.strip()]
    if nums: good.append(f"porte un chiffre concret ({', '.join(nums[:3])})")
    else: issues.append(("sans-chiffre", "ni chiffre, ni date, ni nom : la correction la plus fiable"))
    if t.endswith("?"): good.append("question ouverte dans le titre")
    front = [w for w in words(t)[:3] if w not in STOP]
    if not front: issues.append(("ouverture", "les trois premiers mots sont du remplissage : avance le sujet"))
    if thumb:
        tw, hw = set(words(t)) - STOP, set(words(thumb)) - STOP
        shared = tw & hw
        if shared:
            issues.append(("doublon", f"la miniature répète le titre sur {', '.join(sorted(shared))} : "
                                      "la miniature doit dire ce que le titre ne dit pas"))
        else:
            good.append("titre et miniature portent des mots différents")
        if len(words(thumb)) > 4:
            issues.append(("miniature", f"{len(words(thumb))} mots sur la miniature : trois, c'est le plafond en taille fil"))
    score = max(0, min(100, 100 - 14 * len(issues) + 4 * len(good)))
    return {"titre": t, "caracteres": n, "score": score,
            "problemes": [{"type": k, "detail": m} for k, m in issues], "ok": good}

def show(r):
    print(f'\n  « {r["titre"]} »')
    print(f"  {r['caracteres']} caractères   score {r['score']}/100")
    for p in r["problemes"]: print(f"    x  {p['type']:<13} {p['detail']}")
    for m in r["ok"]:        print(f"    ok               {m}")

def main():
    ap = argparse.ArgumentParser(description="Vérifie la paire titre + miniature.")
    ap.add_argument("fichier", nargs="?", help="un titre par ligne")
    ap.add_argument("--title", "--titre", dest="title", help="un seul titre")
    ap.add_argument("--thumb", "--miniature", dest="thumb", help="le texte de la miniature")
    ap.add_argument("--json", action="store_true", help="sortie JSON")
    args = ap.parse_args()
    if args.title:
        rows = [check(args.title, args.thumb)]
    elif args.fichier and os.path.exists(args.fichier):
        rows = [check(l, args.thumb) for l in open(args.fichier, encoding="utf-8").read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1)
    rows.sort(key=lambda r: -r["score"])
    if args.json: print(json.dumps(rows, ensure_ascii=False, indent=1)); return
    for r in rows: show(r)
    print()

if __name__ == "__main__":
    main()
