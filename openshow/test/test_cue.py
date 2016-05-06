#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
Test cases for openshow.cue
"""
from twisted.trial import unittest
from twisted.internet import defer
from openshow import cue
from openshow import timer
from openshow.actions import osc

class DummyAction(object):
    def __init__(self):
        self.executed = False
    
    def execute(self):
        self.executed = True
        return defer.succeed(None)


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

    @defer.inlineCallbacks
    def test_03_cue_waits_and_execute(self):
        _action = DummyAction()
        _cue = cue.Cue("1", 1.0, 1.0, "title", _action)
        _timer = timer.Timer()
        result = yield _cue.go()
        elapsed = _timer.elapsed()
        self.assertAlmostEqual(elapsed, 2.0, places=2)
        self.assertEqual(_action.executed, True)

    def test_04_cancel_cue(self):
        _action = DummyAction()
        _cue = cue.Cue("1", 1.0, 1.0, "title", _action)
        _timer = timer.Timer()
        d = _cue.go()

        def _cb(result):
            self.assertEqual(_action.executed, False)
            self.assertEqual(result, False)

        d.addCallback(_cb)
        _cue.cancel()
        return d


class TestCueSheet(unittest.TestCase):
    def test_01_cue_sheet_cues(self):
        cue_sheet = cue.CueSheet()
        _timer = timer.Timer()

        cues = [
                # identifier, pre-wait, post-wait
                cue.Cue("1", 0.0, 1.0, "title1",
                        osc.OscAction("localhost", 10000, "/path", [])),
                cue.Cue("2", 0.0, 1.0, "title2",
                        osc.OscAction("localhost", 10000, "/path", [])),
        ]
        cue_sheet.set_cues(cues)
        _cue = cue_sheet.get_cue_by_index(0)
        self.failUnlessEqual(_cue.get_identifier(), cues[0].get_identifier())

        _cue = cue_sheet.get_cue_by_identifier("1")
        self.failUnlessEqual(_cue.get_identifier(), cues[0].get_identifier())

        _size = cue_sheet.get_size()
        self.failUnlessEqual(_size, 2)

        cue_sheet.append_cue(cue.Cue("3", 0.0, 1.0, "title3",
                osc.OscAction("localhost", 10000, "/path", [])))

        _size = cue_sheet.get_size()
        self.failUnlessEqual(_size, 3)

    @defer.inlineCallbacks
    def test_02_follow(self):
        cue_sheet = cue.CueSheet()
        _timer = timer.Timer()

        cues = [
                # identifier, pre-wait, post-wait
                cue.Cue("1", 0.0, 1.0, "title1",
                        DummyAction()),
                cue.Cue("2", 0.0, 1.0, "title2",
                        DummyAction()),
                cue.Cue("3", 0.0, 1.0, "title3",
                        DummyAction()),
        ]
        cue_sheet.set_cues(cues)
        cue_sheet.go()

        yield timer.later(0.1)
        _action = cue_sheet.get_cue_by_identifier("1").get_action()
        self.assertEqual(_action.executed, True)
        _action = cue_sheet.get_cue_by_identifier("2").get_action()
        self.assertEqual(_action.executed, False)
        _action = cue_sheet.get_cue_by_identifier("3").get_action()
        self.assertEqual(_action.executed, False)

        yield timer.later(1.1)
        _action = cue_sheet.get_cue_by_identifier("2").get_action()
        self.assertEqual(_action.executed, True)
        _action = cue_sheet.get_cue_by_identifier("3").get_action()
        self.assertEqual(_action.executed, False)

        yield timer.later(1.1)
        _action = cue_sheet.get_cue_by_identifier("3").get_action()
        self.assertEqual(_action.executed, True)
        yield timer.later(1.1)
