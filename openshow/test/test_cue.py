#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
Test cases for openshow.cue
"""
from twisted.trial import unittest
from twisted.internet import defer
from openshow import cue
from openshow.actions import osc

class TestCue(unittest.TestCase):
    def test_01_cue_attributes(self):
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

    def test_02_action_execute(self):
        action = cue.Action()
        return action.execute()

    def test_03_osc_action_attributes(self):
        IDENTIFIER = "identifier"
        PRE_WAIT = 0.0
        POST_WAIT = 1.0
        TITLE = "title"
        HOST = "localhost"
        PORT = 10000
        PATH = "/path"
        ARGS = ["hello", 2, 3.14159, True]

        osc_cue = cue.Cue(IDENTIFIER, PRE_WAIT, POST_WAIT, TITLE)
        osc_action = osc.OscAction(HOST, PORT, PATH, ARGS)
        osc_cue.set_action(osc_action)

        self.failUnlessEqual(osc_action.get_host(), HOST)
        self.failUnlessEqual(osc_action.get_port(), PORT)
        self.failUnlessEqual(osc_action.get_path(), PATH)
        self.failUnlessEqual(osc_action.get_args(), ARGS)

        HOST = "127.0.0.1"
        PORT = 11000
        PATH = "/other/path"
        ARGS = ["bye", 1, 1.618, False]

        osc_action.set_host(HOST)
        osc_action.set_port(PORT)
        osc_action.set_path(PATH)
        osc_action.set_args(ARGS)

        self.failUnlessEqual(osc_action.get_host(), HOST)
        self.failUnlessEqual(osc_action.get_port(), PORT)
        self.failUnlessEqual(osc_action.get_path(), PATH)
        self.failUnlessEqual(osc_action.get_args(), ARGS)

        # TODO: test trigger.


class TestCueSheet(unittest.TestCase):
    def test_01_cue_sheet(self):
        cue_sheet = cue.CueSheet()

        cues = [
                # identifier, pre-wait, post-wait
                cue.Cue("1", 0.0, 1.0, "title1",
                        osc.OscAction("localhost", 10000, "/path", [])),
                cue.Cue("2", 0.0, 1.0, "title2",
                        osc.OscAction("localhost", 10000, "/path", [])),
        ]
        cue_sheet.set_cues(cues)
        # TODO

    # test_01_cue_sheet.skip = "To do"
