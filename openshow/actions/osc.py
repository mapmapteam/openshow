#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
OscAction
"""
from openshow import cue
from twisted.internet import defer
from twisted.internet import reactor
from txosc import osc
from txosc import async


def send_async_udp(message, port, host):
    """
    Sends a message using UDP.

    @param message: OSC message
    @type message: L{txosc.osc.Message}
    @type port: C{int}
    @type host: C{str}
    """
    # TODO: support explicit type tags
    client = async.DatagramClientProtocol()
    _client_port = reactor.listenUDP(0, client)
    client.send(message, (host, port))
    defer.succeed(None) # FIXME: there is no way to actually wait for when done

def send_async_tcp(message, port, host):
    """
    Is this working at all?
    """
    client = async.ClientFactory()
    _client_port = None
    d = defer.Deferred()

    def _callback(result):
        # print("Connected.")
        client.send(message)
        # print("Sent %s to %s:%d" % (message, host, port))
        reactor.callLater(0.001, d.callback(None))

    def _errback(reason):
        # print("An error occurred: %s" % (reason.getErrorMessage()))
        pass
        reactor.callLater(0.001, d.callback(None))

    _client_port = reactor.connectTCP(host, port, client)
    client.deferred.addCallback(_callback)
    client.deferred.addErrback(_errback)
    return d


def create_message_auto(path, *args):
    """
    Trying to guess the type tags.
    """
    message = osc.Message(path)
    for arg in args:
        if type(arg) == int:
            value = arg
        elif type(arg) == float:
            value = arg
        elif type(arg) == str:
            # TODO: check for quotes
            try:
                value = int(arg)
            except ValueError:
                try:
                    value = float(arg)
                except ValueError:
                    value = str(arg)
        message.add(value)
    return message


# TODO: add from_xml(node)
# TODO: add to_xml(node)
class OscAction(cue.Action):
    """
    OpenSoundControl action.
    """
    def __init__(self, host="localhost", port=31337, path="/default", args=[]):
        super(OscAction, self).__init__()
        # Attributes:
        self._add_attribute("host", host)
        self._add_attribute("port", port)
        self._add_attribute("path", path)
        self._add_attribute("args", args)

    def __str__(self):
        return "%s(%s %s %s %s)" % (self.__class__.__name__,
                self.get_host(), self.get_port(), self.get_path(), self.get_args())

    def get_host(self):
        return self.get_attribute("host")

    def get_port(self):
        return self.get_attribute("port")

    def get_path(self):
        return self.get_attribute("path")

    def get_args(self):
        return self.get_attribute("args")

    def set_host(self, value):
        self.set_attribute("host", str(value))

    def set_port(self, value):
        self.set_attribute("port", int(value))

    def set_path(self, value):
        self.set_attribute("path", str(value))

    def set_args(self, value):
        if type(value) != list:
            value = [value]
        self.set_attribute("args", value)

    # Override
    def get_type(self):
        return "osc"

    @defer.inlineCallbacks
    def execute(self):
        """
        @rtype: L{twisted.internet.defer.Deferred}
        """
        yield defer.succeed(None)
        message = create_message_auto(self._path, *self._args)
        yield send_async_udp(message, self._port, self._host)
        # TODO: support TCP as well
        # print("OscAction.execute: TODO")
        defer.returnValue(None)
