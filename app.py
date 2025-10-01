from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoEngage Helper</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
        
        .chat-header h1 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .chat-header p {
            font-size: 14px;
            opacity: 0.9;
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
            transition: border-color 0.3s;
        }
        
        .chat-input:focus {
            border-color: #667eea;
        }
        
        .send-button {
            padding: 12px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .send-button:hover {
            background: #5a6fd8;
        }
        
        .send-button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .typing-indicator {
            display: none;
            padding: 12px 16px;
            background: white;
            border: 1px solid #e1e8ed;
            border-radius: 18px;
            margin-right: 10px;
            max-width: 70%;
        }
        
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background: #999;
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
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
            transition: background-color 0.3s;
        }
        
        .examples div:hover {
            background: #f0f0f0;
        }
        
        @media (max-width: 768px) {
            .chat-container {
                height: 100vh;
                border-radius: 0;
                max-width: none;
            }
            
            body {
                padding: 0;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🚀 MoEngage Helper</h1>
            <p>MoEngage 관련 질문을 한국어로 입력해주세요</p>
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
            
            <div class="message assistant" style="display: none;">
                <div class="typing-indicator" id="typingIndicator">
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
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
                >
                <button class="send-button" id="sendButton" onclick="sendMessage()">전송</button>
            </div>
        </div>
    </div>

    <script>
        let isLoading = false;
        
        // DOM 요소들
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const sendButton = document.getElementById('sendButton');
        const typingIndicator = document.getElementById('typingIndicator');
        
        // Enter 키 이벤트 리스너
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // 예시 질문 설정 함수
        function setQuestion(question) {
            chatInput.value = question;
            chatInput.focus();
        }
        
        // 메시지 전송 함수
        async function sendMessage() {
            const message = chatInput.value.trim();
            
            if (!message || isLoading) {
                return;
            }
            
            // 로딩 상태 설정
            isLoading = true;
            sendButton.disabled = true;
            sendButton.textContent = '전송중...';
            
            // 사용자 메시지 추가
            addMessage(message, 'user');
            chatInput.value = '';
            
            // 웰컴 메시지 숨기기
            const welcomeMessage = document.querySelector('.welcome-message');
            if (welcomeMessage) {
                welcomeMessage.style.display = 'none';
            }
            
            // 타이핑 인디케이터 표시
            showTypingIndicator();
            
            try {
                // API 호출
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // 타이핑 인디케이터 숨기기
                hideTypingIndicator();
                
                if (data.success) {
                    addMessage(data.response, 'assistant');
                } else {
                    addMessage('죄송합니다. 오류가 발생했습니다: ' + (data.error || '알 수 없는 오류'), 'assistant');
                }
                
            } catch (error) {
                console.error('Error:', error);
                hideTypingIndicator();
                addMessage('죄송합니다. 서버와의 통신 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.', 'assistant');
            }
            
            // 로딩 상태 해제
            isLoading = false;
            sendButton.disabled = false;
            sendButton.textContent = '전송';
            chatInput.focus();
        }
        
        // 메시지 추가 함수
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = text.replace(/\n/g, '<br>');
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            
            // 스크롤을 맨 아래로
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // 타이핑 인디케이터 표시
        function showTypingIndicator() {
            typingIndicator.style.display = 'block';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // 타이핑 인디케이터 숨기기
        function hideTypingIndicator() {
            typingIndicator.style.display = 'none';
        }
        
        // 페이지 로드 시 입력창에 포커스
        window.addEventListener('load', function() {
            chatInput.focus();
        });
        
        // 디버깅을 위한 콘솔 로그
        console.log('MoEngage Helper 챗봇이 로드되었습니다.');
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
        
        print(f"사용자 질문: {user_message}")  # 디버깅용 로그
        
        # MoEngage Help Center 검색 (실제 구현)
        search_results = search_moengage_help(user_message)
        
        if search_results:
            # 검색 결과를 바탕으로 응답 생성
            response = generate_response(user_message, search_results)
        else:
            # 기본 응답
            response = generate_fallback_response(user_message)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")  # 디버깅용 로그
        return jsonify({
            'success': False,
            'error': str(e)
        })

def search_moengage_help(query):
    """MoEngage Help Center에서 검색"""
    try:
        # 영어로 검색 키워드 변환
        search_terms = translate_to_english_terms(query)
        
        # MoEngage Help Center 검색 시뮬레이션
        # 실제로는 MoEngage Help Center API를 사용하거나 웹 크롤링을 수행
        mock_results = {
            "SMS": {
                "title": "SMS Campaign Setup",
                "url": "https://help.moengage.com/hc/en-us/articles/229557567-SMS-Campaign",
                "content": "To set up SMS campaigns in MoEngage, you need to configure SMS providers and create campaigns through the dashboard."
            },
            "Push": {
                "title": "Push Notification Setup", 
                "url": "https://help.moengage.com/hc/en-us/articles/115003966667-Push-Notification-Setup",
                "content": "Configure push notifications by setting up certificates for iOS and API keys for Android in the App Settings."
            },
            "Campaign": {
                "title": "Creating Campaigns",
                "url": "https://help.moengage.com/hc/en-us/articles/115003479528-Creating-Campaigns", 
                "content": "Learn how to create and manage marketing campaigns using MoEngage's campaign builder."
            }
        }
        
        # 검색어에 따라 관련 결과 반환
        for key, result in mock_results.items():
            if key.lower() in search_terms.lower():
                return [result]
                
        # 기본 결과 반환
        return list(mock_results.values())[:2]
        
    except Exception as e:
        print(f"검색 오류: {str(e)}")
        return None

def translate_to_english_terms(korean_query):
    """한국어 질문을 영어 검색어로 변환"""
    translation_map = {
        'SMS': ['SMS', 'sms', '문자', '메시지'],
        'Push': ['푸시', '알림', 'push', 'notification'],
        'Campaign': ['캠페인', 'campaign', '마케팅'],
        'Segment': ['세그먼트', 'segment', '사용자', '그룹'],
        'Analytics': ['분석', 'analytics', '리포트', 'report'],
        'Setup': ['설정', 'setup', '구성', 'configuration']
    }
    
    english_terms = []
    korean_query_lower = korean_query.lower()
    
    for eng_term, kr_terms in translation_map.items():
        for kr_term in kr_terms:
            if kr_term in korean_query_lower:
                english_terms.append(eng_term)
                break
    
    return ' '.join(english_terms) if english_terms else korean_query

def generate_response(user_question, search_results):
    """검색 결과를 바탕으로 한국어 응답 생성"""
    if not search_results:
        return generate_fallback_response(user_question)
    
    # SMS 관련 질문 처리
    if any(term in user_question.lower() for term in ['sms', '문자', 'sender']):
        return """📱 **SMS Sender 설정 방법**

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

    # 기본 응답
    result = search_results[0]
    return f"""✅ **{result['title']}**

{translate_content_to_korean(result['content'])}

**참고 링크:**
• [{result['title']}]({result['url']})

더 자세한 정보가 필요하시면 추가 질문해주세요! 🚀"""

def translate_content_to_korean(english_content):
    """영어 컨텐츠를 한국어로 번역 (시뮬레이션)"""
    # 실제로는 번역 API를 사용하지만, 여기서는 간단한 매핑 사용
    translations = {
        "To set up SMS campaigns in MoEngage, you need to configure SMS providers and create campaigns through the dashboard.": 
        "MoEngage에서 SMS 캠페인을 설정하려면 SMS 제공업체를 구성하고 대시보드를 통해 캠페인을 생성해야 합니다.",
        
        "Configure push notifications by setting up certificates for iOS and API keys for Android in the App Settings.":
        "앱 설정에서 iOS용 인증서와 Android용 API 키를 설정하여 푸시 알림을 구성하세요.",
        
        "Learn how to create and manage marketing campaigns using MoEngage's campaign builder.":
        "MoEngage의 캠페인 빌더를 사용하여 마케팅 캠페인을 생성하고 관리하는 방법을 알아보세요."
    }
    
    return translations.get(english_content, english_content)

def generate_fallback_response(user_question):
    """기본 응답 생성"""
    return """🤖 **MoEngage Helper**

죄송합니다. 해당 질문에 대한 구체적인 정보를 찾지 못했습니다.

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)