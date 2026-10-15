#!/usr/bin/env python3
"""retention.py : lit l'export de rétention d'audience de YouTube Studio et trouve les fuites.

    python3 retention.py retention.csv
    python3 retention.py retention.csv --duration 600                # durée de la vidéo en secondes
    python3 retention.py retention.csv --transcript transcript.srt   # ce que tu disais à chaque chute
    python3 retention.py retention.csv --json

Le fichier sort de Studio : la vidéo > Statistiques > Engagement > le graphique de fidélisation de
l'audience > l'icône de téléchargement. Deux colonnes utiles : une position (en pourcentage ou en
secondes) et le pourcentage de gens encore là.

Le lecteur accepte les exports français comme anglais : séparateur virgule, point-virgule ou
tabulation ; virgule ou point décimal (« 45,3 » reste 45,3) ; positions en « 1:30 » ; valeurs en
ratio (0,453) ramenées en pourcentage.

Il sort trois choses, parce que ce sont trois problèmes différents avec trois corrections différentes :
  FUITE DU HOOK   ce que tu perds dans les 30 premières secondes
  FALAISES        les chutes raides d'un seul coup : un moment précis où les gens partent
  GLISSADE        la perte régulière sur le milieu plat

Avec --transcript, il imprime ce que tu disais à chaque falaise : la seule version de ce rapport sur
laquelle tu peux agir sans repasser la vidéo toi-même.
"""
import argparse, csv, io, json, os, re, sys

def to_number(cell, delim):
    c = cell.strip().replace("%", "").replace(" ", "").replace(" ", "").strip()
    if not c: return None
    m = re.fullmatch(r"(\d+):(\d{2})(?::(\d{2}))?", c)
    if m:
        a, b, d = m.groups()
        return int(a) * 3600 + int(b) * 60 + int(d) if d else int(a) * 60 + int(b)
    c = re.sub(r"(?<=\d) (?=\d{3}\b)", "", c)          # 1 234 -> 1234
    if "," in c and "." in c:
        # le dernier des deux est le séparateur décimal
        if c.rfind(",") > c.rfind("."): c = c.replace(".", "").replace(",", ".")
        else: c = c.replace(",", "")
    elif "," in c:
        # « 1,234 » dans un csv à virgules = milliers à l'anglaise ; partout ailleurs, virgule décimale
        if delim == "," and re.fullmatch(r"-?\d{1,3}(,\d{3})+", c): c = c.replace(",", "")
        else: c = c.replace(",", ".")
    try: return float(c)
    except ValueError: return None

def sniff_delimiter(text):
    head = "\n".join(text.splitlines()[:20])
    counts = {d: head.count(d) for d in (";", "\t", ",")}
    if counts[";"] or counts["\t"]:
        return ";" if counts[";"] >= counts["\t"] else "\t"
    return ","

def load_csv(path):
    text = open(path, encoding="utf-8-sig", errors="replace").read()
    delim = sniff_delimiter(text)
    rows = []
    for r in csv.reader(io.StringIO(text), delimiter=delim):
        vals = [n for n in (to_number(c, delim) for c in r) if n is not None]
        if len(vals) >= 2: rows.append((vals[0], vals[1]))
    if rows:
        xs = [x for x, _ in rows]; ys = [y for _, y in rows]
        if max(xs) <= 1.0: rows = [(x * 100, y) for x, y in rows]                # position en ratio
        if max(ys) <= 1.5 and min(ys) >= 0: rows = [(x, y * 100) for x, y in rows]  # rétention en ratio
    return rows

def main():
    ap = argparse.ArgumentParser(description="Lit un export de rétention YouTube Studio.")
    ap.add_argument("csv", help="l'export de rétention d'audience")
    ap.add_argument("--duration", "--duree", dest="duration", type=float,
                    help="durée de la vidéo en secondes (utile quand l'axe est en pourcentage)")
    ap.add_argument("--transcript", help=".srt, .vtt ou .json de whisper de la même vidéo")
    ap.add_argument("--json", action="store_true", help="sortie JSON")
    args = ap.parse_args()
    if not os.path.exists(args.csv): print(__doc__); sys.exit(1)
    rows = load_csv(args.csv)
    if len(rows) < 8: print("impossible de lire au moins 8 points dans ce csv"); sys.exit(1)
    xs = [r[0] for r in rows]; ys = [r[1] for r in rows]
    pct_axis = max(xs) <= 100.5
    dur = args.duration
    def at(x): return (x / 100.0 * dur) if (pct_axis and dur) else x
    start = ys[0] or 100.0
    # HOOK : les 30 premières secondes, ou les premiers 10 % quand l'axe est en pourcentage sans durée
    cutoff = 30.0 if not pct_axis else (30.0 / dur * 100 if dur else 10.0)
    hook_end = min((y for x, y in rows if x <= cutoff), default=start)
    hook_leak = start - hook_end
    drops = []
    for i in range(1, len(rows)):
        d = ys[i - 1] - ys[i]
        span = xs[i] - xs[i - 1] or 1
        drops.append((d / span, xs[i - 1], xs[i], d))
    drops.sort(reverse=True)
    cliffs = [{"de": round(a1, 2), "a": round(b1, 2), "perdu": round(d, 2),
               "a_la_seconde": round(at(a1), 1) if (not pct_axis or dur) else None}
              for _, a1, b1, d in drops[:5] if d > 0.8]
    mid = [rate for rate, x0, _, _ in drops if x0 > cutoff]
    slide = sum(mid) / len(mid) if mid else 0
    said = {}
    if args.transcript and os.path.exists(args.transcript):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
        from deadair import load as load_cues
        cues = load_cues(args.transcript)
        for c in cliffs:
            if c["a_la_seconde"] is None: continue
            t = c["a_la_seconde"]
            near = [q[2] for q in cues if q[0] <= t + 4 and q[1] >= t - 4]
            said[str(c["de"])] = " ".join(near)[:140]
    out = {"points": len(rows), "depart": start, "fuite_hook": round(hook_leak, 2),
           "arrivee": ys[-1], "falaises": cliffs, "glissade_par_unite": round(slide, 3), "dit": said}
    if args.json: print(json.dumps(out, ensure_ascii=False, indent=1)); return
    print(f"\n  {args.csv}   {len(rows)} points   {ys[0]:.1f} % -> {ys[-1]:.1f} %\n")
    verdict = "sain" if hook_leak < 25 else "fuit" if hook_leak < 40 else "grave"
    print(f"  FUITE DU HOOK   {hook_leak:.1f} % perdus à l'ouverture   [{verdict}]")
    print( "                  sous 25, c'est sain. Corrige la première phrase avant tout le reste.\n")
    print( "  FALAISES        les moments où les gens sont vraiment partis")
    for c in cliffs:
        where = f"{c['a_la_seconde']:.0f} s" if c["a_la_seconde"] is not None else f"{c['de']} %"
        print(f"    -{c['perdu']:5.1f} %  à {where:>8}" + (f"   « {said.get(str(c['de']), '')} »" if said else ""))
    if not cliffs: print("    aucune plus raide que 0,8 % : la perte est toute en glissade, pas en moments")
    print(f"\n  GLISSADE        {slide:.3f} % par {'seconde' if not pct_axis else '% de la vidéo'} sur le milieu")
    print( "                  une glissade plate, c'est du rythme, pas du fond. Coupe le milieu, ne le réécris pas.\n")

if __name__ == "__main__":
    main()
