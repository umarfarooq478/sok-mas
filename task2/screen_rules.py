"""Task 2 step 3b: rule-based title/abstract screen against the Task 1 inclusion rules.
Each rule has an id, so every exclusion carries a reason. Survivors go to manual review."""
import json, re, collections
FREEZE = "2026-11-22"; START = "2023-01-01"
LLM = re.compile(r"\bLLMs?\b|large language model|language model|\bGPT|ChatGPT|Claude|Gemini|foundation model|agentic|generative AI|\bMLLM|vision-language", re.I)
MAS = re.compile(r"multi[- ]?agent|inter-?agent|agent[- ]to[- ]agent|\\bA2A\\b|multiple (LLM |AI |language model )?agents|several agents|agents? (collaborat|communicat|interact|coordinat|debate|negotiat|team)|collaborati\\w+ (of |between |among )?(LLM |AI )?agents|agent (network|societ|swarm|workflow|pipeline|ecosystem)s?|agentic (system|workflow|pipeline|ecosystem|network)s?|LLM[- ]based agents|swarm of|orchestrator|sub-?agents?|(planner|manager|supervisor)[- ](and[- ])?(executor|worker|agent)", re.I)
FAIL = re.compile(r"fail|fault|error|attack|vulnerab|inject|poison|jailbreak|robust|defen[cs]e|risk|threat|hallucinat|safety|secur|malicious|adversar|\bbug|attribut|cascad|collu|trust|misalign|byzantine|resilien|reliab|backdoor|exploit|leak|hijack|infect|sabotag|deceiv|manipulat|anomal", re.I)
SURVEY = re.compile(r"\b(survey|a review|literature review|systematic review|roadmap|position paper|perspective|vision paper|tutorial|primer|we argue|call to action|open challenges)\b", re.I)
NONEN = re.compile(r"[一-鿿Ѐ-ӿ؀-ۿ]")
def screen(r):
    t, a, d = r["title"], r["abstract"], r["date"]
    text = f"{t} {a}"
    if NONEN.search(t): return "exclude", "X6 non-English"
    if not d or d[:10] < START: return "exclude", "X3 before 2023-01-01"
    if d[:10] > FREEZE: return "exclude", "X3 after freeze date"
    if not a: 
        if not (LLM.search(t) and MAS.search(t)): return "exclude", "X0 no abstract and title lacks LLM+multi-agent signal"
    if not LLM.search(text): return "exclude", "X1 not LLM-based"
    if not MAS.search(text): return "exclude", "X2 not multi-agent"
    if not FAIL.search(text): return "exclude", "X4 no failure/attack/defense content"
    if SURVEY.search(t): return "maybe", "M1 survey/position (check: related work only, not coded)"
    return "maybe", "M0 passes rules; manual review"
if __name__ == "__main__":
    recs = json.load(open("deduped.json"))
    c = collections.Counter(); 
    for r in recs:
        r["rule_status"], r["rule_reason"] = screen(r); c[r["rule_reason"][:2]] += 1
    json.dump(recs, open("rule_screened.json", "w"), ensure_ascii=False, indent=0)
    print(c, len(recs))
