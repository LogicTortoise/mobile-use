# Mobile-Use: Universal Mobile Automation Framework

A general-purpose Android emulator automation framework based on AzurLaneAutoScript architecture.

## Features

- **Universal**: Supports various types of operations (click, swipe, drag, long-press)
- **Screenshot**: Multiple screenshot methods (uiautomator2, ADB)
- **OCR**: Text recognition using PaddleOCR
- **Realistic Simulation**: Random click positions, human-like swipe paths
- **Modular Design**: Clean separation of concerns (connection, control, screenshot, OCR)

## Architecture

Based on AzurLaneAutoScript design:

```
mobile-use/
├── module/
│   ├── base/           # Base abstractions
│   │   ├── button.py   # Button/UI element definition
│   │   ├── timer.py    # Timer utilities
│   │   └── utils.py    # Helper functions
│   ├── device/         # Device control
│   │   ├── connection.py  # ADB connection
│   │   ├── control.py     # Touch/swipe controls
│   │   ├── screenshot.py  # Screenshot capture
│   │   └── device.py      # Main device class
│   ├── ocr/            # OCR recognition
│   │   └── ocr.py      # PaddleOCR integration
│   ├── logger.py       # Logging
│   └── exception.py    # Custom exceptions
├── test_browser_search.py  # Browser search test
├── example_simple.py        # Simple examples
└── requirements.txt         # Dependencies
```

## Installation

1. **Create virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Make sure ADB is available**:
```bash
adb version
```

## Quick Start

### 1. Connect to Emulator

Make sure your emulator is running and accessible at `127.0.0.1:5565` (or your specific port).

```python
from module.device.device import Device

# Connect to device
device = Device(serial='127.0.0.1:5565')
```

### 2. Take Screenshots

```python
# Take a screenshot
device.screenshot()

# Save screenshot
device.save_screenshot('screenshot.png')
```

### 3. Control Operations

```python
# Click at a position
device.click((500, 500))

# Swipe
device.swipe((100, 500), (900, 500), duration=0.3)

# Long press
device.long_click((500, 500), duration=1.0)

# Drag
device.drag((100, 100), (500, 500), duration=0.5)
```

### 4. Button Detection

```python
from module.base.button import Button

# Define a button
my_button = Button(
    area=(100, 200, 300, 400),   # Detection area
    color=(255, 100, 100),        # Expected color (RGB)
    button=(100, 200, 300, 400),  # Click area
    name='MY_BUTTON'
)

# Check if button appears
if device.appear(my_button):
    device.click(my_button)
```

### 5. OCR Text Recognition

```python
from module.ocr.ocr import OCR

# Create OCR instance
ocr = OCR(area=(100, 100, 900, 200))

# Recognize text
text = ocr.ocr(device.image)
print(f'Recognized: {text}')
```

## MCP Server (AI Control) 🤖

**NEW**: Control your Android device using AI assistants like Claude Desktop!

Mobile-Use now includes a **Model Context Protocol (MCP)** server that allows AI assistants to directly control Android devices through natural language.

### What is MCP?

MCP (Model Context Protocol) is Anthropic's protocol that lets AI assistants like Claude connect to external tools. With MCP, you can tell Claude in natural language what you want to do, and it will control your Android device automatically.

### Quick Start with MCP

#### 1. Install MCP Package

```bash
pip install mcp
```

#### 2. Choose Your Mode

| Mode | Best For | Documentation |
|------|----------|---------------|
| **stdio** (Recommended) | Local single-user with Claude Desktop | [Quick Start](./MCP_QUICKSTART.md) |
| **HTTP** | Remote access, multiple clients, API integration | [HTTP Guide](./MCP_HTTP.md) |

#### 3. Test the Server

**stdio mode:**
```bash
python3 test_mcp_server.py
```

**HTTP mode:**
```bash
./start_mcp_http.sh
# Server runs on http://localhost:8000
```

#### 4. Configure Claude Desktop

**stdio mode** - Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mobile-use": {
      "command": "bash",
      "args": ["/absolute/path/to/mobile-use/start_mcp_server.sh"]
    }
  }
}
```

**HTTP mode:**

```json
{
  "mcpServers": {
    "mobile-use-http": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### Available MCP Tools

The MCP server provides 11 tools for controlling Android devices:

| Category | Tools | Description |
|----------|-------|-------------|
| **Device** | `connect_device` | Connect to Android device |
| | `get_screen_info` | Get screen dimensions |
| **Screenshot** | `screenshot` | Capture screen |
| **Interaction** | `click` | Tap at coordinates |
| | `long_click` | Long press |
| | `swipe` | Swipe gesture |
| | `drag` | Drag element |
| **OCR** | `ocr_text` | Recognize text on screen |
| | `ocr_find_text` | Find text location |
| | `ocr_click_text` | Find and click text |
| **Detection** | `check_button` | Check if button appears |

### Usage Examples

Once configured, you can control your device using natural language in Claude Desktop:

**Take a screenshot and analyze:**
```
Please take a screenshot and tell me what's on the screen
```

**Find and click text:**
```
Please find the "Settings" text and click it
```

**Automate a task:**
```
Please do the following:
1. Take a screenshot
2. Find and click "Search"
3. Swipe up from bottom to top
4. Check if there's a red button at (100, 200, 300, 400)
```

**OCR and interact:**
```
Please use OCR to find all text on screen, then click on "Confirm" if it exists
```

### MCP Documentation

- 📖 **[Quick Start Guide](./MCP_QUICKSTART.md)** - 5-minute setup
- 📕 **[Complete Documentation](./MCP_README.md)** - All tools and features
- 🌐 **[HTTP Mode Guide](./MCP_HTTP.md)** - Remote access and deployment
- ⚙️ **[Implementation Details](./MCP_IMPLEMENTATION.md)** - Technical architecture
- 📁 **[File Structure](./MCP_FILES.md)** - All MCP files explained

### MCP Features

✅ **Natural Language Control** - Tell Claude what you want, it handles the details
✅ **11 Powerful Tools** - Screenshot, click, swipe, OCR, and more
✅ **Two Modes** - stdio (local) or HTTP (remote/multi-client)
✅ **Smart OCR** - Find and click text automatically
✅ **Multi-Client Support** - HTTP mode supports multiple connections
✅ **Well Documented** - Comprehensive guides and examples

### MCP vs Direct Python API

| Feature | Direct Python API | MCP Server |
|---------|-------------------|------------|
| **Control Method** | Write Python code | Natural language |
| **Learning Curve** | Need to learn API | Just describe what you want |
| **Flexibility** | Full programmatic control | AI interprets intent |
| **Use Case** | Automation scripts | Interactive exploration |
| **Best For** | Developers | Everyone |

Both methods are supported - use whichever fits your needs!

---

## Examples

### Basic Test

```bash
python test_browser_search.py
```

This will:
1. Connect to emulator at 127.0.0.1:5565
2. Take screenshots
3. Perform various touch operations
4. Save screenshots

### Simple Examples

```bash
python example_simple.py
```

## Supported Operations

- **Click**: Single tap at a position
- **Long Click**: Press and hold
- **Swipe**: Slide from one point to another
- **Drag**: Same as swipe with longer duration
- **Swipe Vector**: Swipe with a directional vector
- **Multi-Click**: Multiple rapid clicks

## Configuration

The framework uses sensible defaults but can be customized:

- **Screenshot Interval**: Default 0.3s between screenshots
- **ADB Retry**: 3 retry attempts for failed operations
- **OCR Language**: English by default (can be changed to other languages)
- **Random Click**: Randomizes click position within button area

## Testing

The project has been designed for testing with emulator at `127.0.0.1:5565`.

To test browser search scenario:
```bash
python test_browser_search.py
```

## Design Philosophy

Following AzurLaneAutoScript's proven architecture:

1. **Modularity**: Clean separation between connection, control, screenshot, and OCR
2. **Reliability**: Retry mechanisms and fallback methods
3. **Human-like**: Random delays and positions for realistic simulation
4. **Extensibility**: Easy to add new control methods or screenshot techniques

## Dependencies

- `adbutils`: ADB communication
- `uiautomator2`: Android UI automation
- `opencv-python`: Image processing
- `paddleocr`: Text recognition
- `numpy`, `pillow`: Image manipulation

## Troubleshooting

**Device not found**:
- Make sure emulator is running
- Check ADB connection: `adb devices`
- Verify serial number matches

**Screenshot failed**:
- The framework tries multiple methods automatically
- Check device permissions

**OCR not working**:
- First OCR call may be slow (model loading)
- Check if PaddleOCR installed correctly

## License

Based on AzurLaneAutoScript architecture. Please refer to the original project for licensing details.

## Acknowledgments

This project architecture is inspired by [AzurLaneAutoScript](https://github.com/LmeSzinc/AzurLaneAutoScript), an excellent automation framework for mobile games.
