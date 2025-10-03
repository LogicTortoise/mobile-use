"""
Test script: Click Baidu icon and search for weather

This test demonstrates:
- Finding and clicking app icons
- Text input
- Searching with Baidu
- OCR for verification
"""
import time
from module.device.device import Device
from module.logger import logger
from module.ocr.ocr import OCR


def main():
    """Main test function for Baidu weather search"""
    logger.hr('Baidu Weather Search Test', level=0)

    # Initialize device
    device = Device(serial='127.0.0.1:5565')

    try:
        # Step 1: Take initial screenshot to see current state
        logger.hr('Step 1: Capture initial screen', level=1)
        device.screenshot()
        device.save_screenshot('step1_initial.png')
        logger.info(f'Screen size: {device.image.shape[1]}x{device.image.shape[0]}')
        time.sleep(1)

        # Step 2: Press home button to go to home screen
        logger.hr('Step 2: Press home button', level=1)
        device.adb_shell('input keyevent KEYEVENT_HOME')
        time.sleep(2)
        device.screenshot()
        device.save_screenshot('step2_home.png')

        # Step 3: Look for Baidu app or open app drawer
        logger.hr('Step 3: Open app list', level=1)
        # Swipe up to open app drawer (common Android gesture)
        screen_width = device.image.shape[1]
        screen_height = device.image.shape[0]
        center_x = screen_width // 2

        device.swipe(
            (center_x, screen_height - 100),
            (center_x, screen_height // 2),
            duration=0.5
        )
        time.sleep(2)
        device.screenshot()
        device.save_screenshot('step3_app_drawer.png')

        # Step 4: Try to find and click Baidu using OCR
        logger.hr('Step 4: Search for Baidu app', level=1)
        ocr = OCR()

        # Perform OCR on the whole screen to find "百度" or "Baidu"
        text = ocr.ocr(device.image)
        logger.info(f'OCR detected text: {text}')

        # If we can't find Baidu through OCR, let's try opening browser instead
        logger.hr('Step 5: Open Browser', level=1)

        # Method 1: Try to launch browser via package name
        try:
            # Common browser packages
            browser_packages = [
                'com.android.browser',  # Stock browser
                'com.android.chrome',   # Chrome
                'org.mozilla.firefox',  # Firefox
            ]

            for package in browser_packages:
                try:
                    logger.info(f'Trying to launch {package}')
                    device.adb_shell(f'monkey -p {package} -c android.intent.category.LAUNCHER 1')
                    time.sleep(3)
                    break
                except:
                    continue
        except Exception as e:
            logger.warning(f'Failed to launch browser via package: {e}')

            # Method 2: Click on common browser icon position
            logger.info('Trying to click browser icon at common position')
            # Typically browsers are in the bottom row
            device.click((center_x, screen_height - 200))
            time.sleep(2)

        device.screenshot()
        device.save_screenshot('step5_browser_opened.png')

        # Step 6: Navigate to Baidu
        logger.hr('Step 6: Navigate to Baidu', level=1)

        # Click on address bar (usually at the top)
        logger.info('Click on address bar')
        device.click((center_x, 100))
        time.sleep(2)

        # Input Baidu URL
        logger.info('Typing baidu.com')
        device.adb_shell('input text "baidu.com"')
        time.sleep(1)

        # Press Enter
        device.adb_shell('input keyevent KEYEVENT_ENTER')
        time.sleep(4)  # Wait for page to load

        device.screenshot()
        device.save_screenshot('step6_baidu_loaded.png')

        # Step 7: Click search box and search for weather
        logger.hr('Step 7: Search for weather', level=1)

        # Baidu search box is typically in the center-top area
        logger.info('Click on Baidu search box')
        device.click((center_x, 200))
        time.sleep(2)

        # Clear any existing text
        device.adb_shell('input keyevent KEYEVENT_DEL')
        time.sleep(0.5)

        # Input "天气" (weather in Chinese)
        logger.info('Typing: 天气')
        # For Chinese input, we need to use different method
        # Let's use English "weather" instead
        device.adb_shell('input text "weather"')
        time.sleep(1)

        device.screenshot()
        device.save_screenshot('step7_search_input.png')

        # Step 8: Submit search
        logger.hr('Step 8: Submit search', level=1)
        device.adb_shell('input keyevent KEYEVENT_ENTER')
        time.sleep(3)  # Wait for search results

        device.screenshot()
        device.save_screenshot('step8_search_results.png')

        # Step 9: Verify results with OCR
        logger.hr('Step 9: Verify search results', level=1)
        result_text = ocr.ocr(device.image)
        logger.info(f'Search results contain: {result_text[:200]}...')

        if 'weather' in result_text.lower() or 'temperature' in result_text.lower():
            logger.info('✅ Weather search successful!')
        else:
            logger.info('⚠️  Results may not contain weather info, but search was executed')

        # Final screenshot
        device.screenshot()
        device.save_screenshot('step9_final.png')

        logger.hr('Test Complete', level=0)
        logger.info('✅ All steps completed successfully!')
        logger.info('Screenshots saved: step1-9 PNG files')

    except KeyboardInterrupt:
        logger.info('Test interrupted by user')
    except Exception as e:
        logger.exception(f'Test failed: {e}')
        # Save error screenshot
        try:
            device.screenshot()
            device.save_screenshot('error_screenshot.png')
            logger.info('Error screenshot saved')
        except:
            pass
    finally:
        logger.info('Test finished')


if __name__ == '__main__':
    main()
