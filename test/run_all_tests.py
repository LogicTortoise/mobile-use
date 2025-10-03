"""
运行所有测试脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.logger import logger
import subprocess
import time


def run_test(test_file):
    """
    运行单个测试文件

    Args:
        test_file: 测试文件名

    Returns:
        bool: 测试是否成功
    """
    test_path = os.path.join('test', test_file)

    logger.hr(f'运行测试: {test_file}', level=0)

    try:
        # 使用当前Python解释器运行测试
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=120  # 2分钟超时
        )

        # 输出测试结果
        print(result.stdout)

        if result.stderr:
            print(result.stderr)

        # 检查返回码
        if result.returncode == 0:
            logger.info(f'✅ {test_file} 测试通过')
            return True
        else:
            logger.error(f'❌ {test_file} 测试失败')
            return False

    except subprocess.TimeoutExpired:
        logger.error(f'❌ {test_file} 测试超时')
        return False
    except Exception as e:
        logger.error(f'❌ {test_file} 运行出错: {e}')
        return False


def main():
    """运行所有测试"""
    logger.hr('开始运行所有测试', level=0)

    # 测试文件列表（按依赖顺序）
    test_files = [
        'test_connection.py',      # 1. 连接测试
        'test_screenshot.py',      # 2. 截图测试
        'test_utils.py',           # 3. 工具测试
        'test_click.py',           # 4. 点击测试
        'test_swipe.py',           # 5. 滑动测试
        'test_long_click.py',      # 6. 长按测试
        'test_drag.py',            # 7. 拖拽测试
        'test_button.py',          # 8. 按钮测试
        'test_ocr.py',             # 9. OCR测试
        'test_ocr_locate.py',      # 10. OCR定位测试
    ]

    results = []
    start_time = time.time()

    # 运行所有测试
    for test_file in test_files:
        success = run_test(test_file)
        results.append((test_file, success))
        time.sleep(1)  # 测试间隔

    # 统计结果
    elapsed_time = time.time() - start_time
    passed = sum(1 for _, success in results if success)
    total = len(results)

    # 输出汇总
    logger.hr('所有测试结果汇总', level=0)

    for test_file, success in results:
        status = '✅ 通过' if success else '❌ 失败'
        logger.info(f'{test_file:30s} {status}')

    logger.hr('', level=0)
    logger.info(f'总计: {passed}/{total} 通过')
    logger.info(f'耗时: {elapsed_time:.1f}秒')

    if passed == total:
        logger.hr('🎉 所有测试通过！', level=0)
        return 0
    else:
        logger.hr(f'⚠️  {total - passed} 个测试失败', level=0)
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
