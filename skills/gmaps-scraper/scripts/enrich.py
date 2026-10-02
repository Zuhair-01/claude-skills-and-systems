#!/usr/bin/env python3
"""Enrich results.csv rows that have a website: pull emails, social links, extra phones. Cache: <run>/enrich.json. Usage: enrich.py <run_dir>"""
import csv, json, os, re, sys, concurrent.futures as cf
import urllib.request, urllib.parse, ssl
run = sys.argv[1]; csv.field_size_limit(10**9)
cache_p = os.path.join(run, "enrich.json")
cache = json.load(open(cache_p, encoding="utf-8")) if os.path.exists(cache_p) else {}
SOC = {"facebook": r"facebook\.com/(?!sharer|tr\?|plugins|dialog)[\w.\-/%]+", "instagram": r"instagram\.com/[\w.\-]+", "telegram": r"(?:t\.me|telegram\.me)/[\w\-]+",
       "youtube": r"youtube\.com/(?:@|channel/|c/|user/)[\w.\-]+", "tiktok": r"tiktok\.com/@[\w.\-]+", "linkedin": r"linkedin\.com/(?:company|in)/[\w.\-%]+",
       "x": r"(?:twitter|x)\.com/(?!intent|share)[\w]+", "whatsapp": r"(?:wa\.me|api\.whatsapp\.com/send\?phone=)/?\+?\d+"}
EM = re.compile(r"[\w.+\-]+@[\w\-]+\.[\w.\-]{2,}")
BAD_EM = re.compile(r"\.(png|jpe?g|gif|webp|svg|css|js)$|example\.|sentry|wixpress|@2x", re.I)
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
def get(u):
    try:
        rq = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        return urllib.request.urlopen(rq, timeout=8, context=ctx).read(600000).decode("utf-8", "ignore")
    except Exception: return ""
def scan(url):
    out = {"emails": set(), "social": {}, "phones": set()}
    def fin(o): return {"emails": sorted(o["emails"])[:4], "social": o["social"], "phones": sorted(o["phones"])[:4]}
    host = urllib.parse.urlparse(url).netloc.lower()
    for k in SOC:
        if k in host or (k == "x" and host in ("x.com", "twitter.com")):
            out["social"][k] = url
    if any(s in host for s in ("facebook.com", "instagram.com", "t.me", "linktr.ee", "wa.me")) and not host.startswith("linktr"): return fin(out)
    base = url if url.startswith("http") else "http://" + url
    pages = [base] + [urllib.parse.urljoin(base, p) for p in ("/contact", "/contact-us", "/اتصل-بنا", "/about")]
    for pg in pages:
        h = get(pg)
        if not h: continue
        for e in EM.findall(h):
            if not BAD_EM.search(e): out["emails"].add(e.lower())
        for k, rx in SOC.items():
            m = re.search(rx, h, re.I)
            if m and k not in out["social"]: out["social"][k] = "https://" + m.group(0).lstrip("/")
        for m in re.findall(r"(?:\+|00)?963[\s\-]?\d[\d\s\-]{7,11}|\b09\d[\s\-]?\d{3}[\s\-]?\d{4}\b", h): out["phones"].add(re.sub(r"\D", "", m))
        if out["emails"] and len(out["social"]) >= 2: break
    return fin(out)
todo = {}
for r in csv.DictReader(open(os.path.join(run, "results.csv"), encoding="utf-8", newline="")):
    w = (r.get("website") or "").strip()
    if w and w not in cache: todo[w] = 1
with cf.ThreadPoolExecutor(10) as ex:
    for w, res in zip(todo, ex.map(scan, todo)): cache[w] = res
json.dump(cache, open(cache_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"enriched {len(todo)} new sites; cache={len(cache)}; with email={sum(bool(v['emails']) for v in cache.values())}")
