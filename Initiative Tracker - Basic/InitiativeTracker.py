'''
Created on Mar 11, 2020

@author: Brandon
'''

from tkinter import Tk#, messagebox
from tkinter.constants import BOTH
from GUI.InitTrackerDisplay import DisplayBasic
#import sys

if __name__ == '__main__':
    '''
    '''
    
    #try:
    root = Tk()
    
    w = 800
    h = 480
    
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    
    root.title("Initiative Tracker")
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.configure(background='gray')
    
    
    myScreen = DisplayBasic(master=root)
    
    myScreen.pack(fill = BOTH)
    
    root.mainloop()
        
    #except:
        
    #    messagebox.showerror(title="An Error Occured", message= "Unexpected Error" + str(sys.exc_info()[0]))
        
        
        