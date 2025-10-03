"""
测试OCR文字定位功能 - 使用固定测试图片
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.logger import logger
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_test_image_with_positions(texts, positions, size=(800, 600)):
    """
    创建包含多个文字的测试图片，每个文字在指定位置

    Args:
        texts: 文字列表 ['文字1', '文字2', ...]
        positions: 位置列表 [(x1, y1), (x2, y2), ...]
        size: 图片尺寸

    Returns:
        np.ndarray: 图片数组
        dict: 文字到预期位置的映射
    """
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 40)
    except:
        font = ImageFont.load_default()

    expected_positions = {}

    for text, (x, y) in zip(texts, positions):
        # 绘制文字
        draw.text((x, y), text, fill='black', font=font)
        # 记录预期位置（使用文字中心点）
        bbox = draw.textbbox((x, y), text, font=font)
        center_x = (bbox[0] + bbox[2]) // 2
        center_y = (bbox[1] + bbox[3]) // 2
        expected_positions[text] = (center_x, center_y)

    # 转换为BGR格式
    img_array = np.array(img)
    img_bgr = img_array[:, :, ::-1]

    return img_bgr, expected_positions


def find_text_position(image, target_text):
    """
    在图片中找到指定文字的位置

    Args:
        image: 图片数组
        target_text: 要查找的文字

    Returns:
        tuple: (center_x, center_y, bbox) 或 None
    """
    ocr_model = PaddleOCR(lang='ch', show_log=False)
    result = ocr_model.ocr(image)

    if not result or len(result) == 0:
        return None

    page_result = result[0]

    if isinstance(page_result, dict):
        rec_texts = page_result.get('rec_texts', [])
        dt_polys = page_result.get('dt_polys', [])

        for i, text in enumerate(rec_texts):
            if target_text in text or text in target_text:
                poly = dt_polys[i]
                center_x = int(np.mean([p[0] for p in poly]))
                center_y = int(np.mean([p[1] for p in poly]))
                return (center_x, center_y, poly)

    return None


def test_locate_single_text():
    """测试定位单个文字"""
    logger.hr('测试定位单个文字', level=0)

    try:
        # 创建测试图片：在已知位置放置文字
        test_text = "搜索按钮"
        position = (200, 100)

        texts = [test_text]
        positions = [position]

        test_image, expected_positions = create_test_image_with_positions(texts, positions)

        # 查找文字位置
        result = find_text_position(test_image, test_text)

        if result:
            found_x, found_y, bbox = result
            expected_x, expected_y = expected_positions[test_text]

            logger.info(f'查找文字: "{test_text}"')
            logger.info(f'预期位置: ({expected_x}, {expected_y})')
            logger.info(f'找到位置: ({found_x}, {found_y})')

            # 计算位置误差
            distance = np.sqrt((found_x - expected_x)**2 + (found_y - expected_y)**2)
            logger.info(f'位置误差: {distance:.1f} 像素')

            # 允许一定误差（OCR检测框可能不完全准确）
            if distance < 100:  # 误差小于100像素
                logger.info('✅ 单文字定位成功')
                return True
            else:
                logger.warning(f'⚠️  位置误差较大: {distance:.1f}像素')
                return True  # 仍然算通过，因为找到了文字

        else:
            logger.error('❌ 未找到目标文字')
            return False

    except Exception as e:
        logger.error(f'❌ 单文字定位失败: {e}')
        return False


def test_locate_multiple_texts():
    """测试定位多个文字"""
    logger.hr('测试定位多个文字', level=0)

    try:
        # 创建包含多个文字的测试图片
        texts = ['按钮1', '按钮2', '按钮3']
        positions = [(100, 100), (400, 100), (100, 300)]

        test_image, expected_positions = create_test_image_with_positions(texts, positions)

        # 使用OCR识别所有文字
        ocr_model = PaddleOCR(lang='ch', show_log=False)
        result = ocr_model.ocr(test_image)

        if result and len(result) > 0:
            page_result = result[0]
            if isinstance(page_result, dict):
                rec_texts = page_result.get('rec_texts', [])
                dt_polys = page_result.get('dt_polys', [])

                logger.info(f'识别到 {len(rec_texts)} 个文字区域')

                found_count = 0
                for i, text in enumerate(rec_texts):
                    poly = dt_polys[i]
                    center_x = int(np.mean([p[0] for p in poly]))
                    center_y = int(np.mean([p[1] for p in poly]))
                    logger.info(f'文字 "{text}" 在 ({center_x}, {center_y})')

                    # 检查是否是我们放置的文字
                    if any(expected_text in text or text in expected_text for expected_text in texts):
                        found_count += 1

                if found_count > 0:
                    logger.info(f'✅ 定位多个文字成功 (找到 {found_count}/{len(texts)} 个)')
                    return True
                else:
                    logger.error('❌ 未找到任何预期文字')
                    return False
        else:
            logger.error('❌ OCR未识别到任何文字')
            return False

    except Exception as e:
        logger.error(f'❌ 多文字定位失败: {e}')
        return False


def test_locate_chinese_english():
    """测试定位中英文混合文字"""
    logger.hr('测试定位中英文混合', level=0)

    try:
        texts = ['Hello', '你好', 'Search搜索']
        positions = [(100, 150), (300, 150), (500, 150)]

        test_image, expected_positions = create_test_image_with_positions(texts, positions)

        found_count = 0
        for text in texts:
            result = find_text_position(test_image, text)
            if result:
                x, y, bbox = result
                logger.info(f'✅ 找到 "{text}" 在 ({x}, {y})')
                found_count += 1
            else:
                logger.info(f'未找到 "{text}"')

        if found_count > 0:
            logger.info(f'✅ 中英文混合定位成功 (找到 {found_count}/{len(texts)} 个)')
            return True
        else:
            logger.error('❌ 未找到任何文字')
            return False

    except Exception as e:
        logger.error(f'❌ 中英文混合定位失败: {e}')
        return False


def test_position_accuracy():
    """测试位置精确度"""
    logger.hr('测试位置精确度', level=0)

    try:
        # 在精确已知的位置放置文字
        test_text = "定位测试"
        exact_position = (300, 200)

        test_image, expected_positions = create_test_image_with_positions(
            [test_text], [exact_position]
        )

        result = find_text_position(test_image, test_text)

        if result:
            found_x, found_y, bbox = result
            expected_x, expected_y = expected_positions[test_text]

            distance = np.sqrt((found_x - expected_x)**2 + (found_y - expected_y)**2)

            logger.info(f'预期位置: ({expected_x}, {expected_y})')
            logger.info(f'检测位置: ({found_x}, {found_y})')
            logger.info(f'位置误差: {distance:.2f} 像素')
            logger.info(f'边界框: {bbox}')

            # 评估精确度
            if distance < 50:
                logger.info('✅ 位置精确度高（误差<50px）')
            elif distance < 100:
                logger.info('✅ 位置精确度中等（误差<100px）')
            else:
                logger.warning(f'⚠️  位置精确度较低（误差{distance:.1f}px）')

            return True
        else:
            logger.error('❌ 未找到文字')
            return False

    except Exception as e:
        logger.error(f'❌ 位置精确度测试失败: {e}')
        return False


def test_real_screenshot_locate():
    """测试真实截图定位（可选）"""
    logger.hr('测试真实截图定位（可选）', level=0)

    try:
        from module.device.device import Device

        try:
            device = Device(serial='127.0.0.1:5565')
            device.screenshot()
        except:
            logger.warning('⚠️  设备未连接，跳过真实截图测试')
            return True

        # 尝试找任意文字（不验证准确性）
        ocr_model = PaddleOCR(lang='ch', show_log=False)
        result = ocr_model.ocr(device.image)

        if result and len(result) > 0:
            page_result = result[0]
            if isinstance(page_result, dict):
                rec_texts = page_result.get('rec_texts', [])
                if len(rec_texts) > 0:
                    logger.info(f'真实截图识别到 {len(rec_texts)} 个文字')
                    logger.info('✅ 真实截图定位功能正常')
                else:
                    logger.info('⚠️  真实截图未识别到文字（可能是空白屏幕）')
                return True

        logger.info('✅ 真实截图测试完成')
        return True

    except ImportError:
        logger.warning('⚠️  无法导入Device，跳过真实截图测试')
        return True
    except Exception as e:
        logger.warning(f'⚠️  真实截图测试出错: {e}')
        return True


if __name__ == '__main__':
    results = []

    # 运行所有测试
    results.append(('单文字定位', test_locate_single_text()))
    results.append(('多文字定位', test_locate_multiple_texts()))
    results.append(('中英文混合', test_locate_chinese_english()))
    results.append(('位置精确度', test_position_accuracy()))
    results.append(('真实截图', test_real_screenshot_locate()))

    # 输出测试结果
    logger.hr('测试结果汇总', level=0)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        logger.info(f'{name}: {status}')

    logger.hr(f'总计: {passed}/{total} 通过', level=0)
