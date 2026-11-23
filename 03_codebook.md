# Codebook for the SoK corpus

**Version:** v1 candidate (revised after the v0 pilot; freezes once the v1 pilot run is adjudicated). Prepared Nov 23, 2026 for Task 3 of the SoK plan (subtask 3.0). This is v1 candidate: the v0 pilot (15 papers, two independent LLM coders) found six ambiguities, resolved in Section 10. It freezes as v1 once the v1 pilot run is adjudicated.
This file is generated from `task3/schema.py`; the validator reads the same schema, so the two cannot disagree. Edit the schema, then run `python3 task3/render_codebook.py`.

## 1. What a row is

One row per paper, 22 coded fields, plus the paper id, the coder, and two review fields. A row says what the paper shows, so that the taxonomy in Task 4 comes from data. It does not say whether the paper is good.

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
- **Task 4 mechanism list:** `mechanism_primary` and `mechanism_secondary`, including every `other:<label>`. Counts per mechanism use the primary value; the secondary value feeds the coverage matrix.
- **Task 5 trace sources:** `trace_release`.
- **Task 6 findings:** `framework`, `evidence_note` and the paper ids.

The four fields that matter most for RQ2 and RQ3, and are the hardest to code the same way twice, are `trigger`, `trigger_evidence_level`, `defense_family` and `defense_evaluated_against`. The reliability check reports them separately.

## 6. Fields

### 1. `system_type`

How the agents in the studied system are organized.

| Value | Meaning |
|---|---|
| `debate` | agents argue or vote over answers in rounds |
| `hierarchy` | an orchestrator, manager or supervisor assigns work to workers |
| `pipeline` | fixed sequence of agents, each consuming the previous output |
| `decentralized` | peer agents on a graph, swarm or network with no single controller |
| `mixed` | the paper studies more than one of the above, or a hybrid |
| `not reported` | the sources read do not say |

**Rules**

- Code the system the failure or attack is demonstrated on. If the paper evaluates several, use `mixed` and list them in `evaluation`.
- A planner that calls tools but has no second LLM agent is not a multi-agent system. That paper should go back to the maybe or exclude list.
- `mixed` only when the paper explicitly studies several organization types. If the paper does not describe the structure (for example, it evaluates generated teams of unspecified shape), use `not reported`.

**Example.** Illustration: three agents that each refine the previous agent's answer in order. Value: `pipeline`.

### 2. `framework`

Named framework or platform the system is built on.

Free text.

**Rules**

- Use the names the paper uses (AutoGen, CrewAI, LangGraph, MetaGPT, ChatDev, AgentVerse, OpenAI Agents SDK, and so on). Separate several with `;`.
- `custom` if the authors built their own. `not reported` if no name or description is given.

**Example.** Illustration: `AutoGen; LangGraph`.

### 3. `n_agents`

Number of agents in the main experiments.

Format: `^(\d+(-\d+)?\+?|varies)$`.

**Rules**

- A single integer (`5`), a range (`3-10`), a lower bound (`10+`), or `varies`.
- Use `varies` whenever the main experiments use more than one agent count, whether or not scale is a studied variable (several systems, datasets or topologies). Put the counts or ranges in `evaluation`.
- If one setting is clearly the main one, give that number, not the largest one mentioned.

**Example.** Illustration: a 10-agent network in the main table, scaled to 50 in an ablation. Value: `10`. Three case-study systems with 3, 5 and 7 agents: `varies`.

### 4. `failure_observed`

One line: what goes wrong (or what the attacker achieves).

Free text.

**Rules**

- Say it in the paper's terms, in one sentence, no more than 30 words.
- For a defense or detection paper, give the failure or attack it targets.

**Example.** Illustration: `A false claim in one agent's output is repeated and reinforced by the next agents until the group answer is wrong.`

### 5. `mechanism_primary`

The one failure mechanism the paper is mainly about, named by how it works, not by its symptom. A working label that Task 4 will regroup; it is not the final taxonomy.

| Value | Meaning |
|---|---|
| `role-or-spec-drift` | an agent leaves its assigned role or specification |
| `message-corruption-or-injection` | inter-agent messages are altered, forged or carry injected instructions |
| `shared-memory-poisoning` | a shared or persistent memory or state store is corrupted |
| `unverified-handoff` | one agent's output is accepted by the next without a check |
| `error-cascade` | an error is passed on and grows or sticks across agents or steps |
| `collusion-or-groupthink` | agents coordinate covertly, or converge on a wrong consensus through social pressure |
| `orchestrator-compromise` | the controlling agent or planner is subverted or fails |
| `tool-misuse` | a tool is called wrongly, with wrong arguments, or with abused authority |
| `termination-failure` | the system does not stop, stops too early, or loops |
| `privacy-or-information-leakage` | private data moves to an agent or place it should not |
| `protocol-or-authorization-flaw` | identity, permission or protocol design lets the wrong party act |
| `coordination-or-communication-failure` | agents fail to align, are misread, or lose context between them |
| `not reported` | the paper gives no way to place it |

**Rules**

- Name the mechanism, not the symptom: `wrong final answer` is a symptom; `error-cascade` is a mechanism.
- Exactly one. Pick the mechanism the paper's main result is about. If two compete equally, take the one the paper names first or tests most, and put the other in `mechanism_secondary`.
- If none fits, use `other:<short label>`; those labels are the data Task 4 uses to extend the list.
- Code what the paper shows or defends against, not what it mentions in related work.

**Example.** Illustration: an attacker rewrites messages between two agents. Value: `message-corruption-or-injection`.

### 6. `mechanism_secondary`

An optional second mechanism that is substantial in the paper.

| Value | Meaning |
|---|---|
| `role-or-spec-drift` | an agent leaves its assigned role or specification |
| `message-corruption-or-injection` | inter-agent messages are altered, forged or carry injected instructions |
| `shared-memory-poisoning` | a shared or persistent memory or state store is corrupted |
| `unverified-handoff` | one agent's output is accepted by the next without a check |
| `error-cascade` | an error is passed on and grows or sticks across agents or steps |
| `collusion-or-groupthink` | agents coordinate covertly, or converge on a wrong consensus through social pressure |
| `orchestrator-compromise` | the controlling agent or planner is subverted or fails |
| `tool-misuse` | a tool is called wrongly, with wrong arguments, or with abused authority |
| `termination-failure` | the system does not stop, stops too early, or loops |
| `privacy-or-information-leakage` | private data moves to an agent or place it should not |
| `protocol-or-authorization-flaw` | identity, permission or protocol design lets the wrong party act |
| `coordination-or-communication-failure` | agents fail to align, are misread, or lose context between them |
| `none` | no second mechanism is substantial in the paper |
| `not reported` | the paper gives no way to place it |

**Rules**

- `none` unless the paper gives a second mechanism real weight (its own experiments or its own section).
- Never the same value as `mechanism_primary`.

**Example.** Illustration: a paper on error cascades that also studies a missing handoff check. Primary: `error-cascade`. Secondary: `unverified-handoff`.

### 7. `trigger`

What causes the failure the paper studies, tests or defends against.

| Value | Meaning |
|---|---|
| `benign-bug` | the failure arises without an adversary (model error, design flaw, bad prompt, framework bug, environment fault) |
| `adversarial` | an attacker or deliberately malicious agent causes it |
| `both` | the paper's experiments or evidence cover both kinds of trigger |
| `not applicable` | the paper has no failure trigger to code (use rarely; record why in `evidence_note`) |

**Rules**

- Code what the paper demonstrates or evaluates, not what it speculates about.
- A defense paper takes the trigger(s) it was evaluated against. If it names an attacker but tests only clean runs, code `benign-bug` and say so in the note.
- A paper that injects faults to simulate errors is `benign-bug`. A paper that simulates a malicious agent is `adversarial`. A paper that does both is `both`.
- Misaligned goals or deception that an agent shows without anyone instructing it is `benign-bug` (no adversary). If an operator tells the agent to deceive, it is `adversarial`.
- **Decide by how the failure is induced, not by the paper's label.** Papers call faulty or weak agents "malicious" or "Byzantine" loosely. A weaker model, an injected error or a corrupted message with no instruction to harm is `benign-bug`. An agent that is instructed to deceive, sabotage or subvert is `adversarial`. If the paper implements both kinds, it is `both`. Say which implementation you relied on in `evidence_note`.

**Example.** Illustration: a study injects wrong answers into one agent to see how errors spread, and separately a prompt-injection attack on the same agent. Value: `both`.

### 8. `trigger_evidence_level`

Whether the paper itself links the two triggers. This feeds RQ2 and the dual-trigger test in Task 4. Two separate papers that each show one side are 'indirect' evidence; that is worked out across papers in Task 4, not coded here.

| Value | Meaning |
|---|---|
| `direct-both` | one paper shows both triggers acting at the same locus: the same agent role, channel, store, tool or orchestrator step, in the same experimental system |
| `both-different-locus` | both triggers appear, but at different loci, or in different systems or datasets |
| `benign-only` | only benign triggers appear |
| `adversarial-only` | only adversarial triggers appear |
| `not applicable` | matches `trigger = not applicable` |

**Rules**

- Must agree with `trigger`: `benign-bug` goes with `benign-only`; `adversarial` with `adversarial-only`; `both` with `direct-both` or `both-different-locus`; `not applicable` with `not applicable`.
- `direct-both` needs a passage showing the same locus under both triggers; quote or cite it in `evidence_note`. If unsure, use `both-different-locus` and flag the row.
- **Same locus means the same role in the same experimental system.** Benign failures taken from one system's traces and attacks run on a different pipeline are `both-different-locus`, even if the paper maps both to the same kind of boundary; record that mapping in `evidence_note`. The same role reached through two interfaces (a system prompt in one condition, a message in another) counts as the same locus only if the paper treats it as the same agent role.

**Example.** Illustration: one pipeline where a hallucinated hand-off and an injected hand-off at the same step are both measured. Value: `direct-both`.

### 9. `locus`

Where the failure starts, not where it ends.

| Value | Meaning |
|---|---|
| `one-agent` | the failure starts inside a single agent (its reasoning, role or model) |
| `message-channel` | it starts in messages passed between agents |
| `shared-memory` | it starts in a shared or persistent store |
| `tool` | it starts in a tool, its description, its output or its permissions |
| `orchestrator` | it starts in the controlling agent, planner or routing step |
| `environment-input` | it starts in outside data the system reads (web page, document, user input) |
| `not reported` | the sources read do not say |

Separate several values with `;`.

**Rules**

- Up to three values. Pick where the first deviation happens or where the attacker acts. If a paper covers more than three loci, give the three it spends the most on and say so in `locus_detail`.
- An injection through a web page that an agent reads is `environment-input` first; if the paper makes the agent's message the vehicle, add `message-channel`.

**Example.** Illustration: a poisoned document read by one agent then summarized to others. Value: `environment-input`.

### 10. `locus_detail`

The specific role, channel, store or tool, as the paper names it.

Free text.

**Rules**

- Short: for example `critic agent`, `planner-to-executor messages`, `vector memory shared by all agents`.
- This is what makes the 'same locus' test possible in Task 4, so be specific.

**Example.** Illustration: `the verifier agent's output channel`.

### 11. `spread`

How the failure moves once it starts.

| Value | Meaning |
|---|---|
| `stays local` | the failure remains in the agent, message or step where it started |
| `cascades` | it passes from agent to agent or step to step |
| `amplifies` | it grows or gets worse as it passes on (more errors, more agents affected, higher attack success) |
| `not studied` | the paper's design does not examine how it moves |
| `not reported` | the sources read do not say |

**Rules**

- Code only what the paper measures or states about movement between agents or steps. A claim that 'the whole system is compromised' is an effect, not a measure of spread; use `not reported` unless the text shows how.
- `amplifies` needs evidence of growth, for example error rate or attack success rising with depth or number of agents.
- Attenuation (the failure fades) is `stays local` if it never passes on, or `cascades` if it passes on and shrinks. Say which in the note.
- `cascades` means the reach grows: more agents or steps are affected (counts of affected agents over time, hops or rounds). `amplifies` means severity grows: the effect gets worse per hop or per added agent (error rate, attack success rate).
- A paper that reports only final performance split by structure, with no measure of movement, is `not reported`.
- In an abstract-only row, an explicit statement in the abstract that the failure propagates between agents may be coded, but set `confidence` to `medium` or `low`.

**Example.** Illustration: attack success rises with the number of agents in the chain. Value: `amplifies`.

### 12. `detection_method`

How the paper finds or localizes failures, if it does.

| Value | Meaning |
|---|---|
| `none` | the paper does not detect or localize failures |
| `trace-analysis` | reads logs or traces after the fact to find the failing agent or step (attribution, debugging) |
| `anomaly-detector` | a trained or statistical model flags abnormal agents or messages |
| `runtime-monitor` | a live check watches behavior during a run |
| `output-check` | a judge or rule checks outputs or claims |
| `not reported` | the sources read do not say |

Separate several values with `;`. `other:<label>` is also accepted.

**Rules**

- Code only methods the paper proposes or evaluates, not ones it cites.
- A paper may have both a detector and a defense. Code the detector here and the response in `defense_family`.
- `anomaly-detector` is a trained or statistical model; `output-check` is a judge or rule on outputs or claims; `trace-analysis` is after-the-fact reading of a run. A method used only to find the failure classes in a study (the authors' analysis) is `trace-analysis`, not a tool they propose.

**Example.** Illustration: an LLM judge that reads the full conversation to name the step that broke the run. Value: `trace-analysis`.

### 13. `defense_family`

The kind of defense or mitigation the paper proposes or evaluates. The columns of the Task 4 coverage matrix.

| Value | Meaning |
|---|---|
| `none` | the paper proposes or evaluates no defense or mitigation |
| `input-filtering` | screens inputs or messages before an agent acts on them |
| `verification-agent` | an extra agent or judge checks another agent's work |
| `provenance-authorization` | tracks where information came from or limits who may act (identity, permissions, signatures) |
| `sandboxing-isolation` | separates agents, tools or memory so a failure cannot reach the rest |
| `monitoring` | watches the system and intervenes, removes or repairs agents |
| `consensus-voting` | aggregates several agents or runs to outvote errors |
| `redundancy-fault-tolerance` | replicates, retries or recovers to survive failures |
| `not reported` | the sources read do not say |

Separate several values with `;`. `other:<label>` is also accepted.

**Rules**

- Code defenses the paper proposes or tests, not ones it only discusses.
- Up to three values. Prefer the main idea over every component.
- `other:<label>` if none fits; those labels are how Task 4 learns that the family list is incomplete.
- A defense that is argued for but never implemented is `none` for `defense_family` unless the paper evaluates it formally (then use the family and `formal-only`).

**Example.** Illustration: a graph model that detects and cuts off a malicious agent. Values: `monitoring`.

### 14. `defense_evaluated_against`

Which trigger the defense was actually tested against. This feeds RQ3: which mechanism-by-trigger cells have no evaluated defense.

| Value | Meaning |
|---|---|
| `benign` | tested only against benign failures |
| `adversarial` | tested only against attackers |
| `both` | tested against both |
| `not evaluated` | proposed but nothing tests it |
| `formal-only` | checked by proof, model checking or formal analysis against the threat model, with no experiment |
| `not applicable` | the paper has no defense (`defense_family = none`) |

**Rules**

- `none` in `defense_family` goes with `not applicable`; any other family goes with one of `benign`, `adversarial`, `both`, `not evaluated` or `formal-only`.
- Test against means an experiment, not a sentence in the discussion. Quote the table or section in `evidence_note`.
- Hardest field after `trigger_evidence_level`: when unsure, code the narrower value and flag the row.

**Example.** Illustration: a monitor tested on injected prompt attacks only. Value: `adversarial`.

### 15. `evaluation`

Benchmarks or datasets, main metrics, models tested, and scale.

Free text.

**Rules**

- One line, for example `MMLU and a custom injection set; attack success rate; GPT-4o and Llama-3-70B; 3 topologies`.
- `not reported` if the sources read do not say.

**Example.** Illustration: `500 runs over 10 domains; hallucination score; three LLMs`.

### 16. `trace_release`

Whether the paper released failure traces or runs, and where. Task 5 depends on this.

Format: `^(yes: .+|no)$`.

**Rules**

- `yes: <host or URL>; license: <name or unknown>` when traces are public, `no` when the paper does not release them.
- Never guess a license. If the paper does not name one, write `license: unknown` and let Task 5 check the host.

**Example.** Illustration: `yes: huggingface.co/datasets/example; license: unknown`.

### 17. `limitation`

The main limit the authors state, or an obvious one.

Free text.

**Rules**

- One line. If you add your own, start with `Reviewer:` so it is not confused with the authors' statement.

**Example.** Illustration: `Tested on three models only; no human baseline.`

### 18. `paper_type`

The main contribution type, for triage.

| Value | Meaning |
|---|---|
| `attack` | proposes or demonstrates an attack |
| `failure-study` | empirical study of how and why failures occur |
| `attribution-method` | locates the failing agent or step in a trace |
| `defense` | proposes or evaluates a defense or detector |
| `benchmark` | a dataset or benchmark for failures or attacks |
| `framework-bug-study` | studies bugs in agent frameworks or deployed systems |
| `theory` | formal or analytical model without a main experiment |
| `mixed` | two or more of the above in roughly equal parts |

**Rules**

- Pick the primary contribution. `mixed` only when no one type dominates.

**Example.** Illustration: a new attack and a defense for it with equal space. Value: `mixed`.

### 19. `evidence_type`

What kind of evidence the paper rests on. Checks the inclusion rule.

| Value | Meaning |
|---|---|
| `experiment` | controlled experiments on a system |
| `trace-analysis` | analysis of recorded runs or traces |
| `documented-incident` | a real incident, CVE or bug report |
| `theory-only` | no empirical evidence |

Separate several values with `;`.

**Rules**

- `theory-only` covers analytical or formal arguments, including formal verification and model checking, with no runs of a system. Such papers should not be in the included set; flag the row so it can move to the exclude list.
- Code the evidence the paper's main results rest on. Up to two values.

**Example.** Illustration: `experiment; trace-analysis`.

### 20. `coded_from`

How much of the paper was read for this row. Honesty about depth.

| Value | Meaning |
|---|---|
| `abstract-only` | only the abstract (and metadata) was read |
| `abstract-plus-sections` | the abstract plus the threat-model or failure section and the evaluation |
| `full-text` | the whole paper was read |

**Rules**

- Papers with no PDF can only be `abstract-only`.
- A row coded from the abstract alone that still has `TBD` values needs a PDF read before it can pass the final check.
- Reading a PDF through text extraction counts as reading it. Use `full-text` only if the whole paper was read, appendices included.

**Example.** Illustration: `abstract-only`.

### 21. `confidence`

How sure the coder is of the row as a whole.

| Value | Meaning |
|---|---|
| `high` | stated plainly in the text read |
| `medium` | clear but inferred from one passage |
| `low` | a judgment call; the reviewer should look first |

**Rules**

- An `abstract-only` row can be `high` only if every substantive field is stated outright in the abstract; the validator warns otherwise.
- Set `low` whenever any of the six key fields (`trigger`, `trigger_evidence_level`, `locus`, `spread`, `defense_family`, `defense_evaluated_against`) is a judgment between two adjacent values, or rests only on a claim in the abstract that the experiments do not show.
- Set `medium` when every key field is clear but at least one rests on a single passage. Set `high` only when all key fields are stated plainly in the text you read.

**Example.** Illustration: `medium`.

### 22. `evidence_note`

The passage, section or figure each key judgment rests on, so a reviewer can check it in seconds.

Free text, with one tagged segment per key field.

**Rules**

- One tagged segment per key field that has a substantive value, in the form `trigger: "quoted or cited passage"; locus: ...`.
- Key fields are: trigger, trigger_evidence_level, locus, spread, defense_family, defense_evaluated_against.
- Fields set to `not reported`, `not applicable`, `none`, `not studied` or `TBD` need no segment.
- Keep each passage under about 25 words. Cite the section or table if you have the PDF (`§5.2`, `Table 3`).

**Example.** Illustration: `trigger: "we inject faulty answers" (§3); locus: agent 2 output (§3); spread: error rate vs depth (Fig. 4)`.

## 7. Worked example: a real row from the corpus

P023, *Red-Teaming LLM Multi-Agent Systems via Communication Attacks* (batch B13). It is not a pilot paper and not in the double-coded sample. It is coded **from the abstract only**, to show how that looks: every value below can be traced to the abstract, and what the abstract does not state is `not reported` or `TBD`. This row is in `task3/coding/example.csv`.

| Field | Value |
|---|---|
| `pid` | P023 |
| `coder` | llm-a |
| `system_type` | not reported |
| `framework` | not reported |
| `n_agents` | TBD |
| `failure_observed` | An attacker intercepts and rewrites messages between agents (Agent-in-the-Middle) to steer the whole multi-agent system. |
| `mechanism_primary` | message-corruption-or-injection |
| `mechanism_secondary` | none |
| `trigger` | adversarial |
| `trigger_evidence_level` | adversarial-only |
| `locus` | message-channel |
| `locus_detail` | messages passing between agents, intercepted and manipulated by an adversarial LLM agent |
| `spread` | not reported |
| `detection_method` | none |
| `defense_family` | none |
| `defense_evaluated_against` | not applicable |
| `evaluation` | Several frameworks, communication structures and real-world applications; benchmarks, metrics and models are not given in the abstract. |
| `trace_release` | not reported |
| `limitation` | not reported |
| `paper_type` | attack |
| `evidence_type` | experiment |
| `coded_from` | abstract-only |
| `confidence` | medium |
| `evidence_note` | trigger: "an adversary can compromise entire multi-agent systems by only manipulating the messages" (abstract); trigger_evidence_level: abstract describes attacks only, no benign condition; locus: "intercepting and manipulating inter-agent messages" (abstract); spread: abstract states whole-system compromise but not how the effect moves, so left not reported |
| `review_status` | pending |
| `review_note` | none |

Reading the row: the abstract describes an attack (Agent-in-the-Middle) and no benign condition, so `trigger = adversarial` and the evidence level is `adversarial-only`. `spread` is `not reported` because "compromise entire multi-agent systems" is an effect, not a measure of how the failure moves. `n_agents` is `TBD` because a PDF exists and the number will be in the experiments section. A full-text read would fill `system_type`, `framework`, `n_agents` and `evaluation`, and could move `confidence` to `high`.

## 8. Hard cases and common confusions

- **Defense paper, attacker named, only clean runs tested.** `trigger = benign-bug`; `defense_evaluated_against = benign`; note it. (The defense may still be meant for attackers; the field records what was tested.)
- **Attribution method (finds the failing agent or step).** `paper_type = attribution-method`, `detection_method = trace-analysis`, `defense_family = none`, `defense_evaluated_against = not applicable`, `trigger = benign-bug` unless the traces include attacks.
- **Benchmark paper.** Code the failures the benchmark covers. If it covers both kinds, `trigger = both`, and `trigger_evidence_level` is `direct-both` only if the same locus appears under both.
- **Single-agent paper that slipped through.** Do not code it; set `review_status = flagged` and write `scope: single-agent` in `review_note`. It moves to the exclude list.
- **Framework bug study or incident report.** `paper_type = framework-bug-study`, `evidence_type = documented-incident` (or `trace-analysis`), `trigger = benign-bug`. These count as grey literature in the corpus but are coded the same way.
- **Collusion.** `adversarial` if an operator or attacker instructs the agents to collude; `benign-bug` if collusion emerges without instruction; `both` if the paper tests both.
- **A paper that states a failure only in the motivation.** Do not code it. Code what the paper demonstrates or defends against.
- **A paper that calls faulty agents "malicious" or "Byzantine".** Decide by how the failure is induced: a weaker model or an injected error is `benign-bug`; an agent instructed to deceive or sabotage is `adversarial`; both implemented is `both`.
- **Benign failures from one system, attacks on another.** `both-different-locus`. `direct-both` needs the same role in the same experimental system.
- **A defense checked only by proof or model checking.** `defense_evaluated_against = formal-only`.
- **Main experiments use different agent counts.** `n_agents = varies`; give the counts in `evaluation`.
- **An abstract claims propagation that the experiments do not show.** Code only what the text you read supports. In an abstract-only row, an explicit abstract statement may be coded with `confidence` medium or low.
- **A judgment call on `trigger_evidence_level` or `defense_evaluated_against`.** Code the narrower value, set `confidence = low`, and say why in `evidence_note`.

## 9. Check a sheet

```
python3 task3/make_sheet.py B01 llm-a      # blank sheet for a batch (llm-b the same; `human` and `adjudicated` cover only the audit sample)
python3 task3/validate_coding.py task3/coding/B01.llm-a.csv            # draft: TBD allowed, warnings shown
python3 task3/validate_coding.py task3/coding/B01.llm-a.csv --final    # final: no TBD, review_status must be accepted or corrected
python3 task3/test_validator.py                                          # 21 tests of the validator
```

The validator fails on: a wrong header, a blank cell, a value outside this codebook, an unknown or duplicate paper id, a broken cross-field rule (`trigger` against `trigger_evidence_level`; `defense_family = none` against `defense_evaluated_against`; `paper_type = defense` with no defense), and a missing `<field>:` segment in `evidence_note`. It warns on an `abstract-only` row marked `high`, on `TBD`, and on `evidence_type = theory-only`.

## 10. Changes

### v0 to v1 candidate (after the v0 pilot)

The v0 pilot had two independent LLM coders (Opus and Sonnet tiers) code the same 15 papers. They agreed on `trigger` and `trigger_evidence_level` for 13 of 15 papers (87%), on `defense_evaluated_against` for 14 of 15 (93%), but only on 67% for `spread`, 60% for `locus` and 47% for `mechanism_candidate` (exact set match). Their notes pointed to six ambiguities. Each is resolved as follows:

1. **"Malicious" fault models.** `trigger` is decided by how the failure is induced, not by the paper's label (Section 8).
2. **"Same locus".** `direct-both` needs the same role in the same experimental system. Benign failures from one system and attacks on another are `both-different-locus`.
3. **Formal verification.** New value `formal-only` for `defense_evaluated_against`, so the RQ3 matrix can separate it from experiments and from untested proposals.
4. **`n_agents`.** `varies` whenever the main experiments use more than one count; the counts go in `evaluation`.
5. **Mechanism and locus.** `mechanism_candidate` is split into `mechanism_primary` (exactly one) and `mechanism_secondary` (optional). `locus` allows up to three values.
6. **Scope.** One pilot paper is a formal analysis of a protocol specification with no running system, and another is a framework bug study centred on a single-agent stage. Decisions: the formal-analysis paper is excluded from the final matrix (it meets neither inclusion rule 1 nor 2); the bug study stays as a flagged framework bug study. See `task3/scope_decisions.csv`.

Smaller clarifications in the field rules: `spread` (reach versus severity; final performance by structure is `not reported`; abstract-only claims), `detection_method`, `defense_family` (a defense never implemented), `evidence_type` (formal analysis is `theory-only`), `system_type` (`mixed` only if several types are studied), `coded_from` (text extraction counts as reading) and `confidence` (now a rule, not a feeling; it was the least reliable field in the pilot, kappa 0.33, so use it for triage only).

### Plan to v0

The plan lists 11 fields. v0 added:

- `mechanism_candidate` (now `mechanism_primary` and `mechanism_secondary`): Task 4 groups by mechanism and needs a label per paper. The list is the plan's candidate mechanisms plus three the corpus clearly calls for (privacy or information leakage; protocol or authorization flaw; coordination or communication failure). `other:<label>` lets the data extend it.
- `trigger_evidence_level` and `defense_evaluated_against`: required by the scope memo for RQ2 and RQ3.
- `locus_detail`: makes the "same locus" test possible.
- `trace_release`: Task 5 needs to know which papers release traces.
- `paper_type`, `evidence_type`: triage, and a check against the inclusion rule.
- `coded_from`, `confidence`, `evidence_note`: so every judgment can be audited.

Other changes: `swarm` is folded into `decentralized` (system type). The memo's "indirect" evidence level is not a value of `trigger_evidence_level`; it is computed across papers in Task 4. A within-paper value, `both-different-locus`, takes its place.

## 11. Still open

1. Whether `direct-both` can be decided from an abstract at all, or always needs the PDF. The rule says to flag if unsure.
2. Whether the `defense_family` list covers the corpus, or there are too many `other:<label>` values. Count them after the first batches.
3. How long a row takes to adjudicate or audit. This sets the pace for B01 to B19.

