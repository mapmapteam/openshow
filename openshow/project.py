#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
"""
A project contains cues. XML files are used to describe projects.
"""
from xml.dom import minidom
import os

class Cue(object):
    """
    Cue.
    """
    def __init__(self, identifier="", pre_wait=0.0, post_wait=0.0):
        self._identifier = identifier
        self._pre_wait = pre_wait
        self._post_wait = post_wait

    def __str__(self):
        return "Cue(\"%s\" %s %s)" % (self._identifier, self._pre_wait,
                self._post_wait)

    def get_identifier(self):
        return self._identifier

    def get_pre_wait(self):
        return self._pre_wait

    def get_post_wait(self):
        return self._post_wait

    def set_identifier(self, value):
        self._identifier = value

    def set_pre_wait(self, value):
        self._pre_wait = value

    def set_post_wait(self, value):
        self._post_wait = value


class OscCue(Cue):
    """
    OpenSoundControl cue.
    """
    def __init__(self, identifier="", pre_wait=0.0, post_wait=0.0,
            host="localhost", port=31337, path="/default", args=[]):
        super(OscCue, self).__init__(identifier, pre_wait, post_wait)
        self._host = host
        self._port = port
        self._path = path
        self._args = args

    def __str__(self):
        return "OscCue(\"%s\" %s %s %s %s)" % (self._identifier, self._host,
                self._port, self._path, self._args)

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port

    def get_path(self):
        return self._path

    def get_args(self):
        return self._args

    def set_host(self, value):
        self._host = value

    def set_port(self, value):
        self._port = value

    def set_path(self, value):
        self._path = value

    def set_args(self, value):
        self._args = value


class CueSheet(object):
    def __init__(self):
        self._cues = {}

    def get_cues(self):
        return self._cues.values()

    def add_cue(self, identifier, value):
        self._cues[identifier] = value


class Project(object):
    """
    Project cue list.

    Loads the list of cues to play.
    """
    def __init__(self):
        self._project_file_path = ""
        self._cues = []

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
        self._cues = self._parse_cues(doc)

    def _parse_cues(self, doc):
        """
        @param doc: xml.dom.minidom.Document instance
        """
        ret = []
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
                    _port = cue_element.getAttribute("port")
                if cue_element.hasAttribute("path"):
                    _path = cue_element.getAttribute("path")
                if cue_element.hasAttribute("args"):
                    _args = cue_element.getAttribute("args")
                cue = OscCue(_identifier, _pre_wait, _post_wait, _host, _port,
                        _path, _args)
                ret.append(cue)
        return ret

    def get_cues(self):
        return self._cues

    def get_cue(self, identifier):
        for cue in self._cues:
            if cue.get_identifier() == identifier:
                return cue
        return None


if __name__ == "__main__":
    project_file_path = "project.xml"
    config = Project()
    config.parse_project_file(project_file_path)
    cues = config.get_cues()
    if len(cues) == 0:
        print("No cue")
    else:
        for cue in cues:
            print("%s" % (cue))
