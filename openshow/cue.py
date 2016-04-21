#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
A project contains cues. XML files are used to describe projects.
"""

class Cue(object):
    """
    Cue.
    """
    def __init__(self, identifier="", pre_wait=0.0, post_wait=0.0):
        self._identifier = identifier
        self._pre_wait = pre_wait
        self._post_wait = post_wait

    def __str__(self):
        return "Cue(\"%s\" %s %s)" % (self._identifier, self._pre_wait,
                self._post_wait)

    def get_identifier(self):
        return self._identifier

    def get_pre_wait(self):
        return self._pre_wait

    def get_post_wait(self):
        return self._post_wait

    def set_identifier(self, value):
        self._identifier = value

    def set_pre_wait(self, value):
        self._pre_wait = value

    def set_post_wait(self, value):
        self._post_wait = value


class OscCue(Cue):
    """
    OpenSoundControl cue.
    """
    def __init__(self, identifier="", pre_wait=0.0, post_wait=0.0,
            host="localhost", port=31337, path="/default", args=[]):
        super(OscCue, self).__init__(identifier, pre_wait, post_wait)
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
        self._host = value

    def set_port(self, value):
        self._port = value

    def set_path(self, value):
        self._path = value

    def set_args(self, value):
        self._args = value


class CueSheet(object):
    def __init__(self):
        self._cues = {}

    def set_cues(self, cues):
        self._cues = cues

    def get_cues(self):
        return self._cues.values()

    def add_cue(self, identifier, value):
        self._cues[identifier] = value

    def get_cue(self, identifier):
        for _cue in self._cues:
            if _cue.get_identifier() == identifier:
                return _cue
        return None
