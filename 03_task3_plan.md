# Task 3 plan: code every paper

Prepared Nov 23, 2026, from the full SoK plan, the scope memo (`01_scope_memo.md`) and the Task 2 corpus (`02_search_protocol.md`, `02_corpus.csv`). **Status (Nov 23): subtask 3.0 is done** (codebook v0, coding-sheet template, validator). The pilot (3.1) and the batches have not started; they begin on your word.

## 1. What the SoK plan asks for

From Task 3 of the plan, in its own words where it matters:

- **Goal:** every included paper is described with the same fields, so the taxonomy comes from data, not impressions.
- **Steps:** (1) draft the codebook before coding; (2) pilot it on 15 papers and fix ambiguous fields; (3) code all papers, reading the abstract, the threat-model or failure section, and the evaluation (not every paper end to end); (4) with a co-author, both code the same 20% of papers, compute Cohen's kappa, discuss disagreements, report kappa in the paper, aim for 0.7 or higher; (5) write a short note each week on patterns, which seeds Task 6.
- **Deliverable:** `03_codebook.md` and `03_lit_matrix.csv` (one row per paper, one column per field), plus a kappa result if there is a co-author.
- **Done when:** every included paper has every field filled, or marked "not reported".
- **Effort in the plan:** about 45 hours, Dec 7 to 27, "the biggest task; give it to a co-author if you can".
- **Risk row:** if fewer than 60 papers are coded by Dec 20, cap the corpus at about 120 and cut Task 5 step 5.
- **Help the plan promises:** pre-code papers from their abstracts for you to check. Nothing made up; anything unverified stays marked TBD.

What Task 4 to 6 need from this task, which shapes the codebook:
- Task 4 groups failures by **mechanism, not symptom**, and counts papers per mechanism with trigger types and defense families. So the matrix needs a free-text mechanism candidate, plus the locus and spread fields.
- Task 4's coverage matrix needs the **defense family** and **which trigger the defense was evaluated against**.
- Task 5 needs to know which papers **release failure traces**, with host and license.
- Task 6 needs every finding tied to paper keys, so every paper has a stable id (below) and short evidence notes.

From the scope memo (Section 7): the codebook needs a field for **trigger evidence level** (direct dual-trigger in one paper, benign only, adversarial only) and one for **the trigger a defense was evaluated against**. RQ2 and RQ3 depend on them, and they are the hardest to code consistently, so the kappa check should look at them first.

## 2. Two things to settle before starting

1. **Effort.** The plan's 45 hours assumed 120 to 180 papers (about 15 to 20 minutes each). We keep **384 included papers plus 54 maybes**, which is 2 to 3 times that. At the plan's pace this would be over 100 hours. The workable split is: I pre-code each paper from its abstract and, where a PDF exists, its threat-model, failure and evaluation sections; you check each row. Checking at about 7 minutes per paper gives about 45 hours for the 384, which matches the plan. If checking runs slower, the plan's fallback (cap at about 120) is still available, and the batch order below puts the most central work first.
2. **No co-author, so two independent LLM passes plus a human anchor (decided Nov 23).** Every paper is coded twice by LLM Coder A and Coder B (different model tiers, different prompts, fresh contexts, same frozen codebook). You adjudicate every disagreement and audit a random 20% of each batch. The paper reports agreement between two LLM passes plus the audit acceptance rate, and says plainly that it is not human inter-coder reliability. Conditions, limits and draft paper text: `03_coding_method.md`.

## 3. Inputs and outputs

| Item | Where |
|---|---|
| Corpus (384 included, 54 maybe) | `02_corpus.csv` |
| Stable paper ids, batch, theme, double-coding flag, PDF path | `task3/paper_index.csv` |
| One list per batch | `task3/batches/<batch>.md` and `.csv` |
| Abstracts (4 papers have none) | `task3/abstracts.json` |
| PDFs (207 of 438 have one; the rest have no arXiv id) | `task2/papers/` |
| How the coding is done and reported | `03_coding_method.md`, prompts in `task3/prompts/` |
| Codebook v0 (subtask 3.0, done) | `03_codebook.md`, generated from `task3/schema.py` |
| Coding-sheet template, blank-sheet maker, validator, tests (done) | `task3/coding/template.csv`, `task3/make_sheet.py`, `task3/validate_coding.py`, `task3/test_validator.py` |
| Worked example row (P023, abstract only) | `task3/coding/example.csv` |
| Per-batch coding sheets (to be written) | `task3/coding/<batch>.csv` |
| Final matrix (to be merged in subtask 3.5) | `03_lit_matrix.csv` |
| Weekly pattern notes | `task3/notes/week-N.md` |
| Rebuild the batches | `python3 task3/build_batches.py` (deterministic) |

**Paper ids:** `P001` to `P384` for included papers (ordered by date), `Q001` to `Q054` for the maybes. They are stable. Task 6 should cite these ids.

## 4. Codebook

The first draft in this plan had 20 fields. **`03_codebook.md` (v0, written in subtask 3.0) supersedes it and has 21 coded fields**, each with a definition, its allowed values, rules, and an example, plus a worked row from the corpus. Changes from the first draft:

- `locus_detail` is a new field (the specific role, channel, store or tool), because the "same locus" test needs it.
- `trigger_evidence_level` no longer has an "indirect" value. Indirect evidence means two separate papers, so it is worked out across rows in Task 4. A within-paper value, `both-different-locus`, replaces it.
- `swarm` is folded into `decentralized`.
- The `mechanism_candidate` list adds three mechanisms the corpus calls for: privacy or information leakage, protocol or authorization flaw, and coordination or communication failure. `other:<label>` lets the data extend it.
- `not reported` versus `TBD` is now defined: `not reported` means the sources read do not say; `TBD` means a reviewer must look, and it is rejected in the final check.

The dual-trigger test from the scope memo is in the codebook as written. The pilot will fix whatever is ambiguous, and then the codebook is frozen as v1.

## 5. How the 384 papers are split

- **Pilot (15 papers):** chosen to span the hardest cases, led by the papers that bear on both triggers (Xie et al. on error cascades, Bappy et al. on pipelines, MAST, the faulty-agents paper, the Byzantine-fault-tolerance paper), plus a framework bug study, a collusion paper, a debate paper, a protocol attack, a privacy case and a handoff study. All 15 are double-coded.
- **Batches B01 to B19 (369 papers, 20 each, 9 in the last):** grouped by theme so you see similar work together, then by date. Themes come from title keywords and are a grouping aid only, not a taxonomy; Task 4 builds the real mechanism list from the coded data. Counts of included papers by theme:
- T1 failure attribution and debugging: 74
- T2 benign error and hallucination propagation: 75
- T3 debate, consensus, sycophancy, conformity: 31
- T4 collusion and steganography: 22
- T5 privacy and leakage: 17
- T6 protocols, authorization, trust boundaries: 29
- T7 attacks: injection, jailbreak, poisoning, backdoor: 75
- T8 defenses and monitors: 45
- T9 other multi-agent failure and risk: 16
- **Batches M1 to M3 (54 maybes):** each paper gets an in-scope or out-of-scope decision first, then is coded if in scope.
- **Human-audit sample:** a random 20% of each batch (picked with a fixed seed; 74 papers across B01 to B19) plus all 15 pilot papers, 89 in total. You check these whether or not the two LLM passes agree. You also adjudicate every paper where they disagree.

## 6. Subtasks

Each subtask ends in a file, in the plan's spirit that a missed deadline still leaves a reusable result.

- **3.0 Set up. Done Nov 23.** `03_codebook.md` v0 (21 fields, each with definition, values, rules and an example; a worked row for P023), the coding-sheet template, a blank-sheet maker per batch, and a validator with 21 tests. The validator passes on the empty template and on the filled example; in `--final` mode it correctly rejects the example because it still has a `TBD` and a pending review.
- **3.1 Pilot, 15 papers.** Coder A (Opus) and Coder B (Sonnet) each code all 15 independently from the abstract and the relevant PDF sections. Compare with `task3/agreement.py`, list every disagreement, you adjudicate, fix the ambiguous field definitions, freeze **codebook v1** and the prompts. *Done when:* a disagreement log exists, v1 is frozen, and no field is left ambiguous.
- **3.2.01 to 3.2.19 Code batches B01 to B19.** For each batch, Coder A and Coder B each fill a sheet; the agreement script lists the disagreements; you adjudicate them and audit the random 20% sample. *Done when:* both sheets pass the validator, every disagreement is adjudicated, and the audit meets the stopping rule in `03_coding_method.md`.
- **3.3.1 to 3.3.3 Resolve and code the maybes.** *Done when:* each of the 54 is marked in or out, with a reason, and the in-scope ones are coded.
- **3.4 Reliability.** Compute agreement between Coder A and Coder B on the whole corpus, per field (Cohen's kappa for single-value fields; report it as agreement between two LLM passes), and the audit acceptance rate on the human-audit sample. Report the trigger and defense fields (6, 7, 11, 12) separately. Discuss disagreements. *Done when:* a kappa table exists, and any field below 0.7 has either been recoded or reported as weak.
- **3.5 Weekly pattern notes.** After every five batches, a short note in `task3/notes/` on patterns seen: mechanisms studied by one community, defenses never tested against benign failures, and so on. These seed Task 6.
- **3.6 Finalize.** Merge all sheets into `03_lit_matrix.csv`, run the completeness check, finalize `03_codebook.md`, and write the kappa result. *Done when:* every included paper has every field filled or `not reported`.

### Batch table

| Subtask | Batch | Papers | Main themes | Double-coded | Pdf available | List |
|---|---|---|---|---|---|---|
| 3.1 | PILOT | 15 | T2×7, T7×4, T9×1 | 15 | 12 | [`PILOT.md`](task3/batches/PILOT.md) |
| 3.2.01 | B01 | 20 | T1×20 | 4 | 9 | [`B01.md`](task3/batches/B01.md) |
| 3.2.02 | B02 | 20 | T1×20 | 4 | 12 | [`B02.md`](task3/batches/B02.md) |
| 3.2.03 | B03 | 20 | T1×20 | 4 | 15 | [`B03.md`](task3/batches/B03.md) |
| 3.2.04 | B04 | 20 | T1×13, T2×7 | 4 | 7 | [`B04.md`](task3/batches/B04.md) |
| 3.2.05 | B05 | 20 | T2×20 | 4 | 5 | [`B05.md`](task3/batches/B05.md) |
| 3.2.06 | B06 | 20 | T2×20 | 4 | 10 | [`B06.md`](task3/batches/B06.md) |
| 3.2.07 | B07 | 20 | T2×20 | 4 | 8 | [`B07.md`](task3/batches/B07.md) |
| 3.2.08 | B08 | 20 | T3×19, T2×1 | 4 | 8 | [`B08.md`](task3/batches/B08.md) |
| 3.2.09 | B09 | 20 | T3×12, T4×8 | 4 | 11 | [`B09.md`](task3/batches/B09.md) |
| 3.2.10 | B10 | 20 | T4×13, T5×7 | 4 | 10 | [`B10.md`](task3/batches/B10.md) |
| 3.2.11 | B11 | 20 | T5×10, T6×10 | 4 | 10 | [`B11.md`](task3/batches/B11.md) |
| 3.2.12 | B12 | 20 | T6×18, T7×2 | 4 | 9 | [`B12.md`](task3/batches/B12.md) |
| 3.2.13 | B13 | 20 | T7×20 | 4 | 11 | [`B13.md`](task3/batches/B13.md) |
| 3.2.14 | B14 | 20 | T7×20 | 4 | 3 | [`B14.md`](task3/batches/B14.md) |
| 3.2.15 | B15 | 20 | T7×20 | 4 | 12 | [`B15.md`](task3/batches/B15.md) |
| 3.2.16 | B16 | 20 | T8×11, T7×9 | 4 | 11 | [`B16.md`](task3/batches/B16.md) |
| 3.2.17 | B17 | 20 | T8×20 | 4 | 14 | [`B17.md`](task3/batches/B17.md) |
| 3.2.18 | B18 | 20 | T8×14, T9×6 | 4 | 11 | [`B18.md`](task3/batches/B18.md) |
| 3.2.19 | B19 | 9 | T9×9 | 2 | 2 | [`B19.md`](task3/batches/B19.md) |
| 3.3.1 | M1 | 20 | T2×6, T8×6, T7×5 | 0 | 10 | [`M1.md`](task3/batches/M1.md) |
| 3.3.2 | M2 | 20 | T2×8, T9×5, T1×3 | 0 | 7 | [`M2.md`](task3/batches/M2.md) |
| 3.3.3 | M3 | 14 | T2×4, T6×4, T1×2 | 0 | 0 | [`M3.md`](task3/batches/M3.md) |

Total 438 papers: 15 pilot, 369 in B01 to B19, 54 maybes.

### Pilot papers

1. **P133** — From Spark to Fire: Modeling and Mitigating Error Cascades in LLM-Based Multi-Agent Collaboration (2026, T2)
2. **P248** — Adversarial Attacks in Multi-Agent LLM Pipelines: Unveiling Structural Vulnerabilities in Agentic AI Architectures (2026, T7)
3. **P026** — Why Do Multi-Agent LLM Systems Fail? (2025, T9)
4. **P008** — On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents (2024, T2)
5. **P080** — Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance (2025, T2)
6. **P012** — Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems (2024, T7)
7. **P128** — MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems (2026, T2)
8. **P032** — Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems (2025, T1)
9. **P230** — Bugs in Modern LLM Agent Frameworks: An Empirical Study (2026, T2)
10. **P003** — Secret Collusion among AI Agents: Multi-Agent Deception via Steganography (2024, T4)
11. **P056** — Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate (2025, T2)
12. **P119** — INFA-Guard: Mitigating Malicious Propagation via Infection-Aware Safeguarding in LLM-Based Multi-Agent Systems (2026, T7)
13. **P289** — A2ABreak: Systematic Security Analysis of the A2A Protocol (2026, T6)
14. **P267** — Handoff Hallucinations: Taxonomy, Benchmark, and Mitigation for Multi-agent Pipeline Failures (2026, T2)
15. **P025** — Multi-Agent Systems Execute Arbitrary Malicious Code (2025, T7)

## 7. Schedule

The plan puts Task 3 at Dec 7 to 27. We are ahead of plan, so this can start sooner; the calendar below keeps the plan's dates and shows the checkpoints.

| Window | Work | Checkpoint |
|---|---|---|
| Dec 7 to 9 | 3.1 pilot (3.0 is already done) | codebook v1 frozen |
| Dec 10 to 13 | B01 to B05 | 100 papers reviewed |
| Dec 14 to 20 | B06 to B13 | 260 papers reviewed; the plan's risk check is 60 by Dec 20, so we aim well above it |
| Dec 21 to 27 | B14 to B19, M1 to M3, 3.4 reliability, 3.6 finalize | `03_lit_matrix.csv` complete |

Weekly check each Sunday against this table. If more than a week behind, use the plan's fallback: cap the corpus (the batch order puts failure-attribution and propagation work first, and the Tier 2 papers can be dropped from the remaining batches).

## 8. Rules for coding

- Read the abstract, the threat-model or failure section, and the evaluation. Full-text reading is optional and recorded in `coded_from`.
- 231 papers have no PDF (no arXiv id). They are coded from the abstract alone and marked `coded_from = abstract only`; `confidence` cannot be `high` for them unless the abstract is explicit.
- Four papers have no abstract. They need the PDF or a manual lookup first.
- A field the text does not settle is `not reported`. A field I could not verify is `TBD` and goes to your review queue. No guessing.
- Each key judgment gets an `evidence_note`, so a reviewer can check it in seconds.
- A paper that fails the inclusion rules on a close read (for example, single-agent) is moved to the maybe or exclude list with a reason, not coded.

## 9. Decisions

1. ~~Co-author for the kappa check.~~ **Decided: no co-author; two LLM passes plus a human audit** (Section 2 and `03_coding_method.md`).
2. Confirm the stopping rule in `03_coding_method.md` Section 2 (review every agreed row for a field if the audit accepts under 90%).
3. Whether to start the batches now or wait for Dec 7. (The pilot is already running with two LLM coders.)
4. Whether the 20-paper batch size and the theme grouping suit you, or you would rather mix themes within a batch for calibration.
