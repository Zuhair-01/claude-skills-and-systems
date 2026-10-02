"""Rebuild prompts.jsonl + categories/ from a prompts.chat checkout. Usage: python build.py [path/to/prompts.csv]"""
import csv, json, re, sys, os
csv.field_size_limit(10**9)
here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.claude/prompts-library-src/pc/prompts.csv')
# ordered: first match wins as primary; all matches kept as tags
CATS = [
 ('jailbreak-unsafe', r'\bDAN\b|jailbreak|do anything now|no (ethical|moral) (guidelines|restrictions)|ignore (all )?(previous|prior) (instructions|rules)|developer mode|without (any )?(restrictions|censorship)|unfiltered'),
 ('image-gen', r'selfie|portrait|photograph|photo|photoreal|hyper-?realis|hiperrealista|cinematic|midjourney|stable diffusion|dall-?e|anime|manga|illustration|watercolor|oil painting|3d (character|render)|avatar|infographic|mirror|golden hour|aesthetic|full-body|lighting'),
 ('design-ui', r'ui|ux|website|landing page|design system|figma|redesign|wireframe|mockup|hud|app design|front-?end design|dashboard design'),
 ('code-dev', r'developer|programmer|software|code|coding|javascript|python|react|\bsql\b|regex|linux|terminal|\bapi\b|github|frontend|backend|full.?stack|debug|algorithm|web ?dev|\bcss\b|\bhtml\b|excel formula|compiler|solidity|smart contract'),
 ('devops-security', r'devops|cyber|security|pentest|penetration|sysadmin|network engineer|docker|kubernetes|\baws\b|it architect|infrastructure'),
 ('data-ai', r'data scien|machine learning|\bai\b|prompt (generator|engineer)|chatgpt|statistic|data analy|midjourney|stable diffusion|dall'),
 ('marketing-business', r'marketing|seo|advertis|\bsales\b|startup|business|entrepreneur|brand|social media|copywrit|product manager|e-?commerce|customer|strategist|influencer|linkedin|slogan'),
 ('finance-trading', r'financ|invest|stock|crypto|trader|trading|accountant|budget|blockchain|economist|tax'),
 ('writing-content', r'writer|writing|essay|editor|proofread|poet|poem|novel|story|screenwriter|journalist|blog|article|copy ?edit|plagiar|rewrite|paraphras|grammar|lyrics|storyteller|speech|title generator|summar'),
 ('education-tutoring', r'teacher|tutor|professor|instructor|lecturer|math|mathematic|science|history|educat|student|learn|quiz|exam|lesson|coach|debate|trivia'),
 ('career-hr', r'interview|recruit|resume|\bcv\b|career|job|\bhr\b|cover letter|negotiat|salary'),
 ('health-wellness', r'doctor|dentist|physician|nutrition|dietit|fitness|trainer|therap|psycholog|mental|medit|health|wellness|sleep|yoga|mindful|psychiatr|counsel'),
 ('legal-gov', r'lawyer|legal|contract|attorney|law\b|judge|politic|government|regulat|compliance'),
 ('language-translation', r'translat|language (tutor|teacher|learner)|english (translator|teacher|pronunciation|speaking)|spoken english|pronunciation|etymolog|linguist'),
 ('creative-media', r'music|composer|song|film|movie|director|actor|artist|painter|design|photograph|drawing|comedian|stand-?up|game|chess|rapper|dj\b|animation|fashion|architect|interior|chef|cook|recipe|travel|tour|guide'),
 ('roleplay-characters', r'act as (a |an |the )?(character|pirate|dungeon|storyteller|fictional|superhero|villain)|you are (a |an )?(character|npc)|roleplay|role-play|text.?based (adventure|game)|rpg|persona|pretend|simulate'),
 ('advice-life', r'relationship|dating|advis|life|friend|astrolog|horoscope|tarot|dream|philosoph|motivat|religio|spiritual|self.?help|emotion|stoic|psychic|fortune'),
]
def norm(s): return re.sub(r'\s+',' ',s).strip()
rows=[]
for i,r in enumerate(csv.DictReader(open(src,encoding='utf-8'))):
    act=norm(r['act']); p=r['prompt'].strip()
    hay=(act+' '+p[:400]).lower()
    tags=[c for c,rx in CATS if re.search(rx,hay,re.I)]
    if r['type']=='IMAGE': cat='image-gen'
    elif ' ' not in act.strip() and len(p)<600 and not tags: cat='roleplay-characters'
    elif 'jailbreak-unsafe' in tags: cat='jailbreak-unsafe'
    else:
        # title match beats body match
        t=[c for c,rx in CATS if c!='jailbreak-unsafe' and re.search(rx,act.lower(),re.I)]
        cat=(t or [c for c in tags if c!='jailbreak-unsafe'] or ['general-utility'])[0]
    rows.append(dict(id=i,act=act,category=cat,tags=[t for t in tags if t!=cat][:3],type=r['type'],devs=r['for_devs']=='TRUE',prompt=p))
with open(os.path.join(here,'prompts.jsonl'),'w',encoding='utf-8') as f:
    for x in rows: f.write(json.dumps(x,ensure_ascii=False)+'\n')
os.makedirs(os.path.join(here,'categories'),exist_ok=True)
from collections import defaultdict
by=defaultdict(list)
for x in rows: by[x['category']].append(x)
for c,xs in by.items():
    with open(os.path.join(here,'categories',c+'.md'),'w',encoding='utf-8') as f:
        f.write(f'# {c} ({len(xs)})\n\nid | title\n---|---\n'+'\n'.join(f"{x['id']} | {x['act']}" for x in sorted(xs,key=lambda x:x['act'].lower()))+'\n')
with open(os.path.join(here,'CATEGORIES.md'),'w',encoding='utf-8') as f:
    f.write('# prompts.chat categories\n\n'+'\n'.join(f'- {c}: {len(xs)}' for c,xs in sorted(by.items(),key=lambda kv:-len(kv[1])))+'\n')
print({c:len(x) for c,x in sorted(by.items(),key=lambda kv:-len(kv[1]))}, len(rows))
