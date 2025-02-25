## 麒麟投屏推送服务端docker部署
推送服务端作用是向其他安装了麒麟投屏的设备，推送视频，这样被推送设备就不用安装Macast，推送的地址包括内网外都行！
### 1.docker compose文件部署，新建docker-compose.yml文件
```yaml
version: '3'
services:
  ql-play:
    image: qilinzhu/ql-play_server:latest
    container_name: ql-play_server
    environment:
      - Web_Server_Ip=127.0.0.1 # 装有麒麟投屏设备的ip或者域名
      - Web_Server_Port=5005
    network_mode: host
```
- 注意事项同首页，关闭或禁用upnp服务
  
将这个内容保存为 docker-compose.yml 文件后，可以使用以下命令启动容器：
```bash
docker-compose up -d
```

### 2.docker一行命令运行
```bash
docker run -d --name ql-play --network host -e Web_Server_Ip=127.0.0.1 -e Web_Server_Prot=5005 qilinzhu/ql-play:latest
```
- 记得修改正确的ip地址
