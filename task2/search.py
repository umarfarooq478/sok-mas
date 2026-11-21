"""Task 2 step 2: run every query on arXiv, Semantic Scholar, DBLP, OpenAlex; write raw_hits.json.
All responses are cached under task2/cache/, so reruns are offline."""
import json, sys, urllib.parse, xml.etree.ElementTree as ET
from net import get
from queries import QUERIES
NS = {"a": "http://www.w3.org/2005/Atom"}
N = 100
hits = []

def row(src, fam, q, rank, **kw):
    hits.append(dict(source=src, family=fam, query=q, rank=rank, **kw))

def oa_abs(inv):
    if not inv: return ""
    w = {}
    for k, pos in inv.items():
        for p in pos: w[p] = k
    return " ".join(w[i] for i in sorted(w))

for fam, qs in QUERIES.items():
    for q in qs:
        terms = " AND ".join(f"all:{w}" for w in q.split() if len(w) > 2)
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
            {"search_query": terms, "max_results": N, "sortBy": "relevance"})
        raw = get(url, ".xml")
        if raw:
            for r, e in enumerate(ET.fromstring(raw).findall("a:entry", NS)):
                aid = e.find("a:id", NS).text.rsplit("/", 1)[-1]
                row("arxiv", fam, q, r, arxiv=aid.split("v")[0],
                    title=" ".join(e.find("a:title", NS).text.split()),
                    date=e.find("a:published", NS).text[:10],
                    authors=[a.find("a:name", NS).text for a in e.findall("a:author", NS)][:8],
                    abstract=" ".join(e.find("a:summary", NS).text.split()))
        url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(
            {"query": q, "limit": N, "fields": "title,authors,year,venue,externalIds,citationCount,abstract,publicationDate,publicationTypes"})
        raw = get(url)
        if raw:
            for r, p in enumerate(json.loads(raw).get("data", [])):
                x = p.get("externalIds") or {}
                row("s2", fam, q, r, s2=p["paperId"], arxiv=x.get("ArXiv"), doi=x.get("DOI"),
                    title=p.get("title"), date=p.get("publicationDate") or str(p.get("year") or ""),
                    venue=p.get("venue"), citations=p.get("citationCount"),
                    authors=[a["name"] for a in (p.get("authors") or [])][:8], abstract=p.get("abstract") or "")
        url = "https://dblp.org/search/publ/api?" + urllib.parse.urlencode({"q": q, "format": "json", "h": N})
        raw = get(url)
        if raw:
            for r, h in enumerate((json.loads(raw)["result"]["hits"].get("hit") or [])):
                i = h["info"]
                au = i.get("authors", {}).get("author", [])
                au = [au] if isinstance(au, dict) else au
                v = i.get("venue", "")
                row("dblp", fam, q, r, doi=i.get("doi"), title=i.get("title"), date=i.get("year"),
                    venue=v if isinstance(v, str) else ", ".join(v),
                    authors=[a["text"] for a in au][:8], abstract="", dblp=i.get("key"))
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
            {"search": q, "per-page": N, "filter": "from_publication_date:2023-01-01",
             "select": "id,doi,title,publication_date,primary_location,cited_by_count,abstract_inverted_index,authorships,ids"})
        raw = get(url)
        if raw:
            for r, w in enumerate(json.loads(raw).get("results", [])):
                loc = (w.get("primary_location") or {}).get("source") or {}
                doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
                ax = (w.get("ids") or {}).get("arxiv")
                row("openalex", fam, q, r, doi=doi, arxiv=ax.rsplit("/", 1)[-1] if ax else None, title=w.get("title"),
                    date=w.get("publication_date"), venue=loc.get("display_name"), citations=w.get("cited_by_count"),
                    authors=[a["author"]["display_name"] for a in w.get("authorships", [])][:8],
                    abstract=oa_abs(w.get("abstract_inverted_index")))
        print(fam, q, len(hits), file=sys.stderr, flush=True)
json.dump(hits, open("raw_hits.json", "w"), ensure_ascii=False, indent=0)
from collections import Counter
print(len(hits), Counter(h["source"] for h in hits))
