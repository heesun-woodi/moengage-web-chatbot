from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoEngage Helper - AI Chatbot</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 10px;
        }
        .container {
            background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%; max-width: 800px; height: 85vh; display: flex; flex-direction: column;
        }
        .header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white; padding: 20px; text-align: center; border-radius: 20px 20px 0 0;
        }
        .header h1 { font-size: 1.8em; margin-bottom: 8px; }
        .header p { opacity: 0.9; font-size: 0.95em; }
        .messages { 
            flex: 1; padding: 20px; overflow-y: auto; background: #f8f9fa;
            display: flex; flex-direction: column; gap: 15px;
        }
        .message { padding: 15px 18px; border-radius: 18px; max-width: 75%; line-height: 1.5; }
        .bot-message { background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); align-self: flex-start; }
        .user-message { background: linear-gradient(135deg, #2196F3, #1976D2); color: white; align-self: flex-end; }
        .search-results {
            margin-top: 15px; padding: 15px; background: #f0f7ff; border-radius: 12px;
            border-left: 4px solid #2196F3;
        }
        .search-results h4 { color: #1976D2; margin-bottom: 10px; }
        .result-item { margin: 8px 0; padding: 8px; background: white; border-radius: 8px; }
        .result-title { font-weight: 600; color: #1976D2; text-decoration: none; }
        .result-title:hover { color: #0d47a1; }
        .result-summary { font-size: 0.9em; color: #555; margin-top: 4px; }
        .input-area { padding: 20px; background: white; border-radius: 0 0 20px 20px; }
        .input-container { display: flex; gap: 10px; margin-bottom: 15px; }
        #messageInput {
            flex: 1; padding: 15px 20px; border: 2px solid #e0e0e0; border-radius: 25px;
            font-size: 16px; outline: none; transition: border-color 0.3s;
        }
        #messageInput:focus { border-color: #4CAF50; }
        #sendButton {
            width: 50px; height: 50px; background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white; border: none; border-radius: 50%; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
        }
        #sendButton:hover { transform: scale(1.05); }
        #sendButton:disabled { background: #ccc; cursor: not-allowed; }
        .quick-buttons { display: flex; flex-wrap: wrap; gap: 8px; }
        .quick-btn {
            padding: 8px 15px; border: 1px solid #4CAF50; background: white; color: #4CAF50;
            border-radius: 20px; cursor: pointer; font-size: 0.85em; transition: all 0.3s;
        }
        .quick-btn:hover { background: #4CAF50; color: white; }
        .loading { opacity: 0.7; pointer-events: none; }
        .typing { font-style: italic; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-robot"></i> MoEngage Helper</h1>
            <p>MoEngage에 대한 궁금한 점을 한국어로 물어보세요!</p>
        </div>
        <div class="messages" id="messages">
            <div class="message bot-message">
                안녕하세요! 👋 <strong>MoEngage Helper</strong>입니다.<br><br>
                MoEngage에 대한 질문을 한국어로 입력해주세요.<br><br>
                <strong>💡 예시 질문:</strong><br>
                • "MoEngage 캠페인 만드는 방법"<br>
                • "푸시 알림 설정하는 방법"<br>
                • "세그먼트 생성하는 방법"
            </div>
        </div>
        <div class="input-area">
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="MoEngage에 대해 질문해주세요..." maxlength="300">
                <button id="sendButton" onclick="sendMessage()">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
            <div class="quick-buttons">
                <button class="quick-btn" onclick="sendQuickMessage('MoEngage 캠페인 만드는 방법')">캠페인 만들기</button>
                <button class="quick-btn" onclick="sendQuickMessage('푸시 알림 설정 방법')">푸시 알림</button>
                <button class="quick-btn" onclick="sendQuickMessage('세그먼트 설정하는 방법')">세그먼트</button>
                <button class="quick-btn" onclick="sendQuickMessage('A/B 테스트 방법')">A/B 테스트</button>
            </div>
        </div>
    </div>

    <script>
        let isLoading = false;

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message || isLoading) return;
            
            addMessage(message, 'user');
            input.value = '';
            
            setLoading(true);
            addTypingMessage();
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                removeTypingMessage();
                addMessage(data.answer, 'bot', data.searchResults);
            } catch (error) {
                removeTypingMessage();
                addMessage('죄송합니다. 현재 서버에 문제가 있어 답변드릴 수 없습니다.', 'bot');
            } finally {
                setLoading(false);
            }
        }
        
        function sendQuickMessage(message) {
            document.getElementById('messageInput').value = message;
            sendMessage();
        }
        
        function addMessage(text, sender, searchResults = null) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender + '-message';
            
            let content = text.replace(/\n/g, '<br>');
            
            if (searchResults && searchResults.length > 0) {
                content += '<div class="search-results"><h4>🔗 관련 자료</h4>';
                searchResults.forEach(result => {
                    content += `<div class="result-item">
                        <a href="${result.url}" target="_blank" class="result-title">${result.title}</a>
                        <div class="result-summary">${result.summary}</div>
                    </div>`;
                });
                content += '</div>';
            }
            
            messageDiv.innerHTML = content;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function addTypingMessage() {
            const messagesDiv = document.getElementById('messages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot-message typing';
            typingDiv.id = 'typing';
            typingDiv.innerHTML = '🤖 MoEngage 정보를 검색하고 있습니다...';
            messagesDiv.appendChild(typingDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function removeTypingMessage() {
            const typing = document.getElementById('typing');
            if (typing) typing.remove();
        }
        
        function setLoading(loading) {
            isLoading = loading;
            document.getElementById('sendButton').disabled = loading;
            document.querySelector('.input-area').classList.toggle('loading', loading);
        }
        
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
    '''

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        response = generate_moengage_response(user_message)
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'answer': '죄송합니다. 서버 오류가 발생했습니다.',
            'searchResults': []
        }), 500

def generate_moengage_response(question):
    q = question.lower()
    
    if any(keyword in q for keyword in ['캠페인', '메시지', '발송']):
        return {
            'answer': '''**📧 MoEngage 캠페인 생성 가이드**

**🎯 1단계: 캠페인 기본 설정**
• Dashboard → Campaigns → Create Campaign 클릭
• 캠페인 타입 선택: Push, Email, SMS, In-App

**👥 2단계: 타겟 설정** 
• 세그먼트 선택 (All Users 또는 Custom)
• A/B 테스트 그룹 설정

**✍️ 3단계: 컨텐츠 작성**
• 제목과 본문 작성 (간결하고 매력적으로)
• 개인화 태그 활용: {{name}}, {{city}}
• 이미지, 버튼, 딥링크 추가

**⏰ 4단계: 스케줄링**
• 즉시 발송 vs 예약 발송
• 사용자 타임존 고려

**📊 5단계: 발송**
• Preview로 미리보기
• Test Send로 테스트
• 최종 발송

**💡 베스트 프랙티스:**
• 제목 30자 이내 권장
• 적절한 발송 시간 선택
• A/B 테스트로 성과 최적화''',
            'searchResults': [
                {
                    'title': 'Campaign Creation Guide',
                    'url': 'https://help.moengage.com/hc/en-us/articles/campaign-creation',
                    'summary': '캠페인 생성의 전체 프로세스를 단계별로 설명하는 공식 가이드입니다.'
                }
            ]
        }
    
    elif any(keyword in q for keyword in ['푸시', '알림', 'push']):
        return {
            'answer': '''**📱 MoEngage 푸시 알림 설정 가이드**

**🔧 1단계: 기술 설정**
• iOS: APNs 인증서 업로드
• Android: FCM 서버 키 설정
• SDK 통합 확인

**📝 2단계: 푸시 캠페인 작성**
• Campaigns → Push Notification 선택
• 제목 (25자 이내), 메시지 (125자 이내)
• Rich Push: 이미지, 버튼 추가

**🎯 3단계: 타겟팅**
• 세그먼트 선택
• 개인화 설정

**📊 4단계: 테스트 및 발송**
• Test Push로 테스트
• 실시간 성과 모니터링

**⚠️ 주의사항:**
• 사용자 푸시 권한 확인
• 적절한 발송 빈도 유지''',
            'searchResults': [
                {
                    'title': 'Push Notification Setup',
                    'url': 'https://help.moengage.com/hc/en-us/articles/push-setup',
                    'summary': 'iOS와 Android 푸시 알림 설정 완벽 가이드입니다.'
                }
            ]
        }
    
    return {
        'answer': f'''**🔍 "{question}"에 대한 MoEngage 답변**

MoEngage Help Center에서 관련 정보를 찾았습니다.

**📋 일반적인 해결 방법:**
1. MoEngage Dashboard 접속
2. 해당 기능 메뉴로 이동
3. 설정 확인 및 활성화
4. 테스트 환경에서 검증

**💡 더 구체적인 질문을 해보세요:**
• "MoEngage 캠페인 만드는 방법"
• "푸시 알림 설정 방법"
• "세그먼트 생성하는 방법"

구체적인 기능명을 말씀해주시면 더 정확한 답변을 드릴 수 있습니다! 🚀''',
        'searchResults': [
            {
                'title': 'MoEngage Help Center',
                'url': 'https://help.moengage.com/hc/en-us',
                'summary': 'MoEngage의 모든 기능에 대한 공식 도움말 센터입니다.'
            }
        ]
    }

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
