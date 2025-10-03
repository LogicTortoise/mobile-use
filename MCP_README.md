# Mobile-Use MCP Server

将Mobile-Use Android自动化工具作为MCP (Model Context Protocol) 服务器提供，使AI助手能够直接控制Android设备。

## 功能特性

MCP服务器提供以下工具：

### 设备连接
- **connect_device**: 连接到Android设备

### 截图操作
- **screenshot**: 截取设备屏幕
- **get_screen_info**: 获取屏幕尺寸信息

### 交互操作
- **click**: 点击指定坐标
- **long_click**: 长按指定坐标
- **swipe**: 滑动屏幕
- **drag**: 拖拽元素

### OCR功能
- **ocr_text**: 识别屏幕上的文字
- **ocr_find_text**: 查找指定文字的位置
- **ocr_click_text**: 通过OCR找到文字并点击

### 按钮检测
- **check_button**: 检测按钮是否出现（颜色匹配）

## 安装

### 1. 安装依赖

```bash
# 安装MCP SDK
pip install mcp

# 安装mobile-use依赖
pip install -r requirements.txt
```

### 2. 配置Claude Desktop

编辑Claude Desktop配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

添加以下配置：

```json
{
  "mcpServers": {
    "mobile-use": {
      "command": "python3",
      "args": [
        "/path/to/mobile-use/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/mobile-use"
      }
    }
  }
}
```

**注意**: 将 `/path/to/mobile-use` 替换为实际的项目路径。

### 3. 重启Claude Desktop

关闭并重新打开Claude Desktop，MCP服务器将自动启动。

## 使用示例

### 连接设备

```
请连接到设备 127.0.0.1:5565
```

### 截图和OCR

```
请截取当前屏幕，然后使用OCR识别所有文字
```

### 点击操作

```
请点击坐标 (640, 360)
```

### OCR点击

```
请在屏幕上找到"设置"并点击它
```

### 滑动操作

```
从 (500, 800) 滑动到 (500, 200)，实现向上滚动
```

### 按钮检测

```
检查区域 (100,200,300,400) 是否有红色按钮 (255,0,0)
```

## 工具详细说明

### connect_device
连接到Android设备（模拟器或真机）

**参数**:
- `serial`: 设备序列号，默认为 `127.0.0.1:5565`

**示例**:
```
connect_device(serial="127.0.0.1:5565")
```

### screenshot
截取当前屏幕

**参数**:
- `serial`: 设备序列号
- `save_path`: 可选，保存路径

**示例**:
```
screenshot(save_path="screenshot.png")
```

### click
点击屏幕坐标

**参数**:
- `x`: X坐标
- `y`: Y坐标
- `serial`: 设备序列号

**示例**:
```
click(x=640, y=360)
```

### long_click
长按屏幕坐标

**参数**:
- `x`: X坐标
- `y`: Y坐标
- `duration`: 持续时间（秒），默认1.0
- `serial`: 设备序列号

**示例**:
```
long_click(x=640, y=360, duration=2.0)
```

### swipe
滑动屏幕

**参数**:
- `start_x`, `start_y`: 起始坐标
- `end_x`, `end_y`: 结束坐标
- `duration`: 持续时间（秒），默认0.3
- `serial`: 设备序列号

**示例**:
```
swipe(start_x=500, start_y=800, end_x=500, end_y=200, duration=0.3)
```

### drag
拖拽元素

**参数**:
- `start_x`, `start_y`: 起始坐标
- `end_x`, `end_y`: 结束坐标
- `duration`: 持续时间（秒），默认0.8
- `serial`: 设备序列号

**示例**:
```
drag(start_x=300, start_y=400, end_x=700, end_y=400, duration=0.8)
```

### ocr_text
使用OCR识别屏幕文字

**参数**:
- `serial`: 设备序列号
- `area`: 可选，识别区域 "x1,y1,x2,y2"

**示例**:
```
ocr_text()
ocr_text(area="100,200,500,400")
```

### ocr_find_text
查找指定文字的位置

**参数**:
- `target_text`: 要查找的文字
- `serial`: 设备序列号

**示例**:
```
ocr_find_text(target_text="设置")
```

### ocr_click_text
通过OCR找到文字并点击

**参数**:
- `target_text`: 要点击的文字
- `serial`: 设备序列号

**示例**:
```
ocr_click_text(target_text="确定")
```

### check_button
检测按钮是否出现

**参数**:
- `area`: 检测区域 "x1,y1,x2,y2"
- `color`: 期望颜色 "R,G,B"
- `name`: 按钮名称
- `serial`: 设备序列号

**示例**:
```
check_button(area="100,200,300,400", color="255,0,0", name="START_BUTTON")
```

### get_screen_info
获取屏幕信息

**参数**:
- `serial`: 设备序列号

**示例**:
```
get_screen_info()
```

## 调试

### 查看MCP服务器日志

在Claude Desktop中：
1. 打开开发者工具（Help > Developer Tools）
2. 查看Console选项卡
3. 查找 `mobile-use` 相关的日志信息

### 直接运行MCP服务器

```bash
python3 mcp_server.py
```

服务器将以stdio模式运行，等待MCP客户端连接。

## 高级用法

### HTTP模式

MCP服务器默认使用stdio传输，也可以配置为HTTP模式：

```python
# 在 mcp_server.py 中修改
if __name__ == "__main__":
    # HTTP模式
    mcp.run(transport='sse')  # 默认在 http://127.0.0.1:8000
```

### 添加自定义工具

在 `mcp_server.py` 中添加新的工具：

```python
@mcp.tool()
def my_custom_tool(param1: str, param2: int) -> str:
    """
    自定义工具说明

    Args:
        param1: 参数1说明
        param2: 参数2说明

    Returns:
        返回值说明
    """
    # 实现你的逻辑
    return "结果"
```

## 故障排除

### 设备连接失败

确保：
1. ADB服务正在运行: `adb devices`
2. 设备已连接并授权
3. 模拟器正在运行（如果使用模拟器）

### OCR识别失败

确保PaddleOCR正确安装：
```bash
pip install paddleocr paddlepaddle
```

### MCP服务器无法启动

1. 检查Python路径是否正确
2. 检查所有依赖是否已安装
3. 查看Claude Desktop的开发者工具中的错误信息

## 相关文档

- [Model Context Protocol 官方文档](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Mobile-Use 主文档](./README.md)

## 许可证

与Mobile-Use项目相同的许可证。
