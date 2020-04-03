'''
Created on Mar 7, 2020

@author: Brandon
'''

from GUI import tkSimpleDialog
from tkinter import *
from tkinter import messagebox

class ModDurDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="Duration:").grid(row=0)
        
        self.duration = 0
        self.isValid = False

        self.durEntry = Entry(master)

        self.durEntry.grid(row=0, column=1)
        
    def validate(self):
        try:
            self.duration = int(self.durEntry.get())
            self.isValid = True
            return 1
        except ValueError:
            messagebox.showwarning(title = "Bad Input", 
                                   message = "Illegal values, please try again.")
            self.isValid = False
            return 0
        
    def apply(self):
        tkSimpleDialog.Dialog.apply(self)