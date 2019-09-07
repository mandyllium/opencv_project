import wx
#from Video_test import Video
from Video_file import Video


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

        self.video_inst = Video(r"C:\Users\qpjg1605\Documents\Python_proj\Auptimo\C2477.MP4")

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.count = -1

    def update(self, event):
        self.count += 1
        _, self.CurBmp = next(self.video_inst.iter_frames())
        self.Refresh()

    def On_Paint(self, event):
        dc = wx.BufferedPaintDC(self.panel, self.CurBmp)

    def On_Play_Btn(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        else:
            self.timer.Start(31.00)

    def On_Prev_Btn(self, event):
        #self.count -= 1
        _, self.CurBmp = self.video_inst.goto_frame(-1)
        self.Refresh()

    def On_Next_Btn(self, event):
        self.count += 1
        _, self.CurBmp = next(self.video_inst.iter_frames())
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