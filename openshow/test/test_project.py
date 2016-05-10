#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
from openshow import project
from twisted.trial import unittest
import os
import tempfile


PROJECT_DATA = """<?xml version="1.0"?>
<project loop="true">
    <options>
        <option name="default_osc_port" value="12345" />
        <option name="default_osc_host" value="localhost" />
    </options>
    <cue identifier="1" title="Load media 1" pre_wait="0.0" post_wait="1.0" follow="auto_continue">
        <action type="osc">
            <attr name="port" value="12345" />
            <attr name="path" value="/mapmap/media/load ,s movie1.mov" />
        </action>
    </cue>
    <cue identifier="2" title="Load media 2" pre_wait="0.0" post_wait="1.0" follow="auto_continue">
        <action type="osc">
            <attr name="port" value="12345" />
            <attr name="path" value="/mapmap/media/load ,s movie2.mov" />
        </action>
    </cue>
</project>
"""


def make_temporary_file(contents=""):
    fd, file_path = tempfile.mkstemp()
    if contents != "":
        os.write(fd, contents)
    os.close(fd) # if os.path.exists(file_path):
    #     os.unlink(file_path)
    return file_path



class ProjectTestCase(unittest.TestCase):
    def test_01_load_from_file(self):
        file_path = make_temporary_file(PROJECT_DATA)
        cue_sheet = project.ProjectPersistance().parse_project_file(file_path)
        cue_1 = cue_sheet.get_cue_by_identifier("1")
        self.assertEqual(cue_1.get_title(), "Load media 1")
        # TODO: more testing for the data loaded from XML
