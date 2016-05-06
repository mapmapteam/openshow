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
        self._deferred = None
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
        """
        @rtype: L{openshow.cue.Action}
        """
        return self._action

    def go(self):
        """
        Starts the pre-wait timer, then execute its actions,
        and then starts the post-wait timer.

        @return: A Deferred whose result is True if done normally,
        False if cancelled.
        @rtype: L{twisted.internet.defer.Deferred}
        """
        self._deferred = defer.Deferred()
        self.signal_go(self)
        self._timer_pre_wait.reset()
        if self._pre_wait == 0.0:
            self._do_after_pre_wait()
        else:
            self._delayed_call_pre_wait = reactor.callLater(self._pre_wait,
                    self._do_after_pre_wait)
        return self._deferred

    def cancel(self):
        if self._delayed_call_pre_wait is not None:
            self._delayed_call_pre_wait.cancel()
        if self._delayed_call_post_wait is not None:
            self._delayed_call_post_wait.cancel()
        if self._callback_deferred is not None:
            self.signal_cancelled(self)
            done_normally = False
            self._callback_deferred(done_normally)
            self._callback_deferred = None

    @defer.inlineCallbacks
    def _do_after_pre_wait(self):
        """
        After the pre_wait (if any)
        Executes its actions.
        """
        self.signal_done_pre_wait(self)
        yield self._do_execute()
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
            # FIXME: return the total pre-wait if done
            print("pre-wait is not running")
            return 0.0

    def get_elapsed_post_wait(self):
        """
        @rtype: C{float}
        """
        if self.is_post_waiting():
            return self._timer_post_wait.elapsed()
        else:
            # FIXME: return the total post-wait if done
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
        self._callback_deferred()

    def _callback_deferred(self, done_normally=True):
        self._deferred.callback(done_normally)

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

    def _do_execute(self):
        """
        @rtype: L{twisted.internet.defer.Deferred}
        """
        if self._action is None:
            return defer.succeed(None)
        else:
            return self._action.execute()


class Action(object):
    def __init__(self):
        self._attributes = {}

    def execute(self):
        return defer.succeed(None)

    def set_attribute(self, name, value):
        self._attributes[name] = value

    def get_attribute(self, name):
        return self._attributes[name]

    def has_attribute(self, name):
        return name in self._attributes

    # TODO: add type support
    def _add_attribute(self, name, default):
        self.set_attribute(name, default)

    def get_type(self):
        return None
# TODO: add from_xml(node)
# TODO: add to_xml(node)


class CueSheet(object):
    """
    A Cue sheet is a list of Cues.
    """
    def __init__(self):
        self._cues = []
        # self._selected_index = 0
        self._selected_identifier = ""
        self._is_running = False

    def go(self):
        """
        @rtype: L{twisted.internet.defer.Deferred}
        """
        identifier = self.get_selected_cue_identifier()
        _cue = self.get_cue_by_identifier(identifier)
        self._go_cue(_cue)

    @defer.inlineCallbacks
    def _go_cue(self, cue_item):
        # TODO: use the signals, not the deferreds, in order to trigger next
        yield cue_item.go()
        next_cue = self.get_cue_after(cue_item.get_identifier())
        if next_cue is not None:
            self._go_cue(next_cue)

    def stop(self):
        if self._is_running:
            self._is_running = False
            for _cue in self._cues:
                _cue.cancel()

    def get_selected_cue_index(self):
        """
        Returns the index of the current selected cue.
        @rtype value: C{int}
        """
        identifier = self.get_selected_cue_identifier()
        if identifier == "":
            return -1
        else:
            return self.get_cue_index(identifier)

    def get_selected_cue_identifier(self):
        """
        Returns the identifier of the current selected cue.
        @rtype value: C{str}
        """
        if self._selected_identifier == "":
            return "" # FIXME
        return self._selected_identifier

    def rename_cue(self, identifier, new_identifier):
        raise NotImplementedError("TODO")
        return False

    def select_cue(self, identifier):
        raise NotImplementedError("TODO")

    def get_cue_after(self, identifier):
        index = self.get_cue_index(identifier)
        if index < self.get_size():
            index = index + 1
            try:
                next_cue = self.get_cue_by_index(index)
                return next_cue
            except RuntimeError:
                return None
        else:
            # print("No more cues.")
            return None

    def get_cue_before(self, identifier):
        raise NotImplementedError("TODO")

    def generate_name_for_cue_after(self, identifier):
        raise NotImplementedError("TODO")

    def _select_next_cue(self):
        """
        Selects the next cue after the current one.
        @rtype value: C{bool}
        """
        selected_index = self.get_selected_cue_index()
        if selected_index < self.get_size():
            selected_index = selected_index + 1
            item = self.get_cue_by_index(selected_index)
            self.select_cue(item.get_identifier())
            return True
        else:
            # print("No more cues.")
            return False

    def set_cues(self, cues):
        """
        @param cues: Dict of cues.
        @type cues: C{list}
        """
        for item in cues:
            self.append_cue(item)
        # self._cues = cues

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
        was_empty = False
        if len(self._cues) == 0:
            was_empty = True
        self._cues.append(value)
        if was_empty:
            self._selected_identifier = value.get_identifier()

    def insert_cue(self, value):
        # TODO: check current selected cue and change it accordingly
        # TODO: check if identifier already exists
        raise NotImplementedError("TODO")

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

    def get_cue_index(self, identifier):
        """
        Returns the index of a cue, given its identifier.
        @rtype: C{int}
        @raise: RuntimeError
        @type identifier: C{str}
        """
        for i in range(len(self._cues)):
            _cue = self._cues[i]
            if _cue.get_identifier() == identifier:
                return i
        raise RuntimeError("No such cue %s" % (identifier))

    def has_cue(self, identifier):
        """
        @rtype: C{bool}
        """
        try:
            self.get_cue_by_identifier(identifier)
            return True
        except RuntimeError:
            return False

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

    def is_running(self):
        return self._is_running
