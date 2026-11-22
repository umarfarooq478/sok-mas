"""Task 2 follow-up: add Semantic Scholar-only finds to the corpus. Run after stage4.py. Idempotent (matches by title)."""
import csv, json, re
rows = list(csv.DictReader(open("../02_corpus.csv"))); cols = list(rows[0].keys())
rv = json.load(open("s2_review.json"))
INC = [6,46,52,61,75,102,105,108,110]; MAY = [20,49,69,103,106]; DUP = [13]
have = {r["title"] for r in rows}
added = collections = 0
for x in rv:
    j = x["j"]
    if x["title"] in have: continue
    if j in INC: st, why = "include", ""
    elif j in MAY: st, why = "maybe", "M2 borderline after title screen: scope or evidence unclear; decide at coding"
    elif j in DUP: st, why = "exclude", "X8 duplicate of another record (same paper, different title)"
    else: st, why = "exclude", "X7 S2 title screen: application framework, capability study, single-agent, or no failure/attack/defense evidence"
    rows.append(dict(id=x.get("arxiv") or x.get("doi") or x["s2"], arxiv=x.get("arxiv") or "", doi=x.get("doi") or "", title=x["title"],
        authors="; ".join(x.get("authors", [])[:4]), year=(x.get("date") or "")[:4], date=x.get("date") or "", venue=x.get("venue") or "",
        citations_openalex=x.get("citations") if x.get("citations") is not None else "", tier=x["tier"], status=st, reason=why,
        screened_by="manual-title", stage="semantic-scholar", sources="s2", families="+".join(sorted({q for q in x["queries"]}))[:0], n_queries=len(x["queries"]), grey=""))
    added += st in ("include", "maybe")
print("added to corpus (include+maybe):", added)
rows.sort(key=lambda r: ({"include": 0, "maybe": 1, "exclude": 2}[r["status"]], r["date"]))
with open("../02_corpus.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)
import shutil, collections as C; shutil.copy("../02_corpus.csv", "02_corpus.csv")
print(C.Counter(r["status"] for r in rows), len(rows))
