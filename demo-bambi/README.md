# demo-bambi/ — with밤비 (PLAVE 밤비 테마)

친구에게 보여주기 위해 만든 **밤비 테마** 버전입니다. `demo-deku/`(데쿠 그린 데모)를 베이스로 테마 색·타이틀·스터디 메이트 대사·아이콘만 밤비에 맞게 바꾼 사본이며, 이 폴더 하나로 독립 동작합니다(2026-11-28).

- 주소: https://lokid8191-svg.github.io/nihongo-study/demo-bambi/
- PWA: 이 폴더 전용 `manifest.json`(`with밤비`, 시작·범위 `./`, standalone, theme `#EC4899` · background `#FFFFFF`)을 씁니다. 루트 앱의 manifest·서비스 워커는 등록하지 않습니다. 아이콘을 새로 올리면 `manifest.json`의 `icons`와 `index.html`의 `?v=` 값을 함께 올려 주세요.
- 저장 키는 `demo-bambi-*`로 완전히 분리했습니다: `demo-bambi-nihongo-v1`(상태), `demo-bambi-bag-v1`(대사 셔플백), `demo-bambi-wo-bag-v1`(운동 셔플백), `demo-bambi-fridge_seed_version`, `demo-bambi-diet_seed_version`, `demo-bambi-weight_seed_version`, `demo-bambi-sync_bundle_imported_at`.
- 데이터: 이 폴더의 `seed-weight.json` · `demo-diet.json` · `demo-fridge.json`을 읽고, 학습 단어·문법·문제는 저장소 루트의 `../study-curriculum.json`을 읽습니다(세온 님의 개인 기록 파일 `weight-data.json` · `diet-data.json` · `fridge-data.json`은 참조하지 않습니다).
  - 체중: `seed-weight.json` (153cm · 시작 61kg · 목표 52kg, version 3)
  - 식단 **하루 기록**은 `demo-diet.json`에서 받고, **섭취 목표**는 앱 기본값(1,250 kcal)을 씁니다.
  - 냉장고: `demo-fridge.json` 기본 목록 + 기기에서 추가·수정·소진한 기록.
- 기능: 홈·루틴·공부·복습·냉장고 5탭, 상단 날짜 이동 바, 운동 추천 32개 셔플백, 당류(g) 표기, 체중·섭취 목표 직접 수정, 식단 탭 맨 아래 `지금 냉장고로 뭐 먹지?` 맞춤 메뉴 — `demo-deku/`와 동일합니다.
- 스터디 메이트: **밤비**(PLAVE) · 상황별 대사 13개 풀 **117문장**(일본어 원문 · 후리가나 · 한국어 뜻). 셔플백이라 한 바퀴를 다 보기 전에는 같은 대사가 다시 나오지 않습니다.
- 이미지: `assets/bambi-1~26.jpg` — 밤비 캐릭터 사진 26장(2026-11-28 세온 님 제공). 스터디 메이트 카드가 열 때마다·`다른 한마디`를 누를 때마다 다음 사진으로 바뀌며, 26장을 한 바퀴 돌기 전에는 같은 사진이 다시 나오지 않습니다. 카드에서는 `object-fit: cover`로 채웁니다. 헤더 로고는 세온 님이 보낸 밤비 일러스트에서 얼굴만 자른 `assets/logo-face.png`, 앱 아이콘·파비콘은 같은 일러스트로 만든 `assets/icon-192.png`(192) · `assets/logo-bambi.png`(512) · `assets/apple-touch-icon.png`(180)입니다. 사진·아이콘을 바꾸면 `index.html`의 `?v=` 값을 올려 주세요(지금은 사진 `?v=2`, 아이콘 `?v=1`).
- 색: 핑크(`#EC4899` / `#DB2777` / `#FDF2F8`, 보더 `#FBCFE8`, 배경 `#FDF7FA`). 정답 표시·섭취목표 3색 게이지(정상 초록·부족 주황·초과 빨강)·체중 감량 그래프의 의미색은 초록/빨강 그대로 남겼습니다.

관리: `demo-bambi/index.html`을 직접 수정합니다(다시 만들지 않습니다).
