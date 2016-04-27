#!/usr/bin/env python
"""
The Sequencer class.

Every time twisted goes to sleep, it computes a wake-up time from the delta of
the desired time of the head of the list and the current time.
Every time it wakes up, it does whatever work is at or before the present time.
"""


class Sequencer(object):
    def __init__(self, cue_sheet):
        pass
