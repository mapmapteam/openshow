#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
OscAction
"""
from openshow import cue
from twisted.internet import defer

# TODO: add from_xml(node)
# TODO: add to_xml(node)
class OscAction(cue.Action):
    """
    OpenSoundControl action.
    """
    def __init__(self, host="localhost", port=31337, path="/default", args=[]):
        super(cue.Action, self).__init__()
        # Attributes:
        self._host = host
        self._port = port
        self._path = path
        self._args = args

    def __str__(self):
        return "%s(%s %s %s %s)" % (self.__class__.__name__,
                self._host, self._port, self._path, self._args)

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

    @defer.inlineCallbacks
    def execute(self):
        """
        @rtype: L{twisted.internet.defer.Deferred}
        """
        yield defer.succeed(None)
        print("OscAction.execute: TODO")
        defer.returnValue(None)
