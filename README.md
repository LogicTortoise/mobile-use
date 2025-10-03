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
