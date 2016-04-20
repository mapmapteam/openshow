#!/usr/bin/env python
"""
The main entry to our application, where we parse command line arguments.
"""
from twisted.python import log
from twisted.internet import wxreactor
wxreactor.install()
# import t.i.reactor only after installing wxreactor:
from twisted.internet import reactor
from openshow.app import gui
import sys

def run():
    """
    Parses the command line options and runs the application.
    """
    log.startLogging(sys.stdout)

    # register the App instance with Twisted:
    app = gui.App(0)
    reactor.registerWxApp(app)

    # start the event loop:
    reactor.run()


if __name__ == '__main__':
    run()
