'''
Created on 16-Dec-2014

@author: Raghavendra Balgi
'''

from Tkconstants import LEFT, RIGHT
from Tkinter import Label, Entry, Text
import tkSimpleDialog


class TripleDesDialog(tkSimpleDialog.Dialog):
    
    def body(self, master):
        Label(master, text='Key ',justify=LEFT).grid(row=0, column=0)
        Label(master, text='Data ',justify=LEFT).grid(row=1, column=0)
        self.key = Entry(master,justify=RIGHT).grid(row=0, column=1, columnspan=10)
        self.data = Text(master,font='Courier 9').grid(row=1, column=1,rowspan=2, columnspan=6)
        return (self.key)
