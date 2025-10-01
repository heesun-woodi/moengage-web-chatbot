# 🚀 MoEngage 슬랙봇 설정 가이드 (비개발자용)

## 📋 준비물
- 슬랙 워크스페이스 관리자 권한
- GitHub 계정  
- Railway 계정 (무료)

---

## 1️⃣ 1단계: 슬랙 앱 만들기 (15분)

### 1-1. 슬랙 개발자 사이트 접속
1. 웹브라우저에서 **https://api.slack.com/apps** 접속
2. **"Create New App"** 버튼 클릭
3. **"From scratch"** 선택
4. 앱 이름: `MoEngage Helper` 입력
5. 본인 슬랙 워크스페이스 선택
6. **"Create App"** 클릭

### 1-2. 봇 권한 설정 ⭐ 중요!
1. 왼쪽 메뉴에서 **"OAuth & Permissions"** 클릭
2. **"Bot Token Scopes"** 섹션으로 스크롤
3. **"Add an OAuth Scope"** 버튼 클릭하여 다음 권한들을 **하나씩** 추가:

```
✅ app_mentions:read      (봇 멘션 읽기)
✅ channels:history       (채널 메시지 기록 읽기)  
✅ channels:read          (채널 정보 읽기)
✅ chat:write             (메시지 전송)
✅ reactions:read         (리액션 읽기)
✅ reactions:write        (리액션 추가)
✅ im:history             (DM 기록 읽기)
✅ im:read                (DM 읽기)
✅ im:write               (DM 전송)
```

### 1-3. 워크스페이스에 설치
1. 같은 페이지에서 **"Install to Workspace"** 버튼 클릭
2. **"허용"** 클릭
3. ✅ **"Bot User OAuth Token"** 복사해서 메모장에 저장 (xoxb-로 시작하는 긴 텍스트)

### 1-4. 서명 키 복사
1. 왼쪽 메뉴에서 **"Basic Information"** 클릭
2. **"App Credentials"** 섹션에서 **"Signing Secret"** 옆 **"Show"** 버튼 클릭
3. ✅ 나타나는 키를 복사해서 메모장에 저장

---

## 2️⃣ 2단계: GitHub에 코드 복사하기 (5분)

### 2-1. 이 링크로 바로 복사하기
👉 **https://github.com/new/import**

1. 위 링크 클릭
2. **"Your old repository's clone URL"**에 다음 입력:
   ```
   https://github.com/genspark-moengage-bot/slackbot
   ```
3. **Repository name**: `moengage-slackbot` 입력
4. **"Begin import"** 클릭
5. 완료될 때까지 1-2분 대기

---

## 3️⃣ 3단계: Railway로 배포하기 (10분)

### 3-1. Railway 계정 만들기
1. **https://railway.app** 접속
2. **"Start a New Project"** 클릭
3. **"Login with GitHub"** 선택
4. GitHub 계정으로 로그인

### 3-2. 프로젝트 배포
1. **"Deploy from GitHub repo"** 클릭
2. 방금 만든 `moengage-slackbot` 저장소 선택
3. **"Deploy Now"** 클릭
4. ⏳ 배포 완료까지 2-3분 대기

### 3-3. 환경변수 설정 ⭐ 중요!
배포 완료 후:
1. **"Variables"** 탭 클릭
2. **"New Variable"** 버튼으로 다음 3개 추가:

**첫 번째 변수:**
- Name: `SLACK_BOT_TOKEN`
- Value: 1단계에서 복사한 xoxb- 토큰

**두 번째 변수:** 
- Name: `SLACK_SIGNING_SECRET`
- Value: 1단계에서 복사한 서명 키  

**세 번째 변수:**
- Name: `PORT`
- Value: `8000`

### 3-4. 서버 주소 확인
1. **"Settings"** 탭 클릭
2. **"Domains"** 섹션에서 **"Generate Domain"** 클릭  
3. ✅ 생성된 주소 복사 (예: https://moengage-slackbot-production.up.railway.app)

---

## 4️⃣ 4단계: 슬랙과 연결하기 (5분)

### 4-1. 이벤트 구독 설정
1. 슬랙 개발자 사이트 **https://api.slack.com/apps** 에서 생성한 앱 선택
2. 왼쪽 메뉴 **"Event Subscriptions"** 클릭
3. **"Enable Events"** 토글을 **ON**으로 변경
4. **"Request URL"** 에 다음 형식으로 입력:
   ```
   https://your-railway-domain.railway.app/slack/events
   ```
   ⚠️ your-railway-domain 부분을 실제 Railway 주소로 변경!

5. ✅ 초록색 "Verified" 표시가 나타나면 성공!

### 4-2. 이벤트 추가
**"Subscribe to bot events"** 섹션에서 **"Add Bot User Event"** 클릭하여 추가:
```
✅ reaction_added
✅ message.channels  
✅ app_mention
```

### 4-3. 저장
페이지 맨 아래 **"Save Changes"** 클릭

---

## 5️⃣ 5단계: 슬랙에서 테스트 (3분)

### 5-1. 봇을 채널에 초대
1. 원하는 슬랙 채널에서 다음 입력:
   ```
   /invite @MoEngage Helper
   ```
2. 엔터 키 누르기

### 5-2. 테스트하기
1. 채널에 다음과 같은 메시지 입력:
   ```
   MoEngage에서 푸시 알림 설정하는 방법이 뭐야?
   ```

2. 해당 메시지에 🔍 (돋보기) 이모티콘 클릭

3. 약 5초 후 봇이 다음과 같이 응답하는지 확인:
   ```
   🤖 MoEngage Helper Bot
   📝 질문: MoEngage에서 푸시 알림 설정하는 방법이 뭐야?
   🔍 영어 검색어: How to 푸시 알림 설정하는 방법이 뭐야? in MoEngage
   💡 답변: 'MoEngage에서 푸시 알림 설정하는 방법이 뭐야?'에 대한 답변을 MoEngage Help Center에서 찾았습니다.
   🔗 관련 자료:
   • Push Notification Setup Guide
   • Campaign Creation Tutorial
   ```

---

## 🆘 문제 해결

### ❌ "URL 인증 실패" 
- Railway 앱이 정상 실행 중인지 확인
- URL 끝에 `/slack/events`가 정확히 있는지 확인
- Railway Variables에서 환경변수 3개 모두 설정했는지 확인

### ❌ 봇이 응답하지 않음
- 슬랙 권한 9개 모두 추가했는지 확인
- 이벤트 3개 모두 추가했는지 확인  
- 봇을 채널에 초대했는지 확인

### ❌ Railway 배포 실패
- GitHub 저장소가 public인지 확인
- requirements.txt 파일이 있는지 확인

---

## ✅ 완료 체크리스트

설정이 완료되면 체크해보세요:

**1단계 슬랙 앱:**
- [ ] 슬랙 앱 생성 완료
- [ ] 봇 권한 9개 추가 완료
- [ ] Bot Token (xoxb-) 복사 완료  
- [ ] Signing Secret 복사 완료

**2단계 GitHub:**
- [ ] 코드 저장소 복사 완료

**3단계 Railway:**
- [ ] Railway 배포 완료
- [ ] 환경변수 3개 설정 완료
- [ ] Domain 생성 완료

**4단계 연결:**
- [ ] Event Subscriptions 활성화 완료
- [ ] Request URL 인증 완료 (✅ Verified)
- [ ] 이벤트 3개 추가 완료

**5단계 테스트:**
- [ ] 봇을 채널에 초대 완료
- [ ] 🔍 이모티콘 테스트 성공

모든 항목이 체크되면 성공! 🎉

---

## 💡 사용 팁

### 다양한 사용법:
1. **이모티콘 방식**: 질문 → 🔍 이모티콘 추가
2. **멘션 방식**: `@MoEngage Helper 질문 내용`
3. **DM 방식**: 봇에게 직접 메시지

### 질문 예시:
- "MoEngage 캠페인 만드는 방법"  
- "푸시 알림 테스트 어떻게 해?"
- "세그먼트 설정 방법"
- "A/B 테스트 설정"

---

📞 **도움이 필요하시면 언제든 문의하세요!**