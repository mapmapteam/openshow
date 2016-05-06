#!/usr/bin/env python
"""
Our graphical user interface.
"""
if __name__ == "__main__":
    from twisted.internet import wxreactor
    wxreactor.install()
# At this point, wxreactor has already been installed.
from twisted.internet import reactor
import sys
import wx
import os
from openshow import cue
from openshow import project

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

        sizer = wx.BoxSizer(wx.VERTICAL)
        list_ctrl_id = wx.NewId()
        self._widget_list_ctrl = wx.ListCtrl(self, list_ctrl_id,
                style=wx.LC_REPORT | wx.BORDER_NONE)
        sizer.Add(self._widget_list_ctrl, 1, wx.EXPAND)

        go_button = wx.Button(self, label="GO")
        go_button.Bind(wx.EVT_BUTTON, self._go_button_cb)
        sizer.Add(go_button, 1, wx.ALL | wx.CENTER)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self._cue_sheet = cue.CueSheet()
        self._current_item = 0 # Do this before _populate_list_ctrl
        self._populate_list_ctrl()
        self._bind_list_ctrl_event_callbacks()

    def load_cue_sheet(self, project_file_path):
      self._cue_sheet = project.ProjectPersistance().parse_project_file(project_file_path)
      self._current_item = 0 # Do this before _populate_list_ctrl
      self._populate_list_ctrl()

    def _exit_menu_cb(self, event):
        reactor.stop()

    def _open_menu_cb(self, event):
        file_path = show_open_file_dialog(self)
        print("Chose file %s" % (file_path))

    def _go_button_cb(self, event):
        print("GO")

    def _bind_list_ctrl_event_callbacks(self):
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._list_item_selected_cb,
                self._widget_list_ctrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._list_item_deselected_cb,
                self._widget_list_ctrl)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._list_item_activated_cb,
                self._widget_list_ctrl)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self._list_delete_item_cb,
                self._widget_list_ctrl)
        self.Bind(wx.EVT_LIST_COL_CLICK, self._list_col_click_cb,
                self._widget_list_ctrl)
        self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self._list_col_right_click_cb,
                self._widget_list_ctrl)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self._list_col_begin_drag_cb,
                self._widget_list_ctrl)
        self.Bind(wx.EVT_LIST_COL_DRAGGING, self._list_col_dragging_cb,
                self._widget_list_ctrl)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self._list_col_end_drag_cb,
                self._widget_list_ctrl)
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self._list_begin_label_edit_cb,
                self._widget_list_ctrl)

        self._widget_list_ctrl.Bind(wx.EVT_LEFT_DCLICK,
                self._list_left_double_click_cb)
        self._widget_list_ctrl.Bind(wx.EVT_RIGHT_DOWN, self._list_right_down_cb)

        # for wxMSW
        self._widget_list_ctrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK,
                self._list_right_click_cb)
        # for wxGTK
        self._widget_list_ctrl.Bind(wx.EVT_RIGHT_UP, self._list_right_click_cb)

    def log_debug(self, text):
        print(text)

    def _list_right_down_cb(self, event):
        x = event.GetX()
        y = event.GetY()
        self.log_debug("x, y = %s" % str((x, y)))
        item, flags = self._widget_list_ctrl.HitTest((x, y))

        # Selects the item
        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self._widget_list_ctrl.Select(item)
        event.Skip()

    def get_item_column_text(self, row_index, column):
        item = self._widget_list_ctrl.GetItem(row_index, column)
        return item.GetText()

    def _list_item_selected_cb(self, event):
        ##print event.GetItem().GetTextColour()
        self._current_item = event.m_itemIndex
        self.log_debug("_list_item_selected_cb: %s, %s, %s, %s\n" %
                (self._current_item,
                self._widget_list_ctrl.GetItemText(self._current_item),
                self.get_item_column_text(self._current_item, 1),
                self.get_item_column_text(self._current_item, 2)))
        # if self.currentItem == 10:
        #     self.log.WriteText("OnItemSelected: Veto'd selection\n")
        #     #event.Veto()  # doesn't work
        #     # this does
        #     self.list.SetItemState(10, 0, wx.LIST_STATE_SELECTED)
        event.Skip()

    def _list_item_deselected_cb(self, evt):
        item = evt.GetItem()
        self.log_debug("_list_item_deselected_cb: %d" % evt.m_itemIndex)
        # # Show how to reselect something we don't want deselected
        # if evt.m_itemIndex == 11:
        #     wx.CallAfter(self.list.SetItemState, 11, wx.LIST_STATE_SELECTED,
        # wx.LIST_STATE_SELECTED)

    def _list_item_activated_cb(self, event):
        self.currentItem = event.m_itemIndex
        self.log_debug("_list_item_activated_cb: %s\nTopItem: %s" %
                (self._widget_list_ctrl.GetItemText(self._current_item),
                        self._widget_list_ctrl.GetTopItem()))

    def _list_begin_label_edit_cb(self, event):
        self.log_debug("_list_begin_label_edit_cb")
        event.Allow()

    def _list_delete_item_cb(self, event):
        self.log_debug("_list_delete_item_cb")

    def _list_col_click_cb(self, event):
        self.log_debug("_list_col_click_cb: %d" % event.GetColumn())
        event.Skip()

    def _list_col_right_click_cb(self, event):
        item = self._widget_list_ctrl.GetColumn(event.GetColumn())
        self.log_debug("_list_col_right_click_cb: %d %s\n" %
                (event.GetColumn(), (item.GetText(), item.GetAlign(),
                    item.GetWidth(), item.GetImage())))
        # if self._widget_list_ctrl.HasColumnOrderSupport():
        #     self.log.WriteText("_list_col_right_click_cb: column order: %d" %
        #             self._widget_list_ctrl.GetColumnOrder(event.GetColumn()))

    def _list_col_begin_drag_cb(self, event):
        self.log_debug("_list_col_begin_drag_cb\n")
        ## Show how to not allow a column to be resized
        #if event.GetColumn() == 0:
        #    event.Veto()

    def _list_col_dragging_cb(self, event):
        self.log_debug("_list_col_dragging_cb")

    def _list_col_end_drag_cb(self, event):
        self.log_debug("_list_col_end_drag_cb")

    def _list_left_double_click_cb(self, event):
        self.log_debug("_list_left_double_click_cb item %s" % (
                self._widget_list_ctrl.GetItemText(self._current_item)))
        event.Skip()

    def _list_right_click_cb(self, event):
        self.log_debug("_list_right_click_cb %s" % (
                self._widget_list_ctrl.GetItemText(self._current_item)))

        # pop-up menu!
        # # only do this part the first time so the events are only bound once
        # if not hasattr(self, "popupID1"):
        #     self.popupID1 = wx.NewId()
        #     self.popupID2 = wx.NewId()
        #     self.popupID3 = wx.NewId()
        #     self.popupID4 = wx.NewId()
        #     self.popupID5 = wx.NewId()
        #     self.popupID6 = wx.NewId()

        #     self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
        #     self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
        #     self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
        #     self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
        #     self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
        #     self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)

        # # make a menu
        # menu = wx.Menu()
        # # add some items
        # menu.Append(self.popupID1, "FindItem tests")
        # menu.Append(self.popupID2, "Iterate Selected")
        # menu.Append(self.popupID3, "ClearAll and repopulate")
        # menu.Append(self.popupID4, "DeleteAllItems")
        # menu.Append(self.popupID5, "GetItem")
        # menu.Append(self.popupID6, "Edit")

        # # Popup the menu.  If an item is selected then its handler
        # # will be called before PopupMenu returns.
        # self.PopupMenu(menu)
        # menu.Destroy()

    def _create_list_columns(self):
        self._widget_list_ctrl.InsertColumn(0, "Number")
        self._widget_list_ctrl.InsertColumn(1, "Host")
        self._widget_list_ctrl.InsertColumn(2, "Port", wx.LIST_FORMAT_RIGHT)
        self._widget_list_ctrl.InsertColumn(3, "Path")
        self._widget_list_ctrl.InsertColumn(4, "Arguments")
        self._widget_list_ctrl.InsertColumn(5, "Pre-Wait")
        self._widget_list_ctrl.InsertColumn(6, "Post-Wait")

        self._widget_list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self._widget_list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self._widget_list_ctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        self._widget_list_ctrl.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
        self._widget_list_ctrl.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)
        self._widget_list_ctrl.SetColumnWidth(5, wx.LIST_AUTOSIZE_USEHEADER)
        self._widget_list_ctrl.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER)

    def _populate_list_ctrl(self):
        self._create_list_columns()
        cues = self._cue_sheet.get_cues()
        for i in range(len(cues)):
            _cue = cues[i]
            self._widget_list_ctrl.InsertStringItem(i, _cue.get_identifier()) # sets columns 0
            self._widget_list_ctrl.SetStringItem(i, 1, "XXY")
            self._widget_list_ctrl.SetStringItem(i, 2, "PORTDUMMY")
            self._widget_list_ctrl.SetStringItem(i, 3, "PATHDUMMY")
            self._widget_list_ctrl.SetStringItem(i, 4, "ARGSDUMMY")
            self._widget_list_ctrl.SetStringItem(i, 5, str(_cue.get_pre_wait()))
            self._widget_list_ctrl.SetStringItem(i, 6, str(_cue.get_post_wait()))

        # Select an item
        if self._cue_sheet.get_size() > 0:
          self._widget_list_ctrl.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self._current_item = 0

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
        self._frame = MainFrame(None, -1, "Open Show")
        self._frame.Show(True)
        self.SetTopWindow(self._frame)
        # look, we can use twisted calls!
        reactor.callLater(2, self._call_later_cb)
        return True

    def get_frame(self):
      return self._frame
