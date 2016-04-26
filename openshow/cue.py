#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
A project contains cues. XML files are used to describe projects.
"""

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
    def __init__(self, identifier="", pre_wait=0.0, post_wait=0.0, title=""):
        self._identifier = identifier # or "Number"
        self._pre_wait = pre_wait
        self._post_wait = post_wait
        self._title = title
        self._continue = AUTO_CONTINUE

    def __str__(self):
        return "Cue(\"%s\" %s %s)" % (self._identifier, self._pre_wait,
                self._post_wait)

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
        raise NotImplementedError("Must be implemented in child classes.")

# TODO: add from_xml(node)
# TODO: add to_xml(node)


# TODO: move to cuetypes/osc.py
# TODO: add from_xml(node)
# TODO: add to_xml(node)
class OscCue(Cue):
    """
    OpenSoundControl cue.
    """
    def __init__(self, identifier="", pre_wait=0.0, post_wait=0.0,
            host="localhost", port=31337, path="/default", args=[]):
        super(OscCue, self).__init__(identifier, pre_wait, post_wait)
        self.set_title(path)
        # Attributes:
        self._host = host
        self._port = port
        self._path = path
        self._args = args

    def __str__(self):
        return "OscCue(\"%s\" %s %s %s %s)" % (self._identifier, self._host,
                self._port, self._path, self._args)

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port

    def get_path(self):
        return self._path

    def get_args(self):
        return self._args

    def set_host(self, value):
        self._host = str(value)

    def set_port(self, value):
        self._port = int(value)

    def set_path(self, value):
        self._path = str(value)

    def set_args(self, value):
        if type(value) != list:
            value = [value]
        self._args = value


class CueSheet(object):
    def __init__(self):
        self._cues = {}

    def set_cues(self, cues):
        """
        @param cues: Dict of cues.
        @type cues: C{dict}
        """
        self._cues = cues

    def get_cues(self):
        """
        @rtype: C{dict}
        """
        return self._cues.values()

    def add_cue(self, identifier, value):
        """
        @param identifier: Number/identifier for the cue.
        @type identifier: C{str}
        @type value: L{Cue}
        """
        self._cues[str(identifier)] = value

    def get_cue(self, identifier):
        """
        @param identifier: Number/identifier for the cue.
        @type identifier: C{str}
        @rtype: L{Cue}
        """
        for _cue in self._cues:
            if _cue.get_identifier() == identifier:
                return _cue
        return None
