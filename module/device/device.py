"""Main Device class integrating connection, screenshot, and control"""
from module.device.connection import Connection
from module.device.screenshot import Screenshot
from module.device.control import Control
from module.logger import logger


class Device(Connection, Screenshot, Control):
    """Main device class for mobile automation

    Integrates:
    - Connection: ADB connection management
    - Screenshot: Screenshot capture
    - Control: Touch and swipe controls
    """

    def __init__(self, serial='127.0.0.1:5565'):
        """
        Initialize device

        Args:
            serial (str): Device serial, e.g. '127.0.0.1:5565'
        """
        logger.hr('Device Init', level=0)

        # Initialize connection
        Connection.__init__(self, serial=serial)

        # Initialize screenshot
        Screenshot.__init__(self)

        # Initialize control
        Control.__init__(self)

        logger.info('Device initialized successfully')

    def appear(self, button, threshold=10):
        """Check if a button appears on screen

        Args:
            button: Button object with area and color
            threshold (int): Color similarity threshold

        Returns:
            bool: True if button appears
        """
        if self.image is None:
            self.screenshot()

        return button.appear_on(self.image, threshold=threshold)

    def appear_then_click(self, button, threshold=10, interval=0.5):
        """Check if button appears and click it

        Args:
            button: Button object
            threshold (int): Color similarity threshold
            interval (float): Wait interval after click

        Returns:
            bool: True if button appeared and was clicked
        """
        if self.appear(button, threshold=threshold):
            self.click(button)
            self.sleep(interval)
            return True
        return False

    def wait_until_appear(self, button, timeout=10, interval=1.0):
        """Wait until button appears

        Args:
            button: Button object
            timeout (float): Max wait time in seconds
            interval (float): Check interval in seconds

        Returns:
            bool: True if button appeared within timeout
        """
        from module.base.timer import Timer

        timer = Timer(timeout).start()
        while not timer.reached():
            self.screenshot()
            if self.appear(button):
                return True
            self.sleep(interval)

        return False

    def wait_until_appear_then_click(self, button, timeout=10, interval=1.0):
        """Wait until button appears and click it

        Args:
            button: Button object
            timeout (float): Max wait time
            interval (float): Check interval

        Returns:
            bool: True if button appeared and was clicked
        """
        if self.wait_until_appear(button, timeout=timeout, interval=interval):
            self.click(button)
            return True
        return False
