"""
Copyright (C) 2014 Andrew Skinner <obs@theandyroid.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""
try:
    from Tkinter import *
    from tkFileDialog import *
except ImportError:
    from tkinter import *
    from tkinter.filedialog import *
try:
    from ttk import Frame, Button, Label, Style, Combobox, LabelFrame
except ImportError:
    from tkinter.ttk import Frame, Button, Label, Style, Combobox, LabelFrame


if sys.version < '3':
    import codecs
    def u(x):
        return unicode(x,"utf-8")
else:
    def u(x):
        return x

import ctypes,ast
import ctypes.wintypes

import OBS

class gui:

    
   
    def __init__(self,config):        

        self.config = config
        self.width = 500
        self.height = 210
        self.left = 0
        self.right = 0
        self.ret = True;
        
        self.parent = Tk()
        self.parent.attributes("-topmost", 1)
        
        self.getHWNDS()
        r = self.winPos(self.obshwnd)
        self.centerOverOBS(r)
        
        self.parent.geometry("%sx%s+%s+%s" % (self.width,self.height,int(self.left),int(self.top)))
        
        self.mainFileSTR = StringVar() #filename
        self.mainSelectedClass = StringVar()
        self.lableMainClassSTR = StringVar()
        self.mainFileSelectedClass = StringVar()

        self.GUIFileSTR = StringVar() #filename
        self.GUISelectedClass = StringVar()
        self.lableGUIClassSTR = StringVar()
        self.GUIFileSelectedClass = StringVar()
        self.GUIFileClasses = []
        self.mainFileClasses = []

        
        self.initUI(config)

    def buttonMainEvent(self,event):
        self.mainFileSTR.set(askopenfilename(parent=self.parent,initialdir=(OBS.GetAppDataPath()+"/pluginData/Python")))
        self.mainRead()

    def entryMainEvent(self,event):
        self.mainFileSTR.set(self.entryMain.get())
        self.mainRead()

    def mainRead(self):
        
        try:
            print(self.mainFileSTR.get())
            self.mainFile = open(self.mainFileSTR.get(),'r')
            text = self.mainFile.read()
            p = ast.parse(text)
            self.mainFileClasses = [ node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
        except:
            print ("Problem Loading Main File")
            self.mainFileClasses = []
        
        self.setMainComboArea()
        self.canApply()

    
		
    def setMainComboArea(self): 
        if(self.mainFileClasses != []):        
            self.optionMainClass = Combobox(self.mainGroup, textvariable=self.mainFileSelectedClass,state='readonly')
            self.optionMainClass['values'] = self.mainFileClasses
            self.optionMainClass.current(0)
            self.labelMainClass.grid_forget()
            self.optionMainClass.grid(row=2,column=2,sticky=W)
        else:
            try:
                self.optionMainClass.grid_forget()
            except AttributeError:
                pass
                
            self.lableMainClassSTR.set("No Classes Found")
            self.labelMainClass.grid(row=2,column=2,sticky=W)
            


    def buttonGUIEvent(self,event):
        self.GUIFileSTR.set(askopenfilename(parent=self.parent,initialdir=(OBS.GetAppDataPath()+"/pluginData/Python")))
        self.GUIRead()

    def entryGUIEvent(self,event):
        self.GUIFileSTR.set(self.entryGUI.get())
        self.GUIRead()


    def GUIRead(self):
        try:
            self.GUIFile = open(self.GUIFileSTR.get(),'r')
            text = self.GUIFile.read()
            p = ast.parse(text)
            self.GUIFileClasses = [ node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
        except:
            print ("Problem Loading GUI File")
            self.GUIFileClasses = []
            
        self.setGUIComboArea()
        self.canApply()


    def setGUIComboArea(self):
        if(self.GUIFileClasses != []):        
            self.optionGUIClass = Combobox(self.GUIGroup, textvariable=self.GUIFileSelectedClass,state='readonly')
            self.optionGUIClass['values'] = self.GUIFileClasses
            self.optionGUIClass.current(0)
            self.labelGUIClass.grid_forget()
            self.optionGUIClass.grid(row=2,column=2,sticky=W)
        else:
            try:
                self.optionGUIClass.grid_forget()
            except AttributeError:
                pass

            self.lableGUIClassSTR.set("No Classes Found")
            self.labelGUIClass.grid(row=2,column=2,sticky=W)



    def applySettings(self,event):
        OBS.Log(self.mainFileSTR.get())
        OBS.Log(u(self.optionMainClass.get()))
        OBS.Log(self.GUIFileSTR.get())
        OBS.Log(u(self.optionGUIClass.get()))
        self.save()
        self.closeGUI(event)

    def closeGUI(self,event):
        self.parent.destroy()
        self.ret = True;
    
    def save(self):        
        self.config.SetString(u"PythonMainFile",self.mainFileSTR.get())
        self.config.SetString(u"PythonMainClass",u(self.optionMainClass.get()))
        self.config.SetString(u"PythonGUIFile",self.GUIFileSTR.get())
        self.config.SetString(u"PythonGUIClass",u(self.optionGUIClass.get()))
        self.config.SetInt(u"Persistant",0)
        self.config.SetInt(u"Background",0)
        
    def load(self):
        self.mainFileSTR.set(self.config.GetString(u"PythonMainFile"))
        self.mainRead()
        try:
            self.optionMainClass.set(self.config.GetString(u"PythonMainClass"))
        except AttributeError:
            pass
        
        self.GUIFileSTR.set(self.config.GetString(u"PythonGUIFile"))
        self.GUIRead()
        try:
            self.optionGUIClass.set(self.config.GetString(u"PythonGUIClass"))
        except AttributeError:
            pass        
        

    def canApply(self):
        try:
            if (self.GUIFileClasses != [] and self.mainFileClasses != []):
                self.btnApply.config(state=NORMAL)
            else:
                 self.btnApply.config(state=DISABLED)
        except AttributeError:
            pass

    def getHWNDS(self):
        self.obshwnd = OBS.GetMainWindow()
        self.hwndTkinter =  self.parent.winfo_id()

        

        
        
    def lockWindow(self):
        #ctypes.windll.user32.SetWindowLongA(self.hwndTkinter,-8,self.obshwnd)
        #ctypes.windll.user32.SetParent(self.hwndTkinter, self.obshwnd)


        if((ctypes.windll.user32.GetKeyState(0x91) & 0x0001) != 0):
            OBS.Log(u"lock on")
        else:
            OBS.Log(u"lock off")
            
        ctypes.windll.user32.SetActiveWindow(self.hwndTkinter)
        ctypes.windll.user32.EnableWindow(self.obshwnd,False)
        

    def unlockWindow(self):        
        ctypes.windll.user32.EnableWindow(self.obshwnd,True)
        ctypes.windll.user32.SetActiveWindow(self.obshwnd)

    def initUI(self,config):
        self.parent.focus()
        self.parent.wm_title("Config Python Plugin")  
        

            

        self.mainGroup = LabelFrame(self.parent,text="Main Python Source File", padding="5 5 5 5")
        self.mainGroup.grid(row=0,column=0,columnspan=5,sticky=W+E+N+S,pady=5,padx=5)

        self.mainGroup.columnconfigure(0, weight=1)
        self.mainGroup.columnconfigure(1, weight=1)
        self.mainGroup.columnconfigure(2, weight=1)
        self.mainGroup.columnconfigure(3, weight=1)
        self.mainGroup.columnconfigure(4, weight=1)


        self.entryMain = Entry(self.mainGroup,textvariable=self.mainFileSTR)
        self.entryMain.grid(row=0,column=0,columnspan=4,sticky=W+E)
        self.entryMain.bind("<Return>",self.entryMainEvent)
        
        btnMainBrowse = Button(self.mainGroup,text="Browse")
        btnMainBrowse.grid(row=0,column=4,columnspan=1,sticky=W+E)
        btnMainBrowse.bind("<Button-1>",self.buttonMainEvent)

       
        Label(self.mainGroup, text="Python Class:").grid(row=2,column=1,sticky=E)
        self.labelMainClass = Label(self.mainGroup, textvariable=self.lableMainClassSTR)
        self.lableMainClassSTR.set("Please Select File")
        self.labelMainClass.grid(row=2,column=2,sticky=W)


        

    
        self.GUIGroup = LabelFrame(self.parent,text="GUI Python Source File", padding="5 5 5 5")
        self.GUIGroup.grid(row=1,column=0,columnspan=5,sticky=W+E+N+S,pady=5,padx=5)

        self.GUIGroup.columnconfigure(0, weight=1)
        self.GUIGroup.columnconfigure(1, weight=1)
        self.GUIGroup.columnconfigure(2, weight=1)
        self.GUIGroup.columnconfigure(3, weight=1)
        self.GUIGroup.columnconfigure(4, weight=1)

    
        btnGUIBrowse = Button(self.GUIGroup,text="Browse")
        btnGUIBrowse.grid(row=0,column=4,columnspan=1,sticky=W+E)
        btnGUIBrowse.bind("<Button-1>",self.buttonGUIEvent)

        self.entryGUI = Entry(self.GUIGroup,textvariable=self.GUIFileSTR)
        self.entryGUI.grid(row=0,column=0,columnspan=4,sticky=W+E)
        self.entryGUI.bind("<Return>",self.entryGUIEvent)
        
        Label(self.GUIGroup, text="Python Class:").grid(row=2,column=1,sticky=E)
        self.labelGUIClass = Label(self.GUIGroup, textvariable=self.lableGUIClassSTR)
        self.lableGUIClassSTR.set("Please Select File")
        self.labelGUIClass.grid(row=2,column=2,sticky=W)


        self.frame = Frame()


        self.btnApply = Button(self.frame,text="OK",state=DISABLED)
        self.btnApply.grid(row=0,column=0,columnspan=1,padx=5,pady=5,sticky=W+E)
        self.btnApply.bind("<Button-1>",self.applySettings)

        self.btnCancel = Button(self.frame,text="Cancel")
        self.btnCancel.grid(row=0,column=1,columnspan=1,padx=5,pady=5,sticky=W+E)
        self.btnCancel.bind("<Button-1>",self.closeGUI)

        self.frame.grid(row=2,column=0,columnspan=5,sticky=E,pady=5,padx=5)
        
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        self.parent.columnconfigure(2, weight=1)
        self.parent.columnconfigure(3, weight=1)
        self.parent.columnconfigure(4, weight=1)

        self.load()#Load old settings

        self.parent.after(1,self.lockWindow)
        #self.lockWindow()
        self.parent.mainloop()
        self.unlockWindow()


    def centerWindow(self):
        self.winPos(self.parent.winfo_id())
    

    def winPos(self,hwnd):
        f = ctypes.windll.user32.GetWindowRect
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.byref(rect)
          )
        return rect
    
    def centerOverOBS(self,r):
        obsWidth = r.right-r.left
        obsHeight = r.bottom-r.top
        self.left = r.left + (obsWidth/2) - (self.width/2)
        self.top = r.top + (obsHeight/2) - (self.height/2)
        

        

