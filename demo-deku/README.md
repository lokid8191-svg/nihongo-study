# demo-deku/ — 미도리야 이즈쿠(데쿠) 그린 데모

친구에게 보여주려고 만든 **데쿠 테마** 버전입니다. `demo/index.html`(바쿠고 레드 데모 v29)을 베이스로 테마 색·타이틀·스터디 메이트 대사만 데쿠에 맞게 바꾼 사본이며, 루트 앱과 `/demo/`는 그대로 둡니다.

- 주소: https://lokid8191-svg.github.io/nihongo-study/demo-deku/
- 타이틀: `withデク` (DEMO 배지 유지) · 애플 웹앱 타이틀 `withデク デモ`
- 저장 키는 `demo-deku-*`로 완전히 분리했습니다(`demo-deku-nihongo-v1`, `demo-deku-fridge_seed_version`, `demo-deku-diet_seed_version`, `demo-deku-weight_seed_version`, `demo-deku-sync_bundle_imported_at`). 루트 앱·바쿠고 데모와 기록이 섞이지 않고, 루트 PWA의 서비스 워커도 등록하지 않습니다.
- 예시 데이터는 `/demo/`의 `../demo/demo-weight.json` · `demo-diet.json` · `demo-fridge.json`을 그대로 읽고, 학습 단어·문법·문제는 저장소 루트의 `../study-curriculum.json`을 읽습니다.
- 스터디 메이트: 緑谷出久(미도리야 이즈쿠) · 상황별 대사 13개 풀 39문장(일본어 원문 · 후리가나 · 한국어 뜻)
- 이미지: `assets/deku-1~10.jpg` — 히로아카 공식 사이트(heroaca.com)의 공식 캐릭터 일러스트와 공식 애니메이션 키 비주얼을 3:4로 크롭한 것. 팬아트는 쓰지 않았습니다. 헤더 로고·파비콘은 공식 캐릭터 얼굴 일러스트에서 만든 정사각 이미지(`assets/logo-deku.png`, `assets/icon-192.png`, `assets/apple-touch-icon.png`)입니다.
- 색: 레드(`#DC2626` 계열) → 데쿠 그린(`#16A34A` / `#15803D` / `#22C55E`, 배경 `#F0FDF4`, 보더 `#BBF7D0`). 오답·경고·삭제·체중 증가 표시는 의미색이라 레드를 남겼습니다.

다시 만들 때: `work/nihongo-demo/build-demo-deku.py` (베이스 `demo/index.html` → `demo-deku/index.html`).
