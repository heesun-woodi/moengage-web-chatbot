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
    <title>MoEngage Helper</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Apple SD Gothic Neo', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; justify-content: center; align-items: center;
        }
        .container {
            background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%; max-width: 600px; height: 70vh; display: flex; flex-direction: column;
        }
        .header {
            background: linear-gradient(135deg, #4CAF50, #45a049); color: white;
            padding: 20px; text-align: center; border-radius: 20px 20px 0 0;
        }
        .header h1 { font-size: 1.5em; margin-bottom: 5px; }
        .messages { flex: 1; padding: 20px; overflow-y: auto; background: #f8f9fa; }
        .message { margin-bottom: 15px; padding: 10px 15px; border-radius: 15px; max-width: 80%; }
        .bot-message { background: #e3f2fd; align-self: flex-start; }
        .user-message { background: #4CAF50; color: white; align-self: flex-end; margin-left: auto; }
        .input-area { padding: 15px; background: white; border-radius: 0 0 20px 20px; }
        .input-container { display: flex; gap: 10px; }
        #messageInput {
            flex: 1; padding: 10px 15px; border: 2px solid #ddd; border-radius: 25px;
            outline: none; font-size: 14px;
        }
        #messageInput:focus { border-color: #4CAF50; }
        #sendButton {
            padding: 10px 20px; background: #4CAF50; color: white; border: none;
            border-radius: 25px; cursor: pointer; font-size: 14px;
        }
        #sendButton:hover { background: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-robot"></i> MoEngage Helper</h1>
            <p>MoEngage에 대해 궁금한 점을 물어보세요!</p>
        </div>
        <div class="messages" id="messages">
            <div class="message bot-message">
                안녕하세요! MoEngage Helper입니다. 🤖<br>
                MoEngage에 대한 질문을 입력해주세요!
            </div>
        </div>
        <div class="input-area">
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="질문을 입력하세요..." maxlength="200">
                <button id="sendButton" onclick="sendMessage()">전송</button>
            </div>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            input.value = '';
            
            // 시뮬레이션 응답
            setTimeout(() => {
                const response = "'" + message + "'에 대한 답변을 준비중입니다. 곧 MoEngage 전문 답변을 제공해드릴게요!";
                addMessage(response, 'bot');
            }, 1000);
        }
        
        function addMessage(text, sender) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender + '-message';
            messageDiv.textContent = text;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
