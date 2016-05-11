#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
Test cases for cuebidoo.cue
"""
from twisted.trial import unittest
from twisted.internet import defer
from cuebidoo import cue
from cuebidoo import timer
from cuebidoo.actions import osc


class DummyAction(cue.Action):
    def __init__(self):
        super(DummyAction, self).__init__()
        self.executed = False
    
    def execute(self):
        self.executed = True
        return defer.succeed(None)


class ActionThatTakesOneSecond(cue.Action):
    def __init__(self):
        super(ActionThatTakesOneSecond, self).__init__()
        self.executed = False
    
    @defer.inlineCallbacks
    def execute(self):
        yield timer.later(1.0)
        self.executed = True


def _get_action(cue_sheet, cue_identifier):
    return cue_sheet.get_cue_by_identifier(cue_identifier).get_action()


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

        # Initially, the first cue should be done right away
        yield timer.later(0.1)
        _action = cue_sheet.get_cue_by_identifier("1").get_action()
        self.assertEqual(_action.executed, True)
        _action = cue_sheet.get_cue_by_identifier("2").get_action()
        self.assertEqual(_action.executed, False)
        _action = cue_sheet.get_cue_by_identifier("3").get_action()
        self.assertEqual(_action.executed, False)

        # After one second, the second should be triggered
        yield timer.later(1.1)
        _action = cue_sheet.get_cue_by_identifier("2").get_action()
        self.assertEqual(_action.executed, True)
        _action = cue_sheet.get_cue_by_identifier("3").get_action()
        self.assertEqual(_action.executed, False)

        # After two seconds, the third should be triggered
        yield timer.later(1.1)
        _action = cue_sheet.get_cue_by_identifier("3").get_action()
        self.assertEqual(_action.executed, True)
        yield timer.later(1.1)

    @defer.inlineCallbacks
    def test_03_no_follow(self):
        cue_sheet = cue.CueSheet()
        _timer = timer.Timer()

        cues = [
                # identifier, pre-wait, post-wait
                cue.Cue("1", 0.0, 1.0, "title1",
                        DummyAction()),
                cue.Cue("2", 0.0, 1.0, "title2",
                        DummyAction(), cue.FOLLOW_DO_NOT_CONTINUE),
                cue.Cue("3", 0.0, 1.0, "title3",
                        DummyAction()),
        ]
        cue_sheet.set_cues(cues)
        cue_sheet.go()

        # Initially, the first cue should be done right away
        yield timer.later(0.1)
        _action = cue_sheet.get_cue_by_identifier("1").get_action()
        self.assertEqual(_action.executed, True)
        _action = cue_sheet.get_cue_by_identifier("2").get_action()
        self.assertEqual(_action.executed, False)
        _action = cue_sheet.get_cue_by_identifier("3").get_action()
        self.assertEqual(_action.executed, False)

        # After one second, the second should be triggered
        yield timer.later(1.1)
        _action = cue_sheet.get_cue_by_identifier("2").get_action()
        self.assertEqual(_action.executed, True)
        _action = cue_sheet.get_cue_by_identifier("3").get_action()
        self.assertEqual(_action.executed, False)

        # Even after two seconds, the third should NEVER be triggered
        yield timer.later(1.1)
        _action = cue_sheet.get_cue_by_identifier("3").get_action()
        self.assertEqual(_action.executed, False)
        selected = cue_sheet.get_selected_cue_identifier()
        self.assertEqual(selected, "3")
        yield timer.later(1.1)

    @defer.inlineCallbacks
    def test_04_follow_when_done(self):
        cue_sheet = cue.CueSheet()
        _timer = timer.Timer()

        cues = [
                # identifier, pre-wait, post-wait
                cue.Cue("1", 0.0, 1.0, "title1",
                        ActionThatTakesOneSecond(), cue.FOLLOW_WHEN_DONE),
                cue.Cue("2", 0.0, 1.0, "title1",
                        ActionThatTakesOneSecond(), cue.FOLLOW_AUTO_CONTINUE),
                cue.Cue("3", 0.0, 0.0, "title2",
                        DummyAction()),
        ]
        cue_sheet.set_cues(cues)
        cue_sheet.go()

        # Initially, the first cue should in progress
        yield timer.later(0.1)
        _action = cue_sheet.get_cue_by_identifier("1").get_action()
        self.assertEqual(_action.executed, False)
        _action = cue_sheet.get_cue_by_identifier("2").get_action()
        self.assertEqual(_action.executed, False)

        # After one second, the first cue should be done
        # But, it should be in post-wait
        yield timer.later(1.1)
        _action = cue_sheet.get_cue_by_identifier("1").get_action()
        self.assertEqual(_action.executed, True)
        _action = cue_sheet.get_cue_by_identifier("2").get_action()
        self.assertEqual(_action.executed, False)
        _first_is_post_waiting = cue_sheet.get_cue_by_identifier("1").is_post_waiting()
        self.assertEqual(_first_is_post_waiting, True)

        # After two seconds, the first cue should be done
        yield timer.later(1.1)
        self.assertEqual(_get_action(cue_sheet, "1").executed, True)
        self.assertEqual(_get_action(cue_sheet, "2").executed, False)

        # After four seconds, the second cue should finally be done
        yield timer.later(3.1)
        self.assertEqual(_get_action(cue_sheet, "2").executed, True)
        # But the last cue should never be triggered
        self.assertEqual(_get_action(cue_sheet, "3").executed, False)

    test_04_follow_when_done.skip = "FIXME: action 2 is never executed, it seems"
