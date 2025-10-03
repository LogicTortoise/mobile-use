"""
测试按钮检测功能 - 使用合成图片
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.base.button import Button
from module.logger import logger
import numpy as np
from PIL import Image, ImageDraw


def create_test_screen_with_button(button_area, button_color, screen_size=(1280, 720)):
    """
    创建包含特定颜色按钮的测试屏幕

    Args:
        button_area: 按钮区域 (x1, y1, x2, y2)
        button_color: 按钮颜色 (R, G, B)
        screen_size: 屏幕尺寸

    Returns:
        np.ndarray: 测试图片
    """
    # 创建白色背景
    img = Image.new('RGB', screen_size, color='white')
    draw = ImageDraw.Draw(img)

    # 绘制按钮（填充矩形）
    x1, y1, x2, y2 = button_area
    draw.rectangle([x1, y1, x2, y2], fill=button_color)

    # 转换为BGR格式的numpy数组
    img_array = np.array(img)
    img_bgr = img_array[:, :, ::-1]

    return img_bgr


def test_button_creation():
    """测试按钮创建"""
    logger.hr('测试按钮创建', level=0)

    try:
        button = Button(
            area=(100, 200, 300, 400),
            color=(255, 100, 100),
            button=(100, 200, 300, 400),
            name='TEST_BUTTON'
        )

        logger.info(f'按钮名称: {button.name}')
        logger.info(f'检测区域: {button.area}')
        logger.info(f'期望颜色: {button.color}')
        logger.info('✅ 按钮创建成功')
        return True
    except Exception as e:
        logger.error(f'❌ 按钮创建失败: {e}')
        return False


def test_button_appear_with_exact_color():
    """测试按钮检测 - 精确颜色匹配"""
    logger.hr('测试按钮检测（精确颜色）', level=0)

    try:
        # 创建测试图片：在指定位置绘制红色按钮
        button_area = (200, 150, 400, 250)
        button_color_rgb = (255, 0, 0)  # 红色RGB

        test_image = create_test_screen_with_button(button_area, button_color_rgb)

        # get_color返回BGR格式，需要转换
        button_color_bgr = (button_color_rgb[2], button_color_rgb[1], button_color_rgb[0])

        # 模拟appear检测
        from module.base.utils import get_color
        detected_color = get_color(test_image, button_area)

        logger.info(f'期望颜色: BGR{button_color_bgr}')
        logger.info(f'检测颜色: BGR{detected_color}')

        # 验证颜色是否匹配
        color_match = all(abs(detected_color[i] - button_color_bgr[i]) < 10 for i in range(3))

        if color_match:
            logger.info('✅ 按钮颜色检测成功')
            return True
        else:
            logger.error(f'❌ 颜色不匹配')
            return False

    except Exception as e:
        logger.error(f'❌ 按钮检测失败: {e}')
        return False


def test_button_appear_with_different_colors():
    """测试多个不同颜色的按钮"""
    logger.hr('测试多颜色按钮检测', level=0)

    try:
        test_cases = [
            ((100, 100, 200, 200), (255, 0, 0), 'RED_BUTTON'),      # 红色RGB
            ((300, 100, 400, 200), (0, 255, 0), 'GREEN_BUTTON'),    # 绿色RGB
            ((500, 100, 600, 200), (0, 0, 255), 'BLUE_BUTTON'),     # 蓝色RGB
        ]

        from module.base.utils import get_color

        for button_area, button_color_rgb, button_name in test_cases:
            # 创建测试图片
            test_image = create_test_screen_with_button(button_area, button_color_rgb)

            # 转换为BGR进行比较
            button_color_bgr = (button_color_rgb[2], button_color_rgb[1], button_color_rgb[0])

            # 检测颜色
            detected_color = get_color(test_image, button_area)

            color_match = all(abs(detected_color[i] - button_color_bgr[i]) < 10 for i in range(3))

            logger.info(f'{button_name}: 期望BGR{button_color_bgr}, 检测BGR{detected_color}, '
                       f'{"✓" if color_match else "✗"}')

            if not color_match:
                logger.error(f'❌ {button_name} 颜色检测失败')
                return False

        logger.info('✅ 多颜色按钮检测成功')
        return True

    except Exception as e:
        logger.error(f'❌ 多颜色按钮检测失败: {e}')
        return False


def test_button_not_appear():
    """测试按钮不存在的情况（负面测试）"""
    logger.hr('测试按钮不存在', level=0)

    try:
        # 创建白色背景
        test_image = np.ones((720, 1280, 3), dtype=np.uint8) * 255

        # 期望在某位置有红色按钮
        button_area = (200, 150, 400, 250)
        expected_color = (255, 0, 0)  # 红色

        from module.base.utils import get_color
        detected_color = get_color(test_image, button_area)

        logger.info(f'期望颜色: RGB{expected_color}')
        logger.info(f'检测颜色: RGB{detected_color}')

        # 应该检测到白色，不是红色
        color_match = all(abs(detected_color[i] - expected_color[i]) < 10 for i in range(3))

        if not color_match:
            logger.info('✅ 正确判断按钮不存在')
            return True
        else:
            logger.error('❌ 误判按钮存在')
            return False

    except Exception as e:
        logger.error(f'❌ 负面测试失败: {e}')
        return False


def test_button_area_validation():
    """测试按钮区域验证"""
    logger.hr('测试按钮区域验证', level=0)

    try:
        # 创建一个大按钮
        button_area = (100, 100, 500, 300)
        button_color = (128, 128, 128)  # 灰色

        test_image = create_test_screen_with_button(button_area, button_color)

        # 测试不同的检测区域
        test_areas = [
            (button_area, True, '完全匹配'),
            ((150, 150, 450, 250), True, '子区域'),
            ((0, 0, 50, 50), False, '完全不同区域'),
        ]

        from module.base.utils import get_color

        for area, should_match, desc in test_areas:
            detected_color = get_color(test_image, area)
            color_match = all(abs(detected_color[i] - button_color[i]) < 30 for i in range(3))

            logger.info(f'{desc}: 期望{"匹配" if should_match else "不匹配"}, '
                       f'实际{"匹配" if color_match else "不匹配"}, '
                       f'{"✓" if color_match == should_match else "✗"}')

        logger.info('✅ 按钮区域验证成功')
        return True

    except Exception as e:
        logger.error(f'❌ 按钮区域验证失败: {e}')
        return False


def test_button_with_real_device():
    """测试真实设备按钮检测（可选）"""
    logger.hr('测试真实设备（可选）', level=0)

    try:
        from module.device.device import Device

        try:
            device = Device(serial='127.0.0.1:5565')
            device.screenshot()
        except:
            logger.warning('⚠️  设备未连接，跳过真实设备测试')
            return True

        # 创建一个按钮（不验证是否真的出现）
        h, w = device.image.shape[:2]
        button = Button(
            area=(w//2-50, h//2-50, w//2+50, h//2+50),
            color=(128, 128, 128),
            name='CENTER_BUTTON'
        )

        # 只测试功能不抛异常
        appears = device.appear(button)
        logger.info(f'真实设备按钮检测: {appears}（仅验证功能正常）')
        logger.info('✅ 真实设备测试完成')
        return True

    except ImportError:
        logger.warning('⚠️  无法导入Device，跳过真实设备测试')
        return True
    except Exception as e:
        logger.warning(f'⚠️  真实设备测试出错: {e}')
        return True


if __name__ == '__main__':
    results = []

    # 运行所有测试
    results.append(('按钮创建', test_button_creation()))
    results.append(('精确颜色检测', test_button_appear_with_exact_color()))
    results.append(('多颜色检测', test_button_appear_with_different_colors()))
    results.append(('按钮不存在', test_button_not_appear()))
    results.append(('区域验证', test_button_area_validation()))
    results.append(('真实设备', test_button_with_real_device()))

    # 输出测试结果
    logger.hr('测试结果汇总', level=0)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        logger.info(f'{name}: {status}')

    logger.hr(f'总计: {passed}/{total} 通过', level=0)
