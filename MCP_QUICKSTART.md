# Mobile-Use MCP Server 快速入门

## 什么是MCP？

Model Context Protocol (MCP) 是Anthropic开发的协议，允许AI助手（如Claude）连接到外部工具和数据源。通过MCP，Claude可以直接控制你的Android设备！

## 传输模式选择

MCP服务器支持两种传输模式：

| 模式 | 优势 | 适用场景 |
|------|------|----------|
| **stdio** | 简单、低延迟、安全 | 单用户本地使用（推荐） |
| **HTTP** | 支持远程、多客户端、易调试 | 远程访问、多用户 |

**推荐**: 如果你只是在本地使用Claude Desktop，选择stdio模式。
**高级**: 如果需要远程访问或多客户端，选择HTTP模式（参见[HTTP模式文档](./MCP_HTTP.md)）。

---

## 5分钟快速开始（stdio模式）

### 1. 安装依赖

```bash
cd /path/to/mobile-use

# 安装MCP SDK
pip install mcp

# 安装项目依赖（如果还没安装）
pip install -r requirements.txt
```

### 2. 测试MCP服务器

```bash
# 测试服务器是否正常工作
python3 test_mcp_server.py
```

你应该看到：
```
✅ 成功注册 11 个工具:
1. connect_device
2. screenshot
3. click
...
```

### 3. 配置Claude Desktop

找到Claude Desktop的配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

编辑配置文件，添加mobile-use服务器：

```json
{
  "mcpServers": {
    "mobile-use": {
      "command": "bash",
      "args": [
        "/绝对路径/to/mobile-use/start_mcp_server.sh"
      ]
    }
  }
}
```

**重要**: 将 `/绝对路径/to/mobile-use` 替换为实际路径！

### 4. 重启Claude Desktop

完全关闭并重新打开Claude Desktop。

### 5. 验证连接

在Claude Desktop中输入：

```
请列出可用的MCP工具
```

你应该看到mobile-use的所有工具列表。

## 第一次使用

### 连接设备

```
请连接到我的Android设备（127.0.0.1:5565）
```

### 截图

```
请截取当前屏幕
```

### OCR识别

```
请识别当前屏幕上的所有文字
```

### 点击文字

```
请找到"设置"文字并点击它
```

### 执行操作序列

```
请执行以下操作：
1. 截取屏幕
2. 识别所有文字
3. 如果看到"确定"按钮，点击它
4. 向上滑动 (从y=800到y=200)
```

## 可用工具列表

| 工具 | 功能 | 示例 |
|------|------|------|
| `connect_device` | 连接设备 | 连接到127.0.0.1:5565 |
| `screenshot` | 截图 | 截取屏幕并保存 |
| `click` | 点击坐标 | 点击(640, 360) |
| `long_click` | 长按 | 长按(640, 360)持续2秒 |
| `swipe` | 滑动 | 从(500,800)滑到(500,200) |
| `drag` | 拖拽 | 从A点拖到B点 |
| `ocr_text` | OCR识别 | 识别屏幕文字 |
| `ocr_find_text` | 查找文字位置 | 查找"设置"的位置 |
| `ocr_click_text` | OCR点击 | 找到"确定"并点击 |
| `check_button` | 检测按钮 | 检测红色按钮是否出现 |
| `get_screen_info` | 屏幕信息 | 获取屏幕尺寸 |

## 高级用法示例

### 自动化任务

```
请帮我执行以下自动化任务：

1. 打开设置应用（通过OCR找到"设置"并点击）
2. 向下滚动3次
3. 找到"关于手机"并点击
4. 截图保存为about.png
```

### 游戏自动化

```
请监控游戏屏幕：

1. 每秒截图一次
2. 使用OCR检测是否出现"领取奖励"文字
3. 如果出现，立即点击
4. 重复10次
```

### UI测试

```
请验证登录功能：

1. 检测区域(100,200,300,400)是否有蓝色按钮
2. 如果有，点击该按钮
3. 等待3秒
4. 检查是否出现"登录成功"文字
5. 截图保存测试结果
```

## 故障排除

### 问题：Claude无法看到mobile-use工具

**解决方案**:
1. 检查配置文件路径是否正确
2. 确保路径是绝对路径（不是相对路径）
3. 检查Claude Desktop开发者工具（Help > Developer Tools）中的错误信息
4. 完全重启Claude Desktop

### 问题：工具调用失败

**解决方案**:
1. 确保ADB设备已连接: `adb devices`
2. 确保模拟器正在运行
3. 检查设备序列号是否正确（默认为127.0.0.1:5565）

### 问题：OCR识别不准确

**解决方案**:
1. 确保PaddleOCR已安装: `pip install paddleocr`
2. 尝试使用`area`参数限制识别区域
3. 确保文字清晰可见

## 开发者信息

### 添加自定义工具

编辑 `mcp_server.py`，添加新的工具：

```python
@mcp.tool()
def my_tool(param1: str, param2: int = 10) -> str:
    """
    我的自定义工具

    Args:
        param1: 参数1说明
        param2: 参数2说明，默认10

    Returns:
        返回值说明
    """
    try:
        # 你的逻辑
        result = f"处理: {param1}, {param2}"
        return f"✅ {result}"
    except Exception as e:
        return f"❌ 失败: {str(e)}"
```

保存后重启Claude Desktop即可使用新工具。

### 查看日志

MCP服务器的日志会在Claude Desktop的开发者工具中显示。

打开方式: Help > Developer Tools > Console

## 示例会话

```
用户: 请帮我自动化填写表单

Claude: 好的，我来帮你。首先让我看看屏幕上有什么。

[调用 screenshot 工具]
[调用 ocr_text 工具]

Claude: 我看到了一个包含以下字段的表单：
- "姓名"输入框
- "邮箱"输入框
- "提交"按钮

您想如何填写这些字段？

用户: 姓名填"张三"，邮箱填"test@example.com"

Claude: 好的，我来操作：

[调用 ocr_find_text 查找"姓名"]
[调用 click 点击姓名输入框]
[提示] 请在设备上手动输入"张三"

[调用 ocr_find_text 查找"邮箱"]
[调用 click 点击邮箱输入框]
[提示] 请在设备上手动输入"test@example.com"

[调用 ocr_click_text 点击"提交"按钮]

Claude: ✅ 表单填写完成并已提交！
```

## 安全提示

⚠️ **重要安全提示**:

1. MCP服务器可以完全控制你的Android设备
2. 只在信任的设备上运行
3. 不要在生产环境使用未经测试的自动化脚本
4. 建议在模拟器上先测试所有操作

## HTTP模式（高级用户）

如果需要通过HTTP访问MCP服务器（支持远程访问和多客户端）：

📖 **[HTTP模式完整文档](./MCP_HTTP.md)**

快速启动：
```bash
./start_mcp_http.sh
# 服务器将运行在 http://localhost:8000
```

Claude Desktop配置（HTTP模式）：
```json
{
  "mcpServers": {
    "mobile-use-http": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## 更多资源

- [MCP完整文档](./MCP_README.md)
- **[HTTP模式文档](./MCP_HTTP.md)** ⭐ 新增
- [Mobile-Use主文档](./README.md)
- [测试用例](./test/)
- [MCP官方网站](https://modelcontextprotocol.io)

## 获得帮助

遇到问题？

1. 查看[MCP_README.md](./MCP_README.md)的故障排除部分
2. 运行测试: `python3 test_mcp_server.py`
3. 检查日志: Claude Desktop开发者工具
4. 提交issue到项目仓库

---

**享受AI驱动的Android自动化！** 🚀
