"""Build 01_novelty_hits.csv: every pre-filtered hit plus web-search hits, with overlap label and reason.
Manual labels override; the rest get a title-screen default label."""
import csv, json, re, sys
hits = json.load(open(sys.argv[1], encoding="utf8"))
out = sys.argv[2]

# id -> (label, reason). Labels: overlaps / partly overlaps / no overlap
M = {
 "2609.00595": ("partly overlaps", "Closest SoK. MAS security only, 197 works; explicitly excludes accuracy loss and drift unless a protected property is violated (Sec 2.1, R4). No benign-trigger axis."),
 "2604.23338": ("partly overlaps", "Agent security survey, 116 papers, 7 layers x 4 temporality classes. Attacks only; MAS is one layer (L5)."),
 "2503.13657": ("partly overlaps", "MAST: 14 benign failure modes from 150 traces, 7 frameworks. No adversary, no defense coverage."),
 "10.1007/978-3-032-35579-9_6": ("partly overlaps", "Google SoK (ARES 2026 workshops, LNCS). 71 papers + 3 CVEs, 5 layers; attacks only; multi-agent is one layer."),
 "2608.00718": ("partly overlaps", "Strongest bridge so far: derives 4 attack classes from 147 benign TRAIL traces and shows they are adversarially inducible. Single study, pipeline-only, 4 classes, no literature systematization or defense map. Supports our thesis."),
 "2603.04474": ("partly overlaps", "Error cascades: same propagation model for endogenous errors and an injected-seed attack; one defense tested on both. One mechanism (cascade/false consensus). Supports our thesis."),
 "2606.08162": ("no overlap", "Silent (non-adversarial) failures; states that the intersection with attacker-triggered failures 'is a topic for future work'. Evidence the bridge is open."),
 "761294afe54faa72133e8635b64350b31f4d866c": ("partly overlaps", "IJISRT 2026 survey: catalogs failure modes across reliability and security, 7-layer trust taxonomy, design patterns. Component layers, no per-mechanism trigger evidence, no corpus counts or coverage matrix. Must cite and differentiate."),
 "MSFT-AIRT-v1": ("partly overlaps", "Microsoft AIRT taxonomy (Apr 2025): safety and security as separate pillars x novel/existing. Notes misalignment can arise benignly or deliberately, but does not map both onto shared mechanisms. Not a literature review."),
 "MSFT-AIRT-v2": ("partly overlaps", "v2.0 (2026): adds 7 attack-oriented modes (e.g. inter-agent trust escalation) from 12 months of red teaming. Same two-pillar structure."),
 "2508.09815": ("partly overlaps", "OWASP MAS threat-model extension: adds benign goal drift and cross-agent hallucination propagation as threat classes. Practitioner guide, no corpus, no mechanism mapping."),
 "2505.02077": ("no overlap", "Multi-agent security agenda (position paper); adversarial framing."),
 "2512.06914": ("no overlap", "Agent security SoK (B-I-P lens), single-agent focus, attacks only."),
 "2603.22928": ("no overlap", "Agentic attack-surface SoK, ~20 studies, attacks only."),
 "2607.12406": ("no overlap", "Isolation-boundary survey of agent safety; adversarial failures (injection, tool misuse, memory poisoning)."),
 "2605.23989": ("no overlap", "Trustworthy agentic AI survey: safety/robustness and privacy/security as two separate dimensions; mostly single-agent."),
 "2609.13731": ("no overlap", "Agentic systems-security survey, 206 studies; attacks only."),
 "a6c42b0164a331819d421f1becc349495f53dfc5": ("no overlap", "KBS 2026 survey of security threats/defenses in agentic and MAS; attacks only (title/venue; abstract not returned)."),
 "2608.10530": ("no overlap", "PRISMA survey of agentic LLM vulnerabilities; attacks and defenses."),
 "2510.23883": ("no overlap", "Agentic AI security survey; attacks only."),
 "2506.23260": ("no overlap", "Threats in agent workflows survey; attacks only."),
 "2503.09648": ("no overlap", "TrustAgent survey (KDD 2025): trustworthiness dimensions, attacks/defenses; not mechanism-level, no benign-failure mapping."),
 "2506.04133": ("no overlap", "TRiSM review: risk taxonomy from coordination failures to adversarial manipulation, governance framing; no mechanism-level trigger mapping."),
 "2512.02682": ("no overlap", "Conceptual taxonomy of emergent systemic risk in LLM-to-LLM interaction; no corpus or trigger axis."),
 "2605.14892": ("no overlap", "Survey of collaboration, failure attribution, self-evolution; benign only."),
 "a087c02f27a96a2b85c961887f38cce9bc5dfe7e": ("no overlap", "TSE survey of agent trajectory analysis and failure attribution; benign only."),
 "2610.32060": ("no overlap", "Communication-failure taxonomy from 3,211 failed debate trajectories; benign only. Candidate corpus + trace source."),
 "2610.15459": ("no overlap", "Communication faults (loss, delay, expiry) taxonomy + injection; benign/infrastructure faults only. Corpus candidate."),
 "2602.19843": ("no overlap", "MAS-FIRE: 15 fault types, fault injection; benign only. Corpus candidate."),
 "2603.06847": ("no overlap", "Fault taxonomy from 385 GitHub faults in agentic systems; software faults, benign. Grey-lit/corpus candidate."),
 "2604.08906": ("no overlap", "409 framework bugs (ASE '26) across LangChain, LangGraph, CrewAI, AutoGen, SmolAgents; benign. Grey-lit source for deployed frameworks."),
 "2408.00989": ("partly overlaps", "Faulty agents (ICML 2025): 'clumsy or malicious' agents simulated by error injection; treats both as one robustness problem but does not systematize mechanisms. Corpus paper, key bridge evidence."),
 "2511.10400": ("partly overlaps", "BFT view of LLM-MAS reliability (AAAI 2026): faulty and malicious messages under one fault model. Corpus paper, bridge evidence."),
 "2505.00212": ("no overlap", "Who&When failure attribution (ICML 2025); benign. Trace source for Task 5."),
 "2607.21912": ("no overlap", "Error contagion network model; benign. Corpus candidate."),
 "2605.19240": ("no overlap", "CASPIAN cascade-attack detection; adversarial only. Corpus candidate (defense)."),
 "2601.14667": ("no overlap", "INFA-Guard defense against malicious propagation; adversarial only."),
 "2512.18733": ("no overlap", "XG-Guard malicious-agent detection; adversarial only."),
 "2611.23362": ("no overlap", "TRACE-MAS diagnosis/repair of collaboration failures; benign-trained detector. Corpus candidate (defense to test on both triggers)."),
 "2606.07937": ("no overlap", "Hallucination cascade analysis; benign only."),
}
WEB = [  # hits found only via web search (not in API results)
 ("MSFT-AIRT-v1", "Taxonomy of Failure Modes in Agentic AI Systems (Microsoft AI Red Team, whitepaper v1.0)", "2025-04", "grey"),
 ("MSFT-AIRT-v2", "Taxonomy of Failure Modes in Agentic AI Systems v2.0 (Microsoft AI Red Team)", "2026-04", "grey"),
 ("10.1007/978-3-032-35579-9_6", "SoK: Security Vulnerabilities in Agentic AI Systems (Guan, Kovalev, Xie; ARES 2026 Workshops, LNCS, pp. 98-115)", "2026-08", "crossref"),
 ("2608.00718", "Adversarial Attacks in Multi-Agent LLM Pipelines: Unveiling Structural Vulnerabilities in Agentic AI Architectures", "2026-08", "arxiv"),
 ("2606.08162", "Silent Failure in LLM Agent Systems: The Entropy Principle and the Inevitable Disorder of Autonomous Agents", "2026-06", "arxiv"),
 ("2508.09815", "Extending the OWASP Multi-Agentic System Threat Modeling Guide", "2025-08", "arxiv"),
 ("2505.02077", "Open Challenges in Multi-Agent Security", "2025-05", "arxiv"),
 ("2512.06914", "SoK: Trust-Authorization Mismatch in LLM Agent Interactions", "2025-12", "arxiv"),
 ("2607.12406", "Isolation as a First-Class Principle for LLM-Agent System Safety", "2026-07", "arxiv"),
 ("2608.10530", "On Understanding, Identifying, and Mitigating Vulnerabilities in Agentic Large Language Models", "2026-08", "arxiv"),
 ("2510.23883", "Agentic AI Security: Threats, Defenses, Evaluation, and Open Challenges", "2025-10", "arxiv"),
 ("2506.23260", "From Prompt Injections to Protocol Exploits: Threats in LLM-Powered AI Agents Workflows", "2025-06", "arxiv"),
 ("2511.10400", "Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance", "2025-11", "arxiv"),
 ("2601.14667", "INFA-Guard", "2026-01", "arxiv"),
 ("2512.18733", "XG-Guard (Bi-Level Graph Anomaly Detection)", "2025-12", "arxiv"),
 ("2503.13657", "Why Do Multi-Agent LLM Systems Fail?", "2025-03", "arxiv"),
 ("2609.00595", "SoK: When Safe Agents Fail Together", "2026-09", "arxiv"),
]
ma = re.compile(r"multi[- ]?agent|agentic|LLM agents?|agent systems?", re.I)
kind = re.compile(r"survey|taxonom|systemati|SoK|review|failure|fault|cascad|error propagat|reliab|robust", re.I)
rows, seen = [], set()
for h in hits.values():
    text = (h.get("title") or "") + " " + (h.get("abstract") or "")
    pre = bool(ma.search(text) and kind.search(h.get("title") or ""))
    if not pre and h["id"] not in M:
        continue
    lab, why = M.get(h["id"], ("no overlap", "Title/abstract screen: single-side (benign-only method/benchmark, attack-only, or off-topic); no cross-trigger systematization."))
    rows.append([h["id"], h["src"], (h.get("published") or "")[:10], h.get("venue") or "", h.get("citations") if h.get("citations") is not None else "",
                 h["title"], lab, why, "; ".join(h.get("queries", [])), "manual" if h["id"] in M else "title-screen"])
    seen.add(h["id"])
for i, t, d, src in WEB:
    if i in seen: continue
    lab, why = M[i]
    rows.append([i, src, d, "", "", t, lab, why, "web search", "manual"])
order = {"overlaps": 0, "partly overlaps": 1, "no overlap": 2}
rows.sort(key=lambda r: (order[r[6]], r[9] != "manual", r[2]), reverse=False)
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "source", "date", "venue", "citations_s2", "title", "overlap", "reason", "queries", "screened_by"])
    w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r[6] for r in rows), Counter(r[9] for r in rows))
