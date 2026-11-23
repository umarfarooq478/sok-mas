# How the papers are coded, and how to report it

Nov 23, 2026. Answers the question: *there is no co-author, so can two LLM passes replace the second coder, and can we say so honestly in the paper?*

## 1. Short answer

**Yes, with conditions.** Two independent LLM passes plus a human anchor is a defensible method, and it can be reported honestly. It cannot be reported as "two coders, kappa 0.8", because that wording claims something the method does not deliver. What it delivers is:

1. A measure of whether the **codebook can be applied the same way twice** (agreement between two LLM passes).
2. A measure of whether **agreement means correctness** (how often you accept the agreed codes when you audit them).
3. A human decision on **every disagreement**.

The conditions that make it honest are in Section 4. The main one: do not present LLM-LLM agreement as human inter-coder reliability.

## 2. The design

| Step | Who | What |
|---|---|---|
| Pass A (`llm-a`) | LLM, Opus tier, prompt A | Codes every paper. Careful research-assistant framing: reads the abstract first, then the PDF to confirm and add detail. |
| Pass B (`llm-b`) | LLM, Sonnet tier, prompt B | Codes every paper. Skeptical-auditor framing: reads the evaluation first, then the abstract; treats abstract claims as unsupported until the experiments back them; picks the narrower code when unsure. |
| Independence | | Fresh context for each pass; the two cannot see each other's sheets; same frozen codebook; different model, prompt, reading order and burden of proof. |
| Compare | script (`task3/agreement.py`) | Per-field agreement, Cohen's kappa for single-value fields, set agreement for multi-value fields, and a list of every disagreement. |
| Adjudicate | **you** | Decide every field where A and B differ, with both rows and both `evidence_note`s in front of you. Result: `<batch>.adjudicated.csv`. |
| Audit | **you** | A random 20% of each batch (`human_audit = Y`; fixed seed, listed in `task3/paper_index.csv`), checked whether or not A and B agreed. Result: the audit acceptance rate. |
| Final label | | Adjudicated value where the passes disagreed; the agreed value elsewhere, corrected where the audit found an error. |

The two models are different tiers of the same vendor. A first attempt to use a third model for Pass B failed because that model required usage credits, so Sonnet was used. The prompts are in `task3/prompts/` and are used verbatim. Prompts are frozen after the pilot, together with the codebook (v1), and every later change is logged.

### Stopping rule (proposed; confirm before the batches start)

If, in a batch, you accept fewer than **90%** of the audited agreed rows on any of the six key fields (`trigger`, `trigger_evidence_level`, `locus`, `spread`, `defense_family`, `defense_evaluated_against`), you review **every** agreed row for that field in that batch, and the codebook entry for it is reopened. A high agreement between the passes does not by itself release a field from human review.

## 3. What you can and cannot claim

**Can claim:**
- The corpus was coded twice by independent LLM passes (different models and prompts), against a fixed codebook, and the agreement per field is X.
- A human adjudicated every disagreement and audited a random 20% of the rest, and accepted Y% of audited agreed codes unchanged.
- The codebook, prompts, both sheets and the adjudication log are released.

**Cannot claim:**
- "Inter-coder reliability" or "inter-rater reliability" without saying the raters are LLMs.
- That a kappa of 0.7 or higher (the threshold from the human-coding literature) validates the codes. Here it only says the codebook gives stable results across two LLM passes.
- That the human reviewed every row, if you only reviewed disagreements and the audit sample.
- Independence in the full sense. See the limits below.

## 4. Conditions for honest reporting

1. **Call it what it is.** Say "agreement between two LLM coding passes". Give model ids, prompt versions and dates. (Exact model ids still need recording from the run log; the sub-agent aliases are not enough for a paper.)
2. **State the limits of independence.** Both passes are language models from one vendor. They share training data, so their errors are correlated, and agreement can reflect shared bias. The human audit is the control for this, so report it with its sample size and an interval.
3. **Use the human where the risk is.** Adjudicate all disagreements, and audit agreed rows at random. Report how many agreed rows you changed.
4. **Fix the method before coding and log changes.** Prompts and codebook are frozen after the pilot; later edits are logged with the reason. No tuning prompts on the corpus to raise the agreement.
5. **Release everything.** Codebook, both prompts, both sheets, the disagreement list and your adjudications, in the anonymized repository for review.
6. **Disclose in the paper's methods and, if required, in an AI-use statement.** I have **not** checked the USENIX Security '27 CFP or its policy on generative-AI use, so this must be read in Task 9 (the plan already has "reread the CFP" there). Do not assume a rule either way.
7. **Do not let the LLM judge be the only evidence for a key finding.** Task 6 findings that rest on a handful of papers should be checked against the source papers by you.

## 5. Limits (say these in the paper)

- Same vendor, correlated errors. A different vendor's model for Pass B would reduce this; it is not available in this setup. If you can get one (or one human coder for even 30 papers), it would strengthen the claim noticeably, and it is optional.
- The coders read abstracts for the 231 papers that have no PDF, so for those rows the data is only as good as the abstract. `coded_from` records this per row.
- The codebook was written by an LLM with you, and then applied by LLMs. Neither coder is a naive reader of it.
- The pilot has 15 papers. Agreement from a sample that small is a pointer to ambiguous fields, not an estimate.
- The audit sample is 20% of each batch. A rare error type can still slip through.
- Some reviewers will be skeptical of LLM coding. The audit numbers and the released materials are the answer to that.

## 6. What to report (checklist for the paper)

- The two models (exact ids), prompt versions, run dates, and any settings known.
- Per-field agreement and kappa between pass A and pass B; the four fields that matter most for RQ2 and RQ3 reported separately.
- Number and share of rows with at least one disagreement; the fields where disagreements concentrate; how they were resolved.
- Audit sample size, acceptance rate per key field, and how many corrections.
- The 15-paper pilot, what it changed in the codebook, and the frozen version.
- Share of rows coded from the abstract only.

## 7. Draft text for the methods section (placeholders to fill)

> **Coding procedure.** We coded each of the *N* papers against a fixed codebook of 21 fields (Appendix X). Because the study had a single human author, we used two independent LLM coding passes instead of a second human coder. Pass A used [model A id] with a research-assistant prompt; pass B used [model B id] with a skeptical-auditor prompt that required support in the experiments for the trigger and defense fields. Each pass ran in a fresh context, could not see the other's output, and read the same frozen codebook (v1, frozen after a 15-paper pilot). Prompts, sheets and the codebook are in the artifact [anonymized link]. Agreement between the two passes was κ = [..] on average over single-valued fields (range [..]–[..]); for the four fields that carry RQ2 and RQ3 (trigger, trigger-evidence level, defense family, defense evaluated against) it was [..]. The first author resolved all [..] disagreements and audited a random [20]% sample of the remaining rows, accepting [..]% of the audited codes unchanged. We report this as agreement between two LLM passes, not as human inter-coder reliability: both passes come from one model vendor, so their errors may be correlated, and the human audit is our check on that.

Fill the brackets from `task3/agreement.py` output and the audit log. Do not fill any bracket you cannot back with a file.

## 8. What the v0 pilot showed (Nov 23)

Coder A (Opus tier) and Coder B (Sonnet tier) coded the 15 pilot papers independently under codebook v0. Results, with the caveat that n = 15 makes every kappa unstable:

- `trigger` and `trigger_evidence_level`: 87% exact agreement (13 of 15), kappa 0.79. `defense_evaluated_against`: 93%, kappa 0.91. `spread`: 67%, kappa 0.55. `locus`: 60% exact, Jaccard 0.74. `mechanism_candidate`: 47% exact, Jaccard 0.67. `confidence`: 60%, kappa 0.33.
- Both coders independently flagged the same ambiguities, which led to the v1 changes (codebook Section 10).
- **Some disagreement comes from the prompts, not the codebook.** Coder B's rule to require experimental support makes it write `not reported` for `spread` where Coder A accepts the abstract's claim. This is by design, but it means the agreement figure partly measures how different the two prompts are. Report it that way. The pilot disagreements are in `task3/coding/v0/`.
- On the two papers that matter most for the bridge claim, both coders agreed (`both` and `both-different-locus`), and both marked those rows low confidence.

The **v1 pilot run** then has the same two models code the same 15 papers again under v1, in fresh contexts. It is a **regression test of the new rules, not an independent reliability estimate**, because the rules were written after seeing these papers. Its agreement is expected to be higher than v0, and the paper must not present that as the reliability of the method. The reliability figures for the paper come from batches B01 to B19.

## 9. Cost and effort

- The LLM cost doubles (two passes over 384 papers plus the 54 maybes).
- Your time changes: instead of reviewing every row, you adjudicate disagreements and audit 20% of the rest. I cannot yet say how large that is; the pilot gives a first estimate of the disagreement rate. If the disagreement rate is high, the human time can approach the original plan's 45 hours.
- Because every paper is coded twice, disagreements are found automatically and the human effort goes where the codes are least stable.
