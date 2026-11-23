"""Render 03_codebook.md from task3/schema.py and task3/coding/example.csv. Rerun after editing the schema."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema as S
ex = list(csv.DictReader(open("task3/coding/example.csv", encoding="utf-8")))[0]
out = []
w = out.append
w(f"""# Codebook for the SoK corpus

**Version:** {S.VERSION}. Prepared Nov 23, 2026 for Task 3 of the SoK plan (subtask 3.0). The 15-paper pilot (subtask 3.1) will fix the fields that turn out to be ambiguous, and then this file is frozen as v1.
This file is generated from `task3/schema.py`; the validator reads the same schema, so the two cannot disagree. Edit the schema, then run `python3 task3/render_codebook.py`.

## 1. What a row is

One row per paper, 21 coded fields, plus the paper id, the coder, and two review fields. A row says what the paper shows, so that the taxonomy in Task 4 comes from data. It does not say whether the paper is good.

Papers have stable ids: `P001` to `P384` (included) and `Q001` to `Q054` (maybe). See `task3/paper_index.csv`.

## 2. Who codes what

There is no co-author and no second human coder. Instead every paper is coded **twice by two independent LLM passes**, and the human anchors the result. Full reasoning, limits and the text for the paper are in `03_coding_method.md`.

- **Coder A (`llm-a`)** and **Coder B (`llm-b`)** each code every paper from a fresh context, with a different model, a different prompt (`task3/prompts/`), and a different reading order and burden of proof. They share the codebook, and they cannot see each other's sheets. Output: `task3/coding/<batch>.llm-a.csv` and `<batch>.llm-b.csv`.
- Where A and B **disagree** on any field, the human decides, with both rows side by side and each coder's `evidence_note` in front of them. The decision goes in `<batch>.adjudicated.csv` (`coder = adjudicated`).
- A random **audit sample** (20% of each batch, and the whole pilot; `human_audit = Y` in `paper_index.csv`) is checked by the human whether or not the passes agree. This is what shows whether agreement means correctness or shared error.
- The numbers reported in the paper are: agreement between A and B per field (kappa for single-value fields), and the share of audited rows where the human accepts the agreed codes unchanged. The paper must call the first **agreement between two LLM passes**, not human inter-coder reliability.

Limits worth stating: both passes are language models from one vendor, so their errors are correlated, and a high agreement can mean shared bias. That is why the human audit exists. The agreement tells us whether the codebook is clear enough to be applied the same way twice; the audit tells us whether the codes are right.

## 3. What to read, and how to say so

1. The abstract and the metadata (always).
2. The threat-model or failure section and the evaluation section, if a PDF exists (231 of 438 papers have none; they are coded from the abstract alone).
3. The rest of the paper only if a key field cannot be settled otherwise.

`coded_from` records how much was read. A paper with a PDF that was only skimmed is `abstract-only`; do not claim more.

### Special values

| Value | Meaning | Where allowed |
|---|---|---|
| `not reported` | the sources read do not say | every coded field except `paper_type`, `evidence_type`, `coded_from`, `confidence` |
| `TBD` | a reviewer must look (typically a PDF exists but has not been read) | draft sheets only; the final check rejects it |
| `not applicable` | the question does not apply to this paper | `trigger`, `trigger_evidence_level`, `defense_evaluated_against` |
| `none` | the paper has no such thing | `detection_method`, `defense_family` |
| `not studied` | the paper's design does not examine it | `spread` |

Never guess. A value that cannot be checked is `TBD` or `not reported`, not the most likely answer.

## 4. Key definitions

- **LLM multi-agent system (MAS):** two or more separately addressable LLM-based agents whose outputs affect each other through messages, shared state, collective decisions or delegated actions. This is the Task 1 inclusion rule.
- **Failure:** the system's behavior departs from its intended behavior or from a stated safety or integrity property. This covers faults, errors and attacks.
- **Benign trigger:** the failure arises without an adversary: a model error, a design flaw, a bad prompt, a framework bug, a tool or environment fault. Injecting faults to simulate errors is still benign.
- **Adversarial trigger:** an attacker or a deliberately malicious agent causes the failure.
- **Locus:** where the failure starts (one agent, message channel, shared memory, tool, orchestrator, environment input). Two triggers act at the **same locus** if they hit the same agent role, channel, store, tool or orchestrator step.
- **Mechanism vs symptom:** a mechanism says how the failure works (an unchecked hand-off passes a hallucination on); a symptom says what you see (a wrong answer). Task 4 groups by mechanism.
- **Detection vs defense:** detection finds or localizes a failure (`detection_method`); a defense limits or prevents it (`defense_family`). A paper can have both.

## 5. How the fields feed the later tasks

- **RQ2 (shared triggers):** `trigger`, `trigger_evidence_level`, `locus`, `locus_detail`. A mechanism is **dual-trigger** when at least one included paper shows it arising without an adversary and at least one shows an adversary inducing it at the same locus. One paper showing both is direct evidence (`direct-both`); two separate papers are indirect evidence. Indirect evidence is worked out across rows in Task 4, so it is not a value of the field.
- **RQ3 (defense coverage):** `defense_family` and `defense_evaluated_against`. The coverage matrix in Task 4 is built from them.
- **Task 4 mechanism list:** `mechanism_candidate`, including every `other:<label>`.
- **Task 5 trace sources:** `trace_release`.
- **Task 6 findings:** `framework`, `evidence_note` and the paper ids.

The four fields that matter most for RQ2 and RQ3, and are the hardest to code the same way twice, are `trigger`, `trigger_evidence_level`, `defense_family` and `defense_evaluated_against`. The reliability check reports them separately.

## 6. Fields
""")
for i, f in enumerate(S.FIELDS, 1):
    w(f"### {i}. `{f['name']}`\n")
    w(f"{f['definition']}\n")
    k = f["kind"]
    if "values" in f:
        w("| Value | Meaning |\n|---|---|")
        for v, m in f["values"].items(): w(f"| `{v}` | {m} |")
        if k == "multi": w("\nSeparate several values with `;`." + (" `other:<label>` is also accepted." if f.get("other_ok") else ""))
    elif k == "pattern": w(f"Format: `{f['pattern']}`.")
    elif k == "evidence": w("Free text, with one tagged segment per key field.")
    else: w("Free text.")
    w("\n**Rules**\n")
    for r in f["rules"]: w(f"- {r}")
    w(f"\n**Example.** {f['example']}\n")
w("""## 7. Worked example: a real row from the corpus

P023, *Red-Teaming LLM Multi-Agent Systems via Communication Attacks* (batch B13). It is not a pilot paper and not in the double-coded sample. It is coded **from the abstract only**, to show how that looks: every value below can be traced to the abstract, and what the abstract does not state is `not reported` or `TBD`. This row is in `task3/coding/example.csv`.

| Field | Value |
|---|---|""")
for c in S.COLUMNS:
    w(f"| `{c}` | {ex[c].replace('|', '/')} |")
w("""
Reading the row: the abstract describes an attack (Agent-in-the-Middle) and no benign condition, so `trigger = adversarial` and the evidence level is `adversarial-only`. `spread` is `not reported` because "compromise entire multi-agent systems" is an effect, not a measure of how the failure moves. `n_agents` is `TBD` because a PDF exists and the number will be in the experiments section. A full-text read would fill `system_type`, `framework`, `n_agents` and `evaluation`, and could move `confidence` to `high`.

## 8. Hard cases and common confusions

- **Defense paper, attacker named, only clean runs tested.** `trigger = benign-bug`; `defense_evaluated_against = benign`; note it. (The defense may still be meant for attackers; the field records what was tested.)
- **Attribution method (finds the failing agent or step).** `paper_type = attribution-method`, `detection_method = trace-analysis`, `defense_family = none`, `defense_evaluated_against = not applicable`, `trigger = benign-bug` unless the traces include attacks.
- **Benchmark paper.** Code the failures the benchmark covers. If it covers both kinds, `trigger = both`, and `trigger_evidence_level` is `direct-both` only if the same locus appears under both.
- **Single-agent paper that slipped through.** Do not code it; set `review_status = flagged` and write `scope: single-agent` in `review_note`. It moves to the exclude list.
- **Framework bug study or incident report.** `paper_type = framework-bug-study`, `evidence_type = documented-incident` (or `trace-analysis`), `trigger = benign-bug`. These count as grey literature in the corpus but are coded the same way.
- **Collusion.** `adversarial` if an operator or attacker instructs the agents to collude; `benign-bug` if collusion emerges without instruction; `both` if the paper tests both.
- **A paper that states a failure only in the motivation.** Do not code it. Code what the paper demonstrates or defends against.
- **A judgment call on `trigger_evidence_level` or `defense_evaluated_against`.** Code the narrower value, set `confidence = low`, and say why in `evidence_note`.

## 9. Check a sheet

```
python3 task3/make_sheet.py B01 llm-a      # blank sheet for a batch (llm-b the same; `human` and `adjudicated` cover only the audit sample)
python3 task3/validate_coding.py task3/coding/B01.llm-a.csv            # draft: TBD allowed, warnings shown
python3 task3/validate_coding.py task3/coding/B01.llm-a.csv --final    # final: no TBD, review_status must be accepted or corrected
python3 task3/test_validator.py                                          # 21 tests of the validator
```

The validator fails on: a wrong header, a blank cell, a value outside this codebook, an unknown or duplicate paper id, a broken cross-field rule (`trigger` against `trigger_evidence_level`; `defense_family = none` against `defense_evaluated_against`; `paper_type = defense` with no defense), and a missing `<field>:` segment in `evidence_note`. It warns on an `abstract-only` row marked `high`, on `TBD`, and on `evidence_type = theory-only`.

## 10. Changes from the plan's suggested fields (v0)

The plan lists 11 fields. This version adds:

- `mechanism_candidate`: Task 4 groups by mechanism and needs a label per paper. The list is the plan's candidate mechanisms plus three the corpus clearly calls for (privacy or information leakage; protocol or authorization flaw; coordination or communication failure). `other:<label>` lets the data extend it.
- `trigger_evidence_level` and `defense_evaluated_against`: required by the scope memo for RQ2 and RQ3.
- `locus_detail`: makes the "same locus" test possible.
- `trace_release`: Task 5 needs to know which papers release traces.
- `paper_type`, `evidence_type`: triage, and a check against the inclusion rule.
- `coded_from`, `confidence`, `evidence_note`: so every judgment can be audited.

Changes in how plan values are written:

- `swarm` is folded into `decentralized` (system type).
- The memo's "indirect" evidence level is not a value of `trigger_evidence_level`; it is computed across papers in Task 4. A within-paper value, `both-different-locus`, takes its place.

## 11. Open questions for the pilot

1. Is `trigger` clear for papers that simulate errors by injection, and for emergent deception?
2. Can `direct-both` be decided from an abstract, or does it always need the PDF? (The draft rule says to flag if unsure.)
3. Does the `defense_family` list cover the corpus, or are there too many `other:<label>` values?
4. Is up to three `mechanism_candidate` values too many?
5. Does `locus` (up to two values) lose information for orchestrator-related papers?
6. How long does a row take to review? This sets the pace for B01 to B19.
""")
open("03_codebook.md", "w", encoding="utf-8").write("\n".join(out))
print(len("\n".join(out).split()), "words")
