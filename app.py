from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
    <head><title>MoEngage Helper</title></head>
    <body>
        <h1>MoEngage Helper Bot</h1>
        <p>Hello World!</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
