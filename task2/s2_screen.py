"""Task 2 follow-up: dedup Semantic Scholar hits against the corpus, apply rules X0-X6 (with S2 citation counts), write manual-review list."""
import csv, json, re, collections
from screen_rules import screen, FAIL
FAIL2 = re.compile(FAIL.pattern + r"|drift|authoriz|privacy|propagat|guard|heal|collapse|conformity|sycophan|contagion|diagnos|debug|audit|monitor|integrity|misinform", re.I)
hits = json.load(open("raw_hits_s2.json"))
rows = list(csv.DictReader(open("../02_corpus.csv")))
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()
have_t = {norm(r["title"]) for r in rows}; have_a = {r["arxiv"] for r in rows if r["arxiv"]}; have_d = {r["doi"].lower() for r in rows if r["doi"]}
uniq = {}
for h in hits:
    k = h.get("arxiv") or (h.get("doi") or "").lower() or norm(h["title"])
    u = uniq.setdefault(k, dict(h, queries=set()))
    u["queries"].add(h["query"])
print("S2 raw", len(hits), "unique", len(uniq))
MAS2 = re.compile(r"multi[- ]?agent|\bMAS(s|es)?\b|inter-?agent|agent[- ]to[- ]agent|\bA2A\b|multiple (LLM |AI )?agents|sub-?agents?|agents? (collaborat|communicat|interact|coordinat|debate|negotiat|team)|agent (network|societ|swarm)s?|agentic (system|workflow|pipeline|ecosystem|network)s?|orchestrator", re.I)
ARX = re.compile(r"arxiv|corr|ssrn|preprint|research square|zenodo|techrxiv|openreview", re.I)
c = collections.Counter(); keep = []
for k, h in uniq.items():
    if norm(h["title"]) in have_t or (h.get("arxiv") and h["arxiv"] in have_a) or (h.get("doi") and h["doi"].lower() in have_d): c["already in corpus/screened"] += 1; continue
    text = h["title"] + " " + (h.get("abstract") or "")
    st, why = screen(dict(title=h["title"], abstract=h.get("abstract") or "", date=h.get("date") or ""))
    if st == "exclude": c[why[:2]] += 1; continue
    if not (MAS2.search(h["title"]) or (MAS2.search(text) and FAIL2.search(h["title"]))): c["X2b"] += 1; continue
    peer = bool(h.get("venue")) and not ARX.search(h["venue"])
    cites = h.get("citations") or 0
    tier = "T1-venue" if peer else ("T1-citations" if cites >= 10 else ("T2" if h["date"] >= "2026-05-22" else None))
    if not tier: c["X5"] += 1; continue
    keep.append(dict(h, tier=tier, queries=sorted(h["queries"])))
keep.sort(key=lambda x: (x["tier"], x["date"]))
for i, x in enumerate(keep): x["j"] = i
json.dump(keep, open("s2_review.json", "w"), ensure_ascii=False, indent=0)
print(c, "-> manual review", len(keep))
for x in keep: print(f"{x['j']}|{x['date'][:7]}|{x['tier'][:6]}|{x.get('citations')}|{x['title'][:95]}")
