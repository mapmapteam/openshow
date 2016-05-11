#!/usr/bin/env python
"""
The main entry to our application, where we parse command line arguments.
"""
from twisted.python import log
from twisted.internet import wxreactor
wxreactor.install()
# import twisted.internet.reactor only after installing wxreactor:
from twisted.internet import reactor
import cuebidoo
from cuebidoo import gui
import sys
import os
import optparse


def run():
    """
    Parses the command line options and runs the application.
    """
    DEFAULT_OSC_RECEIVE_PORT = 13333
    DEFAULT_PROJECT_FILE = ""

    parser = optparse.OptionParser(usage="%prog",
            version=str(cuebidoo.__version__))
    parser.add_option("-p", "--osc-receive-port", type="int",
            default=DEFAULT_OSC_RECEIVE_PORT,
            help="Receive OSC messages port number (%default)")
    parser.add_option("-f", "--project-file", type="string",
            default=DEFAULT_PROJECT_FILE, help="XML project file.")
    parser.add_option("-v", "--verbose", action="store_true",
            help="Makes the logging output verbose.")
    (options, args) = parser.parse_args()

    verbose = False
    osc_receive_port = DEFAULT_OSC_RECEIVE_PORT
    project_file = DEFAULT_PROJECT_FILE

    if options.verbose:
        verbose = True

    # FIXME: for now, let's just make it always verbose
    verbose = True

    osc_receive_port = options.osc_receive_port
    project_file = options.project_file

    log.startLogging(sys.stdout)
    if verbose:
        print("osc_receive_port %s" % (osc_receive_port))
        print("project_file %s" % (project_file))
    project_file = os.path.expanduser(project_file)
    if verbose:
        print("expanded project_file %s" % (project_file))

    # register the App instance with Twisted:
    app = gui.App(0)
    reactor.registerWxApp(app)

    def _later_load_file():
        app.get_frame().load_cue_sheet(project_file)

    if project_file == "":
        if verbose:
            print("No project file to load")
    else:
        if os.path.exists(project_file):
            # TODO: instead of waiting for an arbitrary amount of time
            # wait for the window to actually be created.
            reactor.callLater(0.5, _later_load_file)
        else:
            print("Error: Project file %s does not exist" % (project_file))
            sys.exit(1)

    # start the event loop:
    try:
        reactor.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    run()
