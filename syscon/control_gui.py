import sysconx.control
import wx
import wx.lib.newevent
import os

try:
    from threading import Thread
except ImportError:
    from dummy_threading import Thread

(RedrawEvent, EVT_REDRAW) = wx.lib.newevent.NewEvent()

class ctrlFrame(wx.Frame):
    """syscon control frame"""
    def __init__(self, parent, title, comp_name):
        self.rmname = comp_name
        self.con = sysconx.control.Connection(self.rmname)
        img = wx.Image(os.environ.get("TEMP") + "\\screen.jpeg")
        h = img.GetHeight()
        w = img.GetWidth()
        wx.Frame.__init__(self, parent, title=title, pos=(50,50), size=(w + 110, h), style=wx.DEFAULT_FRAME_STYLE)
        # img control
        #self.control = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE)
        self.control = PaintWindow(self, os.environ.get("TEMP") + "\\screen.jpeg")
        # menu
        filemenu = wx.Menu()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&syscon")
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.SetMenuBar(menuBar)
        # btns
        self.btnsizer = wx.BoxSizer(wx.VERTICAL)
        btntexts = ["run python code", "execute file", "return value", "download", "make screenshot", "shutdown (windows)", "logoff (windows)", "close client"] #...
        self.buttons = []
        func_execpy = self.getEventHandler(btntexts[0])
        func_executefile = self.getEventHandler(btntexts[1])
        func_returnvalue = self.getEventHandler(btntexts[2])
        func_download = self.getEventHandler(btntexts[3])
        func_screenshot = self.getEventHandler(btntexts[4])
        func_shutdown = self.getEventHandler(btntexts[5])
        func_logoff = self.getEventHandler(btntexts[6])
        func_stop = self.getEventHandler(btntexts[7])
        text_execpy = btntexts[0]
        text_executefile = btntexts[1]
        text_returnvalue = btntexts[2]
        text_download = btntexts[3]
        text_screenshot = btntexts[4]
        text_shutdown = btntexts[5]
        text_logoff = btntexts[6]
        text_stop = btntexts[7]
        btn_execpy = wx.Button(self, -1, text_execpy, size=(110, 20))
        btn_executefile = wx.Button(self, -1, text_executefile, size=(110, 20))
        btn_returnvalue = wx.Button(self, -1, text_returnvalue, size=(110, 20))
        btn_download = wx.Button(self, -1, text_download, size=(110, 20))
        btn_screenshot = wx.Button(self, -1, text_screenshot, size=(110, 20))
        btn_shutdown = wx.Button(self, -1, text_shutdown, size=(110, 20))
        btn_logoff = wx.Button(self, -1, text_logoff, size=(110, 20))
        btn_stop = wx.Button(self, -1, text_stop, size=(110, 20))
        self.btnsizer.Add(btn_execpy, 1, wx.EXPAND)
        self.btnsizer.Add(btn_executefile, 1, wx.EXPAND)
        self.btnsizer.Add(btn_returnvalue, 1, wx.EXPAND)
        self.btnsizer.Add(btn_download, 1, wx.EXPAND)
        self.btnsizer.Add(btn_screenshot, 1, wx.EXPAND)
        self.btnsizer.Add(btn_shutdown, 1, wx.EXPAND)
        self.btnsizer.Add(btn_logoff, 1, wx.EXPAND)
        self.btnsizer.Add(btn_stop, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, func_execpy, btn_execpy)
        self.Bind(wx.EVT_BUTTON, func_executefile, btn_executefile)
        self.Bind(wx.EVT_BUTTON, func_returnvalue, btn_returnvalue)
        self.Bind(wx.EVT_BUTTON, func_download, btn_download)
        self.Bind(wx.EVT_BUTTON, func_screenshot, btn_screenshot)
        self.Bind(wx.EVT_BUTTON, func_shutdown, btn_shutdown)
        self.Bind(wx.EVT_BUTTON, func_logoff, btn_logoff)
        self.Bind(wx.EVT_BUTTON, func_stop, btn_stop)
        #f = []
        #for i in btntexts:
        #    f.append(self.getEventHandler(i))
        #for i in range(0, len(btntexts)):
        #    self.buttons.append(wx.Button(self, -1, btntexts[i]))
        #    self.btnsizer.Add(self.buttons[i], 1, wx.EXPAND)
        #   ## f.append(self.getEventHandler(btntexts[i]))
        #    print f[i]
        #    self.Bind(wx.EVT_BUTTON, self.getEventHandler(f[i]), self.buttons[i])
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.btnsizer, 0, wx.EXPAND)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.timer = imgTimer(self)
        self.timer.Bind(EVT_REDRAW, self.TimerEVT)
        self.Show(True)
        # timer
        #TIMER_ID = 100  # pick a number #wx.Timer(self, TIMER_ID)  # message will be sent to the panel
        #self.timer.Start(100)  # x100 milliseconds
        #wx.EVT_TIMER(self, TIMER_ID, self.TimerEVT)  # call the on_timer function
        #elf.timer = wx.Timer()
        #self.timer.Start(100)#, self.timer)

    def OnExit(self,e):
        self.timer.Stop()
        self.con.send("newconnect")
        self.Close(True)
    def getEventHandler(self, capt):
        """get method for syscon function of button with text 'capt'"""
        #print capt
        if capt == "run python code":
            # command execpy
            #print 'execpy'
            return lambda x: self.con.send("execpy", wx.GetTextFromUser("Enter Python code to execute", "syscon control gui"))
        elif capt == "execute file":
            # command executefile
            #print 'executefile'
            return lambda x: self.con.send("executefile", wx.GetTextFromUser("Enter file path to execute", "syscon control gui"))
        elif capt == "return value":
            # command returnvalue
            #print 'returnvalue'
            return lambda x: self.con.send("returnvalue", wx.GetTextFromUser("Enter expression to be evaluated", "syscon control gui"))
        elif capt == "download":
            # command download
            #print 'download'
            return lambda x: self.con.send("download", wx.GetTextFromUser("Enter the local path to download the file to", "syscon control gui"), wx.GetTextFromUser("Enter download URL", "syscon control gui"))
        elif capt == "make screenshot":
            # command screenshot
            #print 'screenshot'
            return lambda x: self.con.screenshot()#self.con.send("screenshot", wx.GetTextFromUser("Enter the port to send the screenshot to (pyscreen: 56000)", "syscon control gui", "56000"))
        elif capt == "shutdown (windows)":
            # command shutdown
            #print 'shutdown'
            return lambda x: self.con.send("shutdown")
        elif capt == "logoff (windows)":
            # command logoff
            #print 'logoff'
            return lambda x: self.con.send("logoff")
        elif capt == "close client":
            # command stopcontrol
            #print 'stopcontrol'
            return lambda x: self.con.close()
        else:
            return lambda x: self.prnt(x) #self.con.close()
    def prnt(self, txt):
        print txt
        return 1 + 1

    def TimerEVT(self, e):
        #print "EVT"
        #self.control.Destroy()
        #self.control = PaintWindow(self, os.environ.get("TEMP") + "\\screen.jpeg")
        self.control.redraw(os.environ.get("TEMP") + "\\screen.jpeg")
        self.Refresh()
        return lambda x: self.control.redraw(os.environ.get("TEMP") + "\\screen.jpeg")#;self.prnt('redraw')

class imgTimer(wx.Timer):
    def __init__(self, parent):#, upper):
        wx.Timer.__init__(self)
        self.parent = parent
        #self.pw = upper.control
        self.Start(275)

    def Notify(self):
        #print 'working'
        #self.pw.redraw(os.environ.get("TEMP") + "\\screen.jpeg")
        evt = RedrawEvent()
        try:
            self.parent.con.send("screenshot", "56000", "No.", False)
        except Exception as inst:
            print type(inst), inst
            #self.Stop()
        self.ProcessEvent(evt)

class PaintWindow(wx.Window):
    def __init__(self, parent, filename):
        wx.Window.__init__(self, parent)
        self.parent = parent
        self.pic = wx.Image(filename).ConvertToBitmap()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.pic, 1, 1, True)
        self.parent.Update()

    def OnClick(self, evt):
        # clicked??
        cx = evt.GetX()
        cy = evt.GetY()
        sz = self.GetSizeTuple()
        wd = sz[0] #width
        hg = sz[1] #height
        scr_h = 1024.0
        scr_w = 1280.0
        correct_x = scr_w / wd
        correct_y = scr_h / hg
        pos_x = int(correct_x * cx)
        pos_y = int(correct_y * cy)
        print pos_x, pos_y, "||", cx, cy, sz, wd, hg, scr_h, scr_w, correct_x, correct_y
        self.parent.con.sendMouseEvent(sysconx.control.MouseEvent("click", pos_x, pos_y))
        #evt.Skip()

    def redraw(self, filename):
        #print 'drawing'
        self.pic = wx.Image(filename, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

#def import_gui_img_listener():
#    import sysconx.gui_img_listener
#    return None

class guithread():
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        import sysconx.gui_img_listener
app = wx.App(False)
cname = wx.GetTextFromUser("Enter name of remote computer", "syscon control gui")
#thread = ThreadEngine.start_new_thread(import_gui_img_listener, ())
#thread = guithread()
frame = ctrlFrame(None, "syscon control gui", cname)
app.MainLoop()
