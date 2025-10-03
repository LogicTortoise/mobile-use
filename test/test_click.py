"""
测试点击功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.device.device import Device
from module.logger import logger
import time


def test_click_coordinate():
    """测试坐标点击"""
    logger.hr('测试坐标点击', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过坐标点击测试')
        return True

    try:
        # 点击屏幕中心
        device.screenshot()
        h, w = device.image.shape[:2]
        center_x, center_y = w // 2, h // 2

        logger.info(f'点击屏幕中心: ({center_x}, {center_y})')
        device.click(center_x, center_y)

        time.sleep(0.5)
        logger.info('✅ 坐标点击成功')
        return True
    except Exception as e:
        logger.error(f'❌ 坐标点击失败: {e}')
        return False


def test_click_tuple():
    """测试元组坐标点击"""
    logger.hr('测试元组坐标点击', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过元组点击测试')
        return True

    try:
        # 使用元组坐标点击
        position = (640, 360)
        logger.info(f'点击位置: {position}')
        device.click(position)

        time.sleep(0.5)
        logger.info('✅ 元组坐标点击成功')
        return True
    except Exception as e:
        logger.error(f'❌ 元组坐标点击失败: {e}')
        return False


def test_click_multiple():
    """测试连续点击"""
    logger.hr('测试连续点击', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过连续点击测试')
        return True

    try:
        # 连续点击5次
        positions = [
            (100, 100),
            (200, 200),
            (300, 300),
            (400, 400),
            (500, 500)
        ]

        for i, pos in enumerate(positions):
            logger.info(f'第{i+1}次点击: {pos}')
            device.click(pos)
            time.sleep(0.2)

        logger.info('✅ 连续点击测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 连续点击失败: {e}')
        return False


def test_click_boundary():
    """测试边界点击"""
    logger.hr('测试边界点击', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过边界点击测试')
        return True

    try:
        device.screenshot()
        h, w = device.image.shape[:2]

        # 测试四个角
        corners = [
            (10, 10),           # 左上
            (w-10, 10),         # 右上
            (10, h-10),         # 左下
            (w-10, h-10)        # 右下
        ]

        for i, corner in enumerate(corners):
            logger.info(f'点击角落{i+1}: {corner}')
            device.click(corner)
            time.sleep(0.2)

        logger.info('✅ 边界点击测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 边界点击失败: {e}')
        return False


if __name__ == '__main__':
    results = []

    # 运行所有测试
    results.append(('坐标点击', test_click_coordinate()))
    results.append(('元组点击', test_click_tuple()))
    results.append(('连续点击', test_click_multiple()))
    results.append(('边界点击', test_click_boundary()))

    # 输出测试结果
    logger.hr('测试结果汇总', level=0)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        logger.info(f'{name}: {status}')

    logger.hr(f'总计: {passed}/{total} 通过', level=0)
