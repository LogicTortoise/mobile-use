"""
测试设备连接功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.device.device import Device
from module.logger import logger


def test_device_connection():
    """测试设备连接"""
    logger.hr('测试设备连接', level=0)

    try:
        # 连接设备
        device = Device(serial='127.0.0.1:5565')
        logger.info('✅ 设备连接成功')
        logger.info(f'设备序列号: {device.serial}')
        return True
    except Exception as e:
        logger.error(f'❌ 设备连接失败: {e}')
        return False


def test_connection_retry():
    """测试连接重试机制"""
    logger.hr('测试连接重试机制', level=0)

    try:
        # 尝试连接不存在的设备
        device = Device(serial='127.0.0.1:9999')
        logger.error('❌ 应该连接失败但没有')
        return False
    except Exception as e:
        logger.info(f'✅ 正确捕获连接失败: {e}')
        return True


def test_device_info():
    """测试获取设备信息"""
    logger.hr('测试获取设备信息', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')

        # 获取设备信息
        logger.info(f'设备序列号: {device.serial}')
        logger.info('✅ 设备信息获取成功')
        return True
    except Exception as e:
        logger.error(f'❌ 获取设备信息失败: {e}')
        return False


if __name__ == '__main__':
    results = []

    # 运行所有测试
    results.append(('设备连接', test_device_connection()))
    results.append(('连接重试', test_connection_retry()))
    results.append(('设备信息', test_device_info()))

    # 输出测试结果
    logger.hr('测试结果汇总', level=0)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        logger.info(f'{name}: {status}')

    logger.hr(f'总计: {passed}/{total} 通过', level=0)
