from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__, static_folder='static')

# 全局变量，用于存储视频 URL
video_url = ""

@app.route('/')
def index():
    return render_template('media2.html')

@app.route('/set_url', methods=['POST'])
def set_url():
    global video_url
    data = request.json
    video_url = data.get('url', '')
    return jsonify(success=True)

@app.route('/get_url')
def get_url():
    return jsonify(url=video_url)

def run_server():
    app.run(host='0.0.0.0', port=5005)

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
