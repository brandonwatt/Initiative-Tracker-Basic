'''
Created on Mar 4, 2020

@author: Brandon
'''

from GUI import tkSimpleDialog
from tkinter import Label, Entry, messagebox

class CharacterDialog(tkSimpleDialog.Dialog):

    def __init__(self, master, theName = "", theHealth = 0, theInit = 0):
        self.name = theName
        self.health = theHealth
        self.initiative = theInit
        self.isValid = False
        
        super().__init__(master)
        
        
    def body(self, master):
        
        Label(master, text="Name:").grid(row=0)
        Label(master, text="Health:").grid(row=1)
        Label(master, text="Initiative:").grid(row=2)

        self.nameEntry = Entry(master)
        self.healthEntry = Entry(master)
        self.initEntry = Entry(master)
        
        self.nameEntry.insert(0, self.name)
        self.healthEntry.insert(0, str(self.health))
        self.initEntry.insert(0, str(self.initiative))
        
        self.nameEntry.grid(row=0, column=1)
        self.healthEntry.grid(row=1, column=1)
        self.initEntry.grid(row=2, column=1)
        
    def validate(self):
        try:
            self.name = self.nameEntry.get()
            self.health = int(self.healthEntry.get())
            self.initiative = int(self.initEntry.get())
            self.isValid = True
            return 1
        except ValueError: 
            messagebox.showwarning(title = "Bad Input", 
                                   message = "Illegal values, please try again.")
            self.isValid = False
            return 0
        
    def apply(self):
        tkSimpleDialog.Dialog.apply(self)