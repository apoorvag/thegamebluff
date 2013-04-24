import os
import wx
import UI_wait_response
import UI_wait_request
import PeerDiscovery.UserModule

        
class UI_Start(wx.Frame):
               
    def __init__(self, backgorund, umobj, parent=None, id=-1):
        #print "inside Example constructor\n"
        self.frame = wx.Frame.__init__(self, parent, id, "Bluff-working", size=(1000, 800)) 
        self.background = background
        self.um = umobj
        self.InitUI()
        
    def InitUI(self):   
        font = wx.Font(20,  wx.ROMAN, wx.ITALIC, wx.NORMAL)
        
        panel = wx.Panel(self) #panel
        #panel = Panel1(self.frame, -1, self.background)
        bmp1 = wx.Image(self.background, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # image's upper left corner anchors at panel coordinates (0, 0)
        self.bg = wx.StaticBitmap(self, -1, bmp1, (0, 0))
        
        
        cbtn1 = wx.Button(self.bg, label='Start Game', pos=(200, 250), size=(200, 80))
        cbtn1.Bind(wx.EVT_BUTTON, self.onButton1)
        cbtn1.SetFont(font)
        
        cbtn2 = wx.Button(self.bg, label='Quit', pos=(400, 500), size=(100, 30))
        cbtn2.Bind(wx.EVT_BUTTON, self.OnClose)
        cbtn1.SetFont(font)
        
        """text"""
        text = wx.StaticText(self.bg, id=-1, label="Please Enter Your Name: ",style=wx.ALIGN_CENTER, pos=(50, 100), size=(100, 50))
        font = wx.Font(20,  wx.ROMAN, wx.ITALIC, wx.NORMAL)
        text.SetFont(font)
        
        """get user name"""
        self.inputbox = wx.TextCtrl(self.bg, -1, "", pos=(200, 150), size=(150, 25))
        font = wx.Font(15,  wx.ROMAN, wx.ITALIC, wx.NORMAL)
        self.inputbox.SetFont(font)
        
            
        self.SetSize((600, 600))
        self.SetTitle('Bluff Game')
        self.Centre()
        
        # show all stuffs
        self.Show(True)          
        
        
    def OnClose(self, e):
        self.Close(True)
    
    def onButton1(self,event):
        self.username = self.inputbox.GetValue()      
        print "Start Game: " + self.username
        
        ui_join = UI_Joingame(self.username, self.background, self.um)
        self.Close(True)

class UI_Joingame(wx.Frame):
    
    def __init__(self, user, background, um, parent=None, id=-1):
        #print "inside Example constructor\n"
        wx.Frame.__init__(self, parent, id, "Bluff-working", size=(1000, 800)) 
        self.username = user
        self.background = background
        self.um = um
        self.InitUI() 
        
        
    def InitUI(self):   
        font = wx.Font(20,  wx.ROMAN, wx.ITALIC, wx.NORMAL)
        
        """panel"""
        panel = wx.Panel(self)
        bmp1 = wx.Image(self.background, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # image's upper left corner anchors at panel coordinates (0, 0)
        self.bg = wx.StaticBitmap(self, -1, bmp1, (0, 0))
        
        """buttons"""
        cbtn1 = wx.Button(self.bg, label='Create a new game', pos=(150, 180), size=(300, 60))
        cbtn1.Bind(wx.EVT_BUTTON, self.onButton1)
        cbtn1.SetFont(font)
        
        cbtn2 = wx.Button(self.bg, label='Join a game', pos=(150, 300), size=(300, 60))
        cbtn2.Bind(wx.EVT_BUTTON, self.onButton2)
        cbtn2.SetFont(font)
        
        cbtn3 = wx.Button(self.bg, label='Quit', pos=(400, 500), size=(100, 30))
        cbtn3.Bind(wx.EVT_BUTTON, self.OnClose)
        
        """show player"""
        text = wx.StaticText(self.bg, id=-1, label='Player: ' + self.username, style=wx.ALIGN_CENTER, pos=(50, 20), size=(100, 50))
        font = wx.Font(20,  wx.ROMAN, wx.ITALIC, wx.NORMAL)
        text.SetFont(font)
        
        self.SetSize((600, 600))
        self.SetTitle('Bluff Game')
        self.Centre()
        self.Show(True)
    
    def OnClose(self, e):
        self.Close(True)
    
    def onButton1(self, event):   
        print "Create a new game"
        ui_wait = UI_wait_response.Wait_response(self.username, self.background)
        
        print "Send Request"
        PeerDiscovery.UserModule.sendGameRequest(self.um, self.username)
        
        self.Close(True)
        
    def onButton2(self, event):
        print "Join a game"
        ui_wait = UI_wait_request.Wait_request(self.username, self.background)
        
        print "Accept Request"  
        PeerDiscovery.UserModule.acceptGameRequest(self.um, self.username)
        
        self.Close(True)
        
        
        
                
if __name__ == '__main__':
    app = wx.PySimpleApp()
    
    picpath = 'pictures'
    tablecloth = 'table1.jpg'
    background = os.path.join(picpath, tablecloth)
    
    """backend UserModule"""
    umobj = PeerDiscovery.UserModule.UsrModule()
    
    login = UI_Start(background, umobj)  
    app.MainLoop()