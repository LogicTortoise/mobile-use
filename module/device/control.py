"""Device control methods"""
import time
import numpy as np

from module.logger import logger
from module.base.utils import random_rectangle_point, ensure_time
from module.base.timer import Timer


def point2str(x, y):
    """Convert point to string"""
    return f'({x}, {y})'


class Control:
    """Device control methods"""

    def click(self, button, control_name='CLICK'):
        """Click a button or point

        Args:
            button: Button object or tuple (x, y) or tuple (x1, y1, x2, y2)
            control_name (str): Name for logging
        """
        # Get click position
        if hasattr(button, 'button'):
            # Button object
            x, y = random_rectangle_point(button.button)
            name = str(button)
        elif len(button) == 4:
            # Area tuple (x1, y1, x2, y2)
            x, y = random_rectangle_point(button)
            name = control_name
        elif len(button) == 2:
            # Point tuple (x, y)
            x, y = button
            name = control_name
        else:
            raise ValueError(f'Invalid button format: {button}')

        x, y = int(x), int(y)
        logger.info(f'Click {point2str(x, y)} @ {name}')

        # Execute click
        try:
            self._click_uiautomator2(x, y)
        except Exception as e:
            logger.warning(f'uiautomator2 click failed: {e}, trying ADB')
            self._click_adb(x, y)

    def _click_uiautomator2(self, x, y):
        """Click using uiautomator2"""
        self.u2.click(x, y)

    def _click_adb(self, x, y):
        """Click using ADB input tap"""
        self.adb_shell(f'input tap {x} {y}')

    def long_click(self, button, duration=1.0, control_name='LONG_CLICK'):
        """Long click a button or point

        Args:
            button: Button object or tuple (x, y) or tuple (x1, y1, x2, y2)
            duration (float): Click duration in seconds
            control_name (str): Name for logging
        """
        # Get click position
        if hasattr(button, 'button'):
            x, y = random_rectangle_point(button.button)
            name = str(button)
        elif len(button) == 4:
            x, y = random_rectangle_point(button)
            name = control_name
        elif len(button) == 2:
            x, y = button
            name = control_name
        else:
            raise ValueError(f'Invalid button format: {button}')

        x, y = int(x), int(y)
        duration = ensure_time(duration)
        logger.info(f'Long click {point2str(x, y)} @ {name}, duration={duration}s')

        # Execute long click using swipe
        self.swipe((x, y), (x, y), duration=duration, name=name)

    def swipe(self, p1, p2, duration=0.2, name='SWIPE'):
        """Swipe from p1 to p2

        Args:
            p1 (tuple): Start point (x, y)
            p2 (tuple): End point (x, y)
            duration (float): Swipe duration in seconds
            name (str): Name for logging
        """
        p1 = (int(p1[0]), int(p1[1]))
        p2 = (int(p2[0]), int(p2[1]))
        duration = ensure_time(duration)

        # Check swipe distance
        distance = np.linalg.norm(np.subtract(p1, p2))
        if distance < 10:
            logger.info(f'Swipe distance {distance:.1f}px < 10px, dropped')
            return

        logger.info(f'{name} {point2str(*p1)} -> {point2str(*p2)}, duration={duration}s')

        try:
            self._swipe_uiautomator2(p1, p2, duration)
        except Exception as e:
            logger.warning(f'uiautomator2 swipe failed: {e}, trying ADB')
            self._swipe_adb(p1, p2, duration)

    def _swipe_uiautomator2(self, p1, p2, duration):
        """Swipe using uiautomator2"""
        self.u2.swipe(p1[0], p1[1], p2[0], p2[1], duration)

    def _swipe_adb(self, p1, p2, duration):
        """Swipe using ADB input swipe"""
        duration_ms = int(duration * 1000)
        self.adb_shell(f'input swipe {p1[0]} {p1[1]} {p2[0]} {p2[1]} {duration_ms}')

    def swipe_vector(self, vector, box=(0, 0, 1920, 1080), duration=0.2, name='SWIPE'):
        """Swipe with a vector within a box

        Args:
            vector (tuple): Swipe vector (dx, dy)
            box (tuple): Swipe within this box (x1, y1, x2, y2)
            duration (float): Swipe duration
            name (str): Name for logging
        """
        # Calculate start and end points
        vector = np.array(vector)
        half_vector = vector // 2

        # Get safe start area
        safe_area = (
            box[0] + abs(half_vector[0]),
            box[1] + abs(half_vector[1]),
            box[2] - abs(half_vector[0]),
            box[3] - abs(half_vector[1])
        )

        # Random start point
        start = random_rectangle_point(safe_area)
        end = (start[0] + vector[0], start[1] + vector[1])

        self.swipe(start, end, duration=duration, name=name)

    def drag(self, p1, p2, duration=0.5, name='DRAG'):
        """Drag from p1 to p2 (same as swipe but with longer duration)

        Args:
            p1 (tuple): Start point (x, y)
            p2 (tuple): End point (x, y)
            duration (float): Drag duration in seconds
            name (str): Name for logging
        """
        self.swipe(p1, p2, duration=duration, name=name)

    def sleep(self, seconds):
        """Sleep for a specified time

        Args:
            seconds (float, tuple): Sleep duration or range (min, max)
        """
        seconds = ensure_time(seconds)
        if seconds > 0:
            time.sleep(seconds)
