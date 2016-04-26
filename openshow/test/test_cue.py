#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
Test cases for openshow.cue
"""
from twisted.trial import unittest
from twisted.internet import defer
from openshow import cue

class TestCue(unittest.TestCase):
    def test_01_cue(self):
        IDENTIFIER = "identifier"
        PRE_WAIT = 0.0
        POST_WAIT = 1.0
        TITLE = "title"

        item = cue.Cue(IDENTIFIER, PRE_WAIT, POST_WAIT, TITLE)
        self.failUnlessEqual(item.get_identifier(), IDENTIFIER)
        self.failUnlessEqual(item.get_pre_wait(), PRE_WAIT)
        self.failUnlessEqual(item.get_post_wait(), POST_WAIT)
        self.failUnlessEqual(item.get_title(), TITLE)

        IDENTIFIER = "other_identifier"
        PRE_WAIT = 2.0
        POST_WAIT = 3.0
        TITLE = "other_title"

        item.set_identifier(IDENTIFIER)
        item.set_pre_wait(PRE_WAIT)
        item.set_post_wait(POST_WAIT)
        item.set_title(TITLE)

        self.failUnlessEqual(item.get_identifier(), IDENTIFIER)
        self.failUnlessEqual(item.get_pre_wait(), PRE_WAIT)
        self.failUnlessEqual(item.get_post_wait(), POST_WAIT)
        self.failUnlessEqual(item.get_title(), TITLE)

    def test_02_osc_cue(self):
        IDENTIFIER = "identifier"
        PRE_WAIT = 0.0
        POST_WAIT = 1.0
        TITLE = "title"
        HOST = "localhost"
        PORT = 10000
        PATH = "/path"
        ARGS = ["hello", 2, 3.14159, True]

        item = cue.OscCue(
                IDENTIFIER, PRE_WAIT, POST_WAIT, #FIXME: TITLE
                HOST, PORT, PATH, ARGS)

        self.failUnlessEqual(item.get_host(), HOST)
        self.failUnlessEqual(item.get_port(), PORT)
        self.failUnlessEqual(item.get_path(), PATH)
        self.failUnlessEqual(item.get_args(), ARGS)

        HOST = "127.0.0.1"
        PORT = 11000
        PATH = "/other/path"
        ARGS = ["bye", 1, 1.618, False]

        item.set_host(HOST)
        item.set_port(PORT)
        item.set_path(PATH)
        item.set_args(ARGS)

        self.failUnlessEqual(item.get_host(), HOST)
        self.failUnlessEqual(item.get_port(), PORT)
        self.failUnlessEqual(item.get_path(), PATH)
        self.failUnlessEqual(item.get_args(), ARGS)

        # TODO: test trigger.

class TestCueSheet(unittest.TestCase):
    def test_01_cue_sheet(self):
        cue_sheet = cue.CueSheet()

        cues = [
                cue.OscCue("1", 0.0, 1.0, #FIXME: title
                        "localhost", 10000, "/path", []),
                cue.OscCue("1", 0.0, 1.0, #FIXME: title
                        "localhost", 10000, "/path", []),
        ]
        cue_sheet.set_cues(cues)
        # TODO

    test_01_cue_sheet.skip = "To do"
