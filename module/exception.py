"""Custom exceptions for mobile-use automation"""


class DeviceException(Exception):
    """Base exception for device errors"""
    pass


class EmulatorNotRunningError(DeviceException):
    """Emulator is not running"""
    pass


class DeviceNotFoundError(DeviceException):
    """Device not found"""
    pass


class ConnectionError(DeviceException):
    """Connection error"""
    pass


class GameStuckError(Exception):
    """Game appears to be stuck"""
    pass


class GameTooManyClickError(Exception):
    """Too many clicks detected"""
    pass


class RequestHumanTakeover(Exception):
    """Request human intervention"""
    pass


class ScriptError(Exception):
    """Script execution error"""
    pass


class ScreenshotError(DeviceException):
    """Screenshot failed"""
    pass
