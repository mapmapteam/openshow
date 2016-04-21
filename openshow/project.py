#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
A project contains cues. XML files are used to describe projects.

Usage:
    PYTHONPATH=$PWD python ./openshow/project.py examples/project_01.xml
"""
from xml.dom import minidom
import os
from openshow import cue


class Project(object):
    """
    Project cue list.

    Loads the list of cues to play.
    """
    def __init__(self):
        self._project_file_path = ""
        self._cue_sheet = cue.CueSheet()

    def parse_project_file(self, project_file_path):
        """
        Make sure to set_screen_identifier first.
        Make sure the config_file_path exists.
        :raise: RuntimeError
        """
        if not os.path.exists(project_file_path):
            raise RuntimeError("Project file does not exist: %s." % (
                    project_file_path))
        self._project_file_path = project_file_path
        doc = minidom.parse(self._project_file_path)
        cues = self._parse_cues(doc)
        self._cue_sheet.set_cues(cues)

    def _parse_cues(self, doc):
        """
        @param doc: xml.dom.minidom.Document instance
        """
        ret = {}
        cue_elements = doc.getElementsByTagName("cue")
        for cue_element in cue_elements:
            # Parse its attributes
            _identifier = None
            _type = "osc" # default
            _pre_wait = 0.0
            _post_wait = 0.0
            if cue_element.hasAttribute("type"):
                _type = cue_element.getAttribute("type")
            if cue_element.hasAttribute("identifier"):
                _identifier = cue_element.getAttribute("identifier")
            if cue_element.hasAttribute("pre_wait"):
                _pre_wait = cue_element.getAttribute("pre_wait")
            if cue_element.hasAttribute("post_wait"):
                _post_wait = cue_element.getAttribute("post_wait")
            if _type == "osc":
                _host = "localhost"
                _port = 31337
                _path = "/default"
                _args = []
                if cue_element.hasAttribute("host"):
                    _host = cue_element.getAttribute("host")
                if cue_element.hasAttribute("port"):
                    try:
                        _port = int(cue_element.getAttribute("port"))
                    except ValueError, e:
                        print("Error parsing int for OSC port: %s" % (e))
                if cue_element.hasAttribute("path"):
                    _path = cue_element.getAttribute("path")
                if cue_element.hasAttribute("args"):
                    _args = cue_element.getAttribute("args")
                _cue = cue.OscCue(_identifier, _pre_wait, _post_wait, _host, _port,
                        _path, _args)
                ret[_identifier] = _cue
        return ret

    def get_cue_sheet(self):
        return self._cue_sheet


if __name__ == "__main__":
    import sys
    project_file_path = "default.xml"
    try:
        project_file_path = sys.argv[1]
    except IndexError:
        print("Usage: %s <XML file path>" % (sys.argv[0]))
    config = Project()
    config.parse_project_file(project_file_path)
    cues = config.get_cue_sheet().get_cues()
    if len(cues) == 0:
        print("No cue")
    else:
        for cue in cues:
            print("%s" % (cue))
