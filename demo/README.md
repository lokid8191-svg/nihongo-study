# demo/ — 공유용 데모 페이지

`withかっちゃん` 기능을 소개하려고 만든 데모입니다. 실제 개인 기록은 들어 있지 않고, 화면에 보이는 체중·식단·냉장고는 모두 예시 데이터입니다.

- `index.html` — 루트 `index.html`을 데모용으로만 바꾼 사본입니다. 개인 정보를 걷어냈고, 저장 키는 `demo-*`로 분리했으며, 루트 PWA의 서비스 워커(`sw.js`)를 등록하지 않습니다.
- `demo-weight.json` · `demo-diet.json` · `demo-fridge.json` — 예시 데이터

루트 앱(`index.html` · `sw.js` · `weight-data.json` · `diet-data.json` · `fridge-data.json`)은 이 폴더와 무관하게 그대로 동작합니다.

데모 주소: https://lokid8191-svg.github.io/nihongo-study/demo/
