"""Task 2 follow-up (Nov 22): spot-check fixes.
 1. Second-chance review of regex-excluded records (rules X1/X2/X2b/X4/X0) using looser patterns (MAS, LLM-MAS, drift, authoriz, privacy, ...).
 2. Flag artifact releases (code/data archives) among includes.
Idempotent: reads 02_corpus.csv, matches by title, writes it back."""
import csv, json, re
rows = list(csv.DictReader(open("../02_corpus.csv")))
cols = list(rows[0].keys())
sc = json.load(open("second_chance_review.json"))
INC2 = [18,19,63,88,108,110,113,114,115,116,149,154,157,175,184,213,239,248,257,259,260,263,272,355,356]
MAY2 = [44,96,117,125,145,158,174,176,217,232,233,251,255,268,269,275,329]
by = {r["title"]: r for r in rows}
n_inc = n_may = 0
for x in sc:
    r = by[x["title"]]
    if x["k"] in INC2 or x["k"] in MAY2:
        r["status"] = "include" if x["k"] in INC2 else "maybe"
        r["reason"] = "" if x["k"] in INC2 else "M2 borderline after second-chance title screen: scope or evidence unclear; decide at coding"
        r["screened_by"] = "manual-title (second chance)"
        r["stage"] = "second-chance"
        r["tier"] = x["tier2"] if not x["tier2"].startswith("T?") else ("T2" if r["date"] >= "2026-05-22" else "T?-citations-unknown")
        n_inc += x["k"] in INC2; n_may += x["k"] in MAY2
print("second chance: +%d include, +%d maybe" % (n_inc, n_may))
ART = re.compile(r"replication package|code and data|data and code|this release archives|replication package", re.I)
ab = {r["title"]: r["abstract"] for r in json.load(open("deduped.json"))}
flag = []
for r in rows:
    if r["status"] in ("include", "maybe") and (ART.search(r["title"]) or ART.search(ab.get(r["title"], "")[:200])):
        r["grey"] = (r["grey"] + "+" if r["grey"] else "") + "artifact-release"; flag.append(r["title"][:70])
print("artifact releases flagged:", flag)
with open("../02_corpus.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)
import shutil, collections; shutil.copy("../02_corpus.csv", "02_corpus.csv")
print(collections.Counter(r["status"] for r in rows))
print(collections.Counter(r["tier"] for r in rows if r["status"] == "include"))
