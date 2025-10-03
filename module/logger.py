import logging
import sys

# Configure logger
logger = logging.getLogger('mobile-use')
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler('mobile-use.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def hr(title='', level=0):
    """Print horizontal rule with title"""
    length = 60
    if level == 0:
        logger.info('=' * length)
        if title:
            logger.info(f' {title} '.center(length, '='))
            logger.info('=' * length)
    elif level == 1:
        logger.info('-' * length)
        if title:
            logger.info(f' {title} '.center(length, '-'))
            logger.info('-' * length)
    else:
        if title:
            logger.info(title)


def attr(key, value):
    """Log attribute"""
    logger.info(f'{key}: {value}')


# Add hr and attr methods to logger
logger.hr = hr
logger.attr = attr
