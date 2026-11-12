# 심리 통역사 (psy-app)

논문 PDF를 올리면 Gemini가 쉽게 풀어 설명해 주는 Streamlit 앱 ("Psy-Interpreter").
분석 스타일: 교수님 브리핑 / 교과서 해설 / 논문 결과 작성.

- GitHub: https://github.com/sidd0262-ops/psy-app
- 파일: app.py, requirements.txt(streamlit, google-generativeai, PyPDF2), .devcontainer/(GitHub Codespaces용)
- 실행: `pip install -r requirements.txt` → `streamlit run app.py`
- API 키: Streamlit Secrets의 `GEMINI_API_KEY` (없으면 사이드바에서 입력). 코드에 키를 쓰지 않기

## 진행 상황
- 2026-01-23: UI·오류 메시지 개선, 응급 진단 모드, 모델 자동 탐지, Dev Container 추가
- 확인 필요: 코드가 찾는 모델(`gemini-1.5-flash` / `1.5-pro` / `gemini-pro`)이 지금도 제공되는지. 서비스가 종료됐으면 모델을 찾지 못할 수 있음

## 내 프로젝트 생태계 (모든 저장소 공통)
GitHub 계정 `sidd0262-ops` 를 기준으로 Windows PC · Mac · 아이폰(클라우드 세션)에서 같은 코드를 씁니다.

| 저장소 | 내용 |
| --- | --- |
| Short-english | 쇼츠로 배우는 영어 회화 PWA (TypeScript, Render 배포) |
| coffee-log | 카페인 조절 기록지 PWA |
| psy-Cultural-adaptation | 문화적응 여정 PWA (Firebase) |
| timebox | 나만 쓰는 한지 타임박스 PWA |
| mind-project | 마음프로젝트 소개 페이지 |
| psy-app | 심리 통역사 (Streamlit + Gemini) |

- **폴더 위치:** Windows `Desktop\클로드 코드\` · Mac `~/Desktop/클로드 코드/` (폴더 이름은 저장소 이름과 달라도 됨)
- **한 번에 최신화:** Short-english 저장소의 `workspace/sync-all.ps1`(Windows) · `workspace/sync-all.sh`(Mac). 없는 저장소는 받고, 있는 저장소는 pull
- **작업 규칙**
  1. 시작 전 `git pull` (클라우드 세션은 항상 최신으로 시작)
  2. 끝나면 커밋하고 `git push` (사용자에게 확인 후). 로컬에만 두면 다른 기기에서 안 보임
  3. 같은 저장소를 두 기기에서 동시에 수정하지 않기
  4. API 키·비밀번호는 코드와 채팅에 쓰지 않기 (`.env`, 배포 서비스 환경변수, Streamlit Secrets 사용)
  5. 작업이 끝나면 이 파일의 "진행 상황"을 갱신해서 다음 기기·세션이 이어받게 하기
- 사용자와는 한국어로 대화
