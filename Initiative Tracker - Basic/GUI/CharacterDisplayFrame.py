'''
Created on Mar 4, 2020

@author: brandon
'''

import os
from tkinter import Frame, filedialog, StringVar, Label, Entry, Button, Radiobutton, DISABLED, messagebox
from tkinter.constants import LEFT, BOTH, W, E, N, S, SUNKEN
from tkinter.font import Font
from Back_End.TemporaryModifier import TempModifier
from GUI.AddModDialog import ModifierDialog
from GUI import ModDurationDialog


class CharaDisplay(Frame):
     
    def __init__(self, master = None, theChara = None, theTracker = None):
         
        super().__init__(master, bd = 10)
        self.boldFont = Font(size=9, weight='bold')
        
        self.hasTracker = False
        self.tracker = theTracker
        if self.tracker != None:
            self.hasTracker = True
        
        self.topFrame = Frame(self)
        self.modFrame = Frame(self)
        self.addFrame = Frame(self)
        self.chara = theChara
        
        self.baseDirectory = os.getcwd()
        
        self.displayName = StringVar()
        self.displayHealth = StringVar()
        self.displayInit = StringVar()
        self.modList = []
        
        self.dmgEntry = StringVar()
        self.toBeRemoved = StringVar()
        self.modSearch = StringVar()
        
        if self.chara == None:
            self.displayName.set("")
            self.displayHealth.set("")
            self.displayInit.set("")
        else:
            self.displayName.set(self.chara.charaName)
            self.displayHealth.set(self.chara.health)
            self.displayInit.set(self.chara.initiative)           
        
        self.buildTopDisplay()
        self.buildModsDisplay()
        self.pack()
        
        
    def buildTopDisplay(self):
        
        nameLabel = Label(self.topFrame, text = "Name: ", justify = LEFT)
        nameLabel.grid(row = 0, column = 0, sticky = W)
        identLabel = Label(self.topFrame, textvariable = self.displayName, justify = LEFT,
                           font = self.boldFont)
        identLabel.grid(row = 0, column = 1, sticky = W)
        
        nameLabel = Label(self.topFrame, text = "Initiative: ", justify = LEFT)
        nameLabel.grid(row = 1, column = 0, sticky = W)
        initEntry = Entry(self.topFrame, textvariable = self.displayInit, width = 5,
                          font = self.boldFont)
        #width = int(identLabel.cget("width"))
        initEntry.bind("<Return>", self.changeInit)
        initEntry.grid(row = 1, column = 1, sticky = W)
        
        
        healthLabel = Label(self.topFrame, text = "Health: ", justify = LEFT)
        healthLabel.grid(row = 2, column = 0, sticky = N+W)
        hpLabel = Label(self.topFrame, textvariable = self.displayHealth, justify = LEFT,
                        font = self.boldFont)
        hpLabel.grid(row = 2, column = 1, sticky = N+W)
        
        
        healthLabel = Label(self.topFrame, text = "DMG: ")
        healthLabel.grid(row = 2, column = 2, sticky = N+W)
        dmgEntry = Entry(self.topFrame, textvariable = self.dmgEntry)
        dmgEntry.bind("<Return>", self.dealDamage)
        dmgEntry.grid(row = 2, column = 3, sticky = N+W)
        
        spaceLabel = Label(self.topFrame, text = "")
        spaceLabel.grid(row = 3, column = 0)
        
        self.topFrame.pack(fill = BOTH)
    
       
    def buildModsDisplay(self):
        if self.modFrame != None:
            for frames in self.modFrame.grid_slaves():
                frames.destroy()
        
        nameLabel = Label(self.modFrame, text = "Status: ", relief=SUNKEN, font = self.boldFont)
        nameLabel.grid(row = 0, column = 0, sticky = W+E+N+S)
        
        rndLabel = Label(self.modFrame, text = "Duration: ", relief=SUNKEN, font = self.boldFont)
        rndLabel.grid(row = 0, column = 1, sticky = W+E+N+S)
        
        descLabel = Label(self.modFrame, text = "Description: ", width = 32, relief=SUNKEN,
                          font = self.boldFont)
        descLabel.grid(row = 0, column = 2, sticky = W+E+N+S)
        
        plusLabel = Label(self.modFrame, text = "  +  ", relief=SUNKEN)
        plusLabel.grid(row = 0, column = 3, sticky = W+E+N+S)
        
        removeLabel = Label(self.modFrame, text = "  X  ", relief=SUNKEN)
        removeLabel.grid(row = 0, column = 4, sticky = W+E+N+S)
        
        AddModButton = Button(self.modFrame, text = "Add Custom Modifier", 
                              command = self.addMod)
        AddFileMod = Button(self.modFrame, text = "Get Mod From File", 
                            command = self.addModFile)
        
        rowCount = 1
        if self.chara != None:
            
            for mod in self.chara.mods.myDict.keys():
                tempNameL = Label(self.modFrame, text = self.chara.mods.myDict[mod].title,
                                  relief=SUNKEN)
                tempNameL.grid(row = rowCount, column = 0, sticky = W+E+N+S)
                
                tempDurL = Label(self.modFrame, text = self.chara.mods.myDict[mod].duration,
                                 relief=SUNKEN)
                tempDurL.grid(row = rowCount, column = 1, sticky = W+E+N+S)
                
                tempDescL = Label(self.modFrame, text = self.chara.mods.myDict[mod].desc,
                                  wraplength = 225, relief=SUNKEN)
                tempDescL.grid(row = rowCount, column = 2, sticky = W+E+N+S)
               
                moreInfoButton = Radiobutton(self.modFrame,
                                       text = " + ",
                                       variable = self.modSearch,
                                       value =  self.chara.mods.myDict[mod].title,
                                       indicatoron = 0,
                                       command = self.moreDetails)
                
                moreInfoButton.grid(row = rowCount, column = 3, sticky=W+E+N+S)
                
                removeButton = Radiobutton(self.modFrame,
                                       text = " X ",
                                       variable = self.toBeRemoved,
                                       value =  self.chara.mods.myDict[mod].title,
                                       indicatoron = 0,
                                       command = self.removeMod)
                
                removeButton.grid(row = rowCount, column = 4, sticky=W+E+N+S)
                
                rowCount += 1
        else:
            AddModButton["state"] = DISABLED
            AddFileMod["state"] = DISABLED
            
        AddModButton.grid(row = rowCount, column = 0) 
        AddFileMod.grid(row = rowCount, column = 1)  
        self.modFrame.pack()
            
    def synchronize(self):
        if self.hasTracker:
            if self.tracker != None:
                try:
                    if self.tracker.turnChara == self.tracker.displayChara:
                        self.tracker.turnCharaFrame.rebuild(self.tracker.turnChara)
                        self.tracker.displayCharaFrame.rebuild(self.tracker.displayChara)
                except AttributeError:
                    self.hasTracker = False
    
    
    def dealDamage(self, event=None):
        value = self.dmgEntry.get()
        if value.isdigit() or value.lstrip("-").isdigit():
            self.chara.damage(int(value))
            self.displayHealth.set(str(self.chara.health))
            
            self.synchronize()
            
        self.dmgEntry.set('')
        self.topFrame.pack()
    
    def changeInit(self, event=None):
        value = self.displayInit.get()
        if value.isdigit():
            if self.hasTracker:
                #try:
                self.tracker.initList.adjustInit(self.chara, int(value))
                self.tracker.charaSelect()
                self.synchronize()
                
                if len(self.tracker.initList.charaList) > 0:
                    self.tracker.turnChara = self.tracker.initList.charaList[self.tracker.initList.turn]
                
                self.tracker.turnCharaFrame.rebuild(self.tracker.turnChara)
                
                
                #except AttributeError:
                #    self.hasTracker = False
            else:
                self.chara.initiative = int(value)
            
        
    def rebuild(self, theChara = None):
        self.chara = theChara
        
        if self.chara != None:
            self.displayName.set(self.chara.charaName)
            self.displayHealth.set(self.chara.health)
            self.displayInit.set(self.chara.initiative)
        else:
            self.displayName.set("")
            self.displayHealth.set("")
            self.displayInit.set("")
        
        for item in self.modFrame.grid_slaves():
            item.grid_remove()
        # listitem.destroy() 
        #pack_forget pack_remove
        #grid_forget grid_remove
        
        self.topFrame.pack()
        self.buildModsDisplay()
        
        self.pack()
        
    def addMod(self):
        
        dialog = ModifierDialog(self)
        if dialog.isValid:
            tempMod = TempModifier(theTitle=dialog.name, theDuration=dialog.duration,
                                   theDesc=dialog.description)
            self.chara.mods.addMod(tempMod)
            self.buildModsDisplay()
            
            self.synchronize()
    
    def removeMod(self):
        self.chara.mods.removeMod(self.toBeRemoved.get())
        self.buildModsDisplay()
        self.synchronize()
        
    def addModFile(self):
        
        modFile = filedialog.askopenfile(mode = "r", initialdir = self.baseDirectory + "/Modifiers/", 
                                         defaultextension = ".txt", title = "Add Pre-Existing Modifier")
        
        if modFile != None:
            statusName = modFile.readline().rstrip(' \n')
            statusDes = modFile.readline().rstrip(' \n')
            modFile.close()
            
            query = ModDurationDialog.ModDurDialog(self)
            
            if query.isValid:
                tempMod = TempModifier(theTitle=statusName, theDuration= query.duration,
                                       theDesc=statusDes)
                self.chara.mods.addMod(tempMod)
                self.buildModsDisplay()
                
                self.synchronize()
    
    def moreDetails(self):
        
        try:
            with open(file = "./Modifiers/" + self.modSearch.get() + ".txt") as modFile:
                modDetails = modFile.read()
                modFile.close()
                messagebox.showinfo(title = "Modifier Details", 
                                    message = modDetails)
        except:
            messagebox.showwarning(title = "Bad File Read", 
                                   message = "This modifier has no associated file.")
               
        