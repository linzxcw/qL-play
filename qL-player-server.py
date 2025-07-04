from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import time
app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")
# 全局变量，用于存储视频状态
video_state = {
    "url": "",
    "isPlaying": False,
    "currentTime": 0,
    "timestamp": 0
}
@app.route('/')
def index():
    return render_template('media2.html')
@app.route('/set_url', methods=['POST'])
def set_url():
    global video_state
    data = request.json
    video_state["url"] = data.get('url', '')
    video_state["timestamp"] = time.time()
    socketio.emit('video_state_update', video_state, broadcast=True)
    return jsonify(success=True)
@app.route('/get_url')
def get_url():
    return jsonify(url=video_state["url"])
# WebSocket事件处理
@socketio.on('connect')
def handle_connect():
    emit('video_state_update', video_state)
@socketio.on('state_update')
def handle_state_update(data):
    global video_state
    # 更新视频状态
    video_state.update(data)
    video_state["timestamp"] = time.time()
    # 广播给所有客户端，除了发送者
    emit('video_state_update', video_state, broadcast=True, include_self=False)
def run_server():
    socketio.run(app, host='0.0.0.0', port=5005, allow_unsafe_werkzeug=True)
if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.start()