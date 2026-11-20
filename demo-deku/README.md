# demo-deku/ — 미도리야 이즈쿠(데쿠) 그린 데모

친구에게 보여주려고 만든 **데쿠 테마** 버전입니다. 원래 `demo/index.html`(바쿠고 레드 데모 v29)을 베이스로 테마 색·타이틀·스터디 메이트 대사만 데쿠에 맞게 바꾼 사본입니다. 세온 님이 바쿠고 데모(`/demo/`)를 정리하기로 해서(2026-11-20) 이제 이 폴더가 단독으로 동작하며, 예시 데이터도 이 폴더 안에 있습니다.

- 주소: https://lokid8191-svg.github.io/nihongo-study/demo-deku/
- PWA: 이 폴더 전용 `manifest.json`(`withデク · 데모`, 시작·범위 `./`, standalone, theme `#16A34A` · background `#FFFFFF`)을 씁니다. 루트 앱의 manifest·서비스 워커는 등록하지 않습니다. 아이콘을 새로 올리면 `manifest.json`의 `icons`와 `index.html`의 `?v=` 값을 함께 올려 주세요.
- 타이틀: `withデク` (DEMO 배지 유지) · 애플 웹앱 타이틀 `withデク デモ`
- 저장 키는 `demo-deku-*`로 완전히 분리했습니다(`demo-deku-nihongo-v1`, `demo-deku-fridge_seed_version`, `demo-deku-diet_seed_version`, `demo-deku-weight_seed_version`, `demo-deku-sync_bundle_imported_at`). 루트 앱·바쿠고 데모와 기록이 섞이지 않고, 루트 PWA의 서비스 워커도 등록하지 않습니다.
- 예시 데이터는 이 폴더의 `seed-weight.json` · `demo-diet.json` · `demo-fridge.json`을 읽고, 학습 단어·문법·문제는 저장소 루트의 `../study-curriculum.json`을 읽습니다. (2026-11-20 바쿠고 데모 `/demo/` 삭제에 맞춰 `demo-diet.json` · `demo-fridge.json`을 이 폴더로 옮기고 경로를 `./` 기준으로 바꿨습니다.)
  - **체중 예시는 이 폴더의 `seed-weight.json`**을 읽습니다(153cm · 시작 61kg · 목표 52kg, 2026-09-14~11-18 예시 기록, version 3).
  - 식단 **하루 기록**은 이 폴더의 `demo-diet.json`에서 받지만, **섭취 목표(칼로리·탄수·단백·지방)는 이 데모의 기본값**을 씁니다(그 파일의 goals는 반영하지 않습니다).
- 체중 목표 · 섭취 목표 직접 수정(2026-11-20 추가)
  - **루틴 › 체중** 카드의 `✎ 목표 수정`: 목표 체중(기본 52kg) · 시작 체중(61kg) · 시작일을 고치면 목표까지 남은 kg과 진행률 바(%)가 바로 다시 계산됩니다.
  - **루틴 › 식단**의 `오늘의 목표` 카드 `✎ 목표 수정`: 일일 칼로리(기본 **1,250 kcal**)와 범위(탄수화물 130~150g · 단백질 65~80g · 지방 35~45g)를 고칩니다. 바꾸면 달성률 바와 맞춤 메뉴 추천(남은 칼로리)에 바로 반영됩니다.
  - 고친 값은 이 기기의 `demo-deku-nihongo-v1`(`weight.profile` · `diet.goals`, `userFields` `goalsEdited` 표시)에 저장되어 새로고침 후에도 유지되고, 시드 파일 동기화가 덮어쓰지 않습니다. 각 시트의 `기본값으로 되돌리기`로 원래 값으로 돌릴 수 있습니다.
  - ⚠️ 이 폴더는 원래 `work/nihongo-demo/build-demo-deku.py`로 `demo/index.html`에서 다시 만들었지만, 이제 `demo/`가 없으므로 **이 폴더의 `index.html`이 원본**입니다. 다시 만들지 말고 직접 고칩니다.
- 스터디 메이트: 緑谷出久(미도리야 이즈쿠) · 상황별 대사 13개 풀 39문장(일본어 원문 · 후리가나 · 한국어 뜻)
- 이미지: `assets/deku-1~11.jpg` — 정사각(1:1) 공식 애니메이션 컷 11장(2026-11-20 교체). 카드에서는 `object-fit: cover`로 채우고, 얼굴이 잘리지 않도록 세로 위치를 위쪽에 맞췄습니다. 헤더 로고·파비콘은 1번 사진(교복 차림 얼굴)에서 만든 정사각 이미지(`assets/logo-deku.png` 512×512, `assets/icon-192.png` 192×192, `assets/apple-touch-icon.png` 180×180)입니다.
  - 이전 10장(3:4 크롭)의 출처는 히로아카 공식 사이트(heroaca.com) 캐릭터 페이지 https://heroaca.com/character/chara_group01/01-01/ · 6기 캐릭터 비주얼 https://heroaca.com/news/18294/ · 갤러리 https://heroaca.com/gallery/ 였습니다.
- 색: 레드(`#DC2626` 계열) → 데쿠 그린(`#16A34A` / `#15803D` / `#22C55E`, 배경 `#F0FDF4`, 보더 `#BBF7D0`). 오답·경고·삭제·체중 증가 표시는 의미색이라 레드를 남겼습니다.

관리: 2026-11-20부터 `demo-deku/index.html`을 직접 수정합니다(베이스였던 `/demo/`는 삭제).
