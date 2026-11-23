# PILOT notes, coder llm-b

Reading: 12 PDFs read in sections (abstract, method or threat model, evaluation tables, limitations; related work skipped). P230, P056, P267 have no PDF and are coded abstract-only. Text was extracted with pdftotext.

## trigger / trigger_evidence_level
- P008, P080 (benign vs adversarial): both papers call the faulty agents "malicious" or "Byzantine", but implement them as error injection (P008) or a weaker model paired with a stronger one (P080). The rule "injecting faults to simulate errors is benign" was applied, with low confidence. The codebook does not say what to do when a paper uses adversarial wording for a fault model.
- P133, P248 (both): each has an endogenous or benign condition and an attack condition. `direct-both` was not used because the benign condition and the attack are not shown at one identical agent or step (P133 seed in the entry agent system prompt vs injection at the hub; P248 benign traces come from a different system than the attack runs). Chose `both-different-locus`, low confidence. The definition of "same locus" is too loose to settle this: P248 maps benign and adversarial failures to the same boundary classes.
- P003: the insider-trading case may be emergent collusion (benign by the collusion hard case) but is a single qualitative anecdote. Coded `adversarial`.
- P025: accidental-hijack anecdote in the discussion is not an experiment; not counted.

## defense_family / defense_evaluated_against
- P133: abstract says the defense suppresses endogenous and exogenous amplification; Tables V-VII use attacker policies only. Coded `adversarial`.
- P289: mitigations were checked only in Alloy and TLA+ models. "Test means an experiment", so `not evaluated`. A formal check against the adversary could be read as `adversarial`; the codebook does not cover formal verification.
- P248: boundary verification is argued as a primitive but never implemented; coded `none`, not `provenance-authorization` + `not evaluated`.
- P003: paraphrasing and parameter optimisation are analyzed theoretically; only the overseer (monitoring), which is tested in group evaluations, is coded.
- P012: LLM Tagging coded `provenance-authorization` (labels message origin); the repurposed marking and delimiting baselines as `input-filtering`.
- P026: interventions are appendix case studies; coded as `verification-agent` plus `other:role-spec-and-workflow-refinement`.
- P080: the confidence probe is both a detector (`anomaly-detector`) and a weight for voting (`consensus-voting`); the main idea is consensus.

## spread
- P008: only final performance by structure is measured; coded `cascades` with medium doubt. P080: same kind of evidence but coded `not reported`; the two are inconsistent by one judgment call (P008 states that higher-level distributors matter, P080 does not discuss movement).
- P119, P012: `amplifies` from infection counts or ASR rising over rounds.
- P056, P267: abstract claims propagation or decline over rounds; per the auditor rule, `not reported`.

## locus
- P026: differs per failure mode, so `not reported` with the detail in `locus_detail`.
- P056: `message-channel` vs `one-agent` (conformity inside the model) is a coin toss.
- P248: four attacks hit four loci; limit of two values forced a choice (environment-input; message-channel).

## Other
- P032: `system_type` left `not reported`; Magentic-One has an orchestrator but the generated teams are unspecified. `n_agents` 1-5 is from the appendix table.
- P289: scope concern. Protocol-spec analysis, no running LLM MAS; `evidence_type = experiment` rests on the extraction pipeline compared with expert review.
- P230: scope concern. Framework bugs, most in the single-agent Self-Action stage.
- P133, P008, P080: `trace_release` coded `no` because the release is code (and data of unknown kind), not clearly failure traces. For P008 the abstract says "code and data".
- P026: `detection_method = trace-analysis` is an LLM annotator labeling modes per trace, not locating the failing agent. Judgment call.
- P128: the codebook has no clean `paper_type` for a fault-injection evaluation framework; chose `failure-study`.
- P003: `paper_type = mixed` (formalization, framework, empirical).
- `n_agents`: not stated in the sections read for P119, P128, P289, P025; coded `not reported`.
