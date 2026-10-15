"""Vérifie que les sept outils tournent sur les exemples français, et que le repo tient ses promesses.

    python3 -m unittest discover tests
"""
import importlib.util, json, os, re, subprocess, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
EX = os.path.join(ROOT, "exemples")

# Les outils PlugKit que le pack a le droit de citer : ils existent dans le serveur MCP.
PLUGKIT_TOOLS = {
    "whoami", "list_accounts", "list_media", "upload_media", "create_media_upload",
    "check_media_upload", "get_publish_options", "create_post", "list_posts", "update_post",
    "publish_post", "list_engagement", "sync_engagement", "reply_to_engagement", "hide_comment",
    "get_post_analytics", "get_top_posts", "get_analytics_summary", "get_analytics_timeseries",
    "get_best_times_to_post", "get_follower_stats", "reel_guide", "reel_create", "reel_status",
    "reel_preview", "reel_render", "reel_revise", "reel_hooks", "reel_cut",
}
PLUGKIT_LINK = "https://www.plugkit.co/fr?utm_source=github&utm_campaign=youtube-agent-skill"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(script, *args):
    out = subprocess.run([sys.executable, "-I", os.path.join(SKILLS, script), *args],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise AssertionError(f"{script} a échoué ({out.returncode}) :\n{out.stderr}")
    return out.stdout


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def text_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f.endswith((".md", ".py", ".json", ".txt", ".srt", ".csv")) or f in ("LICENSE", ".gitignore"):
                yield os.path.join(base, f)


hs = load("hookscore", os.path.join(SKILLS, "yt-script", "hookscore.py"))


class Formules(unittest.TestCase):
    def test_vingt_et_une(self):
        data = json.loads(read(os.path.join(SKILLS, "yt-script", "hooks.json")))
        ids = [h["id"] for h in data["hooks"]]
        self.assertEqual(len(ids), 21)
        self.assertEqual(len(set(ids)), 21)

    def test_chaque_exemple_est_sa_formule_sans_piege(self):
        for f in hs.FORMULAS:
            for p in f["match"]:
                re.compile(p, re.I)
            name, hits = hs.classify(f["example"])
            self.assertEqual(name, f["name"], f["example"])
            _, _, _, pieges = hs.run(f["example"])
            self.assertEqual(pieges, [], f["example"])


class HookScore(unittest.TestCase):
    def test_classement(self):
        rows = json.loads(run("yt-script/hookscore.py", os.path.join(EX, "hooks.txt"), "--json"))
        self.assertEqual(len(rows), 5)
        worst = min(rows, key=lambda r: r["score"])
        self.assertTrue(worst["hook"].startswith("Salut"))
        self.assertEqual(worst["verdict"], "FAIBLE")
        self.assertTrue(any("Salutation" in p for p in worst["pieges"]))
        best = max(rows, key=lambda r: r["score"])
        self.assertEqual(best["formule"], "La Question")
        self.assertIn("vidéo", best["hook"])            # accents intacts

    def test_premiere_phrase_et_pieges(self):
        r = json.loads(run("yt-script/hookscore.py", "--json", "--hook",
                           "Si tu as moins de 1 000 abonnés, arrête tout. Voilà pourquoi."))
        self.assertEqual(r["phrase_notee"], "Si tu as moins de 1 000 abonnés, arrête tout.")
        self.assertTrue(any("Si tu" in p for p in r["pieges"]))
        vague = json.loads(run("yt-script/hookscore.py", "--json", "--hook",
                               "Une méthode incroyable pour exploser sur YouTube."))
        self.assertNotEqual(vague["verdict"], "FORT")

    def test_poids_calibres_charges(self):
        self.assertIsNotNone(hs._POIDS)
        self.assertEqual(hs._POIDS["corpus"]["reels"], 623)


class AntiIA(unittest.TestCase):
    def test_nettoie_et_signale(self):
        src = os.path.join(EX, "description-brouillon.txt")
        out = json.loads(run("yt-script/antiia.py", src, "--json"))
        text, report = out["text"], out["report"]
        self.assertNotIn("booster", text)
        self.assertIn("augmenter", text)
        self.assertIn("chaîne", text)
        self.assertIn("https://exemple.com/template", text)
        names = " ".join(s["name"] for s in report["structures"])
        self.assertIn("Ce n'est pas X, c'est Y", names)
        self.assertIn("Préambule vidéo", names)

    def test_tiret_cadratin_remplace(self):
        anti = load("antiia", os.path.join(SKILLS, "yt-script", "antiia.py"))
        lex = anti.load_lexicon()
        clean, _ = anti.humanize("Ta miniature \u2014 et ton titre \u2014 se répètent.", lex)
        self.assertNotIn("\u2014", clean)
        self.assertIn("miniature, et ton titre, se répètent", clean)


class Titre(unittest.TestCase):
    def test_paire_en_francais(self):
        r = json.loads(run("yt-package/title.py", "--json", "--title", "Ma chaîne gérée par Claude",
                           "--thumb", "CLAUDE GÈRE MA CHAÎNE"))[0]
        kinds = {p["type"] for p in r["problemes"]}
        self.assertIn("doublon", kinds)
        self.assertIn("chaîne", next(p["detail"] for p in r["problemes"] if p["type"] == "doublon"))

    def test_fichier_de_titres(self):
        rows = json.loads(run("yt-package/title.py", os.path.join(EX, "titres.txt"), "--json"))
        shout = next(r for r in rows if r["titre"].startswith("LA MÉTHODE"))
        kinds = {p["type"] for p in shout["problemes"]}
        self.assertTrue({"majuscules", "flou"} <= kinds)
        self.assertEqual(rows[0]["titre"], "Pourquoi tes vidéos meurent à 30 secondes ?")


class Coupes(unittest.TestCase):
    def test_liste_de_coupes(self):
        r = json.loads(run("yt-edit/deadair.py", os.path.join(EX, "rush.srt"), "--json"))
        tics = [c["pourquoi"] for c in r["coupes"] if c["type"] == "TIC"]
        self.assertIn("Euh...", tics)
        self.assertIn("Du coup.", tics)
        reprises = [c for c in r["coupes"] if c["type"] == "REPRISE"]
        self.assertTrue(reprises)
        self.assertIn("le titre il faut", reprises[0]["pourquoi"])
        self.assertGreaterEqual(sum(1 for c in r["coupes"] if c["type"] == "BLANC"), 5)
        self.assertLess(r["reste"], r["duree"])


    def test_sous_titres_auto_youtube(self):
        da = load("deadair", os.path.join(SKILLS, "yt-edit", "deadair.py"))
        cues = da.load(os.path.join(EX, "sous-titres-auto.vtt"))
        self.assertEqual([c[2] for c in cues], ["Tes vidéos perdent la moitié des gens",
                                                "avant trente secondes.", "Et ce n'est pas ton sujet."])
        r = json.loads(run("yt-edit/deadair.py", os.path.join(EX, "sous-titres-auto.vtt"), "--json"))
        self.assertFalse([c for c in r["coupes"] if c["type"] == "REPRISE"])


class Chapitres(unittest.TestCase):
    def test_valides(self):
        r = json.loads(run("yt-seo/chapters.py", os.path.join(EX, "rush.srt"), "--target", "5", "--json"))
        self.assertTrue(r["valide"])
        self.assertEqual(r["chapitres"][0]["debut"], 0)
        self.assertGreaterEqual(len(r["chapitres"]), 3)

    def test_accents(self):
        ch = load("chapters", os.path.join(SKILLS, "yt-seo", "chapters.py"))
        kw = ch.keywords("L'écran était génial, la miniature aussi.")
        self.assertTrue({"écran", "génial", "miniature"} <= kw)
        self.assertNotIn("cran", kw)
        self.assertNotIn("était", kw)


class Retention(unittest.TestCase):
    def test_virgule_decimale(self):
        rt = load("retention", os.path.join(SKILLS, "yt-retention", "retention.py"))
        self.assertEqual(rt.to_number("45,3", ";"), 45.3)
        self.assertEqual(rt.to_number("45,3 %", ","), 45.3)
        self.assertEqual(rt.to_number("1,234", ","), 1234)
        self.assertEqual(rt.to_number("1 234,5", ";"), 1234.5)
        self.assertEqual(rt.to_number("1:30", ";"), 90)

    def test_export_fr_egal_export_en(self):
        fr = json.loads(run("yt-retention/retention.py", os.path.join(EX, "retention-fr.csv"),
                            "--duration", "107", "--json"))
        en = json.loads(run("yt-retention/retention.py", "--duration", "107",
                            os.path.join(EX, "retention-en.csv"), "--json"))
        self.assertEqual(fr, en)
        self.assertEqual(fr["points"], 101)
        self.assertGreater(fr["fuite_hook"], 25)
        self.assertTrue(fr["falaises"])

    def test_transcript_aux_falaises(self):
        r = json.loads(run("yt-retention/retention.py", os.path.join(EX, "retention-fr.csv"),
                           "--duration", "107", "--transcript", os.path.join(EX, "rush.srt"), "--json"))
        self.assertTrue(any("miniature" in t or "Trois mots" in t for t in r["dit"].values()))


class Viralite(unittest.TestCase):
    def test_multiples_et_ytdlp(self):
        r = json.loads(run("yt-viral/swipe.py", os.path.join(EX, "niche.json"),
                           os.path.join(EX, "chaine-ytdlp.json"), "--min", "2", "--json"))
        top = r["outliers"][0]
        self.assertEqual(top["titre"], "Pourquoi tes vidéos meurent à 30 secondes ?")
        self.assertEqual(top["formule"], "La Question")
        self.assertIn("Studio Débutant", {o["chaine"] for o in r["outliers"]})
        self.assertIn(["Petite Chaîne", 2], r["chaines_ignorees"])
        self.assertTrue(all(o["formule"] != "Non classé" for o in r["outliers"]))


class Repo(unittest.TestCase):
    def test_onze_skills(self):
        dirs = sorted(d for d in os.listdir(SKILLS) if d.startswith("yt-"))
        self.assertEqual(len(dirs), 11)
        for d in dirs:
            head = read(os.path.join(SKILLS, d, "SKILL.md")).split("---")[1]
            self.assertIn(f"name: {d}", head)

    def test_aucun_tiret_cadratin(self):
        for path in text_files():
            self.assertNotIn("\u2014", read(path), path)

    def test_outils_plugkit_existent(self):
        cited = set()
        for path in text_files():
            if path.endswith(".md"):
                cited |= set(re.findall(r"`([a-z]+(?:_[a-z]+)+)`", read(path)))
        self.assertTrue(cited)
        self.assertEqual(cited - PLUGKIT_TOOLS, set())

    def test_lien_plugkit_unique(self):
        for path in text_files():
            for url in re.findall(r"https?://(?:www\.)?plugkit\.co[^\s)\"'`]*", read(path)):
                self.assertEqual(url, PLUGKIT_LINK, path)


if __name__ == "__main__":
    unittest.main()
