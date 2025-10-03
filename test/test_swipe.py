"""
测试滑动功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.device.device import Device
from module.logger import logger
import time


def test_swipe_horizontal():
    """测试水平滑动"""
    logger.hr('测试水平滑动', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过水平滑动测试')
        return True

    try:
        # 从左向右滑动
        logger.info('从左向右滑动')
        device.swipe((100, 360), (1000, 360), duration=0.3)
        time.sleep(1)

        # 从右向左滑动
        logger.info('从右向左滑动')
        device.swipe((1000, 360), (100, 360), duration=0.3)
        time.sleep(1)

        logger.info('✅ 水平滑动测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 水平滑动失败: {e}')
        return False


def test_swipe_vertical():
    """测试垂直滑动"""
    logger.hr('测试垂直滑动', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过垂直滑动测试')
        return True

    try:
        # 从上向下滑动
        logger.info('从上向下滑动')
        device.swipe((640, 200), (640, 600), duration=0.3)
        time.sleep(1)

        # 从下向上滑动
        logger.info('从下向上滑动')
        device.swipe((640, 600), (640, 200), duration=0.3)
        time.sleep(1)

        logger.info('✅ 垂直滑动测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 垂直滑动失败: {e}')
        return False


def test_swipe_diagonal():
    """测试对角线滑动"""
    logger.hr('测试对角线滑动', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过对角线滑动测试')
        return True

    try:
        # 对角线滑动
        logger.info('左上到右下滑动')
        device.swipe((100, 100), (900, 600), duration=0.4)
        time.sleep(1)

        logger.info('右下到左上滑动')
        device.swipe((900, 600), (100, 100), duration=0.4)
        time.sleep(1)

        logger.info('✅ 对角线滑动测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 对角线滑动失败: {e}')
        return False


def test_swipe_speed():
    """测试不同速度滑动"""
    logger.hr('测试不同速度滑动', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过不同速度滑动测试')
        return True

    try:
        # 快速滑动
        logger.info('快速滑动 (0.1s)')
        device.swipe((100, 360), (900, 360), duration=0.1)
        time.sleep(1)

        # 慢速滑动
        logger.info('慢速滑动 (1.0s)')
        device.swipe((100, 360), (900, 360), duration=1.0)
        time.sleep(1)

        logger.info('✅ 不同速度滑动测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 不同速度滑动失败: {e}')
        return False


def test_swipe_vector():
    """测试向量滑动"""
    logger.hr('测试向量滑动', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过向量滑动测试')
        return True

    try:
        # 使用向量表示滑动方向
        logger.info('向右滑动（使用向量）')
        device.swipe_vector((800, 0), duration=0.3)
        time.sleep(1)

        logger.info('向下滑动（使用向量）')
        device.swipe_vector((0, 400), duration=0.3)
        time.sleep(1)

        logger.info('✅ 向量滑动测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 向量滑动失败: {e}')
        return False


if __name__ == '__main__':
    results = []

    # 运行所有测试
    results.append(('水平滑动', test_swipe_horizontal()))
    results.append(('垂直滑动', test_swipe_vertical()))
    results.append(('对角线滑动', test_swipe_diagonal()))
    results.append(('不同速度', test_swipe_speed()))
    results.append(('向量滑动', test_swipe_vector()))

    # 输出测试结果
    logger.hr('测试结果汇总', level=0)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        logger.info(f'{name}: {status}')

    logger.hr(f'总计: {passed}/{total} 通过', level=0)
