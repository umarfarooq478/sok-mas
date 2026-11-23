# PILOT, coder llm-a: judgment calls and unclear points

How I read: PDFs were turned into text with `pdftotext` and read section by section (intro, threat model, method, evaluation, limitations, and appendices where a key field needed them). P230, P056 and P267 have no PDF and are coded from the abstract only.

## Field-level judgment calls

| Field | Paper | What was unclear | What I chose |
|---|---|---|---|
| trigger_evidence_level | P133 | The benign tracer seed goes into the entry agent's system-level instructions. The attack is an application-level message injected at hub or aggregator agents. Same agents can be hit, but the interface differs. | `both-different-locus`, low confidence |
| defense_evaluated_against | P133 | The abstract says the governance layer stops endogenous and exogenous amplification, but Tables V to VII report only attack settings. | `adversarial` (trust experiments), flagged in review_note |
| paper_type | P133 | Propagation model, vulnerability study, attack and defense take roughly equal space. | `mixed` |
| trigger / trigger_evidence_level | P248 | Benign failure classes come from TRAIL production traces (a two-tier system), and attacks come from the authors' 10-agent pipeline. Each class sits at the same named boundary but in a different system. | `both` + `both-different-locus`, low confidence |
| system_type | P248 | The paper calls it a five-layer pipeline, but an orchestrator routes and delegates. | `pipeline` (paper's own term, DAG in topological order) |
| detection_method | P248 | Structural trace analysis is how the authors find the failure classes, not a tool they propose. | `trace-analysis` |
| n_agents | P026, P032, P012 | Systems have different agent counts, but scale is not a studied variable (P012 does vary 10 to 50 in the town). The codebook keeps `varies` for a studied scale. | `varies`. The codebook should say what to use when agent counts differ across systems but scale is not studied. |
| defense_family | P026 | Case-study fixes are a verification step plus prompt or role and topology changes. No family fits prompt or workflow redesign. | `verification-agent; other:prompt-and-workflow-redesign` |
| trigger | P008 | AutoTransform tells an agent to "subtly introduce errors" (a simulated malicious agent), while AutoInject is fault injection into messages. The paper calls both "clumsy or malicious". | `both` |
| trigger_evidence_level | P008 | Both methods target the same "Faulty Agent" role per system (Table 1): its profile in one case, its output messages in the other. | `direct-both`, low confidence |
| spread | P008 | The paper measures the final performance drop by structure, not movement between agents. | `not reported` |
| trigger | P080 | "Byzantine/malicious" agents are weaker models (GPT-3.5, LLaMA3-8B) with no malicious instruction. Only their positions are chosen adversarially. | `benign-bug`, low confidence, flagged |
| system_type | P080 | Six graph topologies, including star and tree, but all run a peer consensus protocol. | `decentralized` |
| detection_method | P080 | Hidden-state linear probe that scores agent confidence. | `anomaly-detector` |
| spread | P012 | Infected-agent count follows logistic growth over time. Is that `amplifies` or `cascades`? | `cascades`. Growth in reach over time is not growth in severity per hop. |
| paper_type | P128 | Fault-injection framework plus empirical findings. Could be `benchmark`. | `failure-study` |
| trace_release | P128 | "Experimental data ... publicly available" on GitHub. It may include execution logs, but I did not check. | `yes: github.com/wxhhxn/MASFIRE; license: unknown`, noted |
| trace_release | P008, P133 | "Code and data" or "datasets" are released, but released traces are not stated. | `no` |
| mechanism_candidate | P032 | Decisive-error attribution names no mechanism. Generic agent mistakes fit no listed value. | `other:decisive-agent-error` |
| system_type | P032 | CaptainAgent-generated teams plus the Magentic-One orchestrator. | `mixed` |
| trigger | P003 | Group evaluations instruct covert communication (adversarial). Appendix J.2.1 shows models incentivised to encode secretly with no instruction (benign under the collusion rule). The insider-trading case involves a malicious user. | `both` + `both-different-locus`, low confidence |
| defense_family | P003 | The overseer is part of the evaluation. Paraphrasing and parameter optimisation are only theory. | `monitoring`, `adversarial` |
| evidence_type / scope | P289 | Vulnerabilities come from formal FSM analysis of the spec plus Alloy and TLA+ checks. Experiments test the analysis tool, not a running MAS. | `theory-only`, scope note |
| defense_evaluated_against | P289 | Three mitigations are formally verified, with no experiment. | `not evaluated`, low confidence |
| locus | P230 | Framework code bugs fit no locus value. | `not reported` |
| scope | P230 | Bugs concentrate in single-agent "Self-Action"; the share that is multi-agent is unknown. | scope note |
| spread | P056 | "Decrease in accuracy over time" in the abstract. Is that amplification? | `cascades` (narrower), noted |
| paper_type | P267 | Taxonomy, benchmark and mitigation are roughly equal. | `mixed` |
| locus | P025 | Attack content enters via a file or web agent and reaches the orchestrator as metadata. | `environment-input; message-channel` |

## Codebook points that were most ambiguous

1. **Which simulated faulty agents count as "malicious".** The trigger rule separates "inject faults" (benign) from "simulate a malicious agent" (adversarial). Papers often call a weaker model or an error-prompted agent "malicious" (P080, P008). It is unclear whether the label, the instruction, or the behaviour decides.
2. **"Same locus" for direct-both.** It is unclear whether the same agent role in different systems (P248), or the same agent reached through different interfaces such as system prompt vs message (P133, P008), counts as the same locus.
3. **`n_agents = varies`** is defined only for a studied scale. Multi-system datasets (P026, P032) need a value.
4. **Formal or specification-analysis papers** (P289): whether formal verification counts as "evaluated" for `defense_evaluated_against`, and whether such papers are `theory-only`.
5. **`trace_release`** when a repo releases "data" without saying whether run logs are included.
