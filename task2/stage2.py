"""Task 2: apply citation backfill + manual screen of newly eligible records, then add Task 1 seed papers missed by the queries."""
import json, re, urllib.parse, xml.etree.ElementTree as ET
from net import get
rows = json.load(open("corpus_stage1.json")); cf = json.load(open("citations_filled.json"))
BACK_INC = ["2603.06847","2604.02668","2503.13657","2505.00212","2604.02668","2507.22800","2601.07136","2505.11556","2509.23055","2503.12188","2510.14312","2510.10943","2401.11880","2505.11642"]
BACK_MAYBE = ["2602.02475","2510.10581","2507.06850","2508.01332","2507.21146"]
# first-batch titles (no arXiv id in my list above): match by title prefix
BACK_TITLES_INC = ["AgentTrace: Causal Graph Tracing","Diversity Collapse in Multi-Agent","Inter-Agent Trust Models","The Sum Leaks More","Collaboration Dynamics and Reliability Challenges of Multi-Agent","AgentEval: DAG-Structured"]
BACK_TITLES_MAYBE = ["SentinelAgent: Intent-Verified","MAS-ProVe","Comprehensive Vulnerability Analysis is Necessary"]
n = 0
for r in rows:
    if r["arxiv"] in cf and r["reason"].startswith("X5"):
        r["citations_openalex"] = cf[r["arxiv"]]
        if cf[r["arxiv"]] >= 10:
            r["tier"] = "T1-citations"
            hit_inc = r["arxiv"] in BACK_INC or any(r["title"].startswith(t) for t in BACK_TITLES_INC)
            hit_may = r["arxiv"] in BACK_MAYBE or any(r["title"].startswith(t) for t in BACK_TITLES_MAYBE)
            if hit_inc: r["status"], r["reason"], r["screened_by"] = "include", "", "manual-title"; n += 1
            elif hit_may: r["status"], r["reason"], r["screened_by"] = "maybe", "M2 borderline: scope or evidence unclear; decide at coding", "manual-title"; n += 1
            else: r["reason"], r["screened_by"] = "X7 title screen after citation backfill: application framework, capability study, single-agent, or no failure/attack/defense evidence", "manual-title"
        # <10 citations stays X5
print("backfill promoted", n)
# seeds from the Task 1 memo that the queries never returned
SEEDS = {"2408.00989": "Task1 memo: faulty agents (ICML 2025)", "2606.08162": "Task1 memo: silent failure"}
have = {r["arxiv"] for r in rows if r["arxiv"]}
ids = [s for s in SEEDS if s not in have]
if ids:
    raw = get("https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": ",".join(ids)}), ".xml")
    NS = {"a": "http://www.w3.org/2005/Atom"}
    for e in ET.fromstring(raw).findall("a:entry", NS):
        aid = e.find("a:id", NS).text.rsplit("/", 1)[-1].split("v")[0]
        rows.append(dict(id=aid, arxiv=aid, doi="", title=" ".join(e.find("a:title", NS).text.split()),
            authors="; ".join(a.find("a:name", NS).text for a in e.findall("a:author", NS))[:200], year=e.find("a:published", NS).text[:4],
            date=e.find("a:published", NS).text[:10], venue="", citations_openalex="", tier="seed", status="include", reason="",
            screened_by="seed", sources="task1-memo", families="seed", n_queries=0, grey="", stage="seed"))
        print("seed added", aid)
json.dump(rows, open("corpus_stage2.json", "w"), ensure_ascii=False, indent=0)
import collections; print(collections.Counter(r["status"] for r in rows))
