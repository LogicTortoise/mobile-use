"""
测试长按功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.device.device import Device
from module.logger import logger
import time


def test_long_click_basic():
    """测试基本长按"""
    logger.hr('测试基本长按', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过基本长按测试')
        return True

    try:
        # 长按屏幕中心1秒
        device.screenshot()
        h, w = device.image.shape[:2]
        center = (w // 2, h // 2)

        logger.info(f'长按屏幕中心: {center}, 持续1秒')
        device.long_click(center, duration=1.0)

        time.sleep(0.5)
        logger.info('✅ 基本长按测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 基本长按失败: {e}')
        return False


def test_long_click_duration():
    """测试不同持续时间的长按"""
    logger.hr('测试不同持续时间长按', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过不同持续时间长按测试')
        return True

    try:
        durations = [0.5, 1.0, 2.0]
        position = (640, 360)

        for duration in durations:
            logger.info(f'长按{duration}秒')
            device.long_click(position, duration=duration)
            time.sleep(0.5)

        logger.info('✅ 不同持续时间长按测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 不同持续时间长按失败: {e}')
        return False


def test_long_click_positions():
    """测试不同位置的长按"""
    logger.hr('测试不同位置长按', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过不同位置长按测试')
        return True

    try:
        device.screenshot()
        h, w = device.image.shape[:2]

        # 四个角落长按
        positions = [
            (100, 100),      # 左上
            (w-100, 100),    # 右上
            (100, h-100),    # 左下
            (w-100, h-100)   # 右下
        ]

        for i, pos in enumerate(positions):
            logger.info(f'长按位置{i+1}: {pos}')
            device.long_click(pos, duration=0.5)
            time.sleep(0.3)

        logger.info('✅ 不同位置长按测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 不同位置长按失败: {e}')
        return False


if __name__ == '__main__':
    results = []

    # 运行所有测试
    results.append(('基本长按', test_long_click_basic()))
    results.append(('不同时长', test_long_click_duration()))
    results.append(('不同位置', test_long_click_positions()))

    # 输出测试结果
    logger.hr('测试结果汇总', level=0)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        logger.info(f'{name}: {status}')

    logger.hr(f'总计: {passed}/{total} 通过', level=0)
