"""Validate a Task 3 coding sheet against schema.py.

usage: python3 task3/validate_coding.py SHEET.csv [--final] [--index task3/paper_index.csv]
Errors (exit 1): wrong header, blank cell, value outside the codebook, broken cross-field rule, missing evidence tag, unknown or duplicate pid.
Warnings: abstract-only row marked high, `TBD` left in draft mode.
--final additionally forbids `TBD` and requires review_status accepted or corrected.
"""
import csv, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema as S

NR, TBD = "not reported", "TBD"

def split(v): return [x.strip() for x in v.split(";") if x.strip()]

def check_row(row, final, known_pids, pdf_pids):
    err, warn = [], []
    pid = row.get("pid", "")
    if known_pids is not None and pid not in known_pids: err.append(f"unknown pid {pid!r}")
    if row.get("coder") not in S.CODERS: err.append(f"coder must be one of {S.CODERS}")
    if row.get("review_status") not in S.REVIEW_STATUS: err.append(f"review_status must be one of {S.REVIEW_STATUS}")
    if final and row.get("review_status") not in ("accepted", "corrected"): err.append("final mode: review_status must be accepted or corrected")
    if not row.get("review_note", "").strip(): err.append("review_note is blank (write `none` if nothing to say)")
    for f in S.FIELDS:
        n, v = f["name"], (row.get(f["name"]) or "").strip()
        if v == "": err.append(f"{n}: blank (use `not reported` or `TBD`)"); continue
        if v == TBD:
            if f["strict"]: err.append(f"{n}: `TBD` not allowed here")
            elif final: err.append(f"{n}: `TBD` not allowed in final mode")
            else: warn.append(f"{n}: TBD")
            continue
        if v == NR:
            if f["strict"]: err.append(f"{n}: `not reported` not allowed here")
            continue
        k = f["kind"]
        if k in ("single",):
            if v not in f["values"]: err.append(f"{n}: {v!r} not in {sorted(f['values'])}")
        elif k == "multi":
            vals = split(v)
            if not vals: err.append(f"{n}: empty list")
            for x in vals:
                if x in f["values"]: continue
                if f.get("other_ok") and re.fullmatch(r"other:\S.*", x): continue
                err.append(f"{n}: {x!r} not in {sorted(f['values'])}" + (" or other:<label>" if f.get("other_ok") else ""))
            if n in ("mechanism_candidate", "defense_family") and len(vals) > 3: err.append(f"{n}: at most 3 values")
            if n in ("locus", "evidence_type") and len(vals) > 2: err.append(f"{n}: at most 2 values")
            if "none" in vals and len(vals) > 1: err.append(f"{n}: `none` cannot be combined with other values")
        elif k == "pattern":
            if not re.fullmatch(f["pattern"], v): err.append(f"{n}: {v!r} does not match {f['pattern']}")
        # free and evidence: any non-empty text
    g = lambda n: (row.get(n) or "").strip()
    # cross-field rules
    t, lv = g("trigger"), g("trigger_evidence_level")
    if t in S.TRIGGER_LEVEL and lv not in (TBD, NR) and lv not in S.TRIGGER_LEVEL[t]:
        err.append(f"trigger={t!r} requires trigger_evidence_level in {sorted(S.TRIGGER_LEVEL[t])}, got {lv!r}")
    df, de = split(g("defense_family")), g("defense_evaluated_against")
    if df == ["none"] and de not in ("not applicable", TBD, NR): err.append("defense_family=none requires defense_evaluated_against=not applicable")
    if df and df != ["none"] and not set(df) <= {TBD, NR} and de == "not applicable": err.append("a defense family is set, so defense_evaluated_against cannot be `not applicable`")
    if g("paper_type") == "defense" and df == ["none"]: err.append("paper_type=defense but defense_family=none")
    if g("evidence_type") == "theory-only": warn.append("evidence_type=theory-only: the paper may not meet the inclusion rules")
    # evidence tags
    note = g("evidence_note")
    for fld in S.EVIDENCE_FIELDS:
        val = g(fld)
        if val and not (set(split(val)) <= S.NO_EVIDENCE_VALUES):
            if not re.search(rf"(^|[;\s]){fld}\s*:", note): err.append(f"evidence_note: missing `{fld}:` segment")
    # depth honesty
    if g("coded_from") == "abstract-only":
        if g("confidence") == "high": warn.append("abstract-only row marked high: every substantive field must be stated outright in the abstract")
    if pdf_pids is not None and pid in pdf_pids and g("coded_from") == "abstract-only": warn.append("a PDF exists for this paper but the row is abstract-only")
    return err, warn

def validate(path, final=False, index="task3/paper_index.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f); header = rd.fieldnames or []; rows = list(rd)
    errors, warnings = [], []
    if header != S.COLUMNS:
        errors.append(f"header mismatch.\n  expected: {S.COLUMNS}\n  got:      {header}")
        return errors, warnings, 0
    known = pdfs = None
    if index and os.path.exists(index):
        idx = list(csv.DictReader(open(index, encoding="utf-8")))
        known = {r["pid"] for r in idx}; pdfs = {r["pid"] for r in idx if r["pdf"]}
    seen = set()
    for i, row in enumerate(rows, 2):
        key = (row["pid"], row["coder"])
        if key in seen: errors.append(f"line {i} {row['pid']}: duplicate (pid, coder)")
        seen.add(key)
        e, w = check_row(row, final, known, pdfs)
        errors += [f"line {i} {row['pid']}: {m}" for m in e]; warnings += [f"line {i} {row['pid']}: {m}" for m in w]
    return errors, warnings, len(rows)

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    final = "--final" in a
    index = a[a.index("--index") + 1] if "--index" in a else "task3/paper_index.csv"
    e, w, n = validate(a[0], final, index)
    for m in e: print("ERROR  ", m)
    for m in w: print("warning", m)
    print(f"{a[0]}: {n} row(s), {len(e)} error(s), {len(w)} warning(s)" + (" [final mode]" if final else ""))
    sys.exit(1 if e else 0)
