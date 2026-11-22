#!/usr/bin/env python3
"""오늘의 학습 문제의 '누적 학습 범위' 검증기.

- 각 문제를 그 문제의 day(없으면 문법 배치 일차)까지 배운 단어 + core(기초 허용 어휘)
  범위로 검사한다.
- 검사 방식: 허용 어휘를 문자열 그대로 마스킹한 뒤(janome이 会社員을 会社+員으로
  쪼개는 문제 회피) 나머지를 형태소 분석해 내용어(명사·동사·형용사·부사·접속사·
  감동사·연체사)의 기본형이 허용 목록에 있는지 본다. 활용형은 기본형으로 판정된다.
- 사용: python3 tools/check-quiz-scope.py [n5|n4|n3] [--verbose]
"""
import json, sys
from janome.tokenizer import Tokenizer

T = Tokenizer()
PLACE = '〇'
# 조사·활용 어미처럼 '보기'로만 쓰이는 형태
OPT_OK = set('は が を に で へ も と や の か ね よ より まで から ながら こと です ます '
            'がいい もいい はいい をいい にいい'.split())
LABELS = ('A：', 'B：')
# 문항 안내 문구(어휘가 아니라 문제 지시문)
RUBRIC = ('の読み方は', 'の意味は', 'は日本語で', '（　）', '（　')

def has_hangul(s):
    return any('\uac00' <= ch <= '\ud7a3' for ch in s)


def load(path='study-curriculum.json'):
    return json.load(open(path, encoding='utf-8'))


def scope_words(j, sid, n):
    c = j['stages'][sid]
    ds = c.get('days') or []
    lim = max(0, min(len(ds), n or 0))
    words, ws = [], {}
    for i in range(lim):
        for wid in ds[i].get('words', []):
            if wid and wid not in ws:
                ws[wid] = True
                words.append(wid)
    return words


def allowed_list(j, sid, n):
    c = j['stages'][sid]
    wmap = {w['id']: w for w in c['words']}
    s = set()
    for wid in scope_words(j, sid, n):
        w = wmap.get(wid)
        if w:
            s.add(w['jp'])
            s.add(w['kana'])
    for item in j.get('core', []):
        s.add(item['jp'])
        s.add(item['kana'])
    return s


def mask(text, allowed):
    """허용 어휘를 긴 것부터 지워 PLACE로 바꾼다."""
    out = text
    for w in sorted(allowed, key=len, reverse=True):
        if not w:
            continue
        if w in out:
            out = out.replace(w, PLACE)
    return out


KANJI_OK = set()

def kanji(s):
    return [ch for ch in s if '\u4e00' <= ch <= '\u9fff']

def is_kana(s):
    return all(('\u3040' <= ch <= '\u30ff') for ch in s)

def check_text(text, allowed, opt_ok=()):
    for lab in LABELS:
        text = text.replace(lab, '')
    for rb in RUBRIC:
        text = text.replace(rb, '')
    if has_hangul(text):
        return []
    masked = mask(text, allowed)
    bad = []
    for tok in T.tokenize(masked):
        surf, pos = tok.surface, tok.part_of_speech
        head = pos.split(',')[0]
        if PLACE in surf:
            continue
        if head in ('助詞', '助動詞', '記号', '空白', '数', 'フィラー'):
            continue
        if surf.isdigit() or surf.translate(str.maketrans('０１２３４５６７８９', '0123456789')).isdigit():
            continue
        base = tok.base_form if tok.base_form != '*' else surf
        if surf in allowed or base in allowed or (base + 'する') in allowed or (surf + 'する') in allowed:
            continue
        if surf in opt_ok or base in opt_ok:
            continue
        # 활용 꼬리(かな 1~2자), 또는 허용 단어 앞부분 + 활용 꼬리로 이루어진 조각은 통과
        if len(surf) <= 2 and is_kana(surf):
            continue
        if is_kana(surf) and any(w.startswith(surf[0]) and is_kana(w) for w in allowed):
            continue
        # 한자 조각: 쓰인 한자가 모두 허용 단어 안에 있으면 통과(예: 静くです → 静か)
        ks = kanji(surf)
        if ks and all(any(k in w for w in allowed) for k in ks):
            continue
        bad.append((surf, base, pos))
    return bad


def main():
    j = load()
    stage = None
    for a in sys.argv[1:]:
        if not a.startswith('-'):
            stage = a
    verbose = '--verbose' in sys.argv
    stages = [stage] if stage else ['n5', 'n4', 'n3']
    total_bad = 0
    for sid in stages:
        c = j['stages'][sid]
        gday = {}
        for d in c['days']:
            for g in d.get('grammar', []):
                gday.setdefault(g, d['day'])
        print('########', sid)
        for q in c.get('questions', []):
            tgt = q.get('target', {})
            gd = gday.get(tgt.get('id'), 0)
            day = q.get('day') or gd
            allowed = allowed_list(j, sid, day)
            bad = check_text(q['prompt'], allowed, OPT_OK)
            optbad = []
            for o in q['options']:
                optbad += [(o, b[0], b[1]) for b in check_text(o, allowed, OPT_OK)]
            if bad or optbad:
                total_bad += 1
                print('  [%s] 문법 %s (%d일차) → day=%s' % (q['id'], tgt.get('id'), gd, day))
                print('     %s' % q['prompt'])
                if bad:
                    print('     본문 범위 밖: ' + ', '.join('%s(%s)' % (b[0], b[2].split(',')[0]) for b in bad))
                if optbad:
                    print('     보기 범위 밖: ' + ', '.join('%s→%s' % (o[0], o[1]) for o in optbad))
            elif verbose:
                print('  OK [%s] day=%s %s' % (q['id'], day, q['prompt']))
    print('\n범위 밖 문제 수:', total_bad)


if __name__ == '__main__':
    main()
