'''
Created on Mar 4, 2020

@author: brandon
'''

import os
from tkinter import Frame, filedialog, StringVar, Label, Button, Radiobutton, messagebox, Menu, re
from tkinter.constants import GROOVE, W, E, N, S, LEFT, X
from tkinter.font import Font
from Back_End.TrackerBasic import InitTracker, CharaBasic
from GUI.AddCharacterDialog import CharacterDialog
from GUI.AddModFileDialog import ModFileDialog
from GUI.CharacterDisplayFrame import CharaDisplay
from Back_End.TemporaryModifier import TempModifier 


class DisplayBasic(Frame):   
    
    def __init__(self, master = None, theInitTracker = None):
        '''
        '''
        super().__init__(master)
        self.boldFont = Font(size=12, weight='bold')
        self.config(bg ="gray")
        
        if theInitTracker == None:
            self.initList = InitTracker()
            self.turnChara = None
        else:
            self.initList = theInitTracker
            # Check that the list of characters is not empty.
            if len(self.initList.charaList) > 0:
                self.turnChara = self.initList.charaList[0]
            else:
                self.turnChara = None
        
        # Gets the current working directory of the frame, used to set the initial directories for
        # filedialog.
        self.baseDirectory = os.getcwd()
        # The path and name of the file this display will save to. Initialized as empty to be 
        # defined by the user.
        self.saveName = ''
        
        # The frame containing the list of characters, sorted in order of their initiative.
        self.listFrame = Frame(self)
        # The frame containing the displays for the character who's turn it currently is as well 
        # as the character currently selected.
        self.charaFrame = Frame(self)
        
        # Constructing the menu system for the frame.
        self.menuBar = Menu(self)
        self.buildMenu()
        master.config(menu=self.menuBar)
        
        # The variable that will hold the string value of the round count.
        self.rndString = StringVar()
        self.rndString.set(self.initList.round)
        
        # The label indicating the number of rounds that have passed.
        self.roundLabel = Label(self, text = "Round: " + self.rndString.get(), font= self.boldFont)
        self.roundLabel.grid(row = 0, column = 0, sticky = N+S+E+W)
        
        
        turnCharaLabel = Label(self.charaFrame, text = "Current Turn:", font = self.boldFont,
                               anchor = W)
        turnCharaLabel.pack(fill = X)
        # The frame displaying the information of the character who's current turn it is. 
        self.turnCharaFrame = CharaDisplay(self.charaFrame, self.turnChara, self)
        
        
        EndTurnButton = Button(self, text = "End Turn", font = self.boldFont, bg = "green",
                               command = self.endTurn, relief = GROOVE)
        EndTurnButton.grid(row = 1, column = 2, sticky = W+E+N+S)
        
        # Holds the name of the character that has been selected to be removed.
        self.toBeRemoved = StringVar()
        
        # Holds the name of the character to be copied.
        self.toBeCopied = StringVar()
        
        
        disCharaLabel = Label(self.charaFrame, text = "Selected Character:", font = self.boldFont,
                              anchor = W)
        disCharaLabel.pack(fill = X)
        
        # Holds the name of the character that is currently displayed in the displayCharaFrame.
        self.displayString = StringVar()
        # The character displayed in the displayCharaFrame, initialized to None to be selected 
        # later by the user.
        self.displayChara = None
        # The frame displaying the information of the character currently selected by the user.
        self.displayCharaFrame = CharaDisplay(self.charaFrame, self.displayChara, self)
        
        # A radiobutton list holding the buttons used to change the current display character.
        self.buttonList = []
        # A radiobutton list holding the buttons that will select a character for removal.
        self.removeList = []
        
        self.copyList = []
        
        self.charaSelect()
        
        self.listFrame.grid(row = 1, column = 0, sticky = N)
        self.charaFrame.grid(row = 1, column = 1)
        self.pack()
        
    def buildMenu(self):
        '''
        Constructs the drop down menus of the frame.
        File: Load, Save, Save As, and Close.
        Help: Abbreviations, Initiative, and About.
        '''
        fileMenu = Menu(self.menuBar, tearoff = 0)
        fileMenu.add_command(label = 'Load', command = self.load)
        fileMenu.add_command(label = 'Save', command = self.save)
        fileMenu.add_command(label = 'Save As', command =self.saveAs)
        fileMenu.add_command(label = 'Close', command = self.master.quit)
        self.menuBar.add_cascade(label = 'File', menu = fileMenu)
        
        modsMenu = Menu(self.menuBar, tearoff = 0)
        modsMenu.add_command(label = 'Modifier Info', command = self.modInfo)
        modsMenu.add_command(label = 'Add Modifier File', command = self.addModFile)
        modsMenu.add_command(label = 'Edit Modifier File', command = self.editModFile)
        self.menuBar.add_cascade(label = 'Modifiers', menu = modsMenu)
        
        helpMenu = Menu(self.menuBar, tearoff = 0)
        helpMenu.add_command(label = 'Abbreviations', command = self.abbrevAbout)
        helpMenu.add_command(label = 'Init Limitations', command = self.initiativeAbout)
        helpMenu.add_command(label = 'About', command = self.menuAbout)
        self.menuBar.add_cascade(label = 'Help', menu = helpMenu)
        
     
    def load(self):
        '''
        Opens a file dialog, prompting user to select a file to load.
        Takes text files and reads in the information using regular expression.
        If no file is selected no changes will be made and the frames will refresh themselves.
        
        It expects characters to be written in the format (where X is an integer value):
        name: character name hp: X init: X \n
        
        Modifiers should immediately follow the character they are attached to and have the format
        (where X is an integer value):
        mod: modifier name dur: X des: the description of the modifier, including numeric values \n
        
        Modifiers can also have the format:
        mod: modifirer name dur: X \n
        '''
        loadFileName = filedialog.askopenfilename(initialdir = self.baseDirectory + "/Save_Load_Files/", 
                                                  defaultextension = ".txt", title = "Load File")
        
        if loadFileName != '' and loadFileName != None:
            
            with open(file = loadFileName) as loadFile:
                if loadFile != None:
                    self.saveName = loadFileName
                    self.initList.charaList = []
                    
                    loadChara = None
                    
                    for line in loadFile:
                    
                        charaSearch = re.search('name: *(.*?) *hp: *([-0-9]+) *init: *([-0-9]+)', line, flags = re.IGNORECASE)
                        
                        if charaSearch != None:
                        
                            name = charaSearch.group(1)
                            charaHP = int(charaSearch.group(2))
                            charaInit = int(charaSearch.group(3))
                            
                            loadChara = CharaBasic(theName=name, theHealth=charaHP, theInit=charaInit)
                        
                            self.initList.addChara(loadChara)
                        
                        else:
                            
                            modSearch = re.search('mod: *(.*?) *dur: *([-0-9]+) *des: *(.*)', line, flags = re.IGNORECASE)
                            
                            if modSearch != None:
                                statusName = modSearch.group(1)
                                statusDur = int(modSearch.group(2))
                                statusDes = modSearch.group(3)
                            else:
                                modSearch = re.search('mod: *(.*?) *dur: *([-0-9]+) *', line, flags = re.IGNORECASE)
                                if modSearch != None:
                                    statusName = modSearch.group(1)
                                    statusDur = int(modSearch.group(2))
            
                                    with open(file = "./Modifiers/" + statusName + '.txt')as modFile:
                                        modFile.readline().rstrip(' \n')
                                        statusDes = modFile.readline().rstrip(' \n')                   
                        
                            tempMod = TempModifier(theTitle=statusName, theDuration= statusDur,
                                                   theDesc=statusDes)
                            
                            loadChara.mods.addMod(tempMod)
                    
        self.charaSelect()
        if len(self.initList.charaList) > 0:
            self.initList.turn = 0
            self.turnChara = self.initList.charaList[0]
        self.turnCharaFrame.rebuild(self.turnChara)
        self.displayCharaFrame.rebuild()
                
    def save(self):
        '''
        '''
        # If the name of the file has not been established, run saveAs.
        if self.saveName == '' or self.saveName == None:
            self.saveAs()
        # If the file name has been established overwrite the old file.
        else:
            self.writeSaveFile(self.saveName)
            
            
    def saveAs(self):
        '''
        '''
        saveFileName = filedialog.asksaveasfilename(initialdir = self.baseDirectory + "/Save_Load_Files/", 
                                                    defaultextension = ".txt", 
                                                    initialfile = self.saveName,
                                                    title = "Save As")
        
        if saveFileName != '' and saveFileName != None:
            self.writeSaveFile(saveFileName)
        
                     
    def writeSaveFile(self, fileName):
        '''
        '''
        with open(file =fileName, mode = 'w') as saveFile:
            self.saveName = fileName
            for chara in self.initList.charaList:
                saveFile.write("Name: " + chara.charaName + " HP: " + str(chara.health) + " Init: " + str(chara.initiative) + "\n")
        
                for mod in chara.mods.myDict.keys():
                    tempMod = chara.mods.myDict[mod]
                    
                    saveFile.write("Mod: " + tempMod.title + " Dur: " + str(tempMod.duration) + " Des: " + str(tempMod.desc) + "\n")
    
    def modInfo(self):
        modFileName = filedialog.askopenfilename(initialdir = self.baseDirectory + "/Modifiers/", 
                                                  defaultextension = ".txt", 
                                                  title = "Select a Modifier to View")
        
        if modFileName != '' and modFileName != None:
            
            with open(file = modFileName) as modFile:
                modifierString = modFile.read()
            
            messagebox.showinfo(title="Modifier Information", message = modifierString)
    
    
    def addModFile(self):
        
        addDialog = ModFileDialog(self)
        if addDialog.isValid:
            cleanedModName = addDialog.modName.rstrip(' \n')
            modFileName = self.baseDirectory + "/Modifiers/" + cleanedModName + ".txt"
            self.writeModFile(modFileName, addDialog.modName, addDialog.shortDes, 
                              addDialog.fullDes)
    
    def editModFile(self):
        modFileName = filedialog.askopenfilename(initialdir = self.baseDirectory + "/Modifiers/", 
                                                  defaultextension = ".txt", 
                                                  title = "Select Modifier to Edit")
        
        if modFileName != '' and modFileName != None:
            
            with open(file = modFileName, mode = 'r') as modFile:
                modName = modFile.readline().rstrip(' \n')
                shortDescription = modFile.readline().rstrip(' \n')
                fullDescription = modFile.read().rstrip(' \n')
                
            addDialog = ModFileDialog(self, theName=modName, theShortDes=shortDescription,
                                      theFullDes=fullDescription)
            
            if addDialog.isValid:
                self.writeModFile(modFileName, addDialog.modName, addDialog.shortDes, 
                                  addDialog.fullDes)
    
    def writeModFile(self, theModFileName, theModName, theShortDes, theFullDes):
        cleanedModName = theModName.rstrip(' \n')
        cleanedShortDes = theShortDes.rstrip(' \n')
        cleanedFullDes = theFullDes.lstrip(' \n')
        
        with open(file = theModFileName, mode = 'w') as modFile:
            modFile.write(cleanedModName + '\n' +  cleanedShortDes + '\n\n' + cleanedFullDes)
        
    
    def initiativeAbout(self):
        initMessage = '''As per Pathfinder norms the initiative order is 
sorted from highest to lowest. However there are a few 
occurrences this program does not take into account and is
therefore up to you the user to handle.

Ties: Should two or more characters have the same 
      initiative the program will simply put the 
      characters in the order in which they are added, 
      with whoever was added first being at the top. For
      example if Bob, Jill and Tim all have the same 
      initiative and Bob was added first followed by Tim 
      and then Jill, the program will put them in the 
      order: Bill, Tim, Jill.
      
      The rules for breaking ties in initiative, is that
      the character with the higher initiative modifier
      goes first. If their modifiers are tied as well, 
      then they roll off to see who goes first.
      
      There are a few ways that you can make this work. 
      1. Simply remember who goes first. It can be a bit 
      of a nuisance, but generally most ties are just 
      between two people and aren't game ending if the 
      order gets mixed up on occasion.
      2. Add them in order from first to last. If you add
      them in like this they will be in the correct order,
      and if you happen to mess up don't be afraid to 
      remove one and then re-add them.
      3. Change their initiatives slightly. Simply change 
      one of the character's initiatives so that they are 
      in the correct order. Example: Bob and Jill are tied
      at initiative 18, but Jill's modifier is greater so 
      she goes first. If no one has initiative 19 then, 
      just raise Jill's initiative to 19, but if there is
      you can still just lower Bob's initiative to 17.
      
Surprise Rounds: This program doesn't have a way to sort 
                 out who has a surprise round and who does
                 not. It is down to you and you're players
                 to remember who does and who does not.
                 You can however use the tracker to ensure
                 that everyone in the surprise round goes
                 in the correct order.
'''
        messagebox.showinfo(title = 'Issues Concerning Initiative', 
                            message = initMessage)
      
    def abbrevAbout(self):
        abrevMessage = '''There are a number of abbreviations and symbols used 
in this program. Listed here are the ones used and what 
they mean:

+: Additional. Buttons with this marker will display 
additional information about the related item. Currently 
only used with modifiers, this button will pull up the 
file with the modifiers full description, if it has one.

abi: Ability. This refers to a characters abilities 
(Strength, Dexterity, Constitution, Intelligence, Wisdom,
and Charisma).
    Example: -2 abi checks. Would apply a -2 to ALL 
    ability checks a character makes.

atk: Attack. This is used to refer to the bonus one has to
their attack action. 
    Example: -2 atk would mean that there is a -2 modifier
    attached to all the characters attack actions.

X: Remove. On a button this indicates that this button 
will remove the related item. You will see this next to 
characters in the initiative order and at the end of 
modifiers in the character display. 
        '''
        messagebox.showinfo(title = 'Abbreviations and Symbols', 
                            message = abrevMessage)
    
    def menuAbout(self):
        aboutMessage = '''This program was designed to make handling combat in 
Pathfinder easier, by tracking character initiative order
and the various modifiers that are affecting them during 
combat. It is intended for players who have a working 
knowledge of the Pathfinder system and understand some of
it's nuances and vocabulary. 

While the system is not designed specifically for 5th 
Edition Dungeons and Dragons it can be used for it. One 
would just have to take the time to create modifiers 
appropriate to 5th Edition.

Made by Brandon Watt.
        '''
        messagebox.showinfo(title = 'About the Initiative Tracker', 
                            message = aboutMessage)
    
    def charaSelect(self):
        
        self.resetButtonLists()
        # Remove any previous orphaned internal frames.
        for frames in self.listFrame.pack_slaves():
            frames.destroy()
        
        tempButton = Radiobutton()
        removeButton = Radiobutton()
        copyButton = Radiobutton()
        
        pickFrame = Frame(self.listFrame)
        
        for i in range(0, len(self.initList.charaList)):
            tempButton = Radiobutton(pickFrame, text = self.initList.charaList[i].listDisplay(), 
                                     variable = self.displayString, 
                                     value = self.initList.charaList[i].charaName,
                                     indicatoron = 0, command = self.changeDisChara)
            
            
            self.buttonList.append(tempButton)
            removeButton = Radiobutton(pickFrame,
                                       text = " X ",
                                       variable = self.toBeRemoved,
                                       value =  str(self.initList.charaList[i].charaName),
                                       indicatoron = 0,
                                       command = self.removeButtons)
            
            self.removeList.append(removeButton)
            
            copyButton = Radiobutton(pickFrame,
                                       text = " Copy ",
                                       variable = self.toBeCopied,
                                       value =  str(self.initList.charaList[i].charaName),
                                       indicatoron = 0,
                                       command = self.copyCharaAction)
            
            self.copyList.append(copyButton)
            
            
            self.buttonList[i].grid(row = i, column = 0, sticky = N+S+W+E)
            self.removeList[i].grid(row = i, column = 1, sticky = N+S+W+E)
            self.copyList[i].grid(row = i, column = 2, sticky = N+S+W+E)
        
        
        addButton = Button(pickFrame, text = "Add Character", command = self.addCharacter)
        addButton.grid(row = len(self.buttonList), column = 0)
        self.buttonList.append(addButton)
        
        resetButton = Button(pickFrame, text = "Reset", command = self.charaSelect)
        resetButton.grid(row = len(self.removeList), column = 1, columnspan = 2, sticky = W+E)
        self.removeList.append(resetButton)
        
        pickFrame.pack(side = LEFT, fill = X)
        
          
    def changeDisChara(self):
        
        for chara in self.initList.charaList:
            if chara.charaName == self.displayString.get():
                self.displayChara = chara
                break
        
        self.displayCharaFrame.rebuild(self.displayChara)
        
    def addCharacter(self):
        
        add = CharacterDialog(self)
        if add.isValid:
            self.entryButtonCommand(theName=add.name, theHealth= add.health, 
                                    theInit=add.initiative)
              
    
    def endTurn(self):
        self.initList.nextTurn()
        
        # Check that there are characters in the initiative list.
        if len(self.initList.charaList) > 0:
            self.turnChara = self.initList.charaList[self.initList.turn]
        
        self.rndString.set(self.initList.round)
        self.roundLabel.config(text = "Round: " + self.rndString.get()) 
        
        self.charaSelect()
        self.turnCharaFrame.rebuild(self.turnChara)
        self.displayCharaFrame.rebuild(self.displayChara)
    
    def resetButtonLists(self):
        for button in self.buttonList:
            button.destroy()
            
        for b in self.removeList:
            b.destroy()
        
        for b in self.copyList:
            b.destroy()
        
        self.buttonList = []
        self.removeList = []
        self.copyList = []
    
    def entryButtonCommand(self, theName, theHealth, theInit):
        addedChara = CharaBasic(theName, theInit, theHealth)
        self.initList.addChara(addedChara)
        
        # Check that there are characters in the initiative list.
        if len(self.initList.charaList) > 0:
            self.turnChara = self.initList.charaList[self.initList.turn]
            self.turnCharaFrame.rebuild(self.turnChara)
        
        '''
        # If the list of characters was previously empty.
        if len(self.initList.charaList) == 1:
            # Set the lone character as the turn character.
            self.turnChara = addedChara
            self.turnCharaFrame.rebuild(self.turnChara)
        '''
        
            
        self.resetButtonLists()
        self.charaSelect()
        
    def removeButtons(self):
        
        removeChara = None
        #print(self.toBeRemoved.get())
        for chara in self.initList.charaList:
            if chara.charaName == self.toBeRemoved.get():
                removeChara = chara
                break
        
        #print(removeChara.charaName)
        self.initList.removeChara(removeChara)
        
        if removeChara == self.turnChara:
            if len(self.initList.charaList) > 0:
                self.turnChara = self.initList.charaList[self.initList.turn]
            else:
                self.turnChara = None
        if removeChara == self.displayChara:
            self.displayChara = None
            
        self.charaSelect()
        self.turnCharaFrame.rebuild(self.turnChara)
        self.displayCharaFrame.rebuild(self.displayChara)
        
    def copyCharaAction(self):
        copiedChara = None
        
        for chara in self.initList.charaList:
            if chara.charaName == self.toBeCopied.get():
                copiedChara = chara
                break
            
        add = CharacterDialog(self, theName= copiedChara.charaName, theHealth= copiedChara.health,
                              theInit= copiedChara.initiative)
        
        if add.isValid:
            self.entryButtonCommand(theName=add.name, theHealth= add.health, 
                                    theInit=add.initiative)
    