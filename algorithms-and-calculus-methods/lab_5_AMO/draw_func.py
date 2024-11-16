from tkinter import *
from tkinter import ttk
from functools import partial
import re
import logic_func as lf
import row_spawner as rs


class DrawFuncs:

    def __init__(self):
        self.solver = lf.SLARsolver()
        self.spawner = rs.SlarSpawner()

    def __check_valid_string_of_int(self, value):
        return re.match("^[-+?\d{0,5}\s]+$", value) is not None

    def __check_valid_int(self, value):
        return re.match("^\d{0,1}$", value) is not None

    def __check_valid_int_x(self, value):
        return re.match("^[-+]?\d{0,1}$", value) is not None

    def get_value(self, val):
        int_val = val.get()
        return int_val

    def label_destroer(self, label):
        label.after(1000, label.destroy())

    # def __make_aswer_lables(self, menu):
    #     if self.solver.answers:
    #         lable_x1 = ttk.Label(menu, width=25, text="x1  =   -0.7114890249893494").grid(row=8, column=0, sticky=W, pady=5)
    #         lable_x2 = ttk.Label(menu, width=25, text="x2  =   1.8752496496566575").grid(row=9, column=0, sticky=W, pady=5)
    #         lable_x3 = ttk.Label(menu, width=25, text="x3  =   -0.9219566600239237").grid(row=10, column=0, sticky=W, pady=5)
    #         lable_x4 = ttk.Label(menu, width=25, text="x4  =   -1.9483497953463782").grid(row=11, column=0, sticky=W, pady=5)
    #     else:
    #         lable_x5 = ttk.Label(menu, width=25, text="СЛАР немає коренів").grid(row=12, column=0, sticky=W, pady=5)

    def __make_aswer_lables(self, menu):
        if self.solver.answers:
            lable_x1 = ttk.Label(menu, width=25, text="x1  =   " + str(self.solver.answers[0])).grid(row=8, column=0, sticky=W, pady=5)
            lable_x2 = ttk.Label(menu, width=25, text="x2  =   " + str(self.solver.answers[1])).grid(row=9, column=0, sticky=W, pady=5)
            lable_x3 = ttk.Label(menu, width=25, text="x3  =   " + str(self.solver.answers[2])).grid(row=10, column=0, sticky=W, pady=5)
            lable_x4 = ttk.Label(menu, width=25, text="x4  =   " + str(self.solver.answers[3])).grid(row=11, column=0, sticky=W, pady=5)
        else:
            lable_x5 = ttk.Label(menu, width=25, text="СЛАР немає коренів").grid(row=12, column=0, sticky=W, pady=5)

    def __getting_values(self):
        self.spawner.write_com_values()
        self.spawner.write_free_values()

    def __window_generator(self, e_count, x_count):
        equation = self.get_value(e_count)
        x = self.get_value(x_count)
        setting_window = Tk()
        setting_window.title("MENU")
        setting_window.geometry("290x180")
        setting_window.configure(bg='#ECECEC')
        if equation != x:
            lable = ttk.Label(setting_window, width=30, text="Система не може бути розвязана!").grid(row=1, column=0, sticky=W, pady=5)
        else:
            self.spawner.spawn(setting_window, equation)
        get_btn = ttk.Button(setting_window, width=5, text="Set val", command=partial(self.__getting_values))
        get_btn.grid(row=equation, column=0, columnspan=2, sticky=W, padx=1, pady=1)
        setting_window.mainloop()

    def draw_menu(self):
        menu = Tk()
        menu.title("MENU")
        menu.geometry("464x270")
        menu.configure(bg='#ECECEC')
        label1 = ttk.Label(menu, width=24, text="Введіть кількість рівняннь:").grid(row=0, column=0, sticky=W, pady=5)
        label2 = ttk.Label(menu, width=24, text="Введіть кількість невідомих: ").grid(row=1, column=0, sticky=W, pady=5)
        x_count = IntVar(menu)
        equation_count = IntVar(menu)
        check2 = (menu.register(self.__check_valid_int), "%P")
        entry_equation_count = ttk.Entry(menu, width=4, textvariable=equation_count, validate="all", validatecommand=check2).grid(row=0,
                                                                                                 column=1, columnspan=2, sticky=W, pady=5)
        entry_x_count = ttk.Entry(menu, width=4, textvariable=x_count, validate="all", validatecommand=check2).grid(
            row=1, column=1, columnspan=2, sticky=W, pady=5)
        wn_btn = ttk.Button(menu, width=16, text="Set values", command=partial(self.__window_generator, equation_count, x_count))
        wn_btn.grid(row=2, column=0, sticky=W, padx=1, pady=1)
        solve_btn = ttk.Button(menu, width=16, text="Solve with user data", command=partial(self.solver.gauss_method, 1))
        solve_btn.grid(row=3, column=0, sticky=W, padx=1, pady=1)
        bt_from_file = ttk.Button(menu, width=16, text="Solve with file data", command=partial(self.solver.gauss_method, 0))
        bt_from_file.grid(row=3, column=1, sticky=W, padx=1, pady=1)
        btn_get_answer = ttk.Button(menu, width=9, text="Get answers", command=partial(self.__make_aswer_lables, menu))
        btn_get_answer.grid(row=3, column=2, sticky=W, padx=1, pady=1)
        btn_clear = ttk.Button(menu, width=9, text="Clear", command=partial(self.solver.clear_user_files))
        btn_clear.grid(row=4, column=0, sticky=W, padx=1, pady=1)
        menu.mainloop()
