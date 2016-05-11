#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
Test cases for cuebidoo.timer
"""
from twisted.trial import unittest
from cuebidoo import timer

class TestTimer(unittest.TestCase):
    def test_01_timer(self):
        timer_a = timer.Timer()
        d = timer.later(1.0)

        def _cb(result, arg):
            elapsed = timer_a.elapsed()
            self.assertAlmostEqual(elapsed, 1.0, places=3)
            self.assertEqual(arg, 2)

        d.addCallback(_cb, 2)
        return d
