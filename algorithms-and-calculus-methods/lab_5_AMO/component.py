from tkinter import *
from tkinter import ttk


class Component:

    def __init__(self, window):
        self.value = StringVar(window)
        self.window = window
        self.check = (self.window.register(self.__check_valid_int_x), "%P")

    def cmponent(self, row, col, text):
        entry = ttk.Entry(self.window, width=2, textvariable=self.value, validate="all", validatecommand=self.check).grid(
            row=row, column=col, sticky=W, pady=5)
        lable = ttk.Label(self.window, width=4, text=text).grid(row=row, column=col + 1, sticky=W, pady=5)

    def get_value(self):
        return self.value

    def __check_valid_int_x(self, value):
        return re.match("^[-+]?\d{0,3}$", value) is not None