'''
Created on Mar 26, 2020

@author: Brandon
'''

from GUI import tkSimpleDialog
from tkinter import Label, Entry, Text, END, W, messagebox

class ModFileDialog(tkSimpleDialog.Dialog):

    def __init__(self, master, theName = "", theShortDes = "", theFullDes = ""):
        self.modName = theName
        self.shortDes = theShortDes
        self.fullDes = theFullDes
        self.isValid = False
        
        super().__init__(master)
        
        
    def body(self, master):
        
        Label(master, text="Modifier Name:").grid(row=0)
        Label(master, text="Short Description:").grid(row=1)
        Label(master, text="Full Description:").grid(row=2)

        self.nameEntry = Entry(master)
        self.shortDesEntry = Entry(master)
        self.fullDesEntry = Text(master)
        
        self.fullDesEntry.config(height = 15, width = 58)
        
        self.nameEntry.insert(0, self.modName)
        self.shortDesEntry.insert(0, self.shortDes)
        self.fullDesEntry.insert(END, self.fullDes)
        
        self.nameEntry.grid(row=0, column=1, sticky = W)
        self.shortDesEntry.grid(row=1, column=1, sticky = W)
        self.fullDesEntry.grid(row=2, column=1)
        
    def validate(self):
        try:
            self.modName = self.nameEntry.get()
            self.shortDes = self.shortDesEntry.get()
            self.fullDes = self.fullDesEntry.get("1.0", END)
            self.isValid = True
            return 1
        except ValueError: 
            messagebox.showwarning(title = "Bad Input", 
                                   message = "Illegal values, please try again.")
            self.isValid = False
            return 0
        
    def apply(self):
        tkSimpleDialog.Dialog.apply(self)