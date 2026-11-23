# Notes, coder llm-b, batch PILOT (sheet PILOT.v1)

Method: for the 12 papers with PDFs I extracted text and read the threat-model, method and evaluation sections before the abstract; all are `abstract-plus-sections` (none full-text, appendices only partly read). P230, P056, P267 have no PDF and are `abstract-only`. Rule used throughout: when two codes were plausible I took the narrower one and set `confidence = low`.

## trigger / trigger_evidence_level
- P008: AutoTransform rewrites a profile so the agent makes stealthy errors (instructed sabotage, adversarial by the codebook rule); AutoInject injects errors into messages (benign by the rule). Same faulty-agent role, same six systems, compared directly, so I coded `both` / `direct-both`, confidence low. The paper calls both "clumsy or malicious". Alternative reading: benign-bug / benign-only / defense against `benign`.
- P133: the endogenous probe is a seed placed in the entry agent's system instructions; the attack is an application-layer injected message. Same frameworks, different interface, so `both-different-locus` (narrower than `direct-both`).
- P248: benign failures come from TRAIL traces of GAIA/SWE-Bench agents; attacks run on a separate custom 10-agent pipeline. `both-different-locus` per codebook section 8.
- P003: instructed steganography evaluations plus an emergent insider-trading leak with no instruction. `both` / `both-different-locus`.
- P080: agents the paper calls Byzantine or malicious are GPT-3.5-turbo vs GPT-4o-mini with no deception instruction; coded `benign-bug` by the how-induced rule.
- P025: one accidental-hijack anecdote (App. L) is not treated as a benign arm; `adversarial-only`.

## spread
- P128, P026, P008, P080: papers say failures cascade but report only final performance or robustness by structure. Coded `not reported` per the codebook rule. P128 is the closest call (L_f vs S_f recovery metrics, repeated cascade language in the discussion).
- P025: coded `cascades` from the laundering experiments (§6.4) although no count of affected agents exists; weakest spread code in the batch.
- P012, P119, P133: `cascades` not `amplifies`, because the measures are counts or fractions of affected agents. The codebook distinction reach vs severity is workable but P119 (ASR rising with rounds) and P012 (faster infection in larger populations) could be read as `amplifies`.
- P267: `cascades` rests on the abstract's "propagate forward" only (abstract-only row).

## defense_family / defense_evaluated_against
- P133: abstract claims the governance layer handles endogenous and exogenous errors, but Table V tests only the three attack policies, so `adversarial`.
- P026: no defense method, but App. H has two intervention case studies (role-spec rewrite, added verification step, +9.4% and +15.6%). I coded `verification-agent` / `benign`. A reviewer may prefer `none`.
- P003: section 7 mitigations are mostly theory (Theorem 4 on paraphrasing). Coded `monitoring; input-filtering` / `formal-only`; the insider-trading study only shows a monitor failing, so I did not code it as an experiment against a defense.
- P289: mitigations verified with Alloy and TLA+, `provenance-authorization` / `formal-only`.
- P128, P248, P025: mitigations are discussed, not implemented, so `none`.
- P012: prompt defenses (marking, instruction, sandwich) mapped to `input-filtering`, LLM Tagging to `provenance-authorization`.

## mechanism_primary / mechanism_secondary
- P026: 14 failure modes in 3 categories; primary `role-or-spec-drift` (first category, "system design issues"), secondary `coordination-or-communication-failure`. Arbitrary among several equal options.
- P032: `not reported`; the paper attributes errors to agent and step but does not classify mechanisms. Reviewer may want an `other:` label.
- P230: `other:framework-bug` (root causes are API misuse, incompatibility, documentation desync, none of which fit the 12 values).
- P133, P119: propagation papers where an injected falsehood spreads; primary differs (P133 `error-cascade`, P119 `message-corruption-or-injection`) because P133 centres on the amplification model and P119 on the attack/defense of infected agents. Both could reasonably be swapped.
- P012: secondary `shared-memory-poisoning` although agent memory is per-agent, because RQ4 is a full experiment on memory retrieval.

## system_type / n_agents
- P003, P032: structure not described, `not reported` (P032 has generated teams plus Magentic-One). P003 `n_agents = 2` from the encoder/decoder group evaluations; the insider study is one agent plus an overseer.
- P080: `decentralized` although a star and tree are among six topologies; graph-of-peers framing used. `mixed` is defensible.
- P119: default agent count not found; `varies` because 20 and 50 agent scale-ups and four topologies are reported.
- P248: `pipeline`, as the paper models it, though an orchestrator coordinates layers.

## scope
- P289: formal analysis of a protocol specification, no running MAS; `evidence_type = theory-only`, `paper_type = theory`, `review_status = flagged`, `scope:` in `review_note`.
- P230: framework bug study centred on the single-agent Self-Action stage; `scope:` note, left `pending` because codebook v1 keeps it as a flagged framework bug study.
- P003: part of the evidence is a single agent with an overseer; borderline for the MAS definition.

## trace_release
- P133, P008, P012, P248, P025, P080, P119: code or datasets are mentioned but no failure traces are stated, so `no`. P128 says "experimental data" is public (GitHub), coded `yes`. P032 says the dataset is in a public repository but the URL was not in the extracted text.
- Abstract-only rows: `not reported`.
