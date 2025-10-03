"""
Simple example demonstrating basic mobile automation

This shows how to:
1. Connect to a device
2. Take screenshots
3. Perform clicks and swipes
4. Use OCR (optional)
"""
from module.device.device import Device
from module.base.button import Button
from module.ocr.ocr import OCR
from module.logger import logger


def example_basic_operations():
    """Example of basic device operations"""
    logger.hr('Basic Operations Example', level=0)

    # 1. Connect to device
    device = Device(serial='127.0.0.1:5565')

    # 2. Take a screenshot
    device.screenshot()
    device.save_screenshot('example_screenshot.png')

    # 3. Simple click
    device.click((500, 500))  # Click at position (500, 500)
    device.sleep(1)

    # 4. Swipe
    device.swipe((100, 500), (900, 500))  # Swipe from left to right
    device.sleep(1)


def example_button_detection():
    """Example of button detection using color"""
    logger.hr('Button Detection Example', level=0)

    device = Device(serial='127.0.0.1:5565')

    # Define a button with area and expected color
    my_button = Button(
        area=(100, 200, 300, 400),  # Detection area
        color=(255, 100, 100),      # Expected color (RGB)
        button=(100, 200, 300, 400), # Click area (same as detection area)
        name='MY_BUTTON'
    )

    # Take screenshot
    device.screenshot()

    # Check if button appears
    if device.appear(my_button, threshold=20):
        logger.info('Button detected!')
        device.click(my_button)
    else:
        logger.info('Button not found')


def example_ocr():
    """Example of OCR text recognition"""
    logger.hr('OCR Example', level=0)

    device = Device(serial='127.0.0.1:5565')

    # Take screenshot
    device.screenshot()

    # Perform OCR on a specific area
    ocr = OCR(area=(100, 100, 900, 200))  # Define text area
    text = ocr.ocr(device.image)

    logger.info(f'Recognized text: {text}')


def example_wait_and_click():
    """Example of waiting for a button and clicking it"""
    logger.hr('Wait and Click Example', level=0)

    device = Device(serial='127.0.0.1:5565')

    # Define button
    start_button = Button(
        area=(400, 800, 600, 900),
        color=(100, 200, 100),
        name='START_BUTTON'
    )

    # Wait up to 10 seconds for button to appear, then click
    if device.wait_until_appear_then_click(start_button, timeout=10):
        logger.info('Button found and clicked!')
    else:
        logger.info('Button did not appear within timeout')


if __name__ == '__main__':
    # Run examples
    try:
        example_basic_operations()
        # example_button_detection()
        # example_ocr()
        # example_wait_and_click()
    except Exception as e:
        logger.exception(f'Example failed: {e}')
