# Task 2 — Search protocol and corpus

Search run: Nov 21–22, 2026. Corpus freeze date: **Nov 22, 2026** (the scope memo proposed Dec 6; the search ran earlier, so the freeze moves up. Rerun the delta search on Jan 18, 2027.)
Deliverables: this file, `02_corpus.csv` (3,215 records, every one with a status and a reason), `task2/` (scripts, cache, PDFs).

## 1. Status in one paragraph

The corpus holds **350 included papers and 32 "maybe" papers**. That is above the plan's 120–180 target, so a cap rule is needed before Task 3 (Section 8). Two of the five planned databases were not reachable, and most screening was done on titles, so recall and precision both need the checks in Section 7 before anyone cites these numbers in the paper.

## 2. Databases

| Database | Used? | How | Why / why not |
|---|---|---|---|
| arXiv | Yes | Atom API (`export.arxiv.org`), 100 results per query, relevance order | — |
| OpenAlex | Yes | REST API, 100 results per query, filter `from_publication_date:2023-01-01` | Stands in for ACM DL and IEEE Xplore, which have no open API. Also gives citation counts and venues. |
| Semantic Scholar | **No** | Graph API | Returned HTTP 429 for every call from this network (shared free pool). A key was not provided. Task 1 used it, so this is a gap against Task 1's coverage. |
| DBLP | **No** | Search API | Serves a "Making sure you're not a bot" page to scripts. Not bypassed. |
| ACM DL, IEEE Xplore | **No** | — | No open API; not queried. Their papers enter only if OpenAlex or arXiv index them. |
| Google Scholar | No | — | No API. |

Effect: venue-published papers that are not on arXiv and not in OpenAlex's top 100 for any query are the most likely misses. See Section 7.

## 3. Queries

38 queries in four families, each run on arXiv and OpenAlex (`task2/queries.py` is the single source). arXiv queries are built as `all:<word> AND all:<word> …` over words longer than 2 letters. OpenAlex uses the plain string with `search=`.

**A. Benign failures**
1. multi-agent LLM failure taxonomy
2. failure attribution multi-agent LLM
3. fault injection multi-agent LLM
4. error propagation multi-agent LLM
5. hallucination propagation multi-agent LLM
6. cascading errors multi-agent LLM
7. bugs in LLM agent frameworks empirical study
8. multi-agent LLM communication failure
9. role drift specification multi-agent LLM
10. multi-agent debate failure consensus

**B. Adversarial failures**
11. prompt injection multi-agent LLM
12. attack on LLM multi-agent communication
13. memory poisoning multi-agent LLM
14. malicious agent multi-agent LLM defense
15. infectious jailbreak multi-agent propagation
16. orchestrator compromise multi-agent LLM attack
17. tool misuse attack multi-agent LLM
18. collusion LLM agents
19. multi-agent LLM security survey
20. agent protocol vulnerability MCP A2A

**C. Bridge**
21. cascading errors multi-agent LLM adversarial
22. agent coordination failure adversarial
23. MAST failure modes attack multi-agent
24. benign and adversarial failures multi-agent LLM
25. unified taxonomy faults attacks LLM multi-agent systems
26. accidental versus malicious failures agentic systems
27. faulty and malicious agents robustness multi-agent LLM
28. systematization of knowledge multi-agent LLM
29. AutoGen CrewAI LangGraph failures vulnerabilities
30. reliability and security LLM multi-agent systems survey

**D. Defenses** (one family per defense class in the plan)
31. defense multi-agent LLM robustness
32. anomaly detection multi-agent LLM
33. verification agent multi-agent LLM
34. provenance authorization LLM agents
35. Byzantine fault tolerance LLM agents
36. monitoring multi-agent LLM runtime
37. sandboxing isolation LLM agents
38. voting consensus robustness multi-agent LLM

Date range: Jan 1, 2023 to Nov 22, 2026. Search date: Nov 21–22, 2026.

## 4. Screening rules

Applied in this order. Each exclusion carries a code in the `reason` column.

| Code | Rule | Applied by |
|---|---|---|
| X6 | Not English | script |
| X3 | First public version outside 2023-01-01 … freeze date | script |
| X0 | No abstract and title shows neither LLM nor multi-agent | script |
| X1 | No LLM term in title/abstract | script (regex) |
| X2 / X2b | No multi-agent term in abstract (X2); none in the title, or in the abstract without a failure term in the title (X2b) | script (regex) |
| X4 | No failure / attack / defense term | script (regex) |
| X5 | Evidence tier: not peer-reviewed, under 10 citations, and older than 6 months before freeze | script |
| X7 | Out of scope after reading title (or abstract where marked): application framework, capability study, single-agent, or no failure/attack/defense evidence | me |
| X8 | Duplicate of another record | script and me |
| R1 | Survey, SoK or position paper kept as related work, not coded | me |

Include rules are the Task 1 rules: LLM-based; two or more agents whose outputs affect each other; reports a failure, fault or attack with evidence, or proposes and evaluates a detection method or defense; Tier 1 (peer-reviewed, or ≥10 citations) or Tier 2 (arXiv, within 6 months of freeze). Citation counts are OpenAlex's, not Semantic Scholar's, so they can differ from Task 1's rule.

`maybe` (code M2) means the scope or the evidence was unclear after screening. Decide these at coding in Task 3.

The scripts, in run order: `search.py` → `dedup.py` → `screen_rules.py` → (manual screen, decisions in `decisions_*.py`) → `build_corpus.py` → `fill_citations.py` → `stage2.py` → `snowball.py` → `snowball_screen.py` → `stage3.py` → `download_pdfs.py`. All network responses are cached in `task2/cache/`, so a rerun is offline and gives the same raw hits. The manual decisions are recorded as lists of record indices; they are the only part that is not mechanically reproducible.

## 5. Stage counts (for the flow figure)

| Stage | Records |
|---|---|
| Raw hits, arXiv | 1,538 |
| Raw hits, OpenAlex | 3,770 |
| Raw hits, Semantic Scholar / DBLP | 0 / 0 (blocked) |
| **Total raw hits** | **5,308** |
| After deduplication (arXiv id, DOI, normalized title) | **3,064** |
| Excluded by rules X0–X6 (incl. X5 after citation backfill) | 2,117 |
| Reached manual screening | 947 (795 on title, 152 on abstract) |
| – excluded (X7 609, R1 13, X8 4) | 626 |
| – included | 305 |
| – maybe | 16 |
| Snowball candidates (references and citing papers of the 20 most-cited includes) | 1,853 |
| – already in the corpus or already screened | 465 |
| – excluded by rules | 1,237 |
| – reached manual screening | 151 |
| – included / maybe / excluded | 45 / 15 / 91 |
| **Final included** | **350** |
| **Final maybe** | **32** (31 + CASPIAN, see Section 7) |

By tier (included): Tier 1 peer-reviewed venue 135, Tier 1 by citations 80, Tier 2 emerging 135. By year: 2024: 13, 2025: 70, 2026: 267. There are none from 2023. Grey-literature flag (framework bug studies): 6.

Query family that first returned each included paper: A-benign 155, B-adversarial 126, C-bridge 106, D-defense 93 (a paper can come from several), snowball 45.

## 6. Snowballing

Seeds: the 20 included papers with the most OpenAlex citations (list in `task2/snowball_seeds.json`). For each, all its references and all citing papers since 2023 (up to 100 per seed, most cited first) came from OpenAlex. Candidates then went through the same rules and the same manual screen. Snowballing added 60 records (45 include, 15 maybe), about 16% of the corpus. That is a high yield, which says the keyword search missed things (Section 7).

## 7. Checks and known limits

**Known-item recall check.** Task 1 named 18 papers that belong in the corpus. At first only 12 were included. Four problems explain the gap, and all four were fixed:
- OpenAlex had no citation counts for arXiv-only hits, so rule X5 wrongly dropped MAST (803 citations), Who&When (203) and 2 others. I backfilled counts for 246 records and re-screened. 76 records with 10 or more citations went back into manual screening, and 27 of them were then included.
- Two Task 1 papers (faulty agents, silent failure) carried no arXiv id in OpenAlex, so the check by id said "not retrieved". Both were in the screened set. Faulty agents is included. Silent failure (2606.08162) is excluded as related work (R1): it is a theory paper with no new evidence, which fits its use in the scope memo as gap evidence, not as a coded paper.
- CASPIAN (2605.19240) was posted May 19, 2026, three days before the Tier 2 window opens (May 22). A hard cutoff would drop it. It is recorded as `maybe` (code M3) with that reason. The 385-fault study (2603.06847) is now included.
- The check was run once on a small list. A clean result on 18 known papers does not prove recall.

**Limits:**
1. **Semantic Scholar and DBLP are missing** (Section 2). Request a free Semantic Scholar API key and rerun `search.py` with `SOURCES=s2`. The cache means only new calls hit the network.
2. **Screening is mostly on titles.** 795 of 947 manual decisions used the title alone. Includes are labeled `manual-title` (303) or `manual-abstract` (47) in `screened_by`. Spot-check at least 30 includes and 30 X7 exclusions before relying on precision or recall.
3. **Regex rules can drop real papers.** Rules X1, X2, X2b and X4 removed 1,811 records without a human reading them. A paper that never says "multi-agent" in its title or abstract (for example "agentic workflow" or "swarm") is lost. A sample of 50 rule-excluded records should be read.
4. **The corpus leans toward 2026** (267 of 350). Nothing is from 2023 and only 13 are from 2024. This may be a true reflection of the field, or recall for older work is weak. Test it with year-specific queries.
5. **OpenAlex citation counts** are lower than Semantic Scholar's for some papers and missing for others.
6. **51 included records have no venue**, so their Tier 1 status rests on citations alone.
7. **Several Tier 2 records came from one author's series** of single-author syntheses ("Silent Entropy…", "Failure Propagation and Coordination Collapse…", and similar). They were excluded as syntheses with no new evidence. If you disagree, they are easy to add.
8. **Two arXiv records mention withdrawn sources** (CONCAT, arXiv 2605.29612). They were excluded.

## 8. Corpus size (decided Nov 22, 2026)

The plan's "done when" is 120 to 180 included papers. The rules produce 350 (plus 32 maybe).

**Decision: keep all 350.** No cap by tier or relevance. Task 3 pre-codes every paper from its abstract (Claude drafts, you check), as the plan allows. Tier stays a column in `02_corpus.csv`, so findings in Task 6 can still be reported for Tier 1 alone, and the "cap at about 120" fallback in the risk table remains available if coding runs late. The 32 maybe papers are settled at coding time.

## 9. Saved downloads

Everything fetched from the network is stored in the repo so later work needs no network:
- `task2/cache/<host>/`: every API response (arXiv Atom, OpenAlex JSON), with `task2/cache/_index.tsv` mapping each file to its URL.
- `task2/papers/<arXiv-id>.pdf`: the arXiv PDF of each included or maybe paper that has an arXiv id.
- Raw and intermediate files: `raw_hits_*.json`, `deduped.json`, `rule_screened.json`, `review_set.json`, `snowball_raw.json`.
