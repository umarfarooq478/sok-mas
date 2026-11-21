# SoK Plan: Failures in Multi-Agent LLM Systems

Nov 22, 2026 · @Shaheer ilyas

## Overview

Submit an SoK to USENIX Security 2027 Cycle 2 on Jan 26, 2027, and post it on arXiv the same week. The plan has 9 tasks over 9 weeks, about 180 hours if you work alone. Each task ends in a file you keep, so even a missed deadline leaves you with a reusable corpus and taxonomy.

**Working title:** SoK: Benign and Adversarial Failures in LLM Multi-Agent Systems Share the Same Mechanisms. This is provisional until Task 1 confirms the angle is new.

**Positioning:** existing SoKs cover attacks only ([JHU SoK, arXiv 2609.00595](https://arxiv.org/pdf/2609.00595); [Google SoK](https://research.google/pubs/sok-security-vulnerabilities-in-agentic-ai-systems/); [LASM survey, arXiv 2604.23338](https://arxiv.org/html/2604.23338)). [MAST (arXiv 2503.13657)](https://arxiv.org/abs/2503.13657v3) covers benign failures only. Your contribution is the bridge: one mechanism-level taxonomy that maps both kinds of failure, plus which defenses cover which mechanisms.

| Milestone | Date (AoE) | Source |
| --- | --- | --- |
| Abstract registration (title, authors, abstract, topics) | Jan 19, 2027 | [USENIX Sec '27 CFP](https://www.usenix.org/node/321195) |
| Paper submission | Jan 26, 2027 | same |
| Early-reject notice | Mar 9, 2027 | same |
| Rebuttal window | Apr 8 to 15, 2027 | same |
| Notification | May 6, 2027 | same |

Format: 13 pages of main body. References and appendices don't count at submission. The title must start with "SoK:". The CFP warns that surveys without new insight are rejected, so Tasks 4 to 6 carry the paper.

&#91;embedded content: task schedule · 9 tasks, Nov 23 to Jan 26\]

Tasks 4 to 7 overlap by a few days on purpose. Taxonomy work feeds validation and findings, and writing starts once the taxonomy holds.

## Tasks

### Task 1. Scope and novelty check

**When:** Nov 23 to 29 · **Effort:** about 12 hours

**Goal:** confirm nobody has already published the benign-plus-adversarial bridge, and lock what the paper covers.

**How to do it:**

1. Read the four closest works in full: the JHU SoK, the Google SoK, the LASM survey and MAST. For each one, note its scope, its taxonomy axes, how many papers it covered, and what it leaves out.
2. Run targeted searches on arXiv, Semantic Scholar and Google Scholar. Example queries: "multi-agent LLM failure taxonomy", "cascading errors multi-agent", "agent coordination failure adversarial", "MAST failure modes attack". Check the last 6 months most carefully.
3. For every hit, write one line: overlaps, partly overlaps, or doesn't overlap. Also say why.
4. If a paper already covers the bridge, change the angle. One option is defense coverage only, another is failures in deployed frameworks such as AutoGen, CrewAI and LangGraph.
5. Write 3 research questions. Examples: RQ1, which mechanisms underlie multi-agent failures? RQ2, which mechanisms can be triggered by both bugs and attackers? RQ3, which mechanisms does no defense cover?
6. Write the inclusion rules: LLM-based, two or more agents, published from 2023 to Jan 2027, peer-reviewed or an arXiv paper with 10+ citations or from a known lab.

**Deliverable:** a 2-page scope memo (`01_scope_memo.md`). It holds the final title, the 3 RQs, the inclusion and exclusion rules, a positioning table against the four closest works, and the novelty search log.

**Done when:** you can say in one sentence what this SoK gives that the JHU SoK and MAST don't, and the search log backs it up.

### Task 2. Search protocol and corpus

**When:** Nov 30 to Dec 6 · **Effort:** about 18 hours

**Goal:** a reproducible, documented set of about 150 included papers.

**How to do it:**

1. Write the search protocol: the databases (arXiv, Semantic Scholar API, DBLP, ACM DL, IEEE Xplore), the exact query strings, the date range and the search date.
2. Run the queries and export everything to one spreadsheet, with title, authors, year, venue, DOI or arXiv ID, and citation count. Expect 400 to 800 raw hits.
3. Remove duplicates, then screen titles and abstracts against the Task 1 rules. Mark each one include, exclude (with reason) or maybe.
4. Snowball: check the references and citing papers of the 20 most-cited included papers.
5. Add the grey literature that matters: framework incident reports, CVEs, and documented failures in agent frameworks, kept in a separate column.
6. Record the count at each stage (found, after dedup, after screening, after snowball, final). This becomes the PRISMA-style flow figure.

**Deliverable:** `02_search_protocol.md` and `02_corpus.csv`, with a status and an exclusion reason for every paper, plus the stage counts.

**Done when:** the corpus has 120 to 180 included papers, and someone else could rerun your queries and get the same set.

### Task 3. Code every paper

**When:** Dec 7 to 27 · **Effort:** about 45 hours (the biggest task; give it to a co-author if you can)

**Goal:** every included paper is described with the same fields, so the taxonomy comes from data, not impressions.

**How to do it:**

1. Draft the codebook before you code. Suggested fields:
   - system type (debate, hierarchy, pipeline, swarm)
   - framework
   - number of agents
   - failure observed
   - trigger (benign bug, adversarial, both)
   - where it starts (one agent, the message channel, shared memory, a tool, the orchestrator)
   - how it spreads (stays local, cascades, amplifies)
   - detection method
   - defense proposed
   - evaluation (benchmark, metric)
   - limitation
2. Pilot the codebook on 15 papers, then fix the fields that were ambiguous.
3. Code all papers. Read the abstract, the threat model or failure section, and the evaluation. You don't need to read every paper end to end.
4. With a co-author: both of you code the same 20% of papers, compute Cohen's kappa, and talk through the disagreements. Report kappa in the paper. Aim for 0.7 or higher.
5. Each week, write a short note on patterns you notice. These become the seeds of Task 6.

**Deliverable:** `03_codebook.md` and `03_lit_matrix.csv` (one row per paper, one column per field), plus a kappa result if you have a co-author.

**Done when:** every included paper has every field filled, or marked as not reported.

### Task 4. Build the taxonomy and coverage maps

**When:** Dec 28 to Jan 5 · **Effort:** about 25 hours

**Goal:** the paper's central exhibit is a mechanism-level taxonomy that shows, for each mechanism, whether bugs, attackers or both trigger it, and which defenses cover it.

**How to do it:**

1. From the lit matrix, group the failures by mechanism, not by symptom. Candidate mechanisms: role or spec drift, message corruption or injection, shared-memory poisoning, unverified handoffs, error cascades, collusion or groupthink, orchestrator compromise, tool misuse, and termination failures. Let the data decide the final list.
2. Give each mechanism a one-line definition, its trigger types (benign, adversarial, both), example papers and a paper count.
3. Map MAST's 14 modes and the JHU SoK's risk families onto your mechanisms. A crosswalk table that shows what each existing taxonomy misses is strong evidence of novelty.
4. Build the defense coverage matrix: mechanisms down the rows, defense families across the columns (input filtering, verification agents, provenance and authorization, sandboxing, monitoring, consensus or voting). Mark each cell as covered and evaluated, proposed but not evaluated, or no work. The empty cells are your open problems.
5. Draw the taxonomy figure. Iterate on it until a reader understands the paper's claim from the figure alone, since this is the figure other papers will reuse.

**Deliverable:** `04_taxonomy.md` (definitions, counts, crosswalk to MAST and the JHU SoK), `04_coverage_matrix.csv`, and `fig_taxonomy.pdf`.

**Done when:** every coded paper maps to at least one mechanism, and every mechanism has at least 3 papers or is explicitly marked as emerging.

### Task 5. Validate the taxonomy on real traces (recommended)

**When:** Jan 3 to 10 · **Effort:** about 15 hours

**Goal:** show the taxonomy works on real failures, not just on paper descriptions. This is what lifts an SoK above a survey for USENIX reviewers.

**How to do it:**

1. Find public multi-agent failure traces. MAST released annotated traces alongside its paper. Before using them, check where they're hosted, what they contain and their license. If they're unavailable, use the public trace logs of the benchmarks in your corpus. Don't generate synthetic traces as a substitute.
2. Sample 100 to 200 failed traces from at least 3 frameworks or systems.
3. Label each trace with your mechanisms. With a co-author, double-label 30% of them and report kappa.
4. Report your taxonomy's coverage (the share of traces it explains), the share MAST's modes alone explain, and the traces neither explains.
5. Optional, if time allows: write one or two small proofs of concept showing that a benign failure and an attack hit the same mechanism, for example a hallucinated handoff versus an injected handoff in the same pipeline.

**Deliverable:** `05_trace_labels.csv`, a script that computes the coverage and kappa numbers, and one results table.

**Done when:** the table's numbers come from the script, and none are typed in by hand.

### Task 6. Findings and open problems

**When:** Jan 6 to 10 · **Effort:** about 12 hours

**Goal:** 6 to 10 findings a practitioner or researcher can act on. This is the "new insight" the CFP demands.

**How to do it:**

1. Draw each finding from the matrix or the traces. Pattern to follow: "Of 38 papers on handoff failures, 31 study benign causes and none test an attacker exploiting the same handoff" (example only; use your real counts).
2. Look for these kinds of findings: mechanisms studied by only one community, defenses never evaluated against benign failures, benchmarks that miss whole mechanisms, and frameworks whose defaults leave a mechanism open.
3. Turn each empty cell of the coverage matrix into an open problem with a concrete research question.
4. Write evaluation recommendations: which benchmarks and metrics future work should report.

**Deliverable:** `06_findings.md`, with each finding tied to its evidence (paper IDs or trace IDs) and a research agenda of 5 to 8 items.

**Done when:** every finding has a number behind it and the paper keys that support it.

### Task 7. Write the manuscript

**When:** Jan 8 to 18 · **Effort:** about 35 hours

**Goal:** a complete 13-page draft in the USENIX LaTeX template.

**How to do it:**

1. Download the official USENIX Security template from the CFP page and set up an Overleaf project.
2. Write to this page budget:

| Section | Pages | Holds |
| --- | --- | --- |
| 1. Introduction | 1.5 | problem, gap against existing SoKs, the 3 RQs, numbered contributions |
| 2. Background and scope | 1 | MAS architectures, definitions of failure, what is in and out |
| 3. Methodology | 1 | search protocol, screening flow figure, codebook, kappa |
| 4. Taxonomy | 3 | taxonomy figure, mechanism definitions, crosswalk to MAST and JHU |
| 5. Defense coverage | 2 | coverage matrix, what is evaluated versus only proposed |
| 6. Validation on traces | 1.5 | coverage and kappa table from Task 5 |
| 7. Findings and open problems | 2 | the Task 6 findings and the research agenda |
| 8. Conclusion | 0.5 | answers to RQ1 to RQ3, limitations |
| Appendices | outside the limit | full corpus table, codebook, ethics and open-science statements |

3. Write in this order: Taxonomy, Coverage, Findings, Methodology, Introduction, Abstract. The introduction is easier once you know what you found.
4. Generate every table and figure from the CSVs with a script, so the numbers in the text match the data.
5. Keep it anonymous: no author names, no self-identifying links. Put the corpus in an anonymized repository (for example anonymous.4open.science) for review.

**Deliverable:** `paper/` LaTeX project and `draft_v1.pdf`, 13 pages plus references and appendices.

**Done when:** every contribution in the introduction points to a section, a table or a figure.

### Task 8. Register the abstract

**When:** by Jan 19, 2027 AoE · **Effort:** about 2 hours

**How to do it:** On the submission site (linked from the CFP), enter the final title, all authors and their conflicts, the topic areas, and a 200 to 250-word abstract. The title and author list are fixed after registration, so settle them first.

**Deliverable:** a confirmed registration on the submission site, with a saved copy of the confirmation email.

### Task 9. Review, verify, submit, publish

**When:** Jan 19 to 26 · **Effort:** about 16 hours

**How to do it:**

1. Get two outside readers, a security person and an agents person, to review the draft as strict reviewers by Jan 22. A fresh-eyes review from me also works.
2. Verify every reference against Crossref, DBLP or arXiv, and cite published versions when they exist. Keep `09_reference_check.md` with the key, ID, how you verified it and its status.
3. Check that every number in the abstract and introduction matches the tables.
4. Reread the CFP for the required ethics and open-science appendices, the formatting rules, and the policy on preprints during review.
5. Submit by Jan 25, a day early.
6. Post to arXiv (cs.CR, cross-listed to cs.AI and cs.MA) if the preprint policy allows it. Release the corpus and codebook on GitHub with a DOI from Zenodo. A public, reusable corpus is what makes people cite an SoK.

**Deliverable:** the submitted PDF and its confirmation, the reference check log, the arXiv ID, and the public corpus repository.

**Done when:** submission is confirmed, and every reference shows as verified in the log.

## Risks and fallbacks

| Risk | Early sign | Fallback |
| --- | --- | --- |
| The bridge angle already exists | A Task 1 search turns up a close match | Narrow to defense coverage, or to failures in deployed frameworks |
| Coding runs late | Fewer than 60 papers coded by Dec 20 | Cap the corpus at about 120 and cut Task 5 step 5 |
| No usable public traces | Trace data is missing or its license blocks use | Validate on traces released with benchmark papers in the corpus, or drop Task 5 and strengthen the crosswalk |
| Desk-reject as "just a survey" | Findings in Task 6 have no numbers | Rework the findings until each has a count, before you write |
| Jan 26 can't be met | Draft not complete by Jan 18 | Skip USENIX and aim for the IEEE S&P 2028 first cycle (usually around June; date not yet confirmed) or ACM CCS 2027 (dates not yet confirmed) |
| Rejected on May 6 | Reviews arrive | Revise using the reviews and resubmit to S&P 2028 or CCS 2027 |

**Weekly check:** each Sunday, compare the deliverables done against this plan. If you're more than a week behind, use the fallback for that row.

**Help I can give at each task:** run the novelty search (Task 1), run the Semantic Scholar and arXiv queries and build the corpus CSV (Task 2), pre-code papers from their abstracts for you to check (Task 3), draft the figures and tables from your CSVs (Tasks 4 and 5), draft sections (Task 7), and verify references (Task 9). I won't make up papers or numbers. Anything unverified stays marked TBD.

## Sources

- [USENIX Security '27 Call for Papers](https://www.usenix.org/node/321195) and its [PDF](https://www.usenix.org/sites/default/files/sec27_cfp-070826.pdf)
- [IEEE S&P 2027 Call for Papers](https://sp2027.ieee-security.org/cfpapers.html)
- [SoK: When Safe Agents Fail Together (arXiv 2609.00595)](https://arxiv.org/pdf/2609.00595)
- [SoK: Security Vulnerabilities in Agentic AI Systems](https://research.google/pubs/sok-security-vulnerabilities-in-agentic-ai-systems/)
- [A Systematic Survey of Security Threats and Defenses in LLM-Based AI Agents (arXiv 2604.23338)](https://arxiv.org/html/2604.23338)
- [Why Do Multi-Agent LLM Systems Fail? (arXiv 2503.13657)](https://arxiv.org/abs/2503.13657v3)
