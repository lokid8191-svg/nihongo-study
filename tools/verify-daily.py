#!/usr/bin/env python3
"""생성된 '오늘의 학습 10문제'를 일차별로 뽑아 범위 위반이 없는지 검증한다.

- index.html의 dailyQuestions 로직(quiz-scope-sim)을 그대로 재현하고,
  q.day 필터(수정 후 동작)를 적용한 뒤 janome 검사기로 본문·보기를 검사한다.
"""
import json, sys, importlib.util
from collections import Counter

def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

sim = load_mod('tools/quiz-scope-sim.py', 'sim')
chk = load_mod('tools/check-quiz-scope.py', 'chk')

def run(stage='n5', days=range(1, 11), daykey='2026-11-20'):
    j = chk.load()
    c = j['stages'][stage]
    total = 0
    for n in days:
        qs = sim.daily_questions(c, stage, n, daykey, honor_q_day=True)
        allowed = chk.allowed_list(j, stage, n)
        bad = 0
        ids = Counter(q['id'] for q in qs)
        dup = [k for k, v in ids.items() if v > 1]
        for q in qs:
            b = chk.check_text(q['prompt'], allowed, chk.OPT_OK)
            ob = [x for o in q['options'] for x in chk.check_text(o, allowed, chk.OPT_OK)]
            if b or ob:
                bad += 1
                print('  ✗', stage, n, q['id'], q['prompt'], b and [x[0] for x in b], ob and [x[0] for x in ob])
        kinds = Counter(q['kind'] for q in qs)
        newq = sum(1 for q in qs if not q.get('review'))
        print('%s %2d일차: %2d문제 (%s) · 새 문제 %d · 복습 %d · 범위위반 %d %s' % (
            stage, n, len(qs), '/'.join('%s%d' % (k, kinds[k]) for k in ['moji', 'goi', 'bunpo', 'bunsho']),
            newq, len(qs) - newq, bad, ('중복:' + ','.join(dup)) if dup else ''))
        total += bad
    print('총 범위 위반:', total)

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    stage = args[0] if args else 'n5'
    dk = args[1] if len(args) > 1 else '2026-11-20'
    run(stage, daykey=dk)
