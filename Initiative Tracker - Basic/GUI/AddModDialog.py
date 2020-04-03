'''
Created on Mar 4, 2020

@author: Brandon
'''

from GUI import tkSimpleDialog
from tkinter import Label, Entry, messagebox

class ModifierDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="Mod Name:").grid(row=0)
        Label(master, text="Duration:").grid(row=1)
        Label(master, text="Description:").grid(row=2)

        self.name = ""
        self.duration = 0
        self.description = ""
        self.isValid = False

        self.nameEntry = Entry(master)
        self.durEntry = Entry(master)
        self.desEntry = Entry(master)

        self.nameEntry.grid(row=0, column=1)
        self.durEntry.grid(row=1, column=1)
        self.desEntry.grid(row=2, column=1)
        
    def validate(self):
        try:
            self.name = self.nameEntry.get()
            self.duration = int(self.durEntry.get())
            self.description = self.desEntry.get()
            self.isValid = True
            return 1
        except ValueError: 
            messagebox.showwarning(title = "Bad Input", 
                                   message = "Illegal values, please try again.")
            self.isValid = False
            return 0
        
    def apply(self):
        tkSimpleDialog.Dialog.apply(self)