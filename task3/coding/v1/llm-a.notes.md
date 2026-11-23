# PILOT.v1, coder llm-a: judgment calls

Codebook v1 candidate (22 fields). There are 15 rows. 12 were coded from PDF text extraction: P248 and P012 were read in full, and the rest were read in their main sections. P230, P056 and P267 have no PDF and are coded `abstract-only`.

## Key fields (trigger, evidence level, locus, spread, defense)

- **P133, `trigger_evidence_level`.** Both triggers run on the same six frameworks. The benign seed is prefixed to an agent's *system-level directive* (entry, hub or leaf). The attack is an *application-level injected message* aimed at high-influence nodes, and the paper explicitly separates the two (App. B, §VII-A). The same-locus rule says two interfaces count as one locus only if the paper treats them as the same role, and it does not here. Chosen: `both-different-locus`, with confidence `low`.
- **P133, `defense_evaluated_against`.** The abstract says the layer suppresses "both endogenous and exogenous" amplification. Table V and the ablations only report the attack settings (Baseline, Compliance, Security FUD). Following the experiments, I chose `adversarial`.
- **P008, `trigger` and `trigger_evidence_level`.** AutoTransform rewrites the profile so that it becomes a "vicious agent" that inserts errors on purpose. That is an instructed saboteur, so `adversarial`. AutoInject rewrites the agent's messages so they contain errors, with no instruction to the agent, so `benign` under the "corrupted message with no instruction to harm" rule. Both act on the same "Faulty Agent" per system (Table 1), so I chose `both` / `direct-both`. Confidence is `low` because the two interfaces differ (profile vs message). This is the clearest case where the codebook's induction-based rule and the paper's own framing ("clumsy or malicious") split.
- **P080, `trigger`.** The "Byzantine/malicious" agents are weaker models (GPT-3.5-turbo, LLaMA3-8B) used "to simulate natural performance variability". I chose `benign-bug` under the §8 hard case, even though the paper speaks of "adversarial conditions".
- **P003, `trigger`.** The group steganography evaluations prompt sender and receiver to hide a secret from an overseer (instructed collusion). The insider-trading case involves a "malicious user". Uninstructed (emergent) collusion is shown only qualitatively, so I chose `adversarial` / `adversarial-only` with confidence `low`. If emergent collusion is meant to count, the answer is `both`.
- **P003, defense.** Monitoring by an overseer is measured experimentally (26% undetected). Paraphrasing and parameter optimisation are analysed only through theorems. The field takes a single value, so I chose `adversarial`. The formal-only part sits under the `other:paraphrasing` label.
- **P248, `trigger_evidence_level`.** The benign failures come from TRAIL traces (GAIA two-tier and SWE-Bench single CodeAgent), and the attacks run on a different custom 10-agent pipeline. Following §8, I chose `both-different-locus`.
- **P248, `system_type`.** The paper calls it a pipeline with an orchestrator layer, and the formal model is a sequential DAG composition. I chose `pipeline`, but `hierarchy` is arguable.
- **`spread` (P133, P012, P119, P248).** All four measure reach: the fraction or count of infected agents over time, or the hop count. I coded `cascades`, not `amplifies`, under the reach-vs-severity rule. P119's "ASR" is agent-level (the share of agents behaving maliciously), so it measures reach.
- **`spread` (P008, P128, P080).** These report only final performance by structure, so I chose `not reported`. P128's discussion *states* that errors compound in linear pipelines but does not measure it.
- **`spread` (P056, P267).** Both are coded `cascades` from abstract statements only, with confidence `low`.
- **P026, `defense_family`.** The interventions are case studies in Appendix H, tested on clean runs: improved prompts, a Verifier role, and a cyclic topology. I chose `verification-agent; other:prompt-role-and-topology-redesign`, evaluated against `benign`. One could argue for `none` instead, since these are illustrative rather than proposed defenses.
- **P289.** The adversary is specification-compliant. Mitigations are machine-checked in Alloy and TLA+, so I chose `provenance-authorization`, `formal-only` and `theory-only`. I added a scope note in line with `scope_decisions.csv`.
- **P230, `locus`.** No locus value fits bugs in framework code, so I chose `not reported` and described the bugs in `locus_detail`.

## Other fields

- **`mechanism_primary`.** This was the hardest field to apply the same way twice:
  - P026 (MAST) has three categories of similar weight. I chose `coordination-or-communication-failure` (FC2, the most multi-agent-specific) with `role-or-spec-drift` as secondary. FC1, the most frequent category, mixes specification, repetition and termination modes.
  - P080 and P032 have no clean label. For P080 (faulty nodes swaying consensus) and P032 (a decisive early error causing failure) I chose `error-cascade`. `collusion-or-groupthink` (conformity to a faulty majority) is a plausible alternative for P080.
  - P230 uses `other:framework-api-misuse-or-incompatibility`.
- **`system_type` `mixed` vs `not reported` (P032).** The CaptainAgent-generated teams have no stated structure, and Magentic-One is orchestrated. I chose `not reported` under the "generated teams of unspecified shape" rule.
- **`system_type` for P080 and P119.** P080 is `decentralized`: peer consensus on graphs, even though star and tree topologies are included. P119 is `mixed` because it explicitly evaluates chain, tree, star and random topologies.
- **`n_agents`.** I chose `varies` for P026, P008, P012, P128, P032 and P025. For P119 I found no main-setting agent count in the sections I read (the scaled settings use 20 and 50), so it is `not reported`. P003 is `3` (sender, receiver, overseer in the group evaluations).
- **`trace_release`.** I wrote `yes` only where logs or traces are clearly public:
  - P026: MAST-Data on Hugging Face.
  - P032: Who&When on GitHub.
  - P128: "experimental data" on GitHub. This assumes the data are the execution logs.
  - Where only code is released (P133, P008, P080, P119) or the outputs have no host (P003), I chose `not reported` rather than `no`. The codebook does not say how to code a code-only release.
- **`detection_method`.**
  - P133: the governance layer checks messages inline, so I chose `runtime-monitor`.
  - P008: Challenger and Inspector judge messages, so `output-check`.
  - P119: a GNN classifier, so `anomaly-detector`.
  - P080: a trained hidden-state probe, so `anomaly-detector`.
  - P289: `other:formal-specification-analysis`, because spec-level vulnerability discovery fits no listed value.
- **`paper_type`.**
  - P133 is `mixed`: the dynamics model, the attack and the defense get similar space.
  - P267 is `mixed`: taxonomy, benchmark and mitigation are listed as three equal contributions.
  - P128 is `failure-study`, though `benchmark` (a fault-injection framework) is arguable.
  - P003 is `benchmark` (a model evaluation framework).
- **`review_status`.** All rows are `pending`, as the coder prompt says. The §8 hard case suggests `flagged` for scope problems. Instead, scope concerns are written as `scope:` notes in `review_note` (P003, P230, P289).
