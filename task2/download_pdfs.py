"""Download the arXiv PDF of every included/maybe paper into task2/papers/<arxiv-id>.pdf (skips existing). Uses net.get rate limiting."""
import csv, os, sys
from net import get
os.makedirs("papers", exist_ok=True)
rows = [x for x in csv.DictReader(open("02_corpus.csv")) if x["status"] in ("include", "maybe") and x["arxiv"]]
ok = fail = 0
for x in rows:
    dest = f"papers/{x['arxiv']}.pdf"
    if os.path.exists(dest) and os.path.getsize(dest) > 1000: ok += 1; continue
    d = get(f"https://arxiv.org/pdf/{x['arxiv']}", ext=".pdf", tries=3, dest=dest)
    if d and d[:4] == b"%PDF": ok += 1
    else:
        fail += 1; print("FAIL", x["arxiv"], file=sys.stderr)
        if os.path.exists(dest): os.remove(dest)
    print(ok, fail, file=sys.stderr, flush=True)
print("done", ok, fail)
