#!/usr/bin/env python3
"""deadair.py : une liste de coupes à partir d'un transcript horodaté.

    python3 deadair.py transcript.srt            # ou .vtt, ou le .json de whisper
    python3 deadair.py transcript.srt --floor 0.35 --json

Trouve trois choses et les imprime comme une liste de coupes, dans l'ordre de la vidéo :
  BLANC     les silences entre deux phrases plus longs que le plancher
  TIC       les répliques qui ne sont que du remplissage (« euh », « du coup », « voilà »)
  REPRISE   une phrase recommencée : la deuxième prise de la même ouverture

CE QU'IL NE FAIT PAS. Il ne coupe pas le fichier. Il imprime la liste, le total qu'elle enlève et
la durée sur laquelle tu atterris, et tu l'appliques dans ton logiciel de montage. Rien ici ne
touche à la vidéo.
"""
import argparse, json, os, re, sys

FILLER_ONLY = re.compile(
    r"^[\s,.!?…-]*((euh+|heu+|hum+|hmm+|bah|ben|bon|alors|voilà|voila|bref|du coup|en fait|genre|"
    r"tu vois|vous voyez|enfin|ok|okay|d['’]accord|ouais|quoi|attends|attendez|voyons|donc|"
    r"um+|uh+|er+|ah+|so|right|yeah|like|anyway|basically|actually|you know|i mean|let me see|"
    r"hold on)[\s,.!?…-]*)+$", re.I)

def parse_ts(s):
    s = s.strip().replace(",", ".")
    p = s.split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2]) if len(p) == 3 else int(p[0]) * 60 + float(p[1])

def load(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    if path.endswith(".json"):
        d = json.loads(raw)
        segs = d.get("segments", []) if isinstance(d, dict) else d
        return [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip()) for s in segs]
    cues, cur = [], None
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
        if m:
            cur = [parse_ts(m.group(1)), parse_ts(m.group(2)), []]
            cues.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit():
            cur[2].append(line.strip())
    if ROLLING.search(raw):
        return rolling_to_cues(cues)
    return [(a, b, " ".join(t)) for a, b, t in cues if t]

# Les sous-titres automatiques que yt-dlp sort de YouTube « roulent » : chaque réplique répète la
# ligne d'avant, porte des balises de minutage par mot, et des répliques de 10 ms font la jonction.
# Lues telles quelles, chaque phrase compterait deux fois (et passerait pour une reprise).
ROLLING = re.compile(r"<\d{2}:\d{2}:\d{2}\.\d{3}>|<c>")

def rolling_to_cues(cues):
    out, last = [], None
    for a, b, lines in cues:
        clean = [re.sub(r"\[[^\]]*\]", "", re.sub(r"<[^>]+>", "", l)).strip() for l in lines]
        clean = [l for l in clean if l]
        fresh = [l for l in clean if l != last]
        if clean: last = clean[-1]
        # la réplique de jonction ne fait que fermer la ligne en cours : elle n'ajoute rien
        if fresh and b - a >= 0.05: out.append((a, b, " ".join(fresh)))
    return out

def norm(t):
    return re.sub(r"[^\w ]", " ", t.lower().replace("’", "'")).split()

def main():
    ap = argparse.ArgumentParser(description="Liste de coupes à partir d'un transcript horodaté.")
    ap.add_argument("transcript", help=".srt, .vtt ou .json de whisper")
    ap.add_argument("--floor", "--plancher", dest="floor", type=float, default=0.45,
                    help="silence minimal à couper, en secondes (0.45 par défaut)")
    ap.add_argument("--json", action="store_true", help="sortie JSON")
    args = ap.parse_args()
    if not os.path.exists(args.transcript): print(__doc__); sys.exit(1)
    cues = load(args.transcript)
    if not cues: print("aucune réplique trouvée : est-ce bien un srt, un vtt ou un json de whisper ?"); sys.exit(1)
    floor = args.floor
    dur = cues[-1][1]
    cuts = []
    for i, (s, e, t) in enumerate(cues):
        if FILLER_ONLY.match(t):
            cuts.append({"type": "TIC", "debut": s, "fin": e, "pourquoi": t.strip()[:48]})
        if i:
            gap = s - cues[i - 1][1]
            if gap > floor:
                # on coupe au MILIEU du silence pour que chaque côté garde une respiration
                keep = floor / 2
                cuts.append({"type": "BLANC", "debut": round(cues[i - 1][1] + keep, 3),
                             "fin": round(s - keep, 3), "pourquoi": f"silence de {gap:.2f} s"})
        # Une reprise se compare à la dernière réplique qui était de la PAROLE. Comparer à la
        # réplique juste avant rate toutes les reprises séparées par un « euh », c'est-à-dire la plupart.
        if t.strip() and not FILLER_ONLY.match(t):
            j = i - 1
            while j >= 0 and (FILLER_ONLY.match(cues[j][2]) or not cues[j][2].strip()): j -= 1
            if j >= 0:
                a1, b1 = norm(cues[j][2])[:5], norm(t)[:5]
                if len(a1) >= 3 and a1 == b1:
                    cuts.append({"type": "REPRISE", "debut": cues[j][0], "fin": cues[j][1],
                                 "pourquoi": f"reprise de « {' '.join(a1)} »"})
    cuts = [c for c in cuts if c["fin"] > c["debut"]]
    cuts.sort(key=lambda c: c["debut"])
    removed = sum(c["fin"] - c["debut"] for c in cuts)
    if args.json:
        print(json.dumps({"source": args.transcript, "duree": dur, "coupes": cuts,
                          "retire": round(removed, 3), "reste": round(dur - removed, 3)},
                         ensure_ascii=False, indent=1)); return
    print(f"\n  {args.transcript}   {dur:.2f} s en entrée, {len(cues)} répliques, plancher de silence {floor} s\n")
    for c in cuts:
        print(f"    {c['type']:<8} {c['debut']:8.2f} -> {c['fin']:8.2f}   {c['fin'] - c['debut']:5.2f} s   {c['pourquoi']}")
    print(f"\n  {len(cuts)} coupes, {removed:.2f} s retirées, {dur - removed:.2f} s à l'arrivée "
          f"({removed / dur * 100:.1f} % plus court)\n")

if __name__ == "__main__":
    main()
