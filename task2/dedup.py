"""Task 2 step 3a: merge raw hits from all sources, deduplicate by arXiv id / DOI / normalized title."""
import json, re, sys, glob, collections
raw = []
for f in sorted(glob.glob("raw_hits_*.json")): raw += json.load(open(f))
def norm(t): return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()
def aid(x):
    a = x.get("arxiv")
    return re.sub(r"v\d+$", "", a) if a else None
recs, by = [], {}
def find(h):
    for k in (("a", aid(h)), ("d", (h.get("doi") or "").lower() or None), ("t", norm(h.get("title")))):
        if k[1] and k in by: return by[k]
    return None
for h in raw:
    if not h.get("title"): continue
    r = find(h)
    if r is None:
        r = dict(ids=set(), title=h["title"], date=h.get("date") or "", venue="", citations=None, authors=h.get("authors") or [],
                 abstract="", sources=set(), queries=set(), families=set(), arxiv=None, doi=None)
        recs.append(r)
    r["sources"].add(h["source"]); r["queries"].add(h["query"]); r["families"].add(h["family"])
    if h.get("arxiv") and not r["arxiv"]: r["arxiv"] = aid(h)
    if h.get("doi") and not r["doi"]: r["doi"] = h["doi"].lower()
    if h.get("venue") and not r["venue"]: r["venue"] = h["venue"]
    if h.get("citations") is not None: r["citations"] = max(r["citations"] or 0, h["citations"])
    if len(h.get("abstract") or "") > len(r["abstract"]): r["abstract"] = h["abstract"]
    if h["source"] == "arxiv" or not r["date"]: r["date"] = h.get("date") or r["date"]
    for k in (("a", aid(h)), ("d", (h.get("doi") or "").lower() or None), ("t", norm(h.get("title")))):
        if k[1]: by[k] = r
    by[("t", norm(r["title"]))] = r
for r in recs:
    for k in ("sources", "queries", "families"): r[k] = sorted(r[k])
    r.pop("ids")
json.dump(recs, open("deduped.json", "w"), ensure_ascii=False, indent=0)
print("raw rows", len(raw), "unique records", len(recs))
print(collections.Counter(tuple(r["sources"]) for r in recs))
print("with abstract", sum(bool(r["abstract"]) for r in recs), "with citations", sum(r["citations"] is not None for r in recs))
