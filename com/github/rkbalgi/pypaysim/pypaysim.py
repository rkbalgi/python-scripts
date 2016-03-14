'''
Created on 15-Dec-2014

@author: Raghavendra Balgi
'''
import Tkinter as tk
from Tkinter import *

from com.github.rkbalgi.pypaysim.pydialogs import TripleDesDialog
from com.github.rkbalgi.pypaysim import event_handler as eh

LEFT_BUTTON_CLICK = '<Button-1>'

class RootFrame:
    
    def __init__(self, title_msg):
        self.title_msg = title_msg
        self.root = tk.Tk()
        self.root.title(title_msg)
        self.root.configure(width=800, height=600)
        
        self.event_handler = eh.EventHandler(self)
        # self.root.option_readfile('option_db.txt')
        self.init_components();
    
    def show(self):
        self.root.mainloop()
        self
        
        
    def init_components(self):
        self.add_menubar()
        
        # add paned window
        self.main_window = PanedWindow(self.root, width=800, height=600, orient=HORIZONTAL)
        self.main_window.config(sashwidth=2, showhandle=None, sashpad=2, handlesize=2)
       
        self.main_window.pack(fill=BOTH, expand=YES)
        
        # left pane
        self.left_pane = Frame(self.main_window, width=200, height=600)
        self.left_pane.config(bg='#458b74')
        # right pane
        self.right_pane = Frame(self.main_window)
        self.right_pane.config(bg='#cdb38b')
        
        self.main_window.paneconfig(self.left_pane, minsize=140)
        
        # add left and right panes to the paned window
        self.main_window.add(self.left_pane)
        self.main_window.add(self.right_pane)
        
        
    def add_menubar(self):
        
        self.menubar = Menu(self.root)
        
        self.root.config(menu=self.menubar)
        file_menu = Menu(self.menubar, tearoff=0)
        
        file_menu.add_command(label='Say Hello', command=eh.process_events)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', command=quit)        
        self.menubar.add_cascade(label='File', menu=file_menu)
        
        utils_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Utils', menu=utils_menu)
        utils_menu.add_command(label='3DES', underline=0, accelerator='ALT + 3', command=self.do_3des)    

    def do_3des(self):
        TripleDesDialog(self.right_pane)
        

if __name__ == "__main__":
    
    rf = RootFrame('Test Tkinter').show()


