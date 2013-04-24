import wx
import time

class Wait_response(wx.Frame):
    time_remain = 30
    
    def __init__(self, username, backgorund, parent=None, id=-1):
        self.frame = wx.Frame.__init__(self, parent, id, "Bluff-working", size=(1000, 800)) 
        self.username = username
        self.backgorund = backgorund
        self.InitUI()
    
    def InitUI(self):
        """panel"""
        panel = wx.Panel(self)
        bmp1 = wx.Image(self.backgorund, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # image's upper left corner anchors at panel coordinates (0, 0)
        self.bg = wx.StaticBitmap(self, -1, bmp1, (0, 0))
        
        """wait other players"""
        text = wx.StaticText(self.bg, id=-1, label="Waiting for response: ", style=wx.ALIGN_CENTER, pos=(50, 150), size=(100, 50))
        font = wx.Font(40,  wx.ROMAN, wx.ITALIC, wx.NORMAL)
        text.SetFont(font)
        
        """player name"""
        text = wx.StaticText(self.bg, id=-1, label='Player: ' + self.username, style=wx.ALIGN_CENTER, pos=(50, 20), size=(100, 50))
        font = wx.Font(20,  wx.ROMAN, wx.ITALIC, wx.NORMAL)
        text.SetFont(font)
        
        """for the clock"""
        #style = gizmos.LED_ALIGN_CENTER
        #self.led = gizmos.LEDNumberCtrl(self, -1, (50, 200), (100,50), style)
        # default colours are green on black
        #self.led.SetBackgroundColour("blue")
        #self.led.SetForegroundColour("yellow")
        self.OnTimer(None)
        self.timer = wx.Timer(self, -1)
        # update clock digits every second (1000ms)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        
        """show remain time"""
        self.time_remain = 30
        
        text = wx.StaticText(self.bg, id=-1, label=str(self.time_remain) + 's', style=wx.ALIGN_CENTER, pos=(250, 200), size=(100, 50))
        font = wx.Font(35,  wx.ROMAN, wx.ITALIC, wx.NORMAL)
        text.SetFont(font)
        
        """close button"""
        cbtn = wx.Button(self.bg, label='Quit', pos=(400, 500), size=(100, 30))
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)
        
        self.SetSize((600, 600))
        self.SetTitle('Bluff Game')
        self.Centre()
        
        """show interface"""
        self.Show(True)
        
    def OnClose(self, e):
        self.Close(True)
    
    def OnTimer(self, event):        
        """show remain time"""
        self.time_remain -= 1