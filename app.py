from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import requests
import json

app = Flask(__name__)

# HTML 템플릿 (JavaScript 완전 제거, Form 기반)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoEngage Helper - No JavaScript</title>
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
            min-height: 600px;
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
        
        .status-bar {
            background: #2ed573;
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
            white-space: pre-line;
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
        
        .input-form {
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
        
        .example-form {
            display: inline-block;
            margin: 2px;
        }
        
        .example-button {
            margin: 5px 0;
            padding: 8px 12px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 12px;
            cursor: pointer;
            transition: background-color 0.3s;
            font-size: 13px;
        }
        
        .example-button:hover {
            background: #f0f0f0;
        }
        
        .clear-form {
            margin-top: 10px;
        }
        
        .clear-button {
            padding: 8px 16px;
            background: #ff6b6b;
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-size: 12px;
        }
        
        .clear-button:hover {
            background: #ff5252;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🚀 MoEngage Helper - No JavaScript Version</h1>
            <p>MoEngage 관련 질문을 한국어로 입력해주세요</p>
        </div>
        
        <div class="status-bar">
            ✅ 상태: JavaScript 없이 정상 작동 중 - Form 기반 채팅
        </div>
        
        <div class="chat-messages">
            {% for msg in messages %}
            <div class="message {{ msg.sender }}">
                <div class="message-content">{{ msg.content }}</div>
            </div>
            {% endfor %}
            
            {% if not messages %}
            <div class="welcome-message">
                <div>안녕하세요! 👋 <strong>MoEngage Helper</strong>입니다.</div>
                <div>MoEngage에 대한 질문을 한국어로 입력해주세요.</div>
                
                <div class="examples">
                    <strong>💡 예시 질문 (클릭하면 자동 입력):</strong><br>
                    
                    <form class="example-form" method="POST" action="/ask">
                        <input type="hidden" name="message" value="MoEngage 캠페인 만드는 방법">
                        <button type="submit" class="example-button">• "MoEngage 캠페인 만드는 방법"</button>
                    </form>
                    
                    <form class="example-form" method="POST" action="/ask">
                        <input type="hidden" name="message" value="푸시 알림 설정하는 방법">
                        <button type="submit" class="example-button">• "푸시 알림 설정하는 방법"</button>
                    </form>
                    
                    <form class="example-form" method="POST" action="/ask">
                        <input type="hidden" name="message" value="SMS sender 설정 방법">
                        <button type="submit" class="example-button">• "SMS sender 설정 방법"</button>
                    </form>
                    
                    <form class="example-form" method="POST" action="/ask">
                        <input type="hidden" name="message" value="세그먼트 생성하는 방법">
                        <button type="submit" class="example-button">• "세그먼트 생성하는 방법"</button>
                    </form>
                </div>
            </div>
            {% endif %}
        </div>
        
        <div class="chat-input-container">
            <form class="input-form" method="POST" action="/ask">
                <input 
                    type="text" 
                    class="chat-input" 
                    name="message"
                    placeholder="MoEngage에 대해 질문해주세요..."
                    maxlength="500"
                    required
                    value="{{ user_input or '' }}"
                >
                <button type="submit" class="send-button">전송</button>
            </form>
            
            {% if messages %}
            <form class="clear-form" method="POST" action="/clear">
                <button type="submit" class="clear-button">대화 내역 지우기</button>
            </form>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# 세션 데이터 저장 (실제 운영에서는 데이터베이스 사용)
chat_sessions = {}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, messages=[], user_input="")

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form.get('message', '').strip()
    
    if not user_message:
        return redirect(url_for('index'))
    
    # 기존 대화 내역 가져오기 (간단한 구현)
    session_id = request.remote_addr  # IP를 세션 ID로 사용
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    # 사용자 메시지 추가
    chat_sessions[session_id].append({
        'sender': 'user',
        'content': user_message
    })
    
    # AI 응답 생성
    response = generate_response(user_message)
    
    # AI 응답 추가
    chat_sessions[session_id].append({
        'sender': 'assistant', 
        'content': response
    })
    
    # 대화 내역이 너무 길어지면 오래된 것 삭제
    if len(chat_sessions[session_id]) > 20:
        chat_sessions[session_id] = chat_sessions[session_id][-20:]
    
    return render_template_string(HTML_TEMPLATE, 
                                messages=chat_sessions[session_id], 
                                user_input="")

@app.route('/clear', methods=['POST'])
def clear():
    session_id = request.remote_addr
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return redirect(url_for('index'))

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """기존 API 호환성 유지"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': '메시지가 비어있습니다.'
            })
        
        response = generate_response(user_message)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def generate_response(user_message):
    """사용자 메시지에 대한 응답 생성"""
    user_message_lower = user_message.lower()
    
    if any(term in user_message_lower for term in ['sms', '문자', 'sender']):
        return """📱 SMS Sender 설정 방법

MoEngage에서 SMS 발송을 위한 Sender 설정 방법을 안내해드리겠습니다:

1단계: SMS 제공업체 설정
• MoEngage 대시보드 → Settings → Channels → SMS
• SMS 제공업체(Twilio, AWS SNS 등) 연동
• API 키 및 인증 정보 입력

2단계: Sender ID 구성
• Sender ID 또는 발신번호 등록
• 국가별 규정에 따른 승인 절차 진행
• 테스트 발송으로 설정 확인

3단계: SMS 캠페인 생성
• Campaigns → Create Campaign → SMS
• 대상 세그먼트 선택
• 메시지 내용 작성 및 발송 일정 설정

참고 자료:
• SMS Campaign Setup Guide: https://help.moengage.com/hc/en-us/articles/229557567-SMS-Campaign
• SMS Provider Integration: https://help.moengage.com/hc/en-us/sections/115003735167-SMS

추가 질문이 있으시면 언제든 물어보세요! 🚀"""
    
    elif any(term in user_message_lower for term in ['푸시', '알림', 'push']):
        return """📲 푸시 알림 설정 방법

MoEngage에서 푸시 알림을 설정하는 방법을 안내해드리겠습니다:

1단계: 앱 설정
• MoEngage 대시보드 → Settings → App Settings
• iOS: APNs 인증서 업로드
• Android: FCM Server Key 입력

2단계: SDK 연동
• iOS/Android SDK 설치 및 초기화
• 푸시 토큰 등록 코드 구현
• 알림 권한 요청 설정

3단계: 푸시 캠페인 생성
• Campaigns → Create Campaign → Push
• 메시지 내용 및 이미지 설정
• 타겟 세그먼트 선택 및 발송 일정 설정

참고 자료:
• Push Notification Setup: https://help.moengage.com/hc/en-us/articles/115003966667-Push-Notification-Setup
• SDK Integration Guide: https://help.moengage.com/hc/en-us/sections/115003737207-SDK-Integration

더 자세한 정보가 필요하시면 추가 질문해주세요! 🚀"""
    
    elif any(term in user_message_lower for term in ['캠페인', 'campaign']):
        return """🎯 MoEngage 캠페인 생성 방법

MoEngage에서 마케팅 캠페인을 만드는 방법을 안내해드리겠습니다:

1단계: 캠페인 유형 선택
• Push 알림, SMS, 이메일, 인앱 메시지 중 선택
• Campaigns → Create Campaign

2단계: 타겟 설정
• 사용자 세그먼트 선택
• 개인화 조건 설정
• A/B 테스트 그룹 구성 (선택사항)

3단계: 콘텐츠 작성
• 메시지 내용 작성
• 이미지 및 버튼 추가
• 딥링크 및 랜딩 페이지 설정

4단계: 발송 일정
• 즉시 발송 또는 예약 발송
• 트리거 조건 설정 (이벤트 기반)

참고 자료:
• Creating Campaigns: https://help.moengage.com/hc/en-us/articles/115003479528-Creating-Campaigns
• Campaign Builder Guide: https://help.moengage.com/hc/en-us/sections/115003735127-Campaigns

더 구체적인 질문이 있으시면 언제든 물어보세요! 🚀"""
    
    elif any(term in user_message_lower for term in ['세그먼트', 'segment']):
        return """👥 사용자 세그먼트 생성 방법

MoEngage에서 사용자 세그먼트를 생성하는 방법을 안내해드리겠습니다:

1단계: 세그먼트 생성 시작
• MoEngage 대시보드 → Analytics → Segments
• Create Segment 버튼 클릭

2단계: 조건 설정
• 사용자 속성 (나이, 성별, 위치 등)
• 행동 기반 조건 (앱 사용, 구매 이력 등)
• 이벤트 기반 조건 (특정 액션 수행)

3단계: 조건 조합
• AND/OR 논리 연산자 사용
• 여러 조건을 조합하여 정교한 타겟팅
• 실시간 사용자 수 확인

4단계: 세그먼트 저장 및 활용
• 세그먼트 이름 설정 및 저장
• 캠페인에서 타겟 그룹으로 활용
• 정기적인 세그먼트 성과 분석

참고 자료:
• Segmentation Guide: https://help.moengage.com/hc/en-us/sections/115003737167-Segmentation
• User Analytics: https://help.moengage.com/hc/en-us/sections/115003737147-Analytics

더 구체적인 질문이 있으시면 언제든 물어보세요! 🚀"""
    
    else:
        return f"""🤖 MoEngage Helper

"{user_message}"에 대한 질문을 받았습니다.

추천 질문들:
• MoEngage 캠페인 생성 방법
• 푸시 알림 설정 가이드  
• SMS 캠페인 설정 방법
• 사용자 세그먼트 생성 방법
• 분석 리포트 확인 방법

도움이 되는 링크:
• MoEngage Help Center: https://help.moengage.com/hc/en-us
• Getting Started Guide: https://help.moengage.com/hc/en-us/categories/115003745208-Getting-Started

더 구체적인 질문을 입력해주시면 더 정확한 답변을 드릴 수 있습니다! 🚀"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)