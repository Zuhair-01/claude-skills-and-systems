#!/usr/bin/env python3
"""results.csv (+enrich.json) -> classified/merged/deduped leads + contact approach + import.csv (Ostazi OutreachLead format) + report.html.
Usage: build_report.py <run_dir> [title] [--mark]   (--mark records import.csv phones in the ledger after a successful import)"""
import csv, json, re, sys, os, hashlib, datetime, urllib.parse
args = [a for a in sys.argv[1:] if not a.startswith("--")]
run = args[0]
title = args[1] if len(args) > 1 else os.path.basename(os.path.abspath(run))
HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.expanduser("~/tools/gmaps-scraper/ledger.json")
ledger = json.load(open(LEDGER, encoding="utf-8")) if os.path.exists(LEDGER) else {}
if "--mark" in sys.argv:
    for r in csv.DictReader(open(os.path.join(run, "import.csv"), encoding="utf-8-sig")):
        ledger[r["contact"]] = {"run": os.path.basename(os.path.abspath(run)), "date": str(datetime.date.today()), "id": r["id"]}
    json.dump(ledger, open(LEDGER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ledger", len(ledger))
    sys.exit()
csv.field_size_limit(10**9)
CITIES = ["ريف دمشق", "دمشق", "حلب", "حمص", "حماة", "اللاذقية", "طرطوس", "درعا", "السويداء", "إدلب", "دير الزور", "الحسكة", "الرقة", "القنيطرة"]
T1 = re.compile(r"البرامكة|المزة|الحلبوني|الشعلان|أبو رمانة|ابو رمانة|الصالحية|الروضة|القصاع")
EXCL = re.compile(r"قيادة|driving|ملاكمة|تسوق|طبيب|مؤتمرات|نادي|رياض|دعم الكمبيوتر|أبحاث|ديني|خيرية|جمعية|منظمة|مكتب الشركات|ضيافة|سياحة|جامعة|كلية|university|college|مركز ثقافي")
RA = re.compile(r"مدرس خاص|دروس خصوصية|المركز التعليمي|مؤسسة تعليمية|مركز الدراسة|تقوية|مركز التعليم|^تعليم$|tutor|مدرسة تعليم$|مدرسة تعليمية متخصصة")
RB = re.compile(r"لغ|language|تدريب|training|معهد|أكاديم|academy|institute|course|كمبيوتر|تكنولوجيا|تعليم")
RC = re.compile(r"مدرسة|school|ثانوية|ابتدائية")


def tier(cat, name):
    t = (cat or "") + " " + (name or "")
    if EXCL.search(cat or "") or re.search(r"قيادة|driving", name or ""):
        return "X"
    if RA.search(cat or "") or re.search(r"دروس|تقوية|تدريس|tutor", name or "", re.I):
        return "A"
    if RB.search(t):
        return "B"
    if RC.search(t):
        return "C"
    return "X"


def phone(raw):
    d = re.sub(r"\D", "", raw or "")
    if d.startswith("00963"):
        d = d[5:]
    elif d.startswith("963"):
        d = d[3:]
    d = d.lstrip("0")
    if len(d) < 7:
        return None, None
    return ("+963" + d, "mobile") if d.startswith("9") and len(d) == 9 else ("+963" + d, "landline")


def city(a):
    for c in CITIES:
        if c in (a or ""):
            return c
    return "أخرى"


def nk(n, c):
    return c + "|" + re.sub(r"\bال|[\s\-–—|.،()]|[ً-ْ]|academy|center|institute|مركز|معهد|مؤسسة|اكاديمية|أكاديمية", "", (n or "").lower())


enr_p = os.path.join(run, "enrich.json")
enr = json.load(open(enr_p, encoding="utf-8")) if os.path.exists(enr_p) else {}
by, no_phone, raw_rows = {}, 0, 0
for r in csv.DictReader(open(os.path.join(run, "results.csv"), encoding="utf-8", newline="")):
    raw_rows += 1
    p, kind = phone(r.get("phone"))
    if not p:
        no_phone += 1
    c = city(r.get("address"))
    key = r.get("cid") or nk(r.get("title"), c)
    web = (r.get("website") or "").strip()
    e = enr.get(web, {"emails": [], "social": {}, "phones": []})
    social = dict(e["social"])
    host = urllib.parse.urlparse(web).netloc.lower()
    for k in ("facebook", "instagram", "telegram", "tiktok", "youtube", "linkedin"):
        if k in host:
            social.setdefault(k, web)
    is_social_site = any(k in web.lower() for k in ("facebook.com", "instagram.com", "t.me", "linktr.ee"))
    try:
        rating = float(r.get("review_rating") or 0)
    except ValueError:
        rating = 0
    try:
        rc = int(r.get("review_count") or 0)
    except ValueError:
        rc = 0
    rec = dict(name=r.get("title"), category=r.get("category"), city=c, address=r.get("address"), phones=[p] if p else [], website="" if is_social_site else web,
               social=social, emails=e["emails"], rating=rating, reviews=rc, map=r.get("link"), lat=r.get("latitude"), lng=r.get("longitude"),
               cid=r.get("cid"), tier=tier(r.get("category"), r.get("title")))
    for ep in e["phones"]:
        q, _ = phone(ep)
        if q and q not in rec["phones"]:
            rec["phones"].append(q)
    k2 = key if key in by else next((k for k, v in by.items() if (p and p in v["phones"]) or nk(v["name"], v["city"]) == nk(rec["name"], c)), key)
    if k2 in by:
        o = by[k2]
        o["phones"] += [x for x in rec["phones"] if x not in o["phones"]]
        o["emails"] = sorted(set(o["emails"] + rec["emails"]))
        for s, u in rec["social"].items():
            o["social"].setdefault(s, u)
        o["website"] = o["website"] or rec["website"]
    else:
        by[k2] = rec
leads = list(by.values())
PLAYBOOK = os.path.expanduser("~/Desktop/Empire_Base/Second_Brain/Workflow/10 - Projects/Ostazi/outreach/ostazi_outreach_targets.csv")
known = set()
if os.path.exists(PLAYBOOK):
    for row in csv.reader(open(PLAYBOOK, encoding="utf-8-sig", errors="ignore")):
        for c in row:
            for m in re.findall(r"(?:\+?963|0)?9\d{8}", c.replace(" ", "")):
                q, _ = phone(m)
                if q: known.add(q)
dup_removed = raw_rows - len(leads)
for l in leads:
    mob = next((x for x in l["phones"] if x.startswith("+9639") and len(x) == 13), None)
    l["kind"] = "mobile" if mob else "landline" if l["phones"] else "none"
    l["phone"] = mob or (l["phones"][0] if l["phones"] else "")
    digital = bool(l["website"] or l["social"] or l["emails"])
    l["openness"] = "HIGH" if mob and digital else "MED" if mob else "LOW"
    ch = []
    if mob:
        ch.append("واتساب")
    for s, n in (("instagram", "انستغرام"), ("facebook", "فيسبوك"), ("telegram", "تلغرام")):
        if s in l["social"]:
            ch.append(n + " DM")
    if l["emails"]:
        ch.append("إيميل")
    if l["website"]:
        ch.append("الموقع")
    if l["phones"] and not mob:
        ch.append("اتصال هاتفي")
    l["channels"] = ch
    nm = (l["name"] or "").split(" - ")[0].strip()
    good = l["rating"] >= 4 and l["reviews"] >= 5
    comp = f"شفنا تقييمكم {l['rating']} على خرائط جوجل ({l['reviews']} رأي) وبجد بيشرّف 👏" if good else f"تعرّفنا على {nm} من خرائط جوجل"
    l["msg1"] = f"السلام عليكم، معك فريق أوستازي (منصة سورية لربط المدرسين والطلاب).\n{comp}\nسؤال سريع بدون أي التزام: كيف عم تجيبوا طلاب جدد هالفترة، وشو أكتر شي عم يتعبكم فيها؟"
    l["msg2"] = f"أهلاً مرة تانية 🌷 بس للتذكير — بنجهّز لـ{nm} صفحة على أوستازي مجاناً بـ5 دقايق، وبتوصلوا لطلاب جدد بدون إعلانات. إذا حبيتوا ابعتولنا الاسم والاختصاصات وبنبدأ."
    l["approach"] = f"القناة: {' ← '.join(ch[:3])} | الافتتاح: " + ("مدح التقييم" if good else "تعارف من خرائط جوجل") + " ثم سؤال عن مشكلة جلب الطلاب (بدون بيع) | متابعة بعد 3 أيام ثم توقف"
    l["field"] = not (l["phones"] or l["emails"] or l["social"] or l["website"])
    if l["field"]:
        l["approach"] = "لا رقم ولا إيميل ولا سوشال — زيارة ميدانية فقط (العنوان + الخريطة)"
    l["wa"] = f"https://wa.me/{l['phone'][1:]}?text=" + urllib.parse.quote(l["msg1"]) if mob else ""
    l["score"] = ({"A": 6, "B": 3, "C": 1, "X": 0}[l["tier"]] + (3 if mob else 0) + (1 if l["website"] else 0) + (1 if l["social"] else 0)
                  + (2 if l["emails"] else 0) + (1 if l["rating"] >= 4 else 0) + (1 if l["reviews"] >= 10 else 0))
    l["new"] = (not l["phone"] or l["phone"] not in ledger) and not any(x in known for x in l["phones"])
    l["in_playbook"] = any(x in known for x in l["phones"])
    l["id"] = "GM-" + hashlib.md5((l["cid"] or l["phone"]).encode()).hexdigest()[:8].upper()
leads.sort(key=lambda l: (-l["score"], -l["reviews"]))
fv = [l for l in leads if l["field"] and l["tier"] in ("A", "B", "C")]
fv.sort(key=lambda l: (l["city"], l["tier"], -l["reviews"]))
with open(os.path.join(run, "field_visits.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["city", "tier", "name", "category", "address", "rating", "reviews", "map", "lat", "lng", "visited", "notes"])
    for l in fv:
        w.writerow([l["city"], l["tier"], l["name"], l["category"], l["address"], l["rating"], l["reviews"], l["map"], l["lat"], l["lng"], "", ""])
json.dump(leads, open(os.path.join(run, "leads.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
FLAT = ["id", "tier", "name", "category", "city", "address", "phone", "kind", "emails", "website", "social", "rating", "reviews", "channels", "approach", "map"]


def cell(l, k):
    v = l[k]
    if k == "channels":
        return " | ".join(v)
    return json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v


with open(os.path.join(run, "leads.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(FLAT)
    for l in leads:
        w.writerow([cell(l, k) for k in FLAT])


# Ostazi import: tiers A+B not yet in ledger. Ostazi "tier" field = geography ring.
def ring(l):
    return "T1" if l["city"] == "دمشق" and T1.search(l["address"] or "") else "T2" if l["city"] == "دمشق" else "T3" if l["city"] == "ريف دمشق" else "T5"


TYPE = {"A": "مؤسسة تعليمية", "B": "معهد/مركز تدريب"}
def useful(l):
    # matters for Ostazi: tutoring/language/training providers with a WhatsApp mobile and some real signal (rating, reviews or a web/social presence)
    return l["tier"] in ("A", "B") and l["kind"] == "mobile" and l["new"] and (l["rating"] >= 4 or l["reviews"] >= 3 or bool(l["social"]) or bool(l["website"]))


def cats(l):
    t = (l["name"] or "") + " " + (l["category"] or "")
    out = []
    for rx, c in ((r"لغ|language|english|إنجليز|انجليز|فرنس|ألمان|تركي", "لغات"), (r"كمبيوتر|برمج|تكنولوجيا|IT|computer", "برمجة وحاسوب"), (r"رياض|فيزياء|كيمياء|علوم|بكالوريا|تاسع|شهادة", "مواد علمية")):
        if re.search(rx, t, re.I):
            out.append(c)
    return "|".join(out)


ex = [l for l in leads if useful(l)]
with open(os.path.join(run, "import.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "name_ar", "type", "categories", "tier", "city_area", "contact", "openness", "pitch_angle", "source"])
    for l in ex:
        src = " | ".join(["Google Maps"] + ([f"موقع: {l['website']}"] if l["website"] else []) + [f"{s}: {u}" for s, u in l["social"].items()]
                         + ([f"بريد: {', '.join(l['emails'])}"] if l["emails"] else []) + [f"خريطة: {l['map']}"])
        w.writerow([l["id"], l["name"], TYPE[l["tier"]], cats(l), ring(l), (l["city"] + " - " + (l["address"] or ""))[:120], l["phone"], l["openness"], l["approach"], src])
good = ("A", "B")
S = dict(total=len(leads), rows=raw_rows, no_phone=no_phone, dup=dup_removed, mobile=sum(l["kind"] == "mobile" for l in leads),
         A=sum(l["tier"] == "A" for l in leads), B=sum(l["tier"] == "B" for l in leads), C=sum(l["tier"] == "C" for l in leads), X=sum(l["tier"] == "X" for l in leads),
         web=sum(bool(l["website"]) for l in leads), soc=sum(bool(l["social"]) for l in leads), email=sum(bool(l["emails"]) for l in leads), importable=len(ex), field=len(fv), in_playbook=sum(l["in_playbook"] for l in leads),
         cities={c: sum(l["city"] == c and l["tier"] in good and not l["field"] for l in leads) for c in CITIES + ["أخرى"] if any(l["city"] == c and l["tier"] in good and not l["field"] for l in leads)})
tpl = open(os.path.join(HERE, "report_template.html"), encoding="utf-8").read()
open(os.path.join(run, "report.html"), "w", encoding="utf-8").write(
    tpl.replace("__DATA__", json.dumps({"title": title, "leads": leads, "stats": S}, ensure_ascii=False).replace("</", "<\\/")))
print(json.dumps(S, ensure_ascii=True))
print(os.path.join(run, "report.html"))
