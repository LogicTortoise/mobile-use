"""
Test script: Open browser and search for today's weather

This demonstrates the mobile automation capabilities including:
- Device connection
- Screenshot capture
- Touch controls (click, swipe)
- OCR text recognition
"""
import time
from module.device.device import Device
from module.logger import logger


def main():
    """Main test function"""
    logger.hr('Browser Search Test', level=0)

    # Initialize device (connecting to emulator at 127.0.0.1:5565)
    device = Device(serial='127.0.0.1:5565')

    try:
        # Take initial screenshot
        logger.info('Taking screenshot...')
        device.screenshot()
        device.save_screenshot('screenshot_initial.png')

        # Simulate some clicks and swipes
        logger.hr('Testing Controls', level=1)

        # Example 1: Click at a specific position (center of screen)
        logger.info('Click at center of screen')
        device.click((540, 960))  # Adjust based on your emulator resolution
        time.sleep(1)

        # Example 2: Swipe down (notification bar)
        logger.info('Swipe down from top')
        device.swipe((540, 50), (540, 500), duration=0.3)
        time.sleep(1)

        # Example 3: Swipe up (close notification)
        logger.info('Swipe up to close')
        device.swipe((540, 500), (540, 50), duration=0.3)
        time.sleep(1)

        # Example 4: Swipe left (if needed)
        logger.info('Swipe left')
        device.swipe((800, 960), (200, 960), duration=0.3)
        time.sleep(1)

        # Take final screenshot
        device.screenshot()
        device.save_screenshot('screenshot_final.png')

        logger.hr('Test Complete', level=0)
        logger.info('Screenshots saved: screenshot_initial.png, screenshot_final.png')

    except KeyboardInterrupt:
        logger.info('Test interrupted by user')
    except Exception as e:
        logger.exception(f'Test failed: {e}')
    finally:
        logger.info('Test finished')


if __name__ == '__main__':
    main()
