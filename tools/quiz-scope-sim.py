#!/usr/bin/env python3
"""오늘의 학습 10問題 생성 로직(index.html dailyQuestions) 파이썬 재현 + 범위 검증.

용도: 특정 날짜·단계·일차에서 실제로 나오는 10문제를 뽑아,
      그 일차까지 배운 단어(+기초 허용 어휘) 밖의 어휘가 섞였는지 점검한다.
"""
import json, sys, datetime, re

M32 = 0xFFFFFFFF

def imul(a, b):
    return (a * b) & M32

def daily_hash(s):
    h = 2166136261
    for ch in str(s):
        h ^= ord(ch)
        h = imul(h, 16777619)
    return h & M32

def daily_rng(seed):
    x = [daily_hash(seed) or 1]
    def nxt():
        x[0] = (imul(x[0], 1664525) + 1013904223) & M32
        return x[0] / 4294967296
    return nxt

def shuffle(items, seed):
    a = list(items)
    rnd = daily_rng(seed)
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]
    return a

def pick4(correct, cands, seed):
    seen = {str(correct): True}
    out = []
    for v in shuffle(cands, seed):
        if len(out) >= 3:
            break
        if not v or str(v) in seen:
            continue
        seen[str(v)] = True
        out.append(v)
    if len(out) < 3:
        return None
    lst = shuffle([correct] + out, seed + '#m')
    return {'options': lst, 'answer': lst.index(correct)}

def word_questions(w, pool, seed):
    items = []
    if not w:
        return items
    def near(lst):
        same = [x for x in lst if x and x.get('cat') and x['cat'] == w['cat']]
        rest = [x for x in lst if not (x and x.get('cat') and x['cat'] == w['cat'])]
        return shuffle(same, seed + '#c1') + shuffle(rest, seed + '#c2')
    def others(f):
        return near([x for x in pool if x and x['id'] != w['id'] and f(x)])
    if w['jp'] != w['kana']:
        o = pick4(w['kana'], [x['kana'] for x in others(lambda x: x.get('kana') and x['kana'] != w['kana'])], seed + '#r')
        if o:
            items.append({'id': 'w-' + w['id'] + '-r', 'kind': 'moji', 'sub': '문자·어휘 — 한자 읽기',
                          'target': {'t': 'w', 'id': w['id']}, 'prompt': '「' + w['jp'] + '」の読み方は？',
                          'options': o['options'], 'answer': o['answer'], 'exp': ''})
    o2 = pick4(w['ko'], [x['ko'] for x in others(lambda x: x.get('ko') and x['ko'] != w['ko'])], seed + '#k')
    if o2:
        items.append({'id': 'w-' + w['id'] + '-k', 'kind': 'goi', 'sub': '어휘 — 뜻 고르기',
                      'target': {'t': 'w', 'id': w['id']}, 'prompt': '「' + w['jp'] + '」の意味は？',
                      'options': o2['options'], 'answer': o2['answer'], 'exp': ''})
    o3 = pick4(w['jp'], [x['jp'] for x in others(lambda x: x.get('jp') and x['jp'] != w['jp'])], seed + '#j')
    if o3:
        items.append({'id': 'w-' + w['id'] + '-j', 'kind': 'goi', 'sub': '어휘 — 일본어로 고르기',
                      'target': {'t': 'w', 'id': w['id']}, 'prompt': '「' + w['ko'] + '」は日本語で？',
                      'options': o3['options'], 'answer': o3['answer'], 'exp': ''})
    return items

def spread(pool, count, seed):
    groups, keys = {}, []
    for q in shuffle(pool, seed + '#sp'):
        k = q['target']['id'] if q.get('target') else q['id']
        if k not in groups:
            groups[k] = []
            keys.append(k)
        groups[k].append(q)
    out = []
    guard = 0
    while len(out) < count and guard < 40:
        guard += 1
        moved = False
        for k in keys:
            if len(out) >= count:
                break
            g = groups[k]
            if not g:
                continue
            out.append(g.pop(0))
            moved = True
        if not moved:
            break
    return out

def day_entry(c, n):
    ds = c.get('days') or []
    if not ds:
        return {'words': [], 'grammar': []}
    return ds[max(0, min(len(ds) - 1, n - 1))]

def scope(c, n):
    ds = c.get('days') or []
    lim = max(0, min(len(ds), n or 0))
    words, grammar, ws, gs = [], [], {}, {}
    for i in range(lim):
        for wid in ds[i].get('words', []):
            if wid and wid not in ws:
                ws[wid] = True
                words.append(wid)
        for gid in ds[i].get('grammar', []):
            if gid and gid not in gs:
                gs[gid] = True
                grammar.append(gid)
    return {'words': words, 'grammar': grammar, 'days': lim}

def grammar_questions(c, ids, seed, n=None):
    m = {i: True for i in ids if i}
    out = [q for q in c.get('questions', []) if q.get('target', {}).get('t') == 'g' and m.get(q['target']['id'])
           and (n is None or (q.get('day') or 0) <= n)]
    return shuffle(out, seed)

def daily_questions(c, sid, n, daykey, honor_q_day=False):
    key = sid + '#' + str(n) + '#' + daykey
    wmap = {w['id']: w for w in c['words']}
    gmap = {g['id']: g for g in c['grammar']}
    ds = day_entry(c, n)
    sc = scope(c, n)
    prev = scope(c, n - 1)
    scope_words = [wmap[i] for i in sc['words'] if i in wmap]
    prev_words = [wmap[i] for i in prev['words'] if i in wmap]
    seed = key
    wday, gday = {}, {}
    for d in c.get('days', []):
        for i in d.get('words', []):
            wday.setdefault(i, d['day'])
        for i in d.get('grammar', []):
            gday.setdefault(i, d['day'])
    newWQ, revWQ = [], []
    for wid in ds.get('words', []):
        w = wmap.get(wid)
        for q in word_questions(w, scope_words, seed + ':' + wid):
            q['day'] = n
            newWQ.append(q)
    fn = (lambda x: grammar_questions(c, x, seed + ':g', n)) if honor_q_day else (lambda x: grammar_questions(c, x, seed + ':g'))
    newGQ = fn(ds.get('grammar', []))
    for q in newGQ:
        q['day'] = n
    for w in prev_words:
        for q in word_questions(w, prev_words, seed + 'r:' + w['id']):
            q['review'] = True
            q['day'] = wday.get(w['id'], 0)
            revWQ.append(q)
    fn2 = (lambda x: grammar_questions(c, x, seed + 'rg', n)) if honor_q_day else (lambda x: grammar_questions(c, x, seed + 'rg'))
    revGQ = []
    for q in fn2(prev['grammar']):
        q = dict(q)
        q['review'] = True
        q['day'] = gday.get(q['target']['id'], 0)
        revGQ.append(q)
    newPlan = {'moji': 2, 'goi': 3, 'bunpo': 3, 'bunsho': 2} if n <= 1 else {'moji': 2, 'goi': 2, 'bunpo': 2, 'bunsho': 1}
    revPlan = {'moji': 0, 'goi': 0, 'bunpo': 0, 'bunsho': 0} if n <= 1 else {'moji': 0, 'goi': 1, 'bunpo': 1, 'bunsho': 1}
    order = ['moji', 'goi', 'bunpo', 'bunsho']
    used = {}
    def take(pool, kind, count, tag):
        if count <= 0:
            return []
        src = [q for q in pool if q['kind'] == kind and q['id'] not in used]
        picked = spread(src, count, seed + tag + kind)
        for q in picked:
            used[q['id']] = True
        return picked
    newPool = newWQ + newGQ
    revPool = revWQ + revGQ
    out = []
    for kind in order:
        picked = take(newPool, kind, newPlan[kind], 'n')
        out.extend(picked)
    for kind in order:
        out.extend(take(revPool, kind, revPlan[kind], 'rv'))
    if len(out) < 10:
        rest = shuffle([q for q in newPool if q['id'] not in used], seed + '#fill')
        for q in rest:
            if len(out) >= 10:
                break
            used[q['id']] = True
            out.append(q)
    for q in out:
        isW = q.get('target', {}).get('t') == 'w'
        label = wmap[q['target']['id']]['jp'] if isW and q['target']['id'] in wmap else (gmap[q['target']['id']]['key'] if q['target']['id'] in gmap else '')
        q['srcLabel'] = ('복습 · ' if q.get('review') else '') + (str(q['day']) + '일차 ' if q.get('day') else '') + ('단어 ' if isW else '문법 ') + label
    return out[:10]

# ── 범위 검증용 어휘 사전 ──────────────────────────────────────────────
KANJI = re.compile(r'[\u4e00-\u9fff]')
KANA = re.compile(r'[\u3040-\u30ff]')

def load_core(path='study-curriculum.json'):
    j = json.load(open(path, encoding='utf-8'))
    return j

def allowed_words(j, sid, n, core):
    c = j['stages'][sid]
    sc = scope(c, n)
    wmap = {w['id']: w for w in c['words']}
    allowed = set()
    for wid in sc['words']:
        w = wmap.get(wid)
        if w:
            allowed.add(w['jp'])
            allowed.add(w['kana'])
    for item in core:
        allowed.add(item['jp'])
        allowed.add(item['kana'])
    return allowed

def main():
    j = load_core()
    daykey = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    stage = sys.argv[2] if len(sys.argv) > 2 else 'n5'
    for n in [int(x) for x in (sys.argv[3].split(',') if len(sys.argv) > 3 else ['1', '2'])]:
        c = j['stages'][stage]
        qs = daily_questions(c, stage, n, daykey)
        print('=== %s %d일차 (%s) — %d문제' % (stage, n, daykey, len(qs)))
        for i, q in enumerate(qs, 1):
            print('%2d. [%s] %s' % (i, q['srcLabel'], q['prompt']))
            print('     보기: %s  (정답 %s)' % (' / '.join(q['options']), q['options'][q['answer']]))

if __name__ == '__main__':
    main()
