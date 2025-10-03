"""ADB connection management"""
import time
from functools import wraps

import uiautomator2 as u2
from adbutils import AdbClient, AdbDevice
from adbutils.errors import AdbError

from module.logger import logger
from module.exception import *


RETRY_TRIES = 3


def retry(func):
    """Retry decorator for ADB operations"""
    @wraps(func)
    def retry_wrapper(self, *args, **kwargs):
        for attempt in range(RETRY_TRIES):
            try:
                if attempt > 0:
                    time.sleep(attempt * 1.0)
                    logger.info(f'Retry {func.__name__}() attempt {attempt + 1}/{RETRY_TRIES}')
                return func(self, *args, **kwargs)
            except ConnectionResetError as e:
                logger.error(f'Connection reset: {e}')
                if attempt < RETRY_TRIES - 1:
                    self.adb_reconnect()
            except AdbError as e:
                logger.error(f'ADB error: {e}')
                if attempt < RETRY_TRIES - 1:
                    self.adb_reconnect()
            except Exception as e:
                logger.exception(e)
                if attempt >= RETRY_TRIES - 1:
                    raise

        logger.critical(f'Retry {func.__name__}() failed after {RETRY_TRIES} attempts')
        raise RequestHumanTakeover

    return retry_wrapper


class Connection:
    def __init__(self, serial='127.0.0.1:5565'):
        """
        Initialize ADB connection

        Args:
            serial (str): Device serial number, e.g. '127.0.0.1:5565'
        """
        self.serial = serial
        self.adb_client = None
        self.adb = None
        self.u2 = None

        # Connect
        self.adb_connect()
        logger.attr('Device', self.serial)

    def adb_connect(self):
        """Connect to ADB device"""
        try:
            # Initialize ADB client
            self.adb_client = AdbClient(host="127.0.0.1", port=5037)

            # Check if device is already connected
            devices = self.adb_client.device_list()
            if not any(d.serial == self.serial for d in devices):
                # Connect to device
                logger.info(f'Connecting to {self.serial}')
                self.adb_client.connect(self.serial)
                time.sleep(1.0)

            # Get ADB device
            self.adb = self.adb_client.device(self.serial)
            logger.info(f'Connected to {self.serial}')

            # Initialize uiautomator2
            self.u2 = u2.connect(self.serial)
            logger.info('uiautomator2 initialized')

        except Exception as e:
            logger.error(f'Failed to connect to {self.serial}: {e}')
            raise EmulatorNotRunningError(f'Device {self.serial} not found or not running')

    def adb_reconnect(self):
        """Reconnect to ADB device"""
        logger.info('Reconnecting to device')
        try:
            self.adb_connect()
        except Exception as e:
            logger.error(f'Reconnect failed: {e}')
            raise

    @retry
    def adb_shell(self, cmd):
        """Execute ADB shell command

        Args:
            cmd (str, list): Command to execute

        Returns:
            str: Command output
        """
        if isinstance(cmd, list):
            cmd = ' '.join(cmd)

        result = self.adb.shell(cmd)
        return result

    def is_connected(self):
        """Check if device is connected"""
        try:
            devices = self.adb_client.device_list()
            return any(d.serial == self.serial for d in devices)
        except Exception as e:
            logger.error(f'Check connection failed: {e}')
            return False
