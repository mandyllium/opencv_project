import time
import subprocess

import wx

import numpy

from video import Video


class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size = (800, 500))

        self.pos = (640, 360)

        self.panel = wx.Panel(self, size = self.pos)

        self.panel.Bind(wx.EVT_PAINT, self.On_Paint)
        self.panel.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)

        self.btn = wx.Button(self, label = "Next", pos = (self.pos[0], 60))
        self.btn.Bind(wx.EVT_BUTTON, self.On_Next_Btn)

        self.btn = wx.Button(self, label = "Play", pos = (self.pos[0], 30))
        self.btn.Bind(wx.EVT_BUTTON, self.On_Play_Btn)

        self.btn = wx.Button(self, label = "Prev", pos = (self.pos[0], 0))
        self.btn.Bind(wx.EVT_BUTTON, self.On_Prev_Btn)

        self.text_ctrl = wx.TextCtrl(self, pos = (self.pos[0], 90))
        self.text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.On_Text_Enter)

        self.Bind(wx.EVT_CLOSE, self.On_Close)

        self.CurBmp = wx.Bitmap(0, 0)

        #self.video_inst = Video(r"F:\c_drive_download\Video\JASON DAY PRACTICE ROUND FOOTAGE - GOLF SWING FROM WIN AT 2014 TEMPLETON SYNCED & SLOW MOTION 1080p - YouTube.MP4", 640, 360)
        #self.video_inst = Video(r"WIN_20190811_12_34_58_Pro.mp4", 640, 360)
        #self.video_inst = Video(r"F:\c_drive_desktop\Curador\AnteriorPosterior.MOV", 640, 360)
        #print(self.video_inst.get_last_frame(), self.video_inst.get_frame_rate())

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.count = -1

    def update(self, event):
        self.count += 1
        _, self.CurBmp = self.video_inst.iter_frames()
        self.Refresh()

    def On_Paint(self, event):
        dc = wx.BufferedPaintDC(self.panel, self.CurBmp)

    def On_Play_Btn(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        else:
            self.timer.Start(0.01)

    def On_Prev_Btn(self, event):
        self.count -= 1
        _, self.CurBmp = self.video_inst.goto_frame(self.count)
        self.Refresh()

    def On_Next_Btn(self, event):
        self.count += 1
        _, self.CurBmp = self.video_inst.goto_frame(self.count, True)
        self.Refresh()

    def On_Text_Enter(self, event):
        self.count = int(self.text_ctrl.GetValue())
        _, self.CurBmp = self.video_inst.goto_frame(self.count)
        self.Refresh()

    def On_Close(self, event):
        self.Destroy()

app = wx.App()
frame = Frame(None)
frame.CenterOnScreen()
frame.Show(True)
app.MainLoop()