"""Cached HTTP for Task 2. Every response is saved under task2/cache/ and committed to the repo,
so reruns read from disk and need no network. Delete a cache file to force a refetch."""
import hashlib, json, os, sys, time, urllib.parse, urllib.request, urllib.error

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
UA = "sok-corpus-builder/0.1"
MIN_GAP = {"export.arxiv.org": 3.5, "api.semanticscholar.org": 4.0, "dblp.org": 1.5,
           "api.crossref.org": 0.3, "api.openalex.org": 0.3, "arxiv.org": 3.5}
_last = {}

def _path(url, ext):
    host = urllib.parse.urlparse(url).netloc
    d = os.path.join(ROOT, host); os.makedirs(d, exist_ok=True)
    return os.path.join(d, hashlib.sha1(url.encode()).hexdigest()[:16] + ext)

def get(url, ext=".json", binary=False, tries=5, dest=None):
    """Return bytes (cached or fetched). dest overrides the cache path (used for PDFs)."""
    p = dest or _path(url, ext)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return open(p, "rb").read()
    host = urllib.parse.urlparse(url).netloc
    for i in range(tries):
        gap = MIN_GAP.get(host, 1) - (time.time() - _last.get(host, 0))
        if gap > 0: time.sleep(gap)
        _last[host] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            data = urllib.request.urlopen(req, timeout=90).read()
            if ext == ".json" and not data.lstrip()[:1] in (b"{", b"["):
                print("NOT-JSON (bot check?)", url[:100], file=sys.stderr); return None
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(data)
            with open(os.path.join(ROOT, "_index.tsv"), "a") as f:
                f.write(f"{os.path.relpath(p, ROOT)}\t{url}\n")
            return data
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, url[:110], file=sys.stderr)
            if e.code in (404, 400): return None
            time.sleep(8 * (i + 1))
        except Exception as e:
            print("ERR", repr(e)[:80], url[:110], file=sys.stderr)
            time.sleep(8 * (i + 1))
    return None
