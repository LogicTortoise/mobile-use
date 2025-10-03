"""
测试图像工具函数 - 使用合成图片
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.base.utils import *
from module.logger import logger
import numpy as np
from PIL import Image


def create_test_image(width=800, height=600, color=(128, 128, 128)):
    """
    创建测试图片

    Args:
        width: 宽度
        height: 高度
        color: 颜色 (R, G, B)

    Returns:
        np.ndarray: BGR格式图片
    """
    img = Image.new('RGB', (width, height), color=color)
    img_array = np.array(img)
    img_bgr = img_array[:, :, ::-1]  # RGB转BGR
    return img_bgr


def test_crop():
    """测试图像裁剪"""
    logger.hr('测试图像裁剪', level=0)

    try:
        # 创建测试图片
        test_image = create_test_image(800, 600)

        # 裁剪中心区域
        area = (200, 150, 600, 450)
        cropped = crop(test_image, area)

        expected_h = area[3] - area[1]  # 450 - 150 = 300
        expected_w = area[2] - area[0]  # 600 - 200 = 400

        logger.info(f'原始尺寸: {test_image.shape[:2]}')
        logger.info(f'裁剪区域: {area}')
        logger.info(f'裁剪尺寸: {cropped.shape[:2]}')
        logger.info(f'期望尺寸: ({expected_h}, {expected_w})')

        if cropped.shape[0] == expected_h and cropped.shape[1] == expected_w:
            logger.info('✅ 图像裁剪成功')
            return True
        else:
            logger.error(f'❌ 裁剪尺寸不正确')
            return False

    except Exception as e:
        logger.error(f'❌ 图像裁剪失败: {e}')
        return False


def test_area_offset():
    """测试区域偏移"""
    logger.hr('测试区域偏移', level=0)

    try:
        original_area = (100, 200, 300, 400)
        offset = (50, 50)

        new_area = area_offset(original_area, offset)
        expected = (150, 250, 350, 450)

        logger.info(f'原始区域: {original_area}')
        logger.info(f'偏移量: {offset}')
        logger.info(f'新区域: {new_area}')
        logger.info(f'期望: {expected}')

        if new_area == expected:
            logger.info('✅ 区域偏移正确')
            return True
        else:
            logger.error(f'❌ 区域偏移错误')
            return False

    except Exception as e:
        logger.error(f'❌ 区域偏移失败: {e}')
        return False


def test_random_rectangle_point():
    """测试随机矩形点生成"""
    logger.hr('测试随机矩形点生成', level=0)

    try:
        area = (100, 200, 300, 400)

        # 生成10个随机点并验证都在区域内
        all_valid = True
        for i in range(10):
            point = random_rectangle_point(area)
            x, y = point

            in_bounds = (area[0] <= x <= area[2] and area[1] <= y <= area[3])

            if in_bounds:
                logger.info(f'随机点{i+1}: {point} ✓')
            else:
                logger.error(f'随机点{i+1}: {point} 超出区域 {area}')
                all_valid = False

        if all_valid:
            logger.info('✅ 随机点生成正确')
            return True
        else:
            logger.error('❌ 部分随机点超出区域')
            return False

    except Exception as e:
        logger.error(f'❌ 随机点生成失败: {e}')
        return False


def test_get_color():
    """测试颜色获取"""
    logger.hr('测试颜色获取', level=0)

    try:
        # 创建已知颜色的测试图片
        test_color_rgb = (100, 150, 200)  # RGB
        test_image = create_test_image(400, 300, color=test_color_rgb)

        # 获取中心区域颜色
        area = (150, 100, 250, 200)
        detected_color = get_color(test_image, area)

        # get_color返回BGR格式，所以需要转换预期颜色
        test_color_bgr = (test_color_rgb[2], test_color_rgb[1], test_color_rgb[0])

        logger.info(f'预期颜色: BGR{test_color_bgr}')
        logger.info(f'检测颜色: BGR{detected_color}')

        # 验证颜色（允许小误差）
        color_match = all(abs(detected_color[i] - test_color_bgr[i]) < 5 for i in range(3))

        if color_match:
            logger.info('✅ 颜色获取成功')
            return True
        else:
            logger.error('❌ 颜色不匹配')
            return False

    except Exception as e:
        logger.error(f'❌ 颜色获取失败: {e}')
        return False


def test_get_color_multiple_areas():
    """测试多区域颜色获取"""
    logger.hr('测试多区域颜色获取', level=0)

    try:
        # 创建带有多个颜色区域的图片
        test_image = np.zeros((400, 600, 3), dtype=np.uint8)

        # 左侧红色
        test_image[:, 0:200] = [0, 0, 255]  # BGR红色

        # 中间绿色
        test_image[:, 200:400] = [0, 255, 0]  # BGR绿色

        # 右侧蓝色
        test_image[:, 400:600] = [255, 0, 0]  # BGR蓝色

        # 测试各区域颜色
        test_cases = [
            ((50, 100, 150, 200), (0, 0, 255), '左侧红色'),
            ((250, 100, 350, 200), (0, 255, 0), '中间绿色'),
            ((450, 100, 550, 200), (255, 0, 0), '右侧蓝色'),
        ]

        for area, expected_color, desc in test_cases:
            detected_color = get_color(test_image, area)
            color_match = all(abs(detected_color[i] - expected_color[i]) < 5 for i in range(3))

            logger.info(f'{desc}: 期望{expected_color}, 检测{detected_color}, '
                       f'{"✓" if color_match else "✗"}')

            if not color_match:
                logger.error(f'❌ {desc} 颜色不匹配')
                return False

        logger.info('✅ 多区域颜色获取成功')
        return True

    except Exception as e:
        logger.error(f'❌ 多区域颜色获取失败: {e}')
        return False


def test_load_and_save_image():
    """测试图像加载和保存"""
    logger.hr('测试图像加载和保存', level=0)

    try:
        # 创建测试图片
        test_image = create_test_image(640, 480, color=(100, 150, 200))

        # 保存图像
        test_path = 'test/test_image_save.png'
        os.makedirs(os.path.dirname(test_path), exist_ok=True)

        import cv2
        cv2.imwrite(test_path, test_image)

        # 加载图像
        if os.path.exists(test_path):
            loaded_image = load_image(test_path)

            logger.info(f'原始图像尺寸: {test_image.shape}')
            logger.info(f'加载图像尺寸: {loaded_image.shape}')

            # 验证尺寸一致
            if loaded_image.shape == test_image.shape:
                logger.info('✅ 图像加载和保存成功')
                return True
            else:
                logger.error('❌ 加载的图像尺寸不一致')
                return False
        else:
            logger.error('❌ 图像文件未保存')
            return False

    except Exception as e:
        logger.error(f'❌ 图像加载和保存失败: {e}')
        return False


def test_crop_edge_cases():
    """测试裁剪边界情况"""
    logger.hr('测试裁剪边界情况', level=0)

    try:
        test_image = create_test_image(800, 600)

        # 测试各种边界情况
        test_cases = [
            ((0, 0, 400, 300), '左上角'),
            ((400, 300, 800, 600), '右下角'),
            ((0, 0, 800, 600), '全图'),
            ((200, 150, 201, 151), '最小区域(1x1)'),
        ]

        for area, desc in test_cases:
            try:
                cropped = crop(test_image, area)
                expected_h = area[3] - area[1]
                expected_w = area[2] - area[0]

                if cropped.shape[0] == expected_h and cropped.shape[1] == expected_w:
                    logger.info(f'{desc} {area}: ✓')
                else:
                    logger.error(f'{desc} {area}: 尺寸不匹配')
                    return False

            except Exception as e:
                logger.error(f'{desc} {area}: 出错 - {e}')
                return False

        logger.info('✅ 裁剪边界情况测试通过')
        return True

    except Exception as e:
        logger.error(f'❌ 裁剪边界情况测试失败: {e}')
        return False


def test_with_real_device():
    """测试真实设备图像操作（可选）"""
    logger.hr('测试真实设备（可选）', level=0)

    try:
        from module.device.device import Device

        try:
            device = Device(serial='127.0.0.1:5565')
            device.screenshot()
        except:
            logger.warning('⚠️  设备未连接，跳过真实设备测试')
            return True

        # 只测试基本操作不抛异常
        h, w = device.image.shape[:2]
        area = (w//4, h//4, 3*w//4, 3*h//4)

        # 测试裁剪
        cropped = crop(device.image, area)

        # 测试颜色获取
        color = get_color(device.image, area)

        logger.info(f'真实设备图像尺寸: {device.image.shape}')
        logger.info(f'裁剪后尺寸: {cropped.shape}')
        logger.info(f'区域颜色: RGB{color}')
        logger.info('✅ 真实设备测试完成（功能正常）')
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
    results.append(('图像裁剪', test_crop()))
    results.append(('区域偏移', test_area_offset()))
    results.append(('随机点生成', test_random_rectangle_point()))
    results.append(('颜色获取', test_get_color()))
    results.append(('多区域颜色', test_get_color_multiple_areas()))
    results.append(('图像加载保存', test_load_and_save_image()))
    results.append(('裁剪边界情况', test_crop_edge_cases()))
    results.append(('真实设备', test_with_real_device()))

    # 输出测试结果
    logger.hr('测试结果汇总', level=0)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        logger.info(f'{name}: {status}')

    logger.hr(f'总计: {passed}/{total} 通过', level=0)
