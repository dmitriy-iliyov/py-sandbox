from tkinter import *
from tkinter import ttk
from component import Component


class FreeMember(Component):

    def free_member(self, row, col):
        entry = ttk.Entry(self.window, width=2, textvariable=self.value, validate="all",
                          validatecommand=self.check).grid(row=row, column=col, sticky=W, pady=5)
