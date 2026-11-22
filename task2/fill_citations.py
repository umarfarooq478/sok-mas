"""Fill citation counts for records the keyword search returned without them (arXiv-only hits), via OpenAlex DOI filter (cached)."""
import json, urllib.parse
from net import get
rows = json.load(open("corpus_stage1.json"))
need = [r for r in rows if r["citations_openalex"] == "" and r["arxiv"] and r["reason"].startswith("X5")]
print("need", len(need))
cites = {}
for i in range(0, len(need), 40):
    chunk = need[i:i+40]
    dois = "|".join("https://doi.org/10.48550/arxiv." + r["arxiv"] for r in chunk)
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": "doi:" + dois, "per-page": 50, "select": "doi,cited_by_count,primary_location"})
    raw = get(url)
    if not raw: print("fail chunk", i); continue
    for w in json.loads(raw).get("results", []):
        a = w["doi"].lower().split("arxiv.")[-1]
        cites[a] = w["cited_by_count"]
json.dump(cites, open("citations_filled.json", "w"))
print("filled", len(cites))
