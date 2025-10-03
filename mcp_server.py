#!/usr/bin/env python3
"""
Mobile-Use MCP Server
提供Android设备自动化操作的MCP工具
"""

from mcp.server import FastMCP
from typing import Optional, Any
import base64

# 创建MCP服务器
mcp = FastMCP(
    name="mobile-use",
    instructions="Android设备自动化操作工具集，支持截图、点击、滑动、OCR等功能"
)

# 全局设备实例
_device: Optional[Any] = None


def get_device(serial: str = '127.0.0.1:5565') -> Any:
    """获取或创建设备实例（延迟导入）"""
    global _device
    if _device is None or _device.serial != serial:
        # 延迟导入，避免启动时的依赖问题
        from module.device.device import Device
        _device = Device(serial=serial)
    return _device


@mcp.tool()
def connect_device(serial: str = '127.0.0.1:5565') -> str:
    """
    连接到Android设备

    Args:
        serial: 设备序列号，默认为127.0.0.1:5565（模拟器）

    Returns:
        连接状态信息
    """
    try:
        device = get_device(serial)
        return f"✅ 成功连接到设备: {serial}"
    except Exception as e:
        return f"❌ 连接设备失败: {str(e)}"


@mcp.tool()
def screenshot(serial: str = '127.0.0.1:5565', save_path: Optional[str] = None) -> str:
    """
    截取设备屏幕

    Args:
        serial: 设备序列号
        save_path: 可选的保存路径，如果提供则保存截图到该路径

    Returns:
        截图信息和base64编码的图像数据
    """
    try:
        import cv2  # 延迟导入
        device = get_device(serial)
        device.screenshot()

        if device.image is None:
            return "❌ 截图失败"

        h, w = device.image.shape[:2]

        # 如果提供了保存路径，保存截图
        if save_path:
            device.save_screenshot(save_path)

        # 将图像编码为base64
        _, buffer = cv2.imencode('.png', device.image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return f"✅ 截图成功\n尺寸: {w}x{h}\n" + (f"已保存到: {save_path}\n" if save_path else "") + f"Base64数据: {img_base64[:100]}..."
    except Exception as e:
        return f"❌ 截图失败: {str(e)}"


@mcp.tool()
def click(x: int, y: int, serial: str = '127.0.0.1:5565') -> str:
    """
    点击屏幕指定坐标

    Args:
        x: X坐标
        y: Y坐标
        serial: 设备序列号

    Returns:
        操作结果
    """
    try:
        device = get_device(serial)
        device.click(x, y)
        return f"✅ 已点击坐标: ({x}, {y})"
    except Exception as e:
        return f"❌ 点击失败: {str(e)}"


@mcp.tool()
def long_click(x: int, y: int, duration: float = 1.0, serial: str = '127.0.0.1:5565') -> str:
    """
    长按屏幕指定坐标

    Args:
        x: X坐标
        y: Y坐标
        duration: 长按持续时间（秒），默认1.0秒
        serial: 设备序列号

    Returns:
        操作结果
    """
    try:
        device = get_device(serial)
        device.long_click((x, y), duration=duration)
        return f"✅ 已长按坐标: ({x}, {y})，持续{duration}秒"
    except Exception as e:
        return f"❌ 长按失败: {str(e)}"


@mcp.tool()
def swipe(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.3, serial: str = '127.0.0.1:5565') -> str:
    """
    滑动屏幕

    Args:
        start_x: 起始X坐标
        start_y: 起始Y坐标
        end_x: 结束X坐标
        end_y: 结束Y坐标
        duration: 滑动持续时间（秒），默认0.3秒
        serial: 设备序列号

    Returns:
        操作结果
    """
    try:
        device = get_device(serial)
        device.swipe((start_x, start_y), (end_x, end_y), duration=duration)
        return f"✅ 已滑动: ({start_x}, {start_y}) -> ({end_x}, {end_y})"
    except Exception as e:
        return f"❌ 滑动失败: {str(e)}"


@mcp.tool()
def drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.8, serial: str = '127.0.0.1:5565') -> str:
    """
    拖拽屏幕元素

    Args:
        start_x: 起始X坐标
        start_y: 起始Y坐标
        end_x: 结束X坐标
        end_y: 结束Y坐标
        duration: 拖拽持续时间（秒），默认0.8秒
        serial: 设备序列号

    Returns:
        操作结果
    """
    try:
        device = get_device(serial)
        device.drag((start_x, start_y), (end_x, end_y), duration=duration)
        return f"✅ 已拖拽: ({start_x}, {start_y}) -> ({end_x}, {end_y})"
    except Exception as e:
        return f"❌ 拖拽失败: {str(e)}"


@mcp.tool()
def ocr_text(serial: str = '127.0.0.1:5565', area: Optional[str] = None) -> str:
    """
    使用OCR识别屏幕上的文字

    Args:
        serial: 设备序列号
        area: 可选的识别区域，格式为"x1,y1,x2,y2"（例如："100,200,500,400"）

    Returns:
        识别到的文字内容
    """
    try:
        device = get_device(serial)
        device.screenshot()

        from module.ocr.ocr import OCR

        # 解析area参数
        ocr_area = None
        if area:
            coords = [int(x.strip()) for x in area.split(',')]
            if len(coords) == 4:
                ocr_area = tuple(coords)

        ocr = OCR(area=ocr_area)
        text = ocr.ocr(device.image)

        return f"✅ OCR识别结果:\n{text}"
    except Exception as e:
        return f"❌ OCR识别失败: {str(e)}"


@mcp.tool()
def ocr_find_text(target_text: str, serial: str = '127.0.0.1:5565') -> str:
    """
    在屏幕上查找指定文字的位置

    Args:
        target_text: 要查找的文字
        serial: 设备序列号

    Returns:
        文字位置信息（中心坐标和边界框）
    """
    try:
        device = get_device(serial)
        device.screenshot()

        from paddleocr import PaddleOCR
        import numpy as np

        ocr_model = PaddleOCR(lang='ch', show_log=False)
        result = ocr_model.ocr(device.image)

        if not result or len(result) == 0:
            return f"❌ 未在屏幕上找到任何文字"

        page_result = result[0]

        if isinstance(page_result, dict):
            rec_texts = page_result.get('rec_texts', [])
            dt_polys = page_result.get('dt_polys', [])

            for i, text in enumerate(rec_texts):
                if target_text in text or text in target_text:
                    poly = dt_polys[i]
                    center_x = int(np.mean([p[0] for p in poly]))
                    center_y = int(np.mean([p[1] for p in poly]))
                    return f"✅ 找到文字 '{target_text}'\n中心位置: ({center_x}, {center_y})\n边界框: {poly}"

        return f"❌ 未找到文字: '{target_text}'"
    except Exception as e:
        return f"❌ 查找文字失败: {str(e)}"


@mcp.tool()
def ocr_click_text(target_text: str, serial: str = '127.0.0.1:5565') -> str:
    """
    通过OCR找到指定文字并点击

    Args:
        target_text: 要点击的文字
        serial: 设备序列号

    Returns:
        操作结果
    """
    try:
        device = get_device(serial)
        device.screenshot()

        from paddleocr import PaddleOCR
        import numpy as np

        ocr_model = PaddleOCR(lang='ch', show_log=False)
        result = ocr_model.ocr(device.image)

        if not result or len(result) == 0:
            return f"❌ 未在屏幕上找到任何文字"

        page_result = result[0]

        if isinstance(page_result, dict):
            rec_texts = page_result.get('rec_texts', [])
            dt_polys = page_result.get('dt_polys', [])

            for i, text in enumerate(rec_texts):
                if target_text in text or text in target_text:
                    poly = dt_polys[i]
                    center_x = int(np.mean([p[0] for p in poly]))
                    center_y = int(np.mean([p[1] for p in poly]))

                    # 点击文字中心
                    device.click(center_x, center_y)
                    return f"✅ 已点击文字 '{target_text}'\n位置: ({center_x}, {center_y})"

        return f"❌ 未找到文字: '{target_text}'"
    except Exception as e:
        return f"❌ OCR点击失败: {str(e)}"


@mcp.tool()
def check_button(
    area: str,
    color: str,
    name: str = "BUTTON",
    serial: str = '127.0.0.1:5565'
) -> str:
    """
    检测指定区域的按钮是否出现（通过颜色匹配）

    Args:
        area: 检测区域，格式为"x1,y1,x2,y2"（例如："100,200,300,400"）
        color: 期望的颜色，格式为"R,G,B"（例如："255,0,0"表示红色）
        name: 按钮名称，用于标识
        serial: 设备序列号

    Returns:
        检测结果
    """
    try:
        from module.base.button import Button  # 延迟导入
        device = get_device(serial)
        device.screenshot()

        # 解析area
        coords = [int(x.strip()) for x in area.split(',')]
        if len(coords) != 4:
            return "❌ area格式错误，应为'x1,y1,x2,y2'"
        button_area = tuple(coords)

        # 解析color
        rgb = [int(x.strip()) for x in color.split(',')]
        if len(rgb) != 3:
            return "❌ color格式错误，应为'R,G,B'"
        button_color = tuple(rgb)

        # 创建按钮并检测
        button = Button(area=button_area, color=button_color, name=name)
        appears = device.appear(button)

        if appears:
            return f"✅ 按钮 '{name}' 已出现\n区域: {button_area}\n颜色: RGB{button_color}"
        else:
            return f"❌ 按钮 '{name}' 未出现"
    except Exception as e:
        return f"❌ 检测按钮失败: {str(e)}"


@mcp.tool()
def get_screen_info(serial: str = '127.0.0.1:5565') -> str:
    """
    获取设备屏幕信息

    Args:
        serial: 设备序列号

    Returns:
        屏幕尺寸等信息
    """
    try:
        device = get_device(serial)
        device.screenshot()

        if device.image is None:
            return "❌ 无法获取屏幕信息"

        h, w = device.image.shape[:2]
        return f"✅ 屏幕信息:\n宽度: {w}px\n高度: {h}px"
    except Exception as e:
        return f"❌ 获取屏幕信息失败: {str(e)}"


if __name__ == "__main__":
    # 运行MCP服务器
    mcp.run()
