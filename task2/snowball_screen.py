"""Apply the same dedup + rule screen + tier rule to snowball candidates; write the manual-review list."""
import json, re, collections
from screen_rules import screen, FAIL
rows = json.load(open("corpus_stage2.json")); cands = json.load(open("snowball_raw.json"))
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()
have_t = {norm(r["title"]) for r in rows}; have_a = {r["arxiv"] for r in rows if r["arxiv"]}; have_d = {r["doi"].lower() for r in rows if r["doi"]}
strong = re.compile(r"multi[- ]?agent|inter-?agent|agent[- ]to[- ]agent|\bA2A\b|multiple (LLM |AI |language model )?agents|agents? (collaborat|communicat|interact|coordinat|debate)|agentic (system|workflow|pipeline|ecosystem|network)s?|agent (network|societ|swarm)s?", re.I)
ARX = re.compile(r"arxiv|corr|ssrn|preprint|research square|zenodo|techrxiv|openreview", re.I)
c = collections.Counter(); keep = []
for x in cands:
    if not x["title"]: c["no title"] += 1; continue
    if norm(x["title"]) in have_t or (x["arxiv"] and x["arxiv"] in have_a) or (x["doi"] and x["doi"].lower() in have_d): c["already in corpus/screened"] += 1; continue
    r = dict(title=x["title"], abstract=x["abstract"], date=x["date"])
    st, why = screen(r)
    if st == "exclude": c["rule:" + why[:2]] += 1; continue
    if not (strong.search(x["title"]) or (strong.search(x["abstract"]) and FAIL.search(x["title"]))): c["rule:X2b"] += 1; continue
    peer = bool(x["venue"]) and not ARX.search(x["venue"])
    tier = "T1-venue" if peer else ("T1-citations" if (x["citations"] or 0) >= 10 else ("T2" if x["date"] >= "2026-05-22" else None))
    if tier is None: c["rule:X5"] += 1; continue
    x["tier"] = tier; keep.append(x)
keep.sort(key=lambda x: (x["tier"], x["date"]))
for i, x in enumerate(keep): x["sidx"] = i
json.dump(keep, open("snowball_review.json", "w"), ensure_ascii=False, indent=0)
print(c, "-> manual review:", len(keep))
with open("snowball_list.txt", "w") as f:
    for x in keep: f.write(f"{x['sidx']}|{x['date'][:7]}|{x['tier']}|{x['title'][:100]}\n")
