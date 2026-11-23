"""Tests for validate_coding.py. Run: python3 task3/test_validator.py"""
import csv, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema as S
from validate_coding import validate

base = list(csv.DictReader(open("task3/coding/example.csv", encoding="utf-8")))[0]
def run(mut, final=False, rows=None):
    rs = rows if rows is not None else [dict(base, **mut)]
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, S.COLUMNS); w.writeheader(); w.writerows(rs); p = f.name
    e, wn, n = validate(p, final); os.unlink(p); return e, wn

CASES = [  # (name, mutation, substring that must appear in an error, or None if no error expected)
 ("clean example passes", {}, None),
 ("blank cell", {"locus": ""}, "locus: blank"),
 ("value outside codebook", {"trigger": "attacker"}, "trigger: 'attacker' not in"),
 ("unknown pid", {"pid": "P999"}, "unknown pid"),
 ("bad n_agents", {"n_agents": "many"}, "n_agents"),
 ("trigger/level mismatch", {"trigger_evidence_level": "benign-only"}, "requires trigger_evidence_level"),
 ("both needs a both level", {"trigger": "both"}, "requires trigger_evidence_level"),
 ("missing evidence tag", {"evidence_note": "trigger: \"x\"; locus: \"y\""}, "missing `trigger_evidence_level:`"),
 ("none combined with another family", {"defense_family": "none; monitoring"}, "cannot be combined"),
 ("defense set but not applicable", {"defense_family": "monitoring", "defense_evaluated_against": "not applicable", "evidence_note": base["evidence_note"] + "; defense_family: \"x\""}, "cannot be `not applicable`"),
 ("defense paper without a defense", {"paper_type": "defense"}, "paper_type=defense"),
 ("too many mechanisms", {"mechanism_candidate": "error-cascade; tool-misuse; termination-failure; role-or-spec-drift"}, "at most 3"),
 ("other:<label> accepted", {"mechanism_candidate": "other:clock skew"}, None),
 ("not reported not allowed for paper_type", {"paper_type": "not reported"}, "paper_type"),
 ("bad review status", {"review_status": "done"}, "review_status"),
 ("blank review_note", {"review_note": ""}, "review_note is blank"),
 ("TBD rejected in final mode", {"review_status": "accepted"}, "n_agents: `TBD` not allowed in final mode", True),
 ("final mode passes when complete", {"review_status": "accepted", "n_agents": "not reported"}, None, True),
]
fails = 0
for c in CASES:
    name, mut, want = c[0], c[1], c[2]; final = len(c) > 3
    e, w = run(mut, final)
    ok = (not e) if want is None else any(want in m for m in e)
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> errors: {e}"))
    fails += not ok
# structural cases
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="", encoding="utf-8") as f:
    f.write("pid,coder\nP023,claude\n"); p = f.name
e, _, _ = validate(p); os.unlink(p); ok = any("header mismatch" in m for m in e); print(("PASS " if ok else "FAIL ") + "wrong header"); fails += not ok
e, _ = run({}, rows=[dict(base), dict(base)]); ok = any("duplicate" in m for m in e); print(("PASS " if ok else "FAIL ") + "duplicate (pid, coder)"); fails += not ok
w = run({"confidence": "high"})[1]; ok = any("abstract-only row marked high" in m for m in w); print(("PASS " if ok else "FAIL ") + "warns on abstract-only + high"); fails += not ok
print(f"\n{len(CASES) + 3 - fails}/{len(CASES) + 3} passed"); sys.exit(1 if fails else 0)
