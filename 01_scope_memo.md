# Task 1 — Scope memo

Nov 22, 2026 · Deliverable for Task 1 (scope and novelty check) of the SoK plan
Supporting files: `task1/01_novelty_hits.csv` (129 screened records, one overlap label and reason each), `task1/hits.json` (raw API results), `task1/search.py` and `task1/make_log.py` (rerun scripts).

## 1. Verdict

**The angle holds, but it needs a sharper claim than "first to connect benign and adversarial failures."** No survey or SoK I found organizes multi-agent failures by mechanism and records, for each mechanism, whether benign faults, attackers, or both trigger it, and which defenses have been tested against each trigger. But two 2026 research papers already show that bridge for specific mechanisms (arXiv 2603.04474 for error cascades, arXiv 2608.00718 for four pipeline boundary failures), and the Microsoft AIRT taxonomy and an IJISRT survey list reliability and security failures side by side. The paper should claim the *systematization* and the *defense-by-trigger coverage map*. It should not claim the observation itself.

**One-sentence contribution (the "done when" test):**
> The JHU SoK leaves out benign failures by definition and MAST leaves out attackers. This SoK is the first to map both literatures onto one set of mechanisms. For each mechanism it reports the evidence that bugs, attackers, or both trigger it, and whether any defense has been evaluated against each trigger. Defenses that are only ever tested against one trigger are then the open problems.

## 2. Final title (locked Nov 22, 2026)

**SoK: One Mechanism, Two Triggers — Benign and Adversarial Failures in LLM Multi-Agent Systems**

This replaces the working title, "SoK: Benign and Adversarial Failures in LLM Multi-Agent Systems Share the Same Mechanisms." The old title states the hypothesis as a result, and Task 4 may find mechanisms with only one trigger. The new one names the frame without committing to the outcome, and it starts with "SoK:" as the CFP requires. The title is fixed once the abstract is registered on Jan 19, 2027.

## 3. Research questions

- **RQ1 (mechanisms).** Which mechanisms underlie failures in LLM multi-agent systems, as reported by the reliability (fault, failure-attribution) and security (attack, defense) literatures? The unit is the mechanism (where a failure starts, which interface it crosses, how it spreads), not the symptom.
- **RQ2 (shared triggers).** For which mechanisms does the corpus show both a benign trigger and an adversarial trigger, and do the two share the same locus and propagation path? For which mechanisms has only one community looked?
- **RQ3 (defense coverage).** For each mechanism, which defense families have been *evaluated* against benign triggers, against adversarial triggers, or against both? Which mechanism-by-trigger cells have no evaluated defense?

Operational definition for RQ2, to fix before coding in Task 3: a mechanism counts as **dual-trigger** when at least one included paper shows it arising without an adversary and at least one shows an adversary inducing it at the same locus (same agent role, channel, store, tool, or orchestrator step). One paper showing both, as in 2603.04474, counts as direct evidence. Two separate papers count as indirect evidence. The paper reports the two levels separately.

## 4. Inclusion and exclusion rules

**Include** a work if all of these hold:

1. **LLM-based MAS.** Two or more separately addressable LLM-based agents whose outputs affect one another through messages, shared state, collective decisions, or delegated actions. This matches the JHU SoK system boundary, so the corpora are comparable.
2. **Failure content.** The work reports at least one failure, fault, or attack and gives empirical evidence for it (traces, an experiment, or a documented incident), *or* it proposes and evaluates a detection method or defense for one.
3. **Date.** First public version between Jan 1, 2023 and the corpus freeze date, which Task 2 sets and records (proposed: Dec 6, 2026).
4. **Evidence tier.**
   - *Tier 1:* peer-reviewed (conference, journal, or workshop with archival proceedings), or an arXiv paper with 10 or more citations on Semantic Scholar at the freeze date.
   - *Tier 2 (emerging):* any other arXiv paper posted within 6 months of the freeze date.

   Tier 2 replaces the plan's "from a known lab" rule, which reviewers can call subjective. It follows the JHU SoK's Set 1 / Set 2 split. Counts are reported per tier, and the main findings rest on Tier 1.

**Exclude:**

- single-agent systems, and planner–critic–verifier loops inside one principal (no separate agents);
- non-LLM multi-agent systems (classical MARL, robotics swarms without LLMs);
- capability benchmarks that report task success but no failure analysis;
- position papers and surveys with no new evidence (kept as related work, not coded);
- duplicates (the published version is kept and the arXiv version linked);
- non-English papers.

**Grey literature** goes in a separate column and isn't counted in the paper totals: framework incident reports, CVEs, framework bug studies, vendor taxonomies (Microsoft AIRT, OWASP).

## 5. Positioning against the closest works

| | **JHU SoK** (arXiv 2609.00595, Sep 2026) | **Google SoK** (ARES 2026 Workshops, LNCS, pp. 98–115) | **LASM survey** (arXiv 2604.23338 v2, Apr 2026) | **MAST** (arXiv 2503.13657 v3) | **This SoK** |
|---|---|---|---|---|---|
| Scope | Security of LLM MAS | Security of agentic AI (single- and multi-agent) | Security of LLM agents | Benign MAS failures | Benign **and** adversarial MAS failures |
| Unit of analysis | End-to-end execution path | Execution boundary (layer) | Architectural layer × timescale | Failure mode in a trace | Failure mechanism |
| Taxonomy axes | A-I-R: 4 adversary positions × 6 interfaces × 7 risks; 8 attack paths; 8 configuration dimensions | 5 layers (input, external data, tool and protocol, memory, multi-agent); 4 security invariants | 7 layers × 4 temporality classes | 14 modes in 3 categories (design, inter-agent misalignment, verification) × 3 stages | Mechanism × trigger (benign, adversarial, both) × defense family |
| Evidence base | 197 works (115 Set 1, 82 Set 2); 44 benchmark works audited | 71 papers + 3 CVEs (2022–2026) | 116 papers (2021–2026); single coder, no kappa | 150 traces for the taxonomy (κ = 0.88); 1,600+ traces in MAST-Data, 7 frameworks | target ~150 papers + trace validation (Tasks 2–5) |
| Benign failures | Out of scope by definition: drift and accuracy loss count only if they violate a protected property | Not covered | Not covered | Core subject | Core subject |
| Adversarial failures | Core subject | Core subject | Core subject | Not covered | Core subject |
| Defenses | 4 control primitives, 5-part defense contract | Provenance-conditioned authorization model | 15 defense classes, per-cell coverage | Case-study interventions only | Coverage matrix by mechanism **and** trigger |
| What it leaves out (our opening) | Whether attack paths also occur without an attacker; whether defenses help with faults | Benign failures; MAS beyond one layer | Benign failures; MAS beyond one layer | Attackers; defenses | — |

Notes:
- The JHU SoK's own boundary (Sec. 2.1, and R4 in Sec. 4.2) is the clearest statement of our gap. It counts accuracy loss or drift as a security failure only when it violates a stated protected property. Quote it in the introduction.
- The JHU SoK already cites some fault-oriented work as context: Huang et al. on faulty agents (ICML 2025), the Byzantine fault-tolerance paper by Zheng et al. (AAAI 2026), and RoMa. It doesn't code a benign trigger, though. Our corpus will overlap theirs on the adversarial side. When their corpus is released, reuse it as a cross-check of Task 2 recall rather than rebuilding it.
- Google SoK metadata: Crossref lists the authors as Shuyi Guan, Andrey Kovalev and Li Xie, while the Google Research page lists Andrey Kovalev and Claire Guan. Cite from Crossref (DOI 10.1007/978-3-032-35579-9_6). I couldn't get past the Springer paywall, so the row above rests on the abstract only.
- Venues for MAST and the LASM survey still need checking (Task 9). Both are cited here by their arXiv versions.

**Other partial overlaps that must be cited and differentiated in Related Work:**

| Work | What it does | Why it is not this paper |
|---|---|---|
| Bappy et al., arXiv 2608.00718 (Aug 2026) | Derives 4 attack classes from 147 benign TRAIL traces; shows each can be induced adversarially in a 10-agent pipeline | One study, one pipeline, 4 classes, and no systematization of literature or defenses. It is **evidence for** RQ2 and goes in the corpus. Note that one of its two trace settings (SWE-bench Lite) uses a single agent. |
| Xie et al., arXiv 2603.04474 (Mar 2026) | One propagation model for endogenous error cascades and an injected-seed attack; one defense tested on both | One mechanism (cascade into false consensus). Corpus paper and direct dual-trigger evidence. |
| Microsoft AIRT taxonomy, v1.0 (Apr 2025) and v2.0 (2026) | Failure modes in two pillars, *safety* and *security*, each split into novel and existing | Keeps the pillars apart instead of mapping them onto shared mechanisms. "Safety" there means harm to users and responsible-AI issues, not coordination faults. Built from red teaming and interviews, not a literature review. |
| Vangalapat & Shaikh, IJISRT 2026 (DOI 10.38124/ijisrt/26feb1090) | Catalogs agentic failure modes "across reliability and security dimensions"; 7-layer trust taxonomy and design patterns | Component layers, not mechanisms. No per-mechanism evidence of triggers, no corpus counts, no defense coverage. Low-tier venue, but a reviewer may know it, so cite it. |
| Krawiecka & Schroeder de Witt, arXiv 2508.09815 | OWASP MAS threat-model extension that adds "benign goal drift" and "cross-agent hallucination propagation" as threat classes | Practitioner guidance with no corpus. It supports the motivation: practitioners already treat some benign failures as threats. |
| Liu, arXiv 2606.08162 (Jun 2026) | Silent (non-adversarial) failures | States that the intersection with attacker-triggered failures "is a topic for future work". Direct evidence that the gap is open. |
| Huang et al., ICML 2025 (arXiv 2408.00989); Zheng et al., AAAI 2026 (arXiv 2511.10400) | Treat "clumsy or malicious" agents and erroneous or Byzantine messages under one fault model | Research papers, not systematizations. Corpus papers and bridge evidence. |

## 6. Novelty search log

**Date run:** Nov 22, 2026.
**Sources:**
- arXiv API, 15 queries, 40 results each, by relevance;
- Semantic Scholar Graph API, the same 15 queries, 40 results each;
- 9 web searches (general web, which also surfaced IEEE, ACL Anthology, Springer and ResearchGate pages).

Google Scholar has no API that can be used here. The web searches stand in for it, and that is a stated limitation.

**Queries** (arXiv and Semantic Scholar):
1. multi-agent LLM failure taxonomy
2. cascading errors multi-agent LLM
3. agent coordination failure adversarial
4. MAST failure modes attack multi-agent
5. benign and adversarial failures multi-agent LLM
6. unified taxonomy faults attacks LLM multi-agent systems
7. error propagation multi-agent LLM robustness faulty agents
8. reliability and security LLM multi-agent systems survey
9. survey failures multi-agent large language model systems
10. systematization of knowledge multi-agent LLM
11. failure attribution multi-agent LLM
12. trustworthy LLM multi-agent systems survey taxonomy
13. LLM multi-agent safety risks taxonomy survey
14. AutoGen CrewAI LangGraph failures vulnerabilities
15. accidental versus malicious failures agentic systems

**Web searches:**
- unifying benign and adversarial taxonomy;
- SoK reliability and security with MAST;
- surveys of faults, attacks and propagation;
- surveys of faulty versus malicious agents;
- framework bug studies;
- hallucination and injection propagation;
- Oct–Nov 2026 MAS surveys;
- MAST crosswalk with injection.

**Counts:**

| Stage | Records |
|---|---|
| Unique records from the APIs | 334 |
| After keyword pre-filter (multi-agent or agentic, plus a survey, taxonomy, failure or fault term in the title) | 112 |
| API records outside the pre-filter, kept on manual review | 3 |
| Added from web searches, not returned by the APIs | 14 |
| Screened in total | 129 |
| Overlaps fully | 0 |
| Partly overlap | 12 |
| Don't overlap | 117 |

Each record's label and reason is in `task1/01_novelty_hits.csv`. I read 39 records in more depth (abstract, or full text for the 8 most relevant). The other 90 were screened on title and venue: mostly failure-attribution methods, single-domain surveys and off-topic hits. Their label is the default "no overlap", and the CSV marks them `title-screen` so you can spot-check them.

**Last 6 months (May–Nov 2026), checked most carefully.** Every survey or SoK from this window in the results is single-sided:
- attack-only: the JHU SoK, arXiv 2609.13731, 2608.10530 and 2607.12406, and the KBS 2026 survey;
- benign-only: arXiv 2605.14892, the TSE trajectory-analysis survey, and 2610.32060.

The two bridging studies from this window (2608.00718 and 2606.08162 as gap evidence) are covered in Section 5. The newest relevant records are TRACE-MAS (arXiv 2611.23362, Nov 17) and CoLFA (arXiv 2611.14980). Both are benign-side diagnosis methods.

**Limits of this check.** These are keyword APIs plus web search, so a paper with unusual vocabulary could be missed. Task 2's full protocol and snowballing will widen recall. Rerun the 15 queries on Jan 18, 2027, the week before submission, to catch anything posted in December or January.

## 7. Implications for later tasks

- **Task 2.** Add the benign-side query family (failure attribution, fault injection, error propagation, hallucination cascade, framework bugs). The search returned many 2026 papers in that family, so the corpus may go past 180. If it does, the Tier 1 / Tier 2 split is the place to cap it.
- **Task 3.** The codebook needs a field for *trigger evidence level* (direct dual-trigger in one paper, benign only, adversarial only), and one for *the trigger a defense was evaluated against*. RQ2 and RQ3 depend on them. There is a co-author, so both authors code the same 20% of papers and report Cohen's kappa (target ≥ 0.7). The two trigger fields matter most here, because they are the hardest to code consistently. This also answers a weakness of the LASM survey, which used a single coder and reported no kappa.
- **Task 4.** Add the JHU A-I-R risks and attack paths, and the Microsoft AIRT modes, to the crosswalk next to MAST.
- **Task 5.** Three public trace sources showed up for checking in Task 5: MAST-Data (1,600+ traces), TRAIL (used by 2608.00718), and Who&When (ICML 2025). Host and license for each are still unchecked.
- **Biggest risk.** A reviewer reads the paper as "JHU SoK plus MAST stapled together." The answer is RQ3: the coverage matrix by trigger is the one exhibit neither of them can produce.
