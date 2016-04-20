#!/usr/bin/env python
"""
Our graphical user interface.
"""
import sys
import wx
# At this point, wxreactor has already been installed.
from twisted.internet import reactor


class MainFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        ID_EXIT  = 101
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(300, 200))
        menu = wx.Menu()
        menu.Append(ID_EXIT, "E&xit", "Terminate the program")
        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)
        wx.EVT_MENU(self, ID_EXIT,  self._exit_menu_cb)
        
        # make sure reactor.stop() is used to stop event loop:
        wx.EVT_CLOSE(self, lambda evt: reactor.stop())

    def _exit_menu_cb(self, event):
        reactor.stop()


class App(wx.App):
    """
    Our main application.
    """
    def _call_later_cb(self):
        print("two seconds passed")

    def OnInit(self):
        """
        Called when it's time to initialize this application.
        """
        frame = MainFrame(None, -1, "Open Show")
        frame.Show(True)
        self.SetTopWindow(frame)
        # look, we can use twisted calls!
        reactor.callLater(2, self._call_later_cb)
        return True
