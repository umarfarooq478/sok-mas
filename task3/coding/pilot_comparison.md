# Pilot: v0 versus v1 agreement between the two LLM coders

Same 15 papers, same two models (Opus tier and Sonnet tier), fresh contexts each time. n = 15, so one paper is 6.7 percentage points: **differences of one paper are noise**. The v1 run is a regression test, not a reliability estimate, because the v1 rules were written after seeing these papers.

| Field | v0 exact agreement | v1 exact agreement | Note |
|---|---|---|---|
| system_type | 80% | 93% | |
| n_agents | 87% | 80% | v1 `varies` rule created new splits |
| trigger | 87% | 93% | only P003 disputed in v1 |
| trigger_evidence_level | 87% | 93% | only P003 disputed in v1 |
| defense_evaluated_against | 93% | 93% | only P003 disputed in v1 |
| spread | 67% | 73% | `not studied` versus `not reported` caused two splits; removed in v1.1 |
| locus (set match) | 60% | 53% | more values allowed in v1; v1.1 asks for primary first |
| detection_method (set match) | 67% | 73% | |
| defense_family (set match) | 80% | 60% | add-on and `other:` labels differed; v1.1 caps at two and limits `other:` |
| trace_release | 93% | 53% | `no` versus `not reported`; v1.1 defines the difference |
| paper_type | 87% | 87% | |
| evidence_type (set match) | 80% | 87% | |
| coded_from | 87% | 87% | |
| confidence | 60% | 73% | still a triage flag only |
| mechanism | 47% (set of up to three) | 73% primary, 67% secondary | field was split in v1 |
| **Total disagreements** | **51** | **54** | no net reduction |

## What this shows

- The three fields that carry RQ2 and RQ3 (`trigger`, `trigger_evidence_level`, `defense_evaluated_against`) are now disputed on **one paper only (P003)**, a paper whose scope is borderline (mostly single-model evaluations). The v1 rules resolved the cases the coders had flagged: the faulty-agents paper is `both` and `direct-both` in both sheets, and the two bridge papers are `both-different-locus` in both.
- The new v1 disagreements are in secondary fields and come from four causes, all fixed in v1.1: `trace_release` (`no` versus `not reported`), `defense_family` (add-ons and `other:` labels), `locus` (primary versus extra values), and `spread` (`not studied` versus `not reported`).
- v1 did not reduce the total number of disagreements. Do not describe it as an improvement overall.
- P003 alone accounts for 10 of the 54 v1 disagreements.
- v1.1 changes are **untested**: they were not run again on the pilot. Batch B01 is their first test.

Files: `v0/` and `v1/` hold both runs' sheets, notes and disagreement lists. The agreement tables come from `task3/agreement.py` (v0 numbers copied from its output before the v0 columns were retired).
