from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

# HTML 템플릿 (매우 간단한 버전)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoEngage Helper - Simple</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 800px;
            height: 600px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .debug-bar {
            background: #ff4757;
            color: white;
            padding: 10px;
            text-align: center;
            font-size: 14px;
            font-weight: bold;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }
        
        .message.user {
            flex-direction: row-reverse;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .message.user .message-content {
            background: #667eea;
            color: white;
            margin-left: 10px;
        }
        
        .message.assistant .message-content {
            background: white;
            color: #333;
            margin-right: 10px;
            border: 1px solid #e1e8ed;
        }
        
        .chat-input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e1e8ed;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e1e8ed;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
        }
        
        .send-button {
            padding: 12px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 14px;
            cursor: pointer;
        }
        
        .send-button:hover {
            background: #5a6fd8;
        }
        
        .send-button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .welcome-message {
            text-align: center;
            color: #666;
            padding: 20px;
        }
        
        .examples {
            margin-top: 15px;
            font-size: 13px;
            color: #888;
        }
        
        .examples div {
            margin: 5px 0;
            padding: 8px 12px;
            background: white;
            border-radius: 12px;
            cursor: pointer;
        }
        
        .examples div:hover {
            background: #f0f0f0;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🚀 MoEngage Helper - Simple Version</h1>
            <p>MoEngage 관련 질문을 한국어로 입력해주세요</p>
        </div>
        
        <div class="debug-bar" id="debugBar">
            상태: 페이지 로딩 완료, JavaScript 테스트 중...
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="welcome-message">
                <div>안녕하세요! 👋 <strong>MoEngage Helper</strong>입니다.</div>
                <div>MoEngage에 대한 질문을 한국어로 입력해주세요.</div>
                
                <div class="examples">
                    <strong>💡 예시 질문:</strong>
                    <div onclick="setQuestion('MoEngage 캠페인 만드는 방법')">• "MoEngage 캠페인 만드는 방법"</div>
                    <div onclick="setQuestion('푸시 알림 설정하는 방법')">• "푸시 알림 설정하는 방법"</div>
                    <div onclick="setQuestion('SMS sender 설정 방법')">• "SMS sender 설정 방법"</div>
                    <div onclick="setQuestion('세그먼트 생성하는 방법')">• "세그먼트 생성하는 방법"</div>
                </div>
            </div>
        </div>
        
        <div class="chat-input-container">
            <div class="input-group">
                <input 
                    type="text" 
                    class="chat-input" 
                    id="chatInput"
                    placeholder="MoEngage에 대해 질문해주세요..."
                    maxlength="500"
                    onkeypress="handleKeyPress(event)"
                >
                <button class="send-button" id="sendButton" onclick="sendMessage()">전송</button>
            </div>
        </div>
    </div>

    <script>
        // 전역 변수
        var isLoading = false;
        var debugBar = null;
        var chatMessages = null;
        var chatInput = null;
        var sendButton = null;
        
        // 디버그 메시지 업데이트
        function updateDebug(message) {
            console.log('[DEBUG] ' + message);
            if (debugBar) {
                debugBar.innerHTML = '상태: ' + message;
            }
        }
        
        // 페이지 로드 완료 시 실행
        function initializePage() {
            updateDebug('DOM 요소 찾는 중...');
            
            // DOM 요소 가져오기
            debugBar = document.getElementById('debugBar');
            chatMessages = document.getElementById('chatMessages');
            chatInput = document.getElementById('chatInput');
            sendButton = document.getElementById('sendButton');
            
            if (!debugBar || !chatMessages || !chatInput || !sendButton) {
                updateDebug('오류: 필수 DOM 요소를 찾을 수 없음');
                alert('페이지 로딩 오류가 발생했습니다. 페이지를 새로고침해주세요.');
                return;
            }
            
            updateDebug('초기화 완료 - 테스트 가능');
            
            // 입력창에 포커스
            chatInput.focus();
        }
        
        // 키 입력 처리
        function handleKeyPress(event) {
            updateDebug('키 입력 감지: ' + event.key);
            if (event.key === 'Enter') {
                event.preventDefault();
                updateDebug('Enter 키로 전송 시도');
                sendMessage();
            }
        }
        
        // 예시 질문 설정
        function setQuestion(question) {
            updateDebug('예시 질문 클릭: ' + question);
            if (chatInput) {
                chatInput.value = question;
                chatInput.focus();
            }
        }
        
        // 메시지 전송 (XMLHttpRequest 사용)
        function sendMessage() {
            updateDebug('sendMessage 함수 호출됨');
            
            if (!chatInput) {
                updateDebug('오류: chatInput이 없음');
                return;
            }
            
            var message = chatInput.value.trim();
            updateDebug('전송할 메시지: ' + message);
            
            if (!message) {
                updateDebug('경고: 빈 메시지');
                return;
            }
            
            if (isLoading) {
                updateDebug('경고: 이미 처리 중');
                return;
            }
            
            // 로딩 상태 설정
            isLoading = true;
            sendButton.disabled = true;
            sendButton.innerHTML = '전송중...';
            updateDebug('로딩 상태 설정됨');
            
            // 사용자 메시지 추가
            addMessage(message, 'user');
            chatInput.value = '';
            
            // 웰컴 메시지 숨기기
            var welcomeMessage = document.querySelector('.welcome-message');
            if (welcomeMessage) {
                welcomeMessage.style.display = 'none';
            }
            
            // XMLHttpRequest로 API 호출
            updateDebug('API 호출 시작');
            var xhr = new XMLHttpRequest();
            
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    updateDebug('API 응답 받음, 상태: ' + xhr.status);
                    
                    // 로딩 상태 해제
                    isLoading = false;
                    sendButton.disabled = false;
                    sendButton.innerHTML = '전송';
                    
                    if (xhr.status === 200) {
                        try {
                            var data = JSON.parse(xhr.responseText);
                            updateDebug('응답 파싱 성공');
                            
                            if (data.success) {
                                addMessage(data.response, 'assistant');
                                updateDebug('응답 표시 완료');
                            } else {
                                addMessage('죄송합니다. 오류가 발생했습니다: ' + (data.error || '알 수 없는 오류'), 'assistant');
                                updateDebug('서버 오류: ' + data.error);
                            }
                        } catch (e) {
                            updateDebug('JSON 파싱 오류: ' + e.message);
                            addMessage('응답 처리 중 오류가 발생했습니다.', 'assistant');
                        }
                    } else {
                        updateDebug('HTTP 오류: ' + xhr.status);
                        addMessage('서버와의 통신 중 오류가 발생했습니다. (HTTP ' + xhr.status + ')', 'assistant');
                    }
                    
                    chatInput.focus();
                }
            };
            
            xhr.onerror = function() {
                updateDebug('네트워크 오류 발생');
                isLoading = false;
                sendButton.disabled = false;
                sendButton.innerHTML = '전송';
                addMessage('네트워크 오류가 발생했습니다. 인터넷 연결을 확인해주세요.', 'assistant');
                chatInput.focus();
            };
            
            xhr.open('POST', '/api/chat', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ message: message }));
        }
        
        // 메시지 추가
        function addMessage(text, sender) {
            updateDebug('메시지 추가: ' + sender);
            
            if (!chatMessages) {
                updateDebug('오류: chatMessages가 없음');
                return;
            }
            
            var messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender;
            
            var contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = text.replace(/\n/g, '<br>');
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            
            // 스크롤을 맨 아래로
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // 페이지 로드 시 초기화 (여러 방법으로 시도)
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializePage);
        } else {
            initializePage();
        }
        
        // 윈도우 로드 이벤트도 추가 (backup)
        window.onload = function() {
            updateDebug('window.onload 이벤트 발생');
            if (!debugBar) {
                initializePage();
            }
        };
        
        // 전역 오류 처리
        window.onerror = function(msg, url, line, col, error) {
            updateDebug('전역 오류: ' + msg + ' (line: ' + line + ')');
            console.error('JavaScript 오류:', msg, url, line, col, error);
            return false;
        };
        
        updateDebug('JavaScript 로딩 완료');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': '메시지가 비어있습니다.'
            })
        
        print(f"사용자 질문: {user_message}")
        
        # SMS 관련 질문 처리
        if any(term in user_message.lower() for term in ['sms', '문자', 'sender']):
            response = """📱 **SMS Sender 설정 방법**

MoEngage에서 SMS 발송을 위한 Sender 설정 방법을 안내해드리겠습니다:

**1단계: SMS 제공업체 설정**
• MoEngage 대시보드 → Settings → Channels → SMS
• SMS 제공업체(Twilio, AWS SNS 등) 연동
• API 키 및 인증 정보 입력

**2단계: Sender ID 구성**
• Sender ID 또는 발신번호 등록
• 국가별 규정에 따른 승인 절차 진행
• 테스트 발송으로 설정 확인

**3단계: SMS 캠페인 생성**
• Campaigns → Create Campaign → SMS
• 대상 세그먼트 선택
• 메시지 내용 작성 및 발송 일정 설정

**참고 자료:**
• [SMS Campaign Setup Guide](https://help.moengage.com/hc/en-us/articles/229557567-SMS-Campaign)
• [SMS Provider Integration](https://help.moengage.com/hc/en-us/sections/115003735167-SMS)

추가 질문이 있으시면 언제든 물어보세요! 🚀"""
        
        elif any(term in user_message.lower() for term in ['푸시', '알림', 'push']):
            response = """📲 **푸시 알림 설정 방법**

MoEngage에서 푸시 알림을 설정하는 방법을 안내해드리겠습니다:

**1단계: 앱 설정**
• MoEngage 대시보드 → Settings → App Settings
• iOS: APNs 인증서 업로드
• Android: FCM Server Key 입력

**2단계: SDK 연동**
• iOS/Android SDK 설치 및 초기화
• 푸시 토큰 등록 코드 구현
• 알림 권한 요청 설정

**3단계: 푸시 캠페인 생성**
• Campaigns → Create Campaign → Push
• 메시지 내용 및 이미지 설정
• 타겟 세그먼트 선택 및 발송 일정 설정

더 자세한 정보가 필요하시면 추가 질문해주세요! 🚀"""
        
        elif any(term in user_message.lower() for term in ['캠페인', 'campaign']):
            response = """🎯 **MoEngage 캠페인 생성 방법**

MoEngage에서 마케팅 캠페인을 만드는 방법을 안내해드리겠습니다:

**1단계: 캠페인 유형 선택**
• Push 알림, SMS, 이메일, 인앱 메시지 중 선택
• Campaigns → Create Campaign

**2단계: 타겟 설정**
• 사용자 세그먼트 선택
• 개인화 조건 설정
• A/B 테스트 그룹 구성 (선택사항)

**3단계: 콘텐츠 작성**
• 메시지 내용 작성
• 이미지 및 버튼 추가
• 딥링크 및 랜딩 페이지 설정

**4단계: 발송 일정**
• 즉시 발송 또는 예약 발송
• 트리거 조건 설정 (이벤트 기반)

더 구체적인 질문이 있으시면 언제든 물어보세요! 🚀"""
        
        else:
            response = f"""🤖 **MoEngage Helper**

"{user_message}"에 대한 질문을 받았습니다.

**추천 질문들:**
• MoEngage 캠페인 생성 방법
• 푸시 알림 설정 가이드  
• SMS 캠페인 설정 방법
• 사용자 세그먼트 생성 방법
• 분석 리포트 확인 방법

**도움이 되는 링크:**
• [MoEngage Help Center](https://help.moengage.com/hc/en-us)
• [Getting Started Guide](https://help.moengage.com/hc/en-us/categories/115003745208-Getting-Started)

더 구체적인 질문을 입력해주시면 더 정확한 답변을 드릴 수 있습니다! 🚀"""
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)