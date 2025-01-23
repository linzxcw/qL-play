# 麒麟投屏 (qL-play)

## 介绍
麒麟投屏是一款划时代的投屏播放器，能够将您的视频内容投射到浏览器中。它提供了一种简单而高效的方法，将本地视频分享至多个设备，包括平板和手机等不常用的终端。

## 功能特点
- **跨平台支持**：兼容多个操作系统，包括 Windows、macOS 和 Linux
- **跨终端支持**：只需终端设备具备浏览器，即可完成投屏（支持 iOS 和 Android）
- **高效传输**：支持高清流媒体传输，确保流畅播放
- **简单易用**：用户界面友好，操作简便
- **多浏览器支持**：兼容主流浏览器，如 Chrome、Firefox、Safari 和 Edge
[phone](./qL-play-wb.jpg)
## 安装方法
### 先决条件
- 确保已安装 [Macast](https://github.com/xfangfang/Macast/releases/tag/v0.7)
- 运行 Macast 主程序

### 1. 克隆仓库或下载压缩包
```bash
git clone https://github.com/linzxcw/qL-play.git
cd qL-play
```

### 2. 在 Macast 中安装 qL-web 播放器
- 右击 Macast 托盘图标，选择“设置”——“打开配置目录”
- 将 qL-play 文件夹中的 `web.py` 复制到 Macast 配置目录的 `renderer` 文件夹中
- 重启 Macast
- 重启后，右击 Macast 托盘图标，选择播放器为“qL-web Renderer”

### 3. 安装依赖（Windows 用户可以直接运行第 5 步）
```bash
pip install Flask
```

### 4. 运行程序
```bash
python qL-player-server.py
```

### 5. 运行编译好的程序
- 下载对应设备的麒麟投屏应用
- 双击运行“麒麟投屏”

## 使用方法
1. 打开浏览器并访问 [http://127.0.0.1:5005](http://127.0.0.1:5005)
2. 在手机上搜索投屏，将视频推送到“macast(xxx)”设备
3. 开始享受无缝投屏体验

## 开发计划
- [x] 完成第一版应用，支持 Windows
- [ ] 添加对 Linux 和 macOS 的支持
- [ ] 提供 Docker 镜像部署
- [ ] 增加对直播投屏的支持
- [ ] 支持自定义端口和播放器名称
- [ ] 增加手机控制投屏视频功能
- [ ] 添加 Bilibili 弹幕投屏功能
- [ ] 支持 AirPlay 和 Miracast 等镜像投屏

## 贡献
欢迎任何形式的贡献！请提交 Pull Request，或提出 Issue。  
也欢迎开发者请喝杯咖啡，您的支持是我持续更新的动力！

## 致谢
特别感谢所有为本项目提供帮助和支持的人士。  
- [Macast](https://github.com/xfangfang/Macast/releases/tag/v0.7)
- [xgplayer](https://github.com/bytedance/xgplayer)
