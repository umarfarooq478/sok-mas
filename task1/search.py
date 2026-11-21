"""Novelty search for Task 1: arXiv + Semantic Scholar. Writes hits.json."""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET

OUT = sys.argv[1]
QUERIES = [
    "multi-agent LLM failure taxonomy",
    "cascading errors multi-agent LLM",
    "agent coordination failure adversarial",
    "MAST failure modes attack multi-agent",
    "benign and adversarial failures multi-agent LLM",
    "unified taxonomy faults attacks LLM multi-agent systems",
    "error propagation multi-agent LLM robustness faulty agents",
    "reliability and security LLM multi-agent systems survey",
    "survey failures multi-agent large language model systems",
    "systematization of knowledge multi-agent LLM",
    "failure attribution multi-agent LLM",
    "trustworthy LLM multi-agent systems survey taxonomy",
    "LLM multi-agent safety risks taxonomy survey",
    "AutoGen CrewAI LangGraph failures vulnerabilities",
    "accidental versus malicious failures agentic systems",
]
ARX = ("all", )
ns = {"a": "http://www.w3.org/2005/Atom"}
hits = {}

def add(key, rec, q):
    h = hits.setdefault(key, rec)
    h.setdefault("queries", [])
    if q not in h["queries"]:
        h["queries"].append(q)

def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "sok-novelty-search/0.1"})
            return urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:
            print("retry", i, e, file=sys.stderr)
            time.sleep(5 * (i + 1))
    return None

for q in QUERIES:
    terms = " AND ".join(f"all:{w}" for w in q.split() if len(w) > 2)
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": terms, "max_results": 40, "sortBy": "relevance"})
    raw = get(url)
    if raw:
        for e in ET.fromstring(raw).findall("a:entry", ns):
            aid = e.find("a:id", ns).text.rsplit("/", 1)[-1].split("v")[0]
            add("arxiv:" + aid, {
                "src": "arxiv", "id": aid,
                "title": " ".join(e.find("a:title", ns).text.split()),
                "published": e.find("a:published", ns).text[:10],
                "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)][:6],
                "abstract": " ".join(e.find("a:summary", ns).text.split()),
            }, q)
    time.sleep(3.5)
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(
        {"query": q, "limit": 40,
         "fields": "title,authors,year,venue,externalIds,citationCount,abstract,publicationDate"})
    raw = get(url)
    if raw:
        for p in json.loads(raw).get("data", []):
            ext = p.get("externalIds") or {}
            key = ("arxiv:" + ext["ArXiv"]) if ext.get("ArXiv") else ("s2:" + p["paperId"])
            rec = {"src": "s2", "id": ext.get("ArXiv") or p["paperId"], "doi": ext.get("DOI"),
                   "title": p.get("title"), "published": p.get("publicationDate") or str(p.get("year")),
                   "venue": p.get("venue"), "citations": p.get("citationCount"),
                   "authors": [a["name"] for a in (p.get("authors") or [])][:6],
                   "abstract": p.get("abstract") or ""}
            if key in hits:
                hits[key].update({k: v for k, v in rec.items() if v and k in ("venue", "citations", "doi")})
            add(key, rec, q)
    time.sleep(3.5)
    print(q, len(hits), file=sys.stderr)

json.dump(hits, open(OUT, "w", encoding="utf8"), indent=1, ensure_ascii=False)
print("total", len(hits))
