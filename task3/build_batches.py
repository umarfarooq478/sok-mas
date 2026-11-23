"""Task 3 planning: stable paper ids, themes, pilot set, batches of 20, double-coding sample. Deterministic (seeded)."""
import csv, json, os, random, re, collections
rows = [r for r in csv.DictReader(open("../02_corpus.csv")) if r["status"] in ("include", "maybe")]
ab = json.load(open("abstracts.json"))
for r in rows: r["abstract"] = ab.get(r["title"], "")
# stable ids: included first (P001..), then maybe (Q001..), each ordered by (date, title)
inc = sorted([r for r in rows if r["status"] == "include"], key=lambda r: (r["date"], r["title"]))
may = sorted([r for r in rows if r["status"] == "maybe"], key=lambda r: (r["date"], r["title"]))
for i, r in enumerate(inc, 1): r["pid"] = f"P{i:03d}"
for i, r in enumerate(may, 1): r["pid"] = f"Q{i:03d}"
# themes: first match wins (priority order); used only to group papers so a coder sees similar work together
THEMES = [
 ("T1 failure attribution and debugging", r"attribut|debug|localiz|root cause|diagnos|trajector|failure management|error diagnosis|who broke|fault attribution"),
 ("T2 benign error and hallucination propagation", r"hallucinat|cascad|error propagat|propagat\w* of error|drift|silent|failure mode|failure taxonomy|fault inject|fault|reliab|resilien|bugs?\b|collapse|snowball|contagion|misinformation|common-cause|instabil"),
 ("T3 debate, consensus, sycophancy, conformity", r"debate|consensus|sycophan|conformity|persuasi|deliberat|belief|quorum|voting"),
 ("T4 collusion and steganography", r"collu|steganograph|covert|deception|cartel"),
 ("T5 privacy and leakage", r"leak|privacy|private|secret|confidential|contextual integrity"),
 ("T6 protocols, authorization, trust boundaries", r"protocol|\bA2A\b|\bMCP\b|authoriz|delegat|identity|trust boundar|provenance|privilege|capabilit|reference monitor|handoff|access control"),
 ("T7 attacks: injection, jailbreak, poisoning, backdoor", r"inject|jailbreak|poison|backdoor|attack|malicious|hijack|exploit|adversar|infect|virus|worm|red-?team|vulnerab|threat|sabotag|manipulat|trojan|compromis"),
 ("T8 defenses and monitors", r"defen[cs]e|guard|safeguard|shield|sentinel|monitor|byzantine|detect|robust|secur|trust|safety|audit|verif|firewall|containment|mitigat"),
]
def theme(r):
    t = r["title"]
    for name, pat in THEMES:
        if re.search(pat, t, re.I): return name
    for name, pat in THEMES:
        if re.search(pat, t + " " + r["abstract"][:400], re.I): return name
    return "T9 other multi-agent failure and risk"
for r in rows: r["theme"] = theme(r)
# pilot: 15 papers chosen for coverage, led by the papers that bear directly on both triggers (hardest to code)
PILOT_KEYS = ["From Spark to Fire", "Adversarial Attacks in Multi-Agent LLM Pipelines", "Why Do Multi-Agent LLM Systems Fail", "On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty",
  "Rethinking the Reliability of Multi-agent System", "Prompt Infection", "MAS-FIRE", "Which Agent Causes Task Failures", "Bugs in Modern LLM Agent Frameworks",
  "Secret Collusion among AI Agents", "Talk Isn't Always Cheap", "INFA-Guard", "A2ABreak", "Handoff Hallucinations", "Multi-Agent Systems Execute Arbitrary Malicious Code"]
pilot = []
for k in PILOT_KEYS:
    m = [r for r in inc if r["title"].lower().startswith(k.lower())]
    assert len(m) == 1, (k, [x["title"] for x in m])
    pilot.append(m[0])
pset = {r["pid"] for r in pilot}
for r in pilot: r["batch"] = "PILOT"
rest = [r for r in inc if r["pid"] not in pset]
order = sorted(rest, key=lambda r: (r["theme"], r["date"], r["title"]))
for i, r in enumerate(order): r["batch"] = f"B{i // 20 + 1:02d}"
for i, r in enumerate(may): r["batch"] = f"M{i // 20 + 1}"
# double-coding sample: whole pilot, then 20% of each batch (seeded)
random.seed(3)
for r in rows: r["double_code"] = ""
for r in pilot: r["double_code"] = "Y"
for b in sorted({r["batch"] for r in order}):
    mem = [r for r in order if r["batch"] == b]
    for r in random.sample(mem, max(1, round(len(mem) * 0.2))): r["double_code"] = "Y"
allr = pilot + order + may
for r in allr:
    r["pdf"] = f"task2/papers/{r['arxiv']}.pdf" if r["arxiv"] and os.path.exists(f"../task2/papers/{r['arxiv']}.pdf") else ""
    r["has_abstract"] = "Y" if r["abstract"] else "N"
cols = ["pid", "batch", "theme", "double_code", "status", "title", "year", "tier", "venue", "citations_openalex", "arxiv", "doi", "pdf", "has_abstract", "grey"]
with open("paper_index.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader(); w.writerows(allr)
for b in sorted({r["batch"] for r in allr}):
    mem = [r for r in allr if r["batch"] == b]
    with open(f"batches/{b}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader(); w.writerows(mem)
    with open(f"batches/{b}.md", "w", encoding="utf-8") as f:
        f.write(f"# Batch {b}: {len(mem)} papers\n\nDouble-coded (`Y`) papers are the 20% sample for the kappa check.\n\n| pid | double | theme | year | tier | title |\n|---|---|---|---|---|---|\n")
        for r in mem: f.write(f"| {r['pid']} | {r['double_code']} | {r['theme'][:2]} | {r['year']} | {r['tier']} | {r['title'].replace('|','/')} |\n")
print(collections.Counter(r["batch"] for r in allr))
print(collections.Counter(r["theme"] for r in inc))
print("double-coded:", sum(r["double_code"] == "Y" for r in allr), "no pdf:", sum(not r["pdf"] for r in allr), "no abstract:", sum(r["has_abstract"] == "N" for r in allr))
print("pilot themes:", collections.Counter(r["theme"][:2] for r in pilot))
