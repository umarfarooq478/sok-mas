"""Adjudication of the v1 pilot disagreements (Nov 24, 2026), made by Claude on the user's instruction ("use recommendations"), NOT by a human.
Every decision has a rationale. Builds task3/coding/PILOT.adjudicated.csv (from Coder A's row, overridden field by field) and fills
task3/coding/v1/disagreements.csv. Rules used throughout:
  confidence -> the lower of the two; coded_from -> the deeper read if that coder's notes say so; evidence_type -> union (max two);
  `other:` labels only if no listed family fits; abstract-only claims are not coded as spread; facts are checked against the paper text where a PDF exists."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema as S
D = {
 0: ("decentralized", "The paper states a decentralised setting (\"DecAI\") in Section 4."),
 1: ("varies", "Several scenarios with different agent counts; neither 2 nor 3 verified as the main one."),
 2: ("varies", "Text reports scaling to 20 and 50 agents; main count not verified in the extracted text."),
 3: ("varies", "Hub and other topologies are studied; a single count (4) was not verified in the text."),
 4: ("orchestrator-compromise", "Abstract: adversarial content hijacks control flow so the orchestrator invokes unsafe agents; message corruption is the vector, kept as secondary."),
 5: ("coordination-or-communication-failure", "Broad taxonomy; inter-agent misalignment is its central category. Role/specification issues kept as secondary."),
 6: ("error-cascade", "Attribution of the decisive error step in a failed run; the evidence covers error propagation most."),
 7: ("other:framework-bug", "Simplest label for Task 4 grouping; the more specific label is not needed."),
 8: ("message-corruption-or-injection", "Follows row 4."),
 9: ("role-or-spec-drift", "Follows row 5."),
 10: ("none", "Rule: secondary only if substantial; the paper's fault taxonomy is the main thing."),
 11: ("none", "Abstract-only row; the abstract gives no separate weight to a second mechanism."),
 12: ("none", "No separate weight for leakage in what was read; paper is excluded from the matrix anyway."),
 13: ("adversarial", "Instructed collusion is the evidence; the emergent insider-trading case is a single qualitative anecdote, not counted (codebook hard case)."),
 14: ("adversarial-only", "Follows row 13."),
 15: ("message-channel", "Collusion happens through messages; single-model capability tests are not a separate locus."),
 16: ("environment-input; message-channel", "Attack enters through external content and spreads by messages; one-agent not a separate locus."),
 17: ("message-channel; one-agent", "Abstract: agents shift in response to peer reasoning; both the exchange and the agent's own conformity matter; primary first."),
 18: ("one-agent; shared-memory; tool", "Attacks start in a compromised agent via prompt, memory or tool (PI, MA, TA); propagation by messages is spread, not locus."),
 19: ("one-agent; message-channel", "Abstract names intra-agent cognitive errors and inter-agent coordination faults; an environment locus was not verified."),
 20: ("message-channel; one-agent", "Handoff boundary is the unit of analysis (message channel); Type I hallucination originates in the sending agent."),
 21: ("message-channel", "Protocol-level analysis of agent messages."),
 22: ("not reported", "Abstract states hijack and communication compromise, not how the failure moves between agents; no measure verified."),
 23: ("not reported", "v1.1 removed `not studied`."),
 24: ("not reported", "Abstract-only; abstract describes accuracy loss over rounds, not movement of a failure between agents."),
 25: ("not reported", "v1.1 removed `not studied`."),
 26: ("output-check", "The overseer that checks conversations is a detection mechanism the paper evaluates."),
 27: ("runtime-monitor", "Governance layer watches propagation at run time; main method first."),
 28: ("none", "Analyses bug reports, not run traces; proposes no detection tool."),
 29: ("none", "Formal analysis of a spec is the study's method, not a detection tool; avoids a new `other:` label."),
 30: ("monitoring; input-filtering", "Overseer is the main idea; paraphrasing rewrites messages (input-filtering); no `other:` needed (v1.1)."),
 31: ("verification-agent", "Challenger and inspector are both reviewing agents; no separate input filter."),
 32: ("provenance-authorization; input-filtering", "LLM Tagging marks message origin; marking and delimiting baselines are tested input defenses."),
 33: ("verification-agent", "Case-study fixes include a verification step; `other:` not used when a family fits (v1.1)."),
 34: ("provenance-authorization; monitoring", "Abstract: genealogy-graph-based governance layer with atomic propagation control = provenance tracking plus intervention."),
 35: ("verification-agent", "Abstract: Handoff Verification Layer with factual-consistency checking."),
 36: ("adversarial", "Monitoring was tested in the group evaluations; paraphrasing and parameter optimisation are theoretical and not the main defense."),
 37: ("not reported", "v1.1: paper does not say traces are withheld; only an open evaluation framework is mentioned."),
 38: ("not reported", "Code and data link exists but the text does not say the data are failure traces; Task 5 should check the repository."),
 39: ("yes: github.com/multi-agent-systems-failure-taxonomy/MAST (dataset MAST-Data); license: unknown", "Release of MAST-Data stated; GitHub URL found in the paper text. The Hugging Face URL both coders gave was NOT found in the extracted text, so it is not used."),
 40: ("yes: public repository named in the paper (URL to confirm in Task 5); license: unknown", "Paper says dataset is in a public repository; the specific URL one coder gave could not be confirmed in the text."),
 41: ("not reported", "Code link only; no trace release stated."),
 42: ("not reported", "Code link only; no trace release stated."),
 43: ("not reported", "Code and data link; text does not say the data are failure traces; Task 5 should check the repository."),
 44: ("mixed", "Formal framework, evaluation framework and empirical findings in roughly equal parts."),
 45: ("mixed", "Study of faulty agents plus two fault-injection methods plus two defenses."),
 46: ("trace-analysis; experiment", "Traces analysed and intervention experiments run: union."),
 47: ("trace-analysis; experiment", "Failure logs analysed and methods evaluated: union."),
 48: ("full-text", "Coder A's notes say the paper was read in full."),
 49: ("full-text", "Coder A's notes say the paper was read in full."),
 50: ("medium", "Lower of the two."),
 51: ("low", "Lower of the two."),
 52: ("low", "Lower of the two."),
 53: ("low", "Lower of the two."),
}
base = f"task3/coding/v1/"
A = {r["pid"]: r for r in csv.DictReader(open(base + "llm-a.csv", encoding="utf-8"))}
dis = list(csv.DictReader(open(base + "disagreements.csv", encoding="utf-8")))
assert len(dis) == len(D) == 54
final = {p: dict(r) for p, r in A.items()}
for i, row in enumerate(dis):
    val, why = D[i]
    row["adjudicated"] = val; row["rationale"] = why
    final[row["pid"]][row["field"]] = val
for r in final.values():
    r["coder"] = "adjudicated"; r["review_status"] = "pending"
    if r["spread"] == "not studied": r["spread"] = "not reported"          # v1.1 removed the value
    vals = [x.strip() for x in r["defense_family"].split(";")]
    if len(vals) > 2: r["defense_family"] = "; ".join(vals[:2])
    r["review_note"] = ("adjudicated by Claude on the user's instruction, not by a human; human check pending. " + (r["review_note"] if r["review_note"] != "none" else "")).strip()
with open(base + "disagreements.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["pid", "field", "llm_a", "llm_b", "adjudicated", "rationale", "rule_proposal"]); w.writeheader(); w.writerows(dis)
with open("task3/coding/PILOT.adjudicated.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, S.COLUMNS); w.writeheader(); w.writerows([final[p] for p in A])
print("wrote task3/coding/PILOT.adjudicated.csv,", len(final), "rows")
