#!/usr/bin/env python
"""
The Timer class.
"""
import time


class Timer(object):
    """
    Measures how much time passed since reset.
    """
    def __init__(self):
        self._started = 0.0
        self.reset()

    def reset(self):
        """
        Resets the timer.
        """
        self._started = self._now()

    def elapsed(self):
        """
        Returns elapsed time in seconds.
        @rtype: C{float}
        """
        ret = self._now() - self._started
        return ret

    def _now(self):
        return time.time()

    def __str__(self):
        """
        Readable representation of the elapsed time.
        """
        hours, rem = divmod(self.elapsed(), 3600.0)
        minutes, rem = divmod(rem, 60.0)
        seconds, ms = divmod(rem, 1.0)
        ms = ms * 1000
        return "{:0>2}h:{:0>2}m:{:0>2}s.{:0>3}".format(
                int(hours), int(minutes), int(seconds), int(ms))


if __name__ == '__main__':
    t = Timer()
    time.sleep(1.0)
    print(str(t))
