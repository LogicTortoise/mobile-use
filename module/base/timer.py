import time
from datetime import datetime, timedelta
from functools import wraps


def timer(function):
    """Decorator to time function execution"""
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('%s: %s s' % (function.__name__, str(round(t1 - t0, 10))))
        return result
    return function_timer


class Timer:
    def __init__(self, limit, count=0):
        """
        Args:
            limit (int, float): Timer limit in seconds
            count (int): Timer reach confirm count. Default to 0.
        """
        self.limit = limit
        self.count = count
        self._current = 0
        self._reach_count = count

    def start(self):
        """Start the timer"""
        if not self.started():
            self._current = time.time()
            self._reach_count = 0
        return self

    def started(self):
        """Check if timer has started"""
        return bool(self._current)

    def current(self):
        """Get current elapsed time"""
        if self.started():
            return time.time() - self._current
        else:
            return 0.

    def reached(self):
        """Check if timer has reached the limit"""
        self._reach_count += 1
        return time.time() - self._current > self.limit and self._reach_count > self.count

    def reset(self):
        """Reset the timer"""
        self._current = time.time()
        self._reach_count = 0
        return self

    def clear(self):
        """Clear the timer"""
        self._current = 0
        self._reach_count = self.count
        return self

    def reached_and_reset(self):
        """Check if reached and reset if true"""
        if self.reached():
            self.reset()
            return True
        else:
            return False

    def wait(self):
        """Wait until timer reaches limit"""
        diff = self._current + self.limit - time.time()
        if diff > 0:
            time.sleep(diff)

    def __str__(self):
        return f'Timer(limit={round(self.current(), 3)}/{self.limit}, count={self._reach_count}/{self.count})'

    __repr__ = __str__
