# MoEngage Genspark 슬랙봇

MoEngage Help Center를 Genspark AI로 검색해주는 슬랙봇입니다.

## 🚀 빠른 시작

1. 이 저장소를 GitHub에 복사 (Fork)
2. Railway에서 배포
3. 슬랙 앱 설정
4. 사용 시작!

## 📋 설정 가이드

### 1단계: 슬랙 앱 만들기
1. https://api.slack.com/apps 접속
2. "Create New App" → "From scratch"
3. 앱 이름: `MoEngage Helper`
4. 워크스페이스 선택

### 2단계: 권한 설정
OAuth & Permissions에서 다음 권한 추가:
- `app_mentions:read`
- `channels:history`
- `channels:read`
- `chat:write`
- `reactions:read`
- `reactions:write`
- `im:history`
- `im:read`
- `im:write`

### 3단계: Railway 배포
1. https://railway.app 접속
2. GitHub 로그인
3. 이 저장소 선택하여 배포
4. 환경변수 설정:
   - `SLACK_BOT_TOKEN`: xoxb-로 시작하는 토큰
   - `SLACK_SIGNING_SECRET`: 슬랙 앱의 서명 키
   - `PORT`: 8000

### 4단계: 이벤트 구독
1. 슬랙 앱 → "Event Subscriptions"
2. "Enable Events" ON
3. Request URL: `https://your-app.railway.app/slack/events`
4. 이벤트 추가: `reaction_added`, `message.channels`, `app_mention`

### 5단계: 테스트
1. 슬랙 채널에 봇 초대
2. MoEngage 관련 질문 입력
3. 🔍 이모티콘 리액션 추가
4. 봇 응답 확인

## 💡 사용법

1. 슬랙 채널에 MoEngage 관련 질문 작성
2. 해당 메시지에 🔍 (돋보기) 이모티콘 추가
3. 봇이 Genspark AI로 검색하여 한국어로 답변

## 🛠️ 기능

- 한국어 질문을 영어로 자동 변환
- MoEngage Help Center 실시간 검색
- 검색 결과를 한국어로 번역
- 관련 링크 및 추가 정보 제공

## 📞 문의

문제가 있으시면 이슈를 생성해주세요!