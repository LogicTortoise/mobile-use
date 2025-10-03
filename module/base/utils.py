"""Utility functions for image processing and geometric calculations"""
import random
import cv2
import numpy as np
from PIL import Image


def random_normal_distribution_int(a, b, n=3):
    """
    Generate a normal distribution int within the interval.

    Args:
        a (int): The minimum of the interval.
        b (int): The maximum of the interval.
        n (int): The amount of numbers in simulation. Default to 3.

    Returns:
        int
    """
    a = round(a)
    b = round(b)
    if a < b:
        total = sum(random.randint(a, b) for _ in range(n))
        return round(total / n)
    else:
        return b


def random_rectangle_point(area, n=3):
    """Choose a random point in an area.

    Args:
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        n (int): The amount of numbers in simulation. Default to 3.

    Returns:
        tuple(int): (x, y)
    """
    x = random_normal_distribution_int(area[0], area[2], n=n)
    y = random_normal_distribution_int(area[1], area[3], n=n)
    return x, y


def area_offset(area, offset):
    """
    Move an area.

    Args:
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        offset: (x, y).

    Returns:
        tuple: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
    """
    x, y = offset
    return area[0] + x, area[1] + y, area[2] + x, area[3] + y


def area_pad(area, pad=10):
    """
    Inner offset an area.

    Args:
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
        pad (int):

    Returns:
        tuple: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).
    """
    return area[0] + pad, area[1] + pad, area[2] - pad, area[3] - pad


def crop(image, area):
    """
    Crop image by area.

    Args:
        image: np.ndarray or PIL.Image
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).

    Returns:
        np.ndarray: Cropped image.
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    x1, y1, x2, y2 = area
    return image[y1:y2, x1:x2].copy()


def get_color(image, area):
    """
    Get the color of a button area.

    Args:
        image: Screenshot. (np.ndarray)
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).

    Returns:
        tuple: (r, g, b)
    """
    temp = crop(image, area)
    color = cv2.mean(temp)[:3]
    color = tuple(np.array(color).astype(int))
    return color


def color_similar(color1, color2, threshold=10):
    """
    Check if two colors are similar.

    Args:
        color1: (r, g, b).
        color2: (r, g, b).
        threshold (int): Default to 10.

    Returns:
        bool: True if two colors are similar.
    """
    return np.linalg.norm(np.array(color1) - np.array(color2)) < threshold


def color_similar_1d(im1, im2, threshold=10):
    """
    Check if two colors are similar in 1-dimensional image.

    Args:
        im1: (np.ndarray) shape (n,)
        im2: (np.ndarray) shape (n,)
        threshold (int): Default to 10.

    Returns:
        bool: True if two colors are similar.
    """
    return np.linalg.norm(im1 - im2) < threshold


def ensure_time(second, n=3, precision=3):
    """Ensure to be time.

    Args:
        second (int, float, tuple): time, such as 10, (10, 30), '10, 30'
        n (int): The amount of numbers in simulation. Default to 3.
        precision (int): Decimals.

    Returns:
        float:
    """
    if isinstance(second, tuple):
        multiply = 10 ** precision
        result = random_normal_distribution_int(second[0] * multiply, second[1] * multiply, n) / multiply
        return round(result, precision)
    elif isinstance(second, str):
        if ',' in second:
            lower, upper = second.replace(' ', '').split(',')
            return ensure_time((int(lower), int(upper)), n=n, precision=precision)
        elif '-' in second:
            lower, upper = second.replace(' ', '').split('-')
            return ensure_time((int(lower), int(upper)), n=n, precision=precision)
        else:
            return int(second)
    else:
        return second


def limit_in(x, lower, upper):
    """
    Limit x within range (lower, upper)
    """
    return max(min(x, upper), lower)


def point_limit(point, area):
    """
    Limit point in an area.

    Args:
        point: (x, y).
        area: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y).

    Returns:
        tuple: (x, y).
    """
    return (
        limit_in(point[0], area[0], area[2]),
        limit_in(point[1], area[1], area[3])
    )


def image_size(image):
    """
    Get image size

    Args:
        image: np.ndarray

    Returns:
        tuple: (width, height)
    """
    if isinstance(image, Image.Image):
        return image.size
    else:
        return image.shape[1], image.shape[0]


def load_image(file):
    """
    Load image from file.

    Args:
        file: file path.

    Returns:
        np.ndarray
    """
    return np.array(Image.open(file))
