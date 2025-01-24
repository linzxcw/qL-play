import sys
import webbrowser
import os
import winreg
import threading
import subprocess
import logging
from datetime import datetime, timedelta
from pystray import Icon, Menu, MenuItem
from PIL import Image
from flask import Flask, render_template, request, jsonify
from logging.handlers import RotatingFileHandler

# 设置日志记录
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=1)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.DEBUG)

app = Flask(__name__, static_folder='static')

app.logger.addHandler(log_handler)
app.logger.setLevel(logging.DEBUG)

# Flask 日志配置
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)  # 设置为ERROR级别，禁用GET请求日志记录
werkzeug_logger.addHandler(log_handler)

# 禁用Flask开头的banner
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

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
    try:
        app.logger.info("Starting Flask server")
        app.run(host='0.0.0.0', port=5005)
    except Exception as e:
        app.logger.error("Error running server", exc_info=True)

# 创建托盘图标
def create_image(icon_path):
    try:
        return Image.open(icon_path)
    except Exception as e:
        app.logger.error("Error creating image", exc_info=True)
        return None

# 打开网页
def open_web():
    try:
        webbrowser.open('http://127.0.0.1:5005')
    except Exception as e:
        app.logger.error("Error opening web page", exc_info=True)

# 重启程序
def restart_program(icon, item):
    try:
        app.logger.info("Restarting program")
        icon.stop()
        close_loggers()
        python = sys.executable
        subprocess.Popen([python] + sys.argv)
        os._exit(0)
    except Exception as e:
        app.logger.error("Error restarting program", exc_info=True)

# 退出程序
def quit_program(icon, item):
    try:
        app.logger.info("Quitting program")
        icon.stop()
        close_loggers()
        os._exit(0)
    except Exception as e:
        app.logger.error("Error quitting program", exc_info=True)
        raise e

# 关闭所有日志记录器
def close_loggers():
    app.logger.info("Closing loggers")
    for handler in app.logger.handlers:
        handler.close()
        app.logger.removeHandler(handler)

    for handler in werkzeug_logger.handlers:
        handler.close()
        werkzeug_logger.removeHandler(handler)

# 设置开机自启动
def set_startup(enable):
    try:
        app.logger.info("Setting startup to %s", enable)
        key = winreg.HKEY_CURRENT_USER
        key_value = (
            r'Software\Microsoft\Windows\CurrentVersion\Run'
        )
        key_name = '麒麟投屏'
        exe_path = os.path.abspath(sys.argv[0])

        with winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS) as reg_key:
            if enable:
                winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(reg_key, key_name)
                except FileNotFoundError:
                    pass
    except Exception as e:
        app.logger.error("Error setting startup", exc_info=True)

# 检查开机自启动状态
def is_startup_enabled():
    try:
        app.logger.info("Checking if startup is enabled")
        key = winreg.HKEY_CURRENT_USER
        key_value = (
            r'Software\Microsoft\Windows\CurrentVersion\Run'
        )
        key_name = '麒麟投屏'

        with winreg.OpenKey(key, key_value, 0, winreg.KEY_READ) as reg_key:
            winreg.QueryValueEx(reg_key, key_name)
            return True
    except FileNotFoundError:
        return False
    except Exception as e:
        app.logger.error("Error checking startup status", exc_info=True)
        return False

# 创建托盘菜单
def create_menu():
    return Menu(
        MenuItem('打开麒麟投屏', open_web),
        MenuItem('重启', restart_program),
        MenuItem('退出', quit_program),
        MenuItem('开机自启动', on_clicked_startup, checked=lambda item: is_startup_enabled())
    )

def on_clicked_startup(icon, item):
    set_startup(not item.checked)

def delete_logs():
    try:
        app.logger.info("Deleting old log files")
        log_dir = os.path.dirname(os.path.abspath('app.log'))
        now = datetime.now()
        cutoff = now - timedelta(days=3)
        
        for log_file in os.listdir(log_dir):
            if log_file.startswith('app.log'):
                log_path = os.path.join(log_dir, log_file)
                if os.path.isfile(log_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(log_path))
                    if file_time < cutoff:
                        os.remove(log_path)
                        app.logger.info("Deleted log file: %s", log_path)
    except Exception as e:
        app.logger.error("Error deleting log files", exc_info=True)
    
    threading.Timer(259200, delete_logs).start()  # 259200 秒 = 3 天

if __name__ == '__main__':
    app.logger.info("程序启动")

    # 启动 Flask 服务器线程
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # 启动日志删除线程
    delete_logs()

    # 使用你指定的图标文件路径
    icon_path = os.path.join(app.static_folder, 'qltp-logo.ico')

    # 创建托盘图标并运行
    icon = Icon('麒麟投屏v1.0', create_image(icon_path), '麒麟投屏v1.0', create_menu())
    icon.run()
