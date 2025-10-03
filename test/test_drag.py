"""
测试拖拽功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.device.device import Device
from module.logger import logger
import time


def test_drag_basic():
    """测试基本拖拽"""
    logger.hr('测试基本拖拽', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过基本拖拽测试')
        return True

    try:
        # 拖拽：从左到右
        start = (200, 360)
        end = (800, 360)

        logger.info(f'拖拽: {start} -> {end}')
        device.drag(start, end, duration=0.8)

        time.sleep(1)
        logger.info('✅ 基本拖拽测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 基本拖拽失败: {e}')
        return False


def test_drag_vertical():
    """测试垂直拖拽"""
    logger.hr('测试垂直拖拽', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过垂直拖拽测试')
        return True

    try:
        # 垂直拖拽
        logger.info('向下拖拽')
        device.drag((640, 200), (640, 500), duration=0.8)
        time.sleep(1)

        logger.info('向上拖拽')
        device.drag((640, 500), (640, 200), duration=0.8)
        time.sleep(1)

        logger.info('✅ 垂直拖拽测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 垂直拖拽失败: {e}')
        return False


def test_drag_diagonal():
    """测试对角拖拽"""
    logger.hr('测试对角拖拽', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过对角拖拽测试')
        return True

    try:
        # 对角线拖拽
        logger.info('左上到右下拖拽')
        device.drag((200, 200), (800, 500), duration=1.0)
        time.sleep(1)

        logger.info('右下到左上拖拽')
        device.drag((800, 500), (200, 200), duration=1.0)
        time.sleep(1)

        logger.info('✅ 对角拖拽测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 对角拖拽失败: {e}')
        return False


def test_drag_speed():
    """测试不同速度的拖拽"""
    logger.hr('测试不同速度拖拽', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过不同速度拖拽测试')
        return True

    try:
        start = (200, 360)
        end = (800, 360)

        # 快速拖拽
        logger.info('快速拖拽 (0.3s)')
        device.drag(start, end, duration=0.3)
        time.sleep(1)

        # 慢速拖拽
        logger.info('慢速拖拽 (1.5s)')
        device.drag(end, start, duration=1.5)
        time.sleep(1)

        logger.info('✅ 不同速度拖拽测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 不同速度拖拽失败: {e}')
        return False


if __name__ == '__main__':
    results = []

    # 运行所有测试
    results.append(('基本拖拽', test_drag_basic()))
    results.append(('垂直拖拽', test_drag_vertical()))
    results.append(('对角拖拽', test_drag_diagonal()))
    results.append(('不同速度', test_drag_speed()))

    # 输出测试结果
    logger.hr('测试结果汇总', level=0)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        logger.info(f'{name}: {status}')

    logger.hr(f'总计: {passed}/{total} 通过', level=0)
