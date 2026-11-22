"""Task 2 step 4: backward + forward snowballing from the 20 most-cited included papers (OpenAlex, cached)."""
import json, urllib.parse, sys
from net import get
rows = json.load(open("corpus_stage2.json"))
cf = json.load(open("citations_filled.json"))
inc = [r for r in rows if r["status"] == "include"]
def cites(r):
    v = r["citations_openalex"]
    return v if isinstance(v, int) else 0
top = sorted(inc, key=cites, reverse=True)[:20]
SEL = "id,doi,title,publication_date,cited_by_count,primary_location,abstract_inverted_index,authorships,ids,referenced_works"
cands = {}   # openalex id -> record
log = []
def oa_abs(inv):
    if not inv: return ""
    w = {}
    for k, pos in inv.items():
        for p in pos: w[p] = k
    return " ".join(w[i] for i in sorted(w))
def add(w, how, seed):
    loc = (w.get("primary_location") or {}).get("source") or {}
    ax = (w.get("ids") or {}).get("arxiv")
    c = cands.setdefault(w["id"], dict(oa=w["id"], title=w.get("title"), date=w.get("publication_date") or "", venue=loc.get("display_name") or "",
        citations=w.get("cited_by_count"), arxiv=ax.rsplit("/", 1)[-1] if ax else "", doi=(w.get("doi") or "").replace("https://doi.org/", ""),
        abstract=oa_abs(w.get("abstract_inverted_index")), authors=[a["author"]["display_name"] for a in w.get("authorships", [])][:4], via=[]))
    c["via"].append(f"{how}:{seed}")
for r in top:
    a = r["arxiv"]
    key = ("10.48550/arXiv." + a) if a else r["doi"]
    if not key: log.append((r["title"], "no id")); continue
    raw = get(f"https://api.openalex.org/works/https://doi.org/{key}?select={SEL}")
    if not raw:
        raw = get("https://api.openalex.org/works?" + urllib.parse.urlencode({"search": r["title"], "per-page": 1, "select": SEL}))
        w = (json.loads(raw).get("results") or [None])[0] if raw else None
    else: w = json.loads(raw)
    if not w: log.append((r["title"], "not found")); continue
    refs = w.get("referenced_works", [])
    for i in range(0, len(refs), 50):
        raw = get("https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": "openalex:" + "|".join(x.rsplit("/", 1)[-1] for x in refs[i:i+50]), "per-page": 50, "select": SEL}))
        for x in (json.loads(raw).get("results", []) if raw else []): add(x, "ref", a or key)
    raw = get("https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": "cites:" + w["id"].rsplit("/", 1)[-1] + ",from_publication_date:2023-01-01", "per-page": 100, "select": SEL, "sort": "cited_by_count:desc"}))
    for x in (json.loads(raw).get("results", []) if raw else []): add(x, "cit", a or key)
    log.append((r["title"], f"refs={len(refs)} total_cands={len(cands)}"))
    print(log[-1], file=sys.stderr, flush=True)
json.dump(list(cands.values()), open("snowball_raw.json", "w"), ensure_ascii=False, indent=0)
json.dump([dict(title=r["title"], arxiv=r["arxiv"], citations=cites(r)) for r in top], open("snowball_seeds.json", "w"), indent=1)
print(len(cands))
