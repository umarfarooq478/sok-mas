"""Task 2 step 3c: merge rule screen + manual decisions into the final per-record table, then known-item recall check."""
import json, csv, re, collections
import decisions_1 as a, decisions_2 as b, decisions_3 as c, decisions_may as m
rule = json.load(open("rule_screened.json"))
rev = json.load(open("review_set.json"))
key = lambda r: (r["title"], r["date"])
inc = set(a.INC) | set(b.INC) | set(c.INC) | set(m.MAY_INC)
dup = {**a.DUP, **b.DUP, **c.DUP}
related = set(c.EXCL_RELATED) | set(m.RELATED)
may_all = set(a.MAY) | set(b.MAY) | set(c.MAY)
status = {}
for r in rev:
    i = r["idx"]
    if i in dup:                 s = ("exclude", "X8 duplicate of another record (replication package / same paper)", "manual-title")
    elif i in related:           s = ("exclude", "R1 related work only: survey / SoK / position / taxonomy without new evidence (not coded)", "manual-abstract" if i in may_all else "manual-title")
    elif i in inc and i in m.MAY_BORDERLINE: s = ("maybe", "M2 borderline after abstract check: scope or evidence unclear; decide at coding", "manual-abstract")
    elif i in inc:               s = ("include", "", "manual-abstract" if i in set(m.MAY_INC) else "manual-title")
    elif i in may_all:           s = ("exclude", "X7 abstract screen: single-agent, capability/application paper, or no failure/attack/defense evidence", "manual-abstract")
    else:                        s = ("exclude", "X7 title screen: application framework, capability study, single-agent, or no failure/attack/defense evidence", "manual-title")
    status[(r["title"], r["date"])] = s
rows = []
for r in rule:
    k = (r["title"], r["date"])
    if k in status: st, why, by = status[k]
    else: st, why, by = "exclude", r["rule_reason"], "rule"
    rows.append(dict(id=r["arxiv"] or r["doi"] or "", arxiv=r["arxiv"] or "", doi=r["doi"] or "", title=r["title"], authors="; ".join(r["authors"][:4]),
        year=r["date"][:4], date=r["date"], venue=r["venue"], citations_openalex=r["citations"] if r["citations"] is not None else "",
        tier=r.get("tier") or "", status=st, reason=why, screened_by=by, sources="+".join(r["sources"]),
        families="+".join(r["families"]), n_queries=len(r["queries"]), grey="", stage="screening"))
# duplicate titles among includes (different ids, same title)
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
seen = {}
for x in rows:
    if x["status"] in ("include", "maybe"):
        n = norm(x["title"])
        if n in seen:
            x["status"] = "exclude"; x["reason"] = "X8 duplicate of another record (same title)"
        else: seen[n] = x
json.dump(rows, open("corpus_stage1.json", "w"), ensure_ascii=False, indent=0)
print(collections.Counter(x["status"] for x in rows))
print(collections.Counter(x["tier"] for x in rows if x["status"] in ("include", "maybe")))
# known-item recall check (papers identified in Task 1 as belonging to the corpus)
known = {"2503.13657":"MAST","2505.00212":"Who&When","2408.00989":"Faulty agents","2511.10400":"BFT","2603.04474":"From Spark to Fire","2608.00718":"Bappy pipelines",
 "2601.14667":"INFA-Guard","2602.19843":"MAS-FIRE","2603.06847":"Faults in agentic AI (385)","2604.08906":"409 framework bugs","2605.19240":"CASPIAN","2611.23362":"TRACE-MAS",
 "2606.07937":"Hallucination cascade","2607.21912":"Error contagion network","2610.32060":"Communication failures 3211 traj","2610.15459":"Communication faults","2512.18733":"XG-Guard","2606.08162":"Silent failure"}
byid = {x["arxiv"]: x for x in rows if x["arxiv"]}
print("\nKNOWN-ITEM RECALL")
for k, n in known.items():
    x = byid.get(k)
    print(f"  {k:11} {n:34} ->", f"{x['status']} ({x['reason'][:60]})" if x else "NOT RETRIEVED")
