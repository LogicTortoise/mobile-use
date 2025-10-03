"""Button class for UI element detection and interaction"""
import os
import numpy as np
from module.base.utils import *


class Button:
    def __init__(self, area, color=(), button=None, file=None, name=None):
        """Initialize a Button instance.

        Args:
            area (tuple): Area that the button would appear on the image.
                          (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
            color (tuple): Color we expect the area would be.
                           (r, g, b)
            button (tuple): Area to be click if button appears on the image.
                            (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
                            If None, use area as button.
            file (str): Path to template image file.
            name (str): Button name for logging.

        Examples:
            BUTTON_START = Button(
                area=(100, 200, 200, 300),
                color=(231, 181, 90),
                button=(100, 200, 200, 300)
            )
        """
        self.area = area
        self.color = color
        self._button = button if button is not None else area
        self.file = file
        self.name = name or self._get_name()
        self.image = None

    def _get_name(self):
        """Get button name from file or use default"""
        if self.file:
            return os.path.splitext(os.path.basename(self.file))[0]
        return 'BUTTON'

    def __str__(self):
        return self.name

    __repr__ = __str__

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.name)

    def __bool__(self):
        return True

    @property
    def button(self):
        """Get clickable area"""
        return self._button

    def appear_on(self, image, threshold=10):
        """Check if the button appears on the image.

        Args:
            image (np.ndarray): Screenshot.
            threshold (int): Default to 10.

        Returns:
            bool: True if button appears on screenshot.
        """
        if not self.color:
            return False
        return color_similar(
            color1=get_color(image, self.area),
            color2=self.color,
            threshold=threshold
        )

    def load_color(self, image):
        """Load color from the specific area of the given image.

        Args:
            image: Screenshot.

        Returns:
            tuple: Color (r, g, b).
        """
        self.color = get_color(image, self.area)
        self.image = crop(image, self.area)
        return self.color

    def match_template(self, image, threshold=0.85):
        """Match template on image using OpenCV.

        Args:
            image (np.ndarray): Screenshot.
            threshold (float): Match threshold, 0-1.

        Returns:
            bool: True if template matched.
        """
        if self.file is None:
            return False

        if self.image is None:
            self.image = load_image(self.file)

        import cv2
        result = cv2.matchTemplate(image, self.image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        return max_val >= threshold
