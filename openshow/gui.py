#!/usr/bin/env python
"""
Our graphical user interface.
"""
import sys
import wx
# At this point, wxreactor has already been installed.
from twisted.internet import reactor
import os

def show_open_file_dialog(parent):
    """
    Open a file.
    """
    dirname = ''
    filename = ''
    full_path = ''
    dialog = wx.FileDialog(parent, "Choose a file", dirname, "", "*.xml",
            wx.OPEN)
    if dialog.ShowModal() == wx.ID_OK:
        filename = dialog.GetFilename()
        dirname = dialog.GetDirectory()
        full_path = os.path.join(dirname, filename)
    dialog.Destroy()
    return full_path


class MainFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        # ID_EXIT = wx.NewId() # 101
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition,
                wx.Size(720, 480))
        menuBar = wx.MenuBar()
        # File
        file_menu = wx.Menu()
        # File > Open
        file_menu.Append(wx.ID_OPEN, "&Open", "Open a project file")
        wx.EVT_MENU(self, wx.ID_OPEN, self._open_menu_cb)
        # File > Exit
        file_menu.Append(wx.ID_EXIT, "E&xit", "Exit the program")
        wx.EVT_MENU(self, wx.ID_EXIT, self._exit_menu_cb)

        menuBar.Append(file_menu, "&File")
        self.SetMenuBar(menuBar)
        
        # make sure reactor.stop() is used to stop event loop:
        wx.EVT_CLOSE(self, lambda evt: reactor.stop())

    def _exit_menu_cb(self, event):
        reactor.stop()

    def _open_menu_cb(self, event):
        file_path = show_open_file_dialog(self)
        print("Chose file %s" % (file_path))


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
