"""Task 2: merge snowball decisions, write 02_corpus.csv and stage counts."""
import json, csv, re, collections
rows = json.load(open("corpus_stage2.json")); sb = json.load(open("snowball_review.json"))
INC = [4,13,16,17,18,22,25,33,35,36,38,39,49,53,54,55,56,57,64,67,70,75,77,79,88,97,102,103,106,108,111,113,114,118,131,132,135,137,139,140,141,144,145,148,149]
MAYBE = [15,29,31,40,72,86,95,99,104,107,109,120,125,136,142]
RELATED = [14,24,28,42,47,50,51,52,71,82,83,85,100,101,146,26,20]
DUP = [5]
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
have = {norm(r["title"]) for r in rows}
added = 0
for x in sb:
    i = x["sidx"]
    if i in INC: st, why = "include", ""
    elif i in MAYBE: st, why = "maybe", "M2 borderline after title screen: scope or evidence unclear; decide at coding"
    elif i in RELATED: st, why = "exclude", "R1 related work only: survey / SoK / position (not coded)"
    elif i in DUP: st, why = "exclude", "X8 duplicate of another record (same paper, different title)"
    else: st, why = "exclude", "X7 snowball title screen: application framework, capability study, single-agent, or no failure/attack/defense evidence"
    rows.append(dict(id=x["arxiv"] or x["doi"] or x["oa"], arxiv=x["arxiv"], doi=x["doi"], title=x["title"], authors="; ".join(x["authors"]), year=x["date"][:4], date=x["date"],
        venue=x["venue"], citations_openalex=x["citations"] if x["citations"] is not None else "", tier=x["tier"], status=st, reason=why, screened_by="manual-title",
        sources="snowball", families="snowball", n_queries=0, grey="", stage="snowball"))
    added += st in ("include", "maybe")
print("snowball added", added)
# mark grey literature flag: framework bug studies / incident-type evidence (kept in the corpus, counted separately)
GREY = re.compile(r"bugs? in|understanding bugs|characterizing faults|demystifying the lifecycle|issues of multi-agent|failure patterns|CVE", re.I)
for r in rows:
    if r["status"] in ("include", "maybe") and GREY.search(r["title"]): r["grey"] = "framework-bug-study"
# documented overrides (boundary cases)
OVERRIDE = {"2605.19240": ("maybe", "M3 boundary: posted 2026-05-19, 3 days before the Tier 2 window (2026-05-22); relevant defense paper, decide at coding")}
for r in rows:
    if r["arxiv"] in OVERRIDE: r["status"], r["reason"] = OVERRIDE[r["arxiv"]]; r["tier"] = "T2-boundary"
cols = ["id","arxiv","doi","title","authors","year","date","venue","citations_openalex","tier","status","reason","screened_by","stage","sources","families","n_queries","grey"]
rows.sort(key=lambda r: ({"include": 0, "maybe": 1, "exclude": 2}[r["status"]], r["date"]), reverse=False)
with open("02_corpus.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
c = collections.Counter(r["status"] for r in rows)
print(c, "total", len(rows))
inc = [r for r in rows if r["status"] == "include"]
print("tiers", collections.Counter(r["tier"] for r in inc)); print("grey", sum(bool(r["grey"]) for r in rows if r["status"] in ("include","maybe")))
print("by year", sorted(collections.Counter(r["year"] for r in inc).items()))
print("exclusion reasons", collections.Counter(r["reason"].split()[0] for r in rows if r["status"] == "exclude"))
