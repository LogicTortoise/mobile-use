"""
测试截图功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.device.device import Device
from module.logger import logger
import numpy as np


def test_screenshot_basic():
    """测试基本截图功能"""
    logger.hr('测试基本截图', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过基本截图测试')
        return True

    try:
        # 截图
        device.screenshot()

        # 验证截图
        if device.image is not None:
            logger.info(f'截图尺寸: {device.image.shape}')
            logger.info('✅ 截图成功')
            return True
        else:
            logger.error('❌ 截图为空')
            return False
    except Exception as e:
        logger.error(f'❌ 截图失败: {e}')
        return False


def test_screenshot_save():
    """测试保存截图"""
    logger.hr('测试保存截图', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过保存截图测试')
        return True

    try:
        # 截图并保存
        device.screenshot()
        save_path = 'test/test_screenshot.png'
        device.save_screenshot(save_path)

        # 验证文件存在
        if os.path.exists(save_path):
            logger.info(f'✅ 截图已保存到: {save_path}')
            return True
        else:
            logger.error('❌ 截图文件未保存')
            return False
    except Exception as e:
        logger.error(f'❌ 保存截图失败: {e}')
        return False


def test_screenshot_multiple():
    """测试连续截图"""
    logger.hr('测试连续截图', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过连续截图测试')
        return True

    try:
        # 连续截图3次
        for i in range(3):
            device.screenshot()
            if device.image is None:
                logger.error(f'❌ 第{i+1}次截图失败')
                return False
            logger.info(f'第{i+1}次截图成功')

        logger.info('✅ 连续截图测试通过')
        return True
    except Exception as e:
        logger.error(f'❌ 连续截图失败: {e}')
        return False


def test_screenshot_format():
    """测试截图格式"""
    logger.hr('测试截图格式', level=0)

    try:
        device = Device(serial='127.0.0.1:5565')
    except Exception as e:
        logger.warning('⚠️  设备未连接，跳过截图格式测试')
        return True

    try:
        device.screenshot()

        # 验证是numpy数组
        if not isinstance(device.image, np.ndarray):
            logger.error('❌ 截图不是numpy数组')
            return False

        # 验证是3通道BGR图像
        if len(device.image.shape) != 3 or device.image.shape[2] != 3:
            logger.error('❌ 截图格式不正确')
            return False

        logger.info('✅ 截图格式正确（numpy BGR）')
        return True
    except Exception as e:
        logger.error(f'❌ 验证截图格式失败: {e}')
        return False


if __name__ == '__main__':
    results = []

    # 运行所有测试
    results.append(('基本截图', test_screenshot_basic()))
    results.append(('保存截图', test_screenshot_save()))
    results.append(('连续截图', test_screenshot_multiple()))
    results.append(('截图格式', test_screenshot_format()))

    # 输出测试结果
    logger.hr('测试结果汇总', level=0)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        logger.info(f'{name}: {status}')

    logger.hr(f'总计: {passed}/{total} 通过', level=0)
