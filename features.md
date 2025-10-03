# Mobile-Use 功能清单

## 核心模块

### 1. 设备控制模块 (`module/device/`)

#### `device.py` - 设备主类
整合所有设备功能的核心类。

**主要功能：**
- 连接设备
- 截图和保存截图
- 执行各种触摸操作
- 按钮检测和点击

**主要方法：**
- `screenshot()` - 截取屏幕
- `save_screenshot(path)` - 保存截图到文件
- `click(position)` - 点击指定位置
- `appear(button)` - 检测按钮是否出现
- `appear_then_click(button)` - 检测到按钮后点击

#### `connection.py` - ADB连接管理
管理与Android设备的连接。

**功能：**
- uiautomator2连接
- ADB设备连接
- 连接状态检测和重连

#### `screenshot.py` - 截图功能
提供多种截图方式，自动选择最佳方法。

**功能：**
- uiautomator2截图（主要方式）
- ADB截图（备用方案）
- 自动重试机制
- 图像格式转换

#### `control.py` - 触摸控制
实现各种触摸操作的底层控制。

**主要方法：**
- `click(x, y)` - 单击
- `long_click(x, y, duration)` - 长按
- `swipe(p1, p2, duration)` - 滑动
- `drag(p1, p2, duration)` - 拖拽
- `swipe_vector(vector, duration)` - 方向滑动

**特性：**
- 支持随机点击位置（模拟真人）
- 人性化的滑动路径
- 可配置的操作延迟

---

### 2. OCR模块 (`module/ocr/`)

#### `ocr.py` - 文字识别
基于PaddleOCR的文字识别功能。

**主要功能：**
- 中英文文字识别
- 支持指定区域OCR
- 获取文字位置信息

**主要方法：**
- `ocr(image, area=None)` - 识别图片中的所有文字
- `ocr_single_line(image, area=None)` - 识别单行文字

**OCR结果包含：**
- `rec_texts` - 识别到的文字列表
- `dt_polys` - 每个文字的位置框（4个顶点坐标）
- `rec_scores` - 识别置信度

**使用示例：**
```python
from module.ocr.ocr import OCR

# 创建OCR实例（可指定区域）
ocr = OCR(area=(100, 100, 900, 200))

# 识别整个屏幕
ocr = OCR()
text = ocr.ocr(device.image)
```

---

### 3. 基础工具 (`module/base/`)

#### `button.py` - 按钮定义
定义UI元素的位置和属性。

**Button类属性：**
- `area` - 检测区域 (x1, y1, x2, y2)
- `color` - 期望的颜色 (R, G, B)
- `button` - 点击区域
- `name` - 按钮名称

**使用示例：**
```python
from module.base.button import Button

my_button = Button(
    area=(100, 200, 300, 400),
    color=(255, 100, 100),
    button=(100, 200, 300, 400),
    name='MY_BUTTON'
)
```

#### `timer.py` - 计时器工具
提供操作延迟和超时控制。

**功能：**
- 操作间隔控制
- 超时判断
- 定时任务

#### `utils.py` - 工具函数
各种辅助函数。

**主要函数：**
- `crop(image, area)` - 裁剪图像
- `area_offset(area, offset)` - 区域偏移计算
- `random_rectangle_point(area)` - 随机生成区域内的点
- `load_image(file)` - 加载图片文件

---

### 4. 日志和异常

#### `logger.py` - 日志系统
统一的日志记录系统。

**功能：**
- 分级日志（INFO, WARNING, ERROR）
- 带时间戳的日志
- 格式化输出
- `logger.hr(title, level)` - 输出分隔线标题

#### `exception.py` - 自定义异常
项目专用异常类。

---

## 测试和演示脚本

### 5. 功能测试脚本

#### `test_browser_search.py` - 浏览器搜索测试
测试浏览器打开和搜索功能。

**测试内容：**
1. 连接设备
2. 打开浏览器
3. 输入搜索内容
4. 执行搜索
5. 截图验证

#### `test_baidu_weather.py` - 百度天气查询测试
完整的百度搜索天气流程测试。

**测试内容：**
1. 打开百度
2. 搜索"北京天气"
3. 验证搜索结果
4. 保存截图

#### `verify_adb_operations.py` - ADB操作验证
验证所有基础ADB操作是否正常。

**验证项目：**
- ✅ 设备连接
- ✅ 截图功能
- ✅ 点击操作
- ✅ 滑动操作
- ✅ 长按操作
- ✅ 拖拽操作

---

### 6. 演示脚本

#### `example_simple.py` - 简单示例
基本操作的演示代码。

**包含示例：**
- 连接设备
- 截图
- 点击
- 滑动

---

### 7. OCR工具脚本

#### `check_screen.py` - 屏幕内容OCR检查
检查当前屏幕上的所有文字。

**功能：**
1. 连接设备 (127.0.0.1:5565)
2. 截图
3. OCR识别所有文字
4. 显示识别结果

**使用方法：**
```bash
./venv/bin/python check_screen.py
```

#### `debug_ocr.py` - OCR调试工具
查看OCR返回的原始数据结构。

**功能：**
- 显示OCR结果类型
- 显示文字列表
- 显示位置信息
- 显示置信度

#### `ocr_click_demo.py` - OCR文字定位演示
演示如何找到文字并获取点击位置。

**功能：**
1. 连接设备并截图
2. 使用OCR查找指定文字（如"百度一下"）
3. 获取文字的中心点坐标
4. 返回可点击的位置

**核心函数：**
```python
def find_text_position(image, target_text):
    """
    在图片中找到指定文字的位置

    Args:
        image: 截图（numpy数组）
        target_text: 要查找的文字

    Returns:
        tuple: (center_x, center_y) 文字中心点坐标
    """
```

**使用示例：**
```python
from ocr_click_demo import find_text_position

# 截图
device.screenshot()

# 查找"百度一下"的位置
position = find_text_position(device.image, '百度一下')

if position:
    x, y = position
    device.click(x, y)  # 点击
```

---

## 主要功能对照表

| 功能类别 | 工具/模块 | 主要方法 | 使用场景 |
|---------|----------|---------|---------|
| **设备连接** | `device.py` | `Device(serial)` | 连接Android设备/模拟器 |
| **截图** | `screenshot.py` | `screenshot()`, `save_screenshot()` | 获取屏幕画面 |
| **点击** | `control.py` | `click(x, y)` | 点击按钮、输入框等 |
| **滑动** | `control.py` | `swipe(p1, p2)` | 滚动页面、切换屏幕 |
| **长按** | `control.py` | `long_click(x, y)` | 长按操作 |
| **拖拽** | `control.py` | `drag(p1, p2)` | 拖动元素 |
| **文字识别** | `ocr.py` | `ocr(image)` | 识别屏幕文字 |
| **文字定位** | `ocr_click_demo.py` | `find_text_position()` | 找到文字的点击位置 |
| **按钮检测** | `button.py` + `device.py` | `appear(button)` | 判断UI元素是否出现 |
| **图像处理** | `utils.py` | `crop()`, `load_image()` | 图像裁剪和加载 |
| **日志记录** | `logger.py` | `logger.info()`, `logger.hr()` | 记录操作日志 |

---

## 两种文字定位方法

### 方法1：模板匹配（适合固定UI）
参考 AzurLaneAutoScript 的 `template.py`，使用 OpenCV 模板匹配。

**原理：**
- 预先保存按钮/文字的图片模板
- 在屏幕截图中搜索相似区域
- 返回匹配位置和相似度

**优点：**
- 不需要OCR
- 速度快
- 适合固定UI

**缺点：**
- 需要预先准备模板图片
- UI变化时需要更新模板
- 不适合动态文字

### 方法2：OCR文字定位（适合动态文字）
使用 PaddleOCR 识别文字并获取位置。

**原理：**
1. OCR识别屏幕上所有文字
2. 在 `rec_texts` 中查找目标文字
3. 从 `dt_polys` 获取对应的位置框
4. 计算中心点坐标

**优点：**
- 适合动态内容
- 不需要模板图片
- 可以搜索任意文字

**缺点：**
- 需要OCR模型（较大）
- 识别速度较慢（首次加载）
- 依赖OCR准确度

**使用示例（推荐）：**
```python
from paddleocr import PaddleOCR
import numpy as np

# 初始化OCR
ocr = PaddleOCR(lang='ch')
result = ocr.ocr(image)

# 获取结果
page_result = result[0]
rec_texts = page_result['rec_texts']  # 文字列表
dt_polys = page_result['dt_polys']    # 位置框列表

# 查找"百度一下"
for i, text in enumerate(rec_texts):
    if '百度一下' in text:
        # 获取位置框（4个顶点）
        poly = dt_polys[i]
        # 计算中心点
        center_x = int(sum(p[0] for p in poly) / 4)
        center_y = int(sum(p[1] for p in poly) / 4)

        # 点击
        device.click(center_x, center_y)
        break
```

---

## 依赖项

### 核心依赖
- `adbutils==0.11.0` - ADB通信
- `uiautomator2==2.16.17` - Android UI自动化
- `numpy>=1.26.0` - 数组处理
- `opencv-python>=4.8.0` - 图像处理
- `Pillow>=10.0.0` - 图像操作

### OCR支持
- `paddleocr>=2.7.0` - OCR识别引擎
- `paddlepaddle>=2.5.0` - OCR后端

### 工具库
- `requests>=2.31.0` - HTTP请求
- `retry==0.9.2` - 重试机制
- `retrying==1.3.3` - 重试装饰器
- `pyyaml>=6.0` - YAML配置
- `logzero==1.7.0` - 日志工具
- `psutil>=5.9.3` - 进程工具
- `lxml>=4.9.0` - XML解析
- `imageio>=2.27.0` - 图像IO

---

## 环境配置

### Python环境
- **Python版本**: 3.12
- **虚拟环境**: `venv/`
- **包管理器**: pip

### 设备配置
- **默认模拟器地址**: `127.0.0.1:5565`
- **ADB版本**: 需要安装并配置到PATH
- **uiautomator2**: 自动安装到设备

### 安装步骤
```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 验证ADB
adb devices

# 5. 运行测试
./venv/bin/python verify_adb_operations.py
```

---

## 快速开始示例

### 示例1：连接设备并截图
```python
from module.device.device import Device

# 连接设备
device = Device(serial='127.0.0.1:5565')

# 截图
device.screenshot()

# 保存截图
device.save_screenshot('my_screenshot.png')
```

### 示例2：查找文字并点击
```python
from module.device.device import Device
from ocr_click_demo import find_text_position

# 连接设备
device = Device(serial='127.0.0.1:5565')

# 截图
device.screenshot()

# 查找"百度一下"的位置
position = find_text_position(device.image, '百度一下')

if position:
    x, y = position
    print(f'找到"百度一下"在位置: ({x}, {y})')
    device.click(x, y)
else:
    print('未找到目标文字')
```

### 示例3：使用按钮检测
```python
from module.device.device import Device
from module.base.button import Button

# 连接设备
device = Device(serial='127.0.0.1:5565')

# 定义按钮
search_button = Button(
    area=(1000, 100, 1200, 180),
    color=(66, 133, 244),  # 蓝色
    name='SEARCH_BUTTON'
)

# 检测并点击
device.screenshot()
if device.appear(search_button):
    device.click(search_button)
    print('已点击搜索按钮')
```

### 示例4：完整的OCR识别流程
```python
from module.device.device import Device
from module.ocr.ocr import OCR

# 连接设备
device = Device(serial='127.0.0.1:5565')

# 创建OCR实例
ocr = OCR()

# 截图并识别
device.screenshot()
text = ocr.ocr(device.image)

print(f'识别到的文字: {text}')
```

---

## 注意事项

1. **首次运行OCR较慢**：PaddleOCR首次运行需要下载模型文件，会比较慢，后续会快很多。

2. **截图权限**：确保模拟器/设备已授予截图权限。

3. **ADB连接**：确保ADB server正在运行，设备已连接。

4. **虚拟环境**：建议在虚拟环境中运行，避免依赖冲突。

5. **模拟器端口**：不同模拟器的端口可能不同，请根据实际情况修改。

---

## 项目结构
```
mobile-use/
├── module/                 # 核心模块
│   ├── base/              # 基础工具
│   ├── device/            # 设备控制
│   └── ocr/               # OCR识别
├── venv/                  # 虚拟环境
├── check_screen.py        # 屏幕OCR工具
├── debug_ocr.py           # OCR调试工具
├── ocr_click_demo.py      # OCR定位演示
├── test_browser_search.py # 浏览器测试
├── test_baidu_weather.py  # 天气查询测试
├── verify_adb_operations.py # 操作验证
├── example_simple.py      # 简单示例
├── requirements.txt       # 依赖列表
├── README.md             # 项目说明
└── features.md           # 本文件
```
