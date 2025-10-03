"""Screenshot methods"""
import io
import time
import numpy as np
from PIL import Image

from module.logger import logger
from module.exception import ScreenshotError


class Screenshot:
    """Screenshot management"""

    _screenshot_interval = 0.3
    _screenshot_last = 0
    image = None

    def screenshot(self):
        """Take a screenshot

        Returns:
            np.ndarray: Screenshot image
        """
        # Rate limiting
        now = time.time()
        if now - self._screenshot_last < self._screenshot_interval:
            time.sleep(self._screenshot_interval - (now - self._screenshot_last))

        self._screenshot_last = time.time()

        # Try different screenshot methods
        try:
            # Method 1: uiautomator2 screenshot
            image = self._screenshot_uiautomator2()
            if image is not None:
                self.image = image
                return image
        except Exception as e:
            logger.warning(f'uiautomator2 screenshot failed: {e}')

        try:
            # Method 2: ADB screenshot
            image = self._screenshot_adb()
            if image is not None:
                self.image = image
                return image
        except Exception as e:
            logger.warning(f'ADB screenshot failed: {e}')

        raise ScreenshotError('All screenshot methods failed')

    def _screenshot_uiautomator2(self):
        """Screenshot using uiautomator2

        Returns:
            np.ndarray: Screenshot image
        """
        try:
            # Get screenshot from uiautomator2
            screenshot = self.u2.screenshot(format='pillow')
            if screenshot is None:
                return None

            # Convert to numpy array
            image = np.array(screenshot)
            return image
        except Exception as e:
            logger.debug(f'uiautomator2 screenshot error: {e}')
            return None

    def _screenshot_adb(self):
        """Screenshot using ADB screencap

        Returns:
            np.ndarray: Screenshot image
        """
        try:
            # Method 1: Use screencap and pull
            import tempfile
            import os
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                temp_path = f.name

            try:
                # Take screenshot on device
                remote_path = '/sdcard/screenshot.png'
                self.adb_shell(f'screencap -p {remote_path}')

                # Pull screenshot
                self.adb.sync.pull(remote_path, temp_path)

                # Clean up remote file
                self.adb_shell(f'rm {remote_path}')

                # Load image
                image = Image.open(temp_path)
                image = np.array(image)

                # Clean up local file
                os.unlink(temp_path)

                return image
            except Exception as e:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                raise e

        except Exception as e:
            logger.debug(f'ADB screenshot error: {e}')
            return None

    def save_screenshot(self, filename):
        """Save current screenshot to file

        Args:
            filename (str): File path to save
        """
        if self.image is not None:
            Image.fromarray(self.image).save(filename)
            logger.info(f'Screenshot saved to {filename}')
        else:
            logger.warning('No screenshot to save')
