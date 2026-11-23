"""Create a coding sheet. `make_sheet.py template` writes the empty template; `make_sheet.py B01 [llm-a|llm-b|adjudicated|human]` writes a sheet for a batch
with every row's pid, coder and review fields filled and the coded cells left blank (the validator will flag them until they are coded).
llm-a and llm-b sheets cover every paper in the batch; `human` and `adjudicated` sheets cover only the human-audit sample (human_audit = Y)."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema as S
out = "task3/coding"
os.makedirs(out, exist_ok=True)
what = sys.argv[1] if len(sys.argv) > 1 else "template"
if what == "template":
    with open(f"{out}/template.csv", "w", newline="", encoding="utf-8") as f: csv.writer(f).writerow(S.COLUMNS)
    print(f"wrote {out}/template.csv with {len(S.COLUMNS)} columns")
else:
    coder = sys.argv[2] if len(sys.argv) > 2 else "llm-a"
    idx = [r for r in csv.DictReader(open("task3/paper_index.csv", encoding="utf-8")) if r["batch"] == what]
    if coder in ("human", "adjudicated"): idx = [r for r in idx if r["human_audit"] == "Y"]
    path = f"{out}/{what}.{coder}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, S.COLUMNS); w.writeheader()
        for r in idx: w.writerow({"pid": r["pid"], "coder": coder, "review_status": "pending"})
    print(f"wrote {path} with {len(idx)} rows")
