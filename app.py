from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import quote

app = Flask(__name__)

# HTML 템플릿 (Form 기반)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoEngage Helper - Real Search</title>
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
            background: #ff6b6b;
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
        
        .search-info {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 10px;
            margin: 10px 0;
            font-size: 12px;
            color: #1976d2;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🚀 MoEngage Helper - Real Search</h1>
            <p>MoEngage Help Center에서 실제 검색하여 답변합니다</p>
        </div>
        
        <div class="status-bar" id="statusBar">
            {{ status_message or "✅ 실시간 MoEngage Help Center 검색 준비됨" }}
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
                <div>MoEngage Help Center에서 실제 검색하여 정확한 답변을 제공합니다.</div>
                
                <div class="examples">
                    <strong>💡 예시 질문 (클릭하면 자동 검색):</strong><br>
                    
                    <form class="example-form" method="POST" action="/ask">
                        <input type="hidden" name="message" value="standard attribute는 어떻게 있어?">
                        <button type="submit" class="example-button">• "standard attribute는 어떻게 있어?"</button>
                    </form>
                    
                    <form class="example-form" method="POST" action="/ask">
                        <input type="hidden" name="message" value="SMS 캠페인 설정하는 방법">
                        <button type="submit" class="example-button">• "SMS 캠페인 설정하는 방법"</button>
                    </form>
                    
                    <form class="example-form" method="POST" action="/ask">
                        <input type="hidden" name="message" value="푸시 알림 설정 가이드">
                        <button type="submit" class="example-button">• "푸시 알림 설정 가이드"</button>
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
                <button type="submit" class="send-button">검색 & 답변</button>
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

# 세션 데이터 저장
chat_sessions = {}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, messages=[], user_input="")

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form.get('message', '').strip()
    
    if not user_message:
        return redirect(url_for('index'))
    
    # 기존 대화 내역 가져오기
    session_id = request.remote_addr
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    # 사용자 메시지 추가
    chat_sessions[session_id].append({
        'sender': 'user',
        'content': user_message
    })
    
    # 검색 상태 메시지 추가
    status_message = f"🔍 '{user_message}' 검색 중... MoEngage Help Center에서 검색하고 번역 중입니다."
    
    try:
        # 실제 MoEngage Help Center 검색
        response = search_and_generate_response(user_message)
        
        # AI 응답 추가
        chat_sessions[session_id].append({
            'sender': 'assistant', 
            'content': response
        })
        
        status_message = "✅ 검색 완료 - MoEngage Help Center에서 최신 정보를 가져왔습니다"
        
    except Exception as e:
        # 오류 발생 시 기본 응답
        error_response = f"""❌ **검색 중 오류 발생**

죄송합니다. MoEngage Help Center 검색 중 오류가 발생했습니다.

**오류 내용:** {str(e)}

**직접 확인해보세요:**
• [MoEngage Help Center](https://help.moengage.com/hc/en-us)
• [검색 페이지](https://help.moengage.com/hc/en-us/search?query={quote(user_message)})

다시 시도하거나 다른 질문을 해보세요! 🚀"""
        
        chat_sessions[session_id].append({
            'sender': 'assistant', 
            'content': error_response
        })
        
        status_message = "❌ 검색 오류 발생 - 다시 시도해주세요"
    
    # 대화 내역이 너무 길어지면 오래된 것 삭제
    if len(chat_sessions[session_id]) > 20:
        chat_sessions[session_id] = chat_sessions[session_id][-20:]
    
    return render_template_string(HTML_TEMPLATE, 
                                messages=chat_sessions[session_id], 
                                user_input="",
                                status_message=status_message)

@app.route('/clear', methods=['POST'])
def clear():
    session_id = request.remote_addr
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return redirect(url_for('index'))

def translate_korean_to_english(korean_text):
    """한국어를 영어 검색어로 번역"""
    translation_map = {
        # 기본 용어
        'standard attribute': 'standard attribute',
        '표준 속성': 'standard attribute',
        '스탠다드 어트리뷰트': 'standard attribute',
        
        # SMS 관련
        'sms': 'sms',
        '문자': 'sms',
        '메시지': 'message',
        'sender': 'sender',
        '발신자': 'sender',
        '발송': 'send',
        
        # 푸시 알림
        '푸시': 'push',
        '알림': 'notification',
        'push': 'push notification',
        
        # 캠페인
        '캠페인': 'campaign',
        '마케팅': 'marketing',
        '생성': 'create',
        '만들기': 'create',
        '설정': 'setup configuration',
        
        # 세그먼트
        '세그먼트': 'segment',
        '사용자': 'user',
        '그룹': 'group',
        '타겟': 'target',
        
        # 일반적인 동작
        '방법': 'how to',
        '가이드': 'guide',
        '튜토리얼': 'tutorial',
        '도움말': 'help',
        '어떻게': 'how to'
    }
    
    # 텍스트 정규화
    korean_text = korean_text.lower().strip()
    english_terms = []
    
    # 직접 매핑 확인
    for korean, english in translation_map.items():
        if korean in korean_text:
            english_terms.append(english)
    
    # 매핑되지 않은 경우 원본 텍스트 사용
    if not english_terms:
        english_terms = [korean_text]
    
    return ' '.join(list(set(english_terms)))  # 중복 제거

def search_moengage_help_center(query):
    """MoEngage Help Center에서 실제 검색"""
    try:
        # 검색 URL 구성
        search_url = f"https://help.moengage.com/hc/en-us/search?query={quote(query)}"
        
        print(f"검색 URL: {search_url}")
        
        # 검색 요청
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = []
        
        # 검색 결과 추출 (다양한 선택자 시도)
        article_selectors = [
            'article.search-result',
            '.search-result-article',
            '.search-results .article',
            '.search-results a',
            '[data-search-result]'
        ]
        
        articles = []
        for selector in article_selectors:
            articles = soup.select(selector)
            if articles:
                print(f"찾은 선택자: {selector}, 결과 수: {len(articles)}")
                break
        
        if not articles:
            # 대안: 일반적인 링크 검색
            articles = soup.find_all('a', href=re.compile(r'/articles/'))
            print(f"대안 검색 결과: {len(articles)}")
        
        for article in articles[:5]:  # 상위 5개 결과만
            try:
                # 제목 추출
                title_elem = article.find('h3') or article.find('h2') or article.find('.search-result-title') or article
                title = title_elem.get_text(strip=True) if title_elem else 'No title'
                
                # URL 추출
                url = article.get('href', '')
                if url and not url.startswith('http'):
                    url = 'https://help.moengage.com' + url
                
                # 요약 추출
                summary_elem = article.find('.search-result-description') or article.find('p')
                summary = summary_elem.get_text(strip=True) if summary_elem else ''
                
                if title and url and 'No title' not in title:
                    results.append({
                        'title': title,
                        'url': url,
                        'summary': summary[:200] + '...' if len(summary) > 200 else summary
                    })
                    
            except Exception as e:
                print(f"결과 파싱 오류: {e}")
                continue
        
        print(f"최종 검색 결과: {len(results)}개")
        return results
        
    except Exception as e:
        print(f"검색 오류: {e}")
        return []

def get_article_content(url):
    """개별 문서 내용 가져오기"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 본문 내용 추출
        content_selectors = [
            '.article-body',
            '.article-content', 
            '.section-article-content',
            '#article-body',
            'main article'
        ]
        
        content = ""
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content = content_elem.get_text(strip=True)
                break
        
        return content[:1000] + '...' if len(content) > 1000 else content
        
    except Exception as e:
        print(f"문서 내용 가져오기 오류: {e}")
        return ""

def search_and_generate_response(user_message):
    """검색 및 응답 생성"""
    # 1. 한국어를 영어로 번역
    english_query = translate_korean_to_english(user_message)
    print(f"번역된 검색어: {english_query}")
    
    # 2. MoEngage Help Center 검색
    search_results = search_moengage_help_center(english_query)
    
    if not search_results:
        return f"""❌ **검색 결과 없음**

"{user_message}"에 대한 MoEngage Help Center 검색 결과를 찾지 못했습니다.

**직접 검색해보세요:**
• [MoEngage Help Center 검색](https://help.moengage.com/hc/en-us/search?query={quote(english_query)})
• [MoEngage Help Center](https://help.moengage.com/hc/en-us)

다른 키워드로 다시 검색해보시거나 더 구체적인 질문을 해주세요! 🚀"""
    
    # 3. 첫 번째 결과의 상세 내용 가져오기 (선택사항)
    detailed_content = ""
    if search_results[0]['url']:
        detailed_content = get_article_content(search_results[0]['url'])
    
    # 4. 응답 생성
    response = f"""🔍 **MoEngage Help Center 검색 결과**

**질문:** {user_message}
**검색어:** {english_query}

"""
    
    for i, result in enumerate(search_results[:3], 1):
        response += f"""**{i}. {result['title']}**
{result['summary']}
📎 [자세히 보기]({result['url']})

"""
    
    if detailed_content:
        response += f"""**📋 주요 내용 요약:**
{detailed_content}

"""
    
    response += f"""**🔗 추가 도움말:**
• [MoEngage Help Center](https://help.moengage.com/hc/en-us)
• [직접 검색하기](https://help.moengage.com/hc/en-us/search?query={quote(english_query)})

더 구체적인 질문이 있으시면 언제든 물어보세요! 🚀"""
    
    return response

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
        
        response = search_and_generate_response(user_message)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)