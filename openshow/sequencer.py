#!/usr/bin/env python
"""
The Sequencer class.

Every time twisted goes to sleep, it computes a wake-up time from the delta of
the desired time of the head of the list and the current time.
Every time it wakes up, it does whatever work is at or before the present time.
"""
from openshow import cue
from openshow import project
from openshow import timer


class Sequencer(object):
    """
    Sequencer for cues.
    The default interval precision is 60 Hz.
    """
    def __init__(self, interval=0.016666):
        self._project = None
        self._cue_sheet = None
        self._precision = precision
        self._lc = task.LoopingCall(self._looping_call_cb)
        self._lc.start(precision, now=True)
        self._timer = timer.Timer()
        self._is_running = False

    def go(self):
        """
        Starts to play the cue list.
        """
        self._timer.reset()
        self._is_running = True
        active_cue_index = self._cue_sheet.get_active_cue_index()
        active_cue = self._cue_sheet.get_cue_by_index(active_cue_index)
        pre_wait = active_cue.get_pre_wait()

    def _looping_call_cb(self):
        if self._is_running:
            elapsed = self._timer.elapsed()


    def load_project_file(self, project_file_path):
        self._project = project.Project()
        self._cue_sheet = self._project.parse_project_file(project_file_path)

    def save_project_to_file(self, project_file_path=None):
        raise NotImplementedError("To do")

    def __str__(self):
        ret = ""
        if self._cue_sheet is None:
            ret += "No project loaded."
        else:
            cues = self._cue_sheet.get_cues()
            if len(cues) == 0:
                ret += "No cue in project"
            else:
                ret += "Cues:\n" 
                for cue in cues:
                    ret += "- %s\n" % (cue)
        return ret
