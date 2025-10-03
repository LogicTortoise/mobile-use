# Mobile-Use MCP Server - HTTP模式

## 概述

Mobile-Use MCP服务器支持两种传输模式：

1. **stdio模式** - 通过标准输入/输出通信（默认）
2. **HTTP模式** - 通过HTTP/SSE通信（本文档）

HTTP模式的优势：
- ✅ 可以通过网络访问（支持远程控制）
- ✅ 可以同时服务多个客户端
- ✅ 易于调试和监控
- ✅ 支持Web界面访问
- ✅ 可以集成到Web应用

## 快速开始

### 1. 启动HTTP服务器

```bash
# 方式1: 使用启动脚本
./start_mcp_http.sh

# 方式2: 直接运行
python3 mcp_server_http.py
```

你应该看到：
```
============================================================
Mobile-Use MCP Server (HTTP模式)
============================================================
服务器地址: http://0.0.0.0:8000
SSE端点: http://0.0.0.0:8000/sse
MCP端点: http://0.0.0.0:8000/mcp
============================================================
按Ctrl+C停止服务器
============================================================
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 2. 配置Claude Desktop

编辑配置文件：
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

添加HTTP配置：

```json
{
  "mcpServers": {
    "mobile-use-http": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### 3. 重启Claude Desktop

### 4. 验证连接

在Claude中输入：
```
请列出可用的mobile-use工具
```

## HTTP端点

服务器提供以下端点：

| 端点 | 协议 | 用途 |
|------|------|------|
| `http://localhost:8000` | HTTP | 主页面 |
| `http://localhost:8000/sse` | SSE | MCP Server-Sent Events端点 |
| `http://localhost:8000/mcp` | HTTP | MCP Streamable HTTP端点 |
| `http://localhost:8000/docs` | HTTP | API文档（Swagger UI） |
| `http://localhost:8000/openapi.json` | HTTP | OpenAPI规范 |

## 使用示例

### Web浏览器访问

打开浏览器访问 http://localhost:8000

### curl测试

```bash
# 获取服务器信息
curl http://localhost:8000

# 查看API文档
curl http://localhost:8000/openapi.json
```

### Python客户端

```python
import httpx

# 连接到MCP服务器
async with httpx.AsyncClient() as client:
    # SSE连接
    async with client.stream('GET', 'http://localhost:8000/sse') as response:
        async for line in response.aiter_lines():
            print(line)
```

## 配置选项

### 修改端口

编辑 `mcp_server_http.py`：

```python
mcp = FastMCP(
    name="mobile-use",
    host="0.0.0.0",
    port=9000,  # 修改为你想要的端口
    debug=True
)
```

### 限制访问IP

```python
mcp = FastMCP(
    name="mobile-use",
    host="127.0.0.1",  # 只允许本地访问
    port=8000,
    debug=True
)
```

### 启用HTTPS

```python
mcp = FastMCP(
    name="mobile-use",
    host="0.0.0.0",
    port=8000,
    transport_security={
        "ssl_certfile": "/path/to/cert.pem",
        "ssl_keyfile": "/path/to/key.pem"
    }
)
```

## 远程访问

### 局域网访问

1. 启动服务器（监听0.0.0.0）
2. 查找本机IP地址：
   ```bash
   # macOS/Linux
   ifconfig | grep "inet "

   # Windows
   ipconfig
   ```

3. 在其他设备上配置Claude Desktop：
   ```json
   {
     "mcpServers": {
       "mobile-use-remote": {
         "url": "http://192.168.1.100:8000/sse"
       }
     }
   }
   ```

### 公网访问（使用ngrok）

```bash
# 安装ngrok
brew install ngrok  # macOS
# 或从 https://ngrok.com 下载

# 启动隧道
ngrok http 8000

# 复制ngrok提供的URL
# 示例: https://abc123.ngrok.io
```

配置Claude Desktop：
```json
{
  "mcpServers": {
    "mobile-use-ngrok": {
      "url": "https://abc123.ngrok.io/sse"
    }
  }
}
```

## 多客户端支持

HTTP模式支持多个客户端同时连接：

```
Client 1 (Claude Desktop) ──┐
                             │
Client 2 (Web Browser)   ────┼──→  MCP Server (HTTP)  ──→  Android Device
                             │
Client 3 (Python Script) ────┘
```

**注意**: 多个客户端会共享同一个设备连接。

## 性能和安全

### 性能

- 并发连接数: 无限制（受系统资源限制）
- 延迟: ~50-200ms（比stdio模式稍高）
- 吞吐量: ~100-500请求/秒

### 安全建议

⚠️ **重要安全提示**:

1. **不要暴露在公网** - 除非使用HTTPS和认证
2. **使用防火墙** - 限制访问IP
3. **启用认证** - 对生产环境启用身份验证
4. **监控日志** - 定期检查访问日志

### 启用认证

```python
from mcp.server import FastMCP

mcp = FastMCP(
    name="mobile-use",
    host="0.0.0.0",
    port=8000,
    auth={
        "type": "bearer",
        "token": "your-secret-token-here"
    }
)
```

Claude Desktop配置：
```json
{
  "mcpServers": {
    "mobile-use-auth": {
      "url": "http://localhost:8000/sse",
      "headers": {
        "Authorization": "Bearer your-secret-token-here"
      }
    }
  }
}
```

## 监控和调试

### 查看日志

服务器日志会输出到控制台：

```
INFO:     127.0.0.1:54321 - "GET /sse HTTP/1.1" 200 OK
INFO:     Tool called: screenshot, args: {"serial": "127.0.0.1:5565"}
INFO:     Tool result: ✅ 截图成功
```

### 使用API文档

访问 http://localhost:8000/docs 查看交互式API文档（Swagger UI）。

### 健康检查

```bash
# 检查服务器是否运行
curl http://localhost:8000/health

# 预期输出: {"status": "ok"}
```

### 添加自定义健康检查端点

```python
from starlette.responses import JSONResponse
from starlette.requests import Request

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "mobile-use"})
```

## 部署

### Docker部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install mcp

COPY . .

EXPOSE 8000

CMD ["python3", "mcp_server_http.py"]
```

构建和运行：

```bash
docker build -t mobile-use-mcp .
docker run -p 8000:8000 mobile-use-mcp
```

### systemd服务

创建 `/etc/systemd/system/mobile-use-mcp.service`:

```ini
[Unit]
Description=Mobile-Use MCP Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/mobile-use
ExecStart=/path/to/mobile-use/start_mcp_http.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable mobile-use-mcp
sudo systemctl start mobile-use-mcp
sudo systemctl status mobile-use-mcp
```

### 反向代理（Nginx）

```nginx
server {
    listen 80;
    server_name mobile-use.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /sse {
        proxy_pass http://localhost:8000/sse;
        proxy_http_version 1.1;
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        chunked_transfer_encoding off;
    }
}
```

## stdio vs HTTP 对比

| 特性 | stdio模式 | HTTP模式 |
|------|-----------|----------|
| **配置复杂度** | 简单 | 中等 |
| **延迟** | 低 (~10-50ms) | 中等 (~50-200ms) |
| **多客户端** | ❌ 不支持 | ✅ 支持 |
| **远程访问** | ❌ 不支持 | ✅ 支持 |
| **调试便利** | 中等 | ✅ 易于调试 |
| **安全性** | ✅ 本地隔离 | ⚠️ 需要配置 |
| **适用场景** | 单用户本地 | 多用户/远程 |

## 故障排除

### 问题：端口被占用

```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或使用其他端口
```

### 问题：无法远程访问

1. 检查防火墙设置
2. 确保监听0.0.0.0而不是127.0.0.1
3. 检查路由器端口转发

### 问题：连接断开

SSE连接可能会超时，这是正常的。客户端会自动重连。

### 问题：性能慢

1. 检查网络延迟: `ping localhost`
2. 减少并发客户端数量
3. 考虑使用本地stdio模式

## 高级功能

### WebSocket支持

虽然MCP使用SSE，但你可以添加自定义WebSocket端点：

```python
from starlette.websockets import WebSocket

@mcp.custom_route("/ws", methods=["GET"])
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

### CORS支持

```python
from starlette.middleware.cors import CORSMiddleware

mcp.app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 示例用例

### 1. Web控制面板

创建Web页面通过HTTP端点控制设备：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Mobile-Use Control Panel</title>
</head>
<body>
    <h1>Android Device Control</h1>
    <button onclick="screenshot()">截图</button>
    <button onclick="click(640, 360)">点击中心</button>

    <script>
        async function screenshot() {
            const response = await fetch('http://localhost:8000/tools/screenshot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({serial: '127.0.0.1:5565'})
            });
            console.log(await response.json());
        }
    </script>
</body>
</html>
```

### 2. API集成

其他应用通过API调用MCP工具：

```python
import requests

# 截图
response = requests.post(
    'http://localhost:8000/tools/screenshot',
    json={'serial': '127.0.0.1:5565'}
)
print(response.json())

# OCR识别
response = requests.post(
    'http://localhost:8000/tools/ocr_text',
    json={'serial': '127.0.0.1:5565'}
)
print(response.json())
```

## 总结

HTTP模式适合以下场景：
- ✅ 需要远程访问设备
- ✅ 多个用户/应用需要访问
- ✅ 需要Web界面
- ✅ 需要API集成

对于单用户本地使用，推荐使用stdio模式（更简单、更快）。

## 相关文档

- [MCP快速入门](./MCP_QUICKSTART.md)
- [MCP完整文档](./MCP_README.md)
- [stdio模式配置](./start_mcp_server.sh)
- [HTTP模式配置](./start_mcp_http.sh)
