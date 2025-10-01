from flask import Flask, request, jsonify
import os
import hashlib
import hmac
import json
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import time
from urllib.parse import quote

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask 앱 초기화
app = Flask(__name__)

# 환경 변수
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')
PORT = int(os.environ.get('PORT', 8000))

# Slack 클라이언트 초기화
slack_client = WebClient(token=SLACK_BOT_TOKEN)

def verify_slack_request(request):
    """슬랙 요청 검증"""
    if not SLACK_SIGNING_SECRET:
        return True  # 개발 중에는 검증 건너뛰기
    
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    if not timestamp:
        return False
    
    # 요청이 5분 이상 오래된 경우 거부
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False
    
    signature = request.headers.get('X-Slack-Signature')
    if not signature:
        return False
    
    sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    my_signature = 'v0=' + hmac.new(
        bytes(SLACK_SIGNING_SECRET, 'utf-8'),
        bytes(sig_basestring, 'utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(my_signature, signature)

def process_with_genspark(korean_message):
    """Genspark AI로 MoEngage 질문 처리"""
    
    # 현재는 시뮬레이션 응답 (실제로는 Genspark API 호출)
    prompt = f"""
    사용자가 MoEngage에 대해 다음과 같이 질문했습니다:
    "{korean_message}"
    
    다음 작업을 수행해주세요:
    1. 이 질문을 영어로 변환하여 MoEngage Help Center에서 검색
    2. 검색 결과를 한국어로 번역하여 사용자가 이해하기 쉽게 설명
    3. 관련 링크가 있다면 제공
    
    MoEngage는 모바일 마케팅 자동화 플랫폼입니다.
    """
    
    # 시뮬레이션 응답 (실제로는 Genspark API 호출 결과)
    response = {
        'korean_question': korean_message,
        'english_query': translate_to_english(korean_message),
        'search_results': search_moengage_help(korean_message),
        'korean_answer': f"'{korean_message}'에 대한 답변을 MoEngage Help Center에서 찾았습니다.",
        'related_links': [
            'https://help.moengage.com/hc/en-us/articles/...',
            'https://help.moengage.com/hc/en-us/sections/...'
        ]
    }
    
    return response

def translate_to_english(korean_text):
    """한국어를 영어로 변환 (시뮬레이션)"""
    # 실제로는 Genspark AI 번역 호출
    translations = {
        "푸시 알림": "push notification",
        "캠페인": "campaign", 
        "설정": "setup",
        "만들기": "create",
        "방법": "how to"
    }
    
    english_query = korean_text
    for korean, english in translations.items():
        english_query = english_query.replace(korean, english)
    
    return f"How to {english_query} in MoEngage"

def search_moengage_help(query):
    """MoEngage Help Center 검색 시뮬레이션"""
    return [
        {
            'title': 'Push Notification Setup Guide',
            'url': 'https://help.moengage.com/hc/en-us/articles/push-setup',
            'summary': 'MoEngage에서 푸시 알림을 설정하는 방법에 대한 상세 가이드입니다.'
        },
        {
            'title': 'Campaign Creation Tutorial', 
            'url': 'https://help.moengage.com/hc/en-us/articles/campaign-tutorial',
            'summary': '효과적인 마케팅 캠페인을 만드는 단계별 튜토리얼입니다.'
        }
    ]

def create_slack_response(genspark_result):
    """슬랙 응답 메시지 생성"""
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🤖 MoEngage Helper Bot"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*📝 질문:* {genspark_result['korean_question']}"
            }
        },
        {
            "type": "section", 
            "text": {
                "type": "mrkdwn",
                "text": f"*🔍 영어 검색어:* {genspark_result['english_query']}"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn", 
                "text": f"*💡 답변:*\n{genspark_result['korean_answer']}"
            }
        }
    ]
    
    # 검색 결과 추가
    if genspark_result['search_results']:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*🔗 관련 자료:*"
            }
        })
        
        for result in genspark_result['search_results']:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"• <{result['url']}|{result['title']}>\n  {result['summary']}"
                }
            })
    
    return {"blocks": blocks}

@app.route('/', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({
        'status': 'healthy',
        'message': 'MoEngage Genspark Bot is running!',
        'version': '1.0.0'
    })

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """슬랙 이벤트 처리"""
    
    # 요청 검증
    if not verify_slack_request(request):
        return jsonify({'error': 'Invalid request'}), 400
    
    data = request.json
    
    # URL 검증 요청 처리
    if data.get('type') == 'url_verification':
        return jsonify({'challenge': data.get('challenge')})
    
    # 이벤트 처리
    if data.get('type') == 'event_callback':
        event = data.get('event', {})
        
        # 리액션 추가 이벤트
        if event.get('type') == 'reaction_added':
            if event.get('reaction') == 'mag':  # 🔍 돋보기 이모티콘
                handle_search_reaction(event)
        
        # 멘션 이벤트  
        elif event.get('type') == 'app_mention':
            handle_mention(event)
    
    return jsonify({'status': 'ok'})

def handle_search_reaction(event):
    """🔍 리액션 처리"""
    try:
        channel = event['item']['channel']
        timestamp = event['item']['ts']
        
        # 원본 메시지 가져오기
        result = slack_client.conversations_history(
            channel=channel,
            latest=timestamp,
            inclusive=True,
            limit=1
        )
        
        if result['messages']:
            original_message = result['messages'][0]['text']
            
            # 진행 메시지 전송
            slack_client.chat_postMessage(
                channel=channel,
                text="🔍 MoEngage Help Center에서 검색 중입니다... 잠시만 기다려주세요!",
                thread_ts=timestamp
            )
            
            # Genspark로 처리
            genspark_result = process_with_genspark(original_message)
            
            # 결과 메시지 전송
            response_message = create_slack_response(genspark_result)
            slack_client.chat_postMessage(
                channel=channel,
                thread_ts=timestamp,
                **response_message
            )
            
    except SlackApiError as e:
        logger.error(f"Slack API 오류: {e}")
    except Exception as e:
        logger.error(f"리액션 처리 오류: {e}")

def handle_mention(event):
    """봇 멘션 처리"""
    try:
        channel = event['channel']
        text = event['text']
        timestamp = event['ts']
        
        # 멘션 제거하고 질문만 추출
        question = text.split('>', 1)[1].strip() if '>' in text else text
        
        if question:
            # Genspark로 처리
            genspark_result = process_with_genspark(question)
            
            # 응답 전송
            response_message = create_slack_response(genspark_result)
            slack_client.chat_postMessage(
                channel=channel,
                thread_ts=timestamp,
                **response_message
            )
        else:
            slack_client.chat_postMessage(
                channel=channel,
                thread_ts=timestamp,
                text="안녕하세요! 🤖 MoEngage에 대해 질문하시면 도움을 드릴게요!\n\n사용법: 질문에 🔍 이모티콘을 추가하거나 @MoEngage Helper를 멘션해주세요."
            )
            
    except SlackApiError as e:
        logger.error(f"Slack API 오류: {e}")
    except Exception as e:
        logger.error(f"멘션 처리 오류: {e}")

if __name__ == '__main__':
    if not SLACK_BOT_TOKEN:
        logger.error("SLACK_BOT_TOKEN 환경변수가 설정되지 않았습니다!")
        exit(1)
    
    logger.info(f"MoEngage Genspark Bot 시작 - 포트: {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)