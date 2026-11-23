"""Agreement between two coding sheets (e.g. PILOT.llm-a.csv and PILOT.llm-b.csv).
usage: python3 task3/agreement.py A.csv B.csv [out_prefix]
Single-value fields: percent agreement and Cohen's kappa. Multi-value fields: exact-set agreement and mean Jaccard. Free-text fields are not scored.
Writes <out_prefix>.disagreements.csv (every field where the two sheets differ, for the human to adjudicate) and prints a markdown table."""
import csv, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema as S

def load(p): return {r["pid"]: r for r in csv.DictReader(open(p, newline="", encoding="utf-8"))}
def sset(v): return {x.strip() for x in v.split(";") if x.strip()}
def kappa(a, b):
    n = len(a)
    if n == 0: return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)

def main(pa, pb, prefix):
    A, B = load(pa), load(pb)
    pids = sorted(set(A) & set(B))
    print(f"papers in both sheets: {len(pids)} (only in A: {len(set(A) - set(B))}, only in B: {len(set(B) - set(A))})\n")
    rows, dis = [], []
    for f in S.FIELDS:
        n = f["name"]
        if f["kind"] in ("free", "evidence"): continue
        a = [A[p][n].strip() for p in pids]; b = [B[p][n].strip() for p in pids]
        for p, x, y in zip(pids, a, b):
            if (sset(x) if f["kind"] == "multi" else x) != (sset(y) if f["kind"] == "multi" else y): dis.append((p, n, x, y))
        if f["kind"] == "multi":
            ex = sum(sset(x) == sset(y) for x, y in zip(a, b)) / len(pids)
            jac = sum(len(sset(x) & sset(y)) / max(1, len(sset(x) | sset(y))) for x, y in zip(a, b)) / len(pids)
            rows.append((n, "multi", f"{ex:.0%}", "-", f"{jac:.2f}"))
        else:
            ag = sum(x == y for x, y in zip(a, b)) / len(pids); k = kappa(a, b)
            rows.append((n, "single", f"{ag:.0%}", "n/a" if k is None else f"{k:.2f}", "-"))
    print("| field | kind | exact agreement | Cohen's kappa | mean Jaccard |\n|---|---|---|---|---|")
    for r in rows: print("| " + " | ".join(r) + " |")
    with open(f"{prefix}.disagreements.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["pid", "field", "llm_a", "llm_b", "adjudicated"]); [w.writerow(list(d) + [""]) for d in dis]
    per = collections.Counter(d[0] for d in dis)
    print(f"\n{len(dis)} disagreements on {len(per)} of {len(pids)} papers -> {prefix}.disagreements.csv")
    print("papers with most disagreements:", per.most_common(5))
    print("note: with a small n (e.g. the 15-paper pilot) kappa is unstable; read it as a pointer to ambiguous fields, not an estimate.")

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "task3/coding/agreement")
