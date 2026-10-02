"""Search the prompts.chat library. python search.py <keywords> [-c category] [-n 8] | --show <id> | --cats"""
import json, os, re, sys, math
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
here = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(here, 'prompts.jsonl'), encoding='utf-8')]
a = sys.argv[1:]
if '--cats' in a: print(open(os.path.join(here, 'CATEGORIES.md'), encoding='utf-8').read()); sys.exit()
if '--show' in a:
    x = rows[int(a[a.index('--show') + 1])]
    print(f"[{x['id']}] {x['act']} ({x['category']})\n\n{x['prompt']}"); sys.exit()
cat = a[a.index('-c') + 1] if '-c' in a else None
n = int(a[a.index('-n') + 1]) if '-n' in a else 8
skip = {a.index(f) + 1 for f in ('-c', '-n') if f in a}
q = [w.lower() for i, w in enumerate(a) if not w.startswith('-') and i not in skip]
df = {w: sum(w in (x['act'] + ' ' + x['prompt']).lower() for x in rows) or 1 for w in q}
out = []
for x in rows:
    if cat and x['category'] != cat: continue
    if x['category'] == 'jailbreak-unsafe' and cat != 'jailbreak-unsafe': continue
    t, b = x['act'].lower(), x['prompt'].lower()
    s = sum((3 * (w in t) + min(b.count(w), 3)) * math.log(2200 / df[w]) for w in q)
    if s: out.append((s, x))
for s, x in sorted(out, key=lambda t: -t[0])[:n]:
    print(f"[{x['id']}] {x['act']} ({x['category']}) — {x['prompt'][:70].replace(chr(10), ' ')}...")
