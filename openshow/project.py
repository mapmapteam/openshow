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
from openshow.actions import osc


class ProjectPersistance(object):
    """
    Loads/saves the list of cues to play.
    """
    def __init__(self):
        self._project_file_path = ""
        self._cue_sheet = cue.CueSheet()

    def parse_project_file(self, project_file_path):
        """
        Loads a cue sheet from a project file.

        Saves that path for later use - in case you want to save the project.
        Returns a cue sheet.

        Make sure the config_file_path exists.
        @raise: RuntimeError
        @return: L{openshow.cue.CueSheet}
        """
        cue_sheet = cue.CueSheet()
        if not os.path.exists(project_file_path):
            raise RuntimeError("Project file does not exist: %s." % (
                    project_file_path))
        self._project_file_path = project_file_path
        doc = minidom.parse(self._project_file_path)
        cues = self._parse_cues(doc)
        cue_sheet.set_cues(cues)
        return cue_sheet

    def _parse_cues(self, doc):
        """
        @param doc: xml.dom.minidom.Document instance
        """
        ret = []
        cue_elements = doc.getElementsByTagName("cue")
        for cue_element in cue_elements:
            # Parse its attributes
            _identifier = self._parse_attribute(cue_element, "identifier")
            _title = self._parse_attribute(cue_element, "title", "<no title>")
            _pre_wait = self._parse_attribute(cue_element, "pre_wait", 0.0)
            _post_wait = self._parse_attribute(cue_element, "post_wait", 0.0)
            _follow = self._parse_attribute(cue_element, "follow", cue.FOLLOW_AUTO_CONTINUE)

            # Extract action (for now only supports a single action)
            actions_elements = cue_element.getElementsByTagName("action")
            if len(actions_elements) != 1:
                raise RuntimeError("Found " + len(actions_elements) +
                        " actions, only one action supported.")

            # Create action.
            action_element = actions_elements[0]
            _action_type = self._parse_attribute(action_element, "type", "osc")
            if _action_type != "osc":
                raise RuntimeError("Only OSC actions supported for now, found '"
                        + _action_type + "'.")
            action = osc.OscAction()
            attributes = action_element.getElementsByTagName("attr")
            for attr in attributes:
                name = self._parse_attribute(attr, "name")
                value = self._parse_attribute(attr, "value")
                action.set_attribute(name, value)

            _cue = cue.Cue(_identifier, _pre_wait, _post_wait, _title, action, follow=_follow);
            ret.append(_cue)
        return ret

    def _parse_attribute(self, element, attribute, default=None):
        _type = type(default) 
        if element.hasAttribute(attribute):
            if _type == type(None):
                return element.getAttribute(attribute)
            else:
                return _type(element.getAttribute(attribute))
        else:
            return default

    def save_to_project_file(self, cue_sheet, project_file_path=None):
        raise NotImplementedError("To do")


if __name__ == "__main__":
    import sys
    project_file_path = "default.xml"
    try:
        project_file_path = sys.argv[1]
    except IndexError:
        print("Usage: %s <XML file path>" % (sys.argv[0]))
    project = ProjectPersistance()
    cue_sheet = project.parse_project_file(project_file_path)
    cues = cue_sheet.get_cues()
    if len(cues) == 0:
        print("No cue")
    else:
        for cue in cues:
            print("%s" % (cue))
