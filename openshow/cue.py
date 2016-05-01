#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
A project contains cues. XML files are used to describe projects.
"""
from openshow import sig
from openshow import timer
from twisted.internet import defer
from twisted.internet import reactor

AUTO_CONTINUE = "auto-continue"
AUTO_FOLLOW = "auto-follow"
DO_NOT_CONTINUE = "no-continue"


class Cue(object):
    """
    Cue.

    Each cue has a identifier - its number - that is usually a number,
    sometimes with decimals, but can be any string. They must be unique within
    a cue sheet.

    Cues can have a pre-wait delay, and a post-wait delay.
    Post-wait delay is only useful if in AUTO_CONTINUE continue mode.
    """
    def __init__(self, identifier="", pre_wait=0.0, post_wait=0.0, title="",
            action=None):
        self._identifier = identifier # or "Number"
        self._pre_wait = pre_wait
        self._post_wait = post_wait
        self._title = title
        self._continue = AUTO_CONTINUE
        self._delayed_call_pre_wait  = None
        self._delayed_call_post_wait = None
        self._timer_pre_wait = timer.Timer()
        self._timer_post_wait = timer.Timer()
        self._action = action

        # Public attributes:
        self.signal_go = sig.Signal() # param: self
        self.signal_done_trigger = sig.Signal() # param: self
        self.signal_done_pre_wait = sig.Signal() # param: self
        self.signal_done_post_wait = sig.Signal() # param: self
        self.signal_cancelled = sig.Signal() # param: self

    def set_action(self, action):
        self._action = action

    def get_action(self):
        return self._action

    def go(self):
        self.signal_go(self)
        self._timer_pre_wait.reset()
        if self._pre_wait == 0.0:
            self._do_trigger()
        else:
            self._delayed_call_pre_wait = reactor.callLater(self._pre_wait,
                    self._do_trigger)

    def cancel(self):
        if self._delayed_call_pre_wait is not None:
            self._delayed_call_pre_wait.cancel()
        if self._delayed_call_post_wait is not None:
            self._delayed_call_post_wait.cancel()
        self.signal_cancelled(self)

    def _do_trigger(self):
        self.signal_done_pre_wait(self)
        self.trigger()
        self._delayed_call_pre_wait = None
        self._timer_post_wait.reset()
        if self._post_wait == 0.0:
            self._done_post_wait()
        else:
            self._delayed_call_post_wait = reactor.callLater(self._post_wait,
                    self._done_post_wait)

    def get_elapsed_pre_wait(self):
        """
        @rtype: C{float}
        """
        if self.is_pre_waiting():
            return self._timer_pre_wait.elapsed()
        else:
            print("pre-wait is not running")
            return 0.0

    def get_elapsed_post_wait(self):
        """
        @rtype: C{float}
        """
        if self.is_post_waiting():
            return self._timer_post_wait.elapsed()
        else:
            print("post-wait is not running")
            return 0.0

    def is_pre_waiting(self):
        """
        @rtype: C{bool}
        """
        return self._delayed_call_pre_wait is not None

    def is_post_waiting(self):
        """
        @rtype: C{bool}
        """
        return self._delayed_call_post_wait is not None

    def _done_post_wait(self):
        self.signal_done_post_wait(self)
        self._delayed_call_post_wait = None

    def __str__(self):
        return "Cue(\"%s\" \"%s\" %s %s): %s" % (self._identifier, self._title,
                self._pre_wait, self._post_wait, self._action)

    def get_identifier(self):
        return self._identifier

    def get_pre_wait(self):
        return self._pre_wait

    def get_post_wait(self):
        return self._post_wait

    def get_title(self):
        return self._title

    def get_continue(self):
        return self._continue

    def set_identifier(self, value):
        self._identifier = value

    def set_pre_wait(self, value):
        self._pre_wait = float(value)

    def set_post_wait(self, value):
        self._post_wait = float(value)

    def set_title(self, value):
        self._title = str(value)

    def set_continue(self, value):
        self._continue = value

    def trigger(self):
        """
        @rtype: L{twisted.internet.defer.Deferred}
        """
        if self._action is None:
            return defer.succeed(None)
        else:
            return self._action.execute()


class Action(object):
    def __init__(self):
        pass
    
    def execute(self):
        return defer.succeed(None)


# TODO: add from_xml(node)
# TODO: add to_xml(node)


class CueSheet(object):
    """
    A Cue sheet is a list of Cues.
    """
    def __init__(self):
        self._cues = []
        self._active_index = 0

    def get_active_cue_index(self):
        """
        Returns the index of the current active cue.
        @rtype value: C{int}
        """
        return self._active_index

    def select_next_cue(self):
        """
        Selects the next cue after the active one.
        @rtype value: C{bool}
        """
        if self._active_index < self.get_size():
            self._active_index = self._active_index + 1
            return True
        else:
            # print("No more cues.")
            return False

    def set_cues(self, cues):
        """
        @param cues: Dict of cues.
        @type cues: C{list}
        """
        self._cues = cues

    def get_cues(self):
        """
        @rtype: C{list}
        """
        return self._cues

    def append_cue(self, value):
        """
        @param identifier: Number/identifier for the cue.
        @type value: L{Cue}
        """
        self._cues.append(value)

    def get_cue_by_identifier(self, identifier):
        """
        Get cue by identifier. (Number)
        @param identifier: Number/identifier for the cue.
        @type identifier: C{str}
        @rtype: L{Cue}
        @raise: L{RuntimeError}
        """
        for _cue in self._cues:
            if _cue.get_identifier() == identifier:
                return _cue
        raise RuntimeError("No such cue %s" % (identifier))
        # return None
    
    def get_size(self):
        """
        @rtype: C{int}
        """
        return len(self._cues)
    
    def get_cue_by_index(self, index):
        """
        Get cue by index.
        @type index: C{int}
        @raise: L{RuntimeError}
        @rtype: L{Cue}
        """
        if index >= self.get_size():
            raise RuntimeError("No cue for index %s" % (index))
        else:
            return self._cues[index]
