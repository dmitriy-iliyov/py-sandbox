from tkinter import *
from tkinter import ttk
import re
from functools import partial
from PIL import ImageTk, Image
import logic_func as lf


def read_file(name):
    file = open(name, 'r')
    digits = re.findall(r"[-+]?\d+", file.read())
    file.close()
    return digits


def check_valid(newval):
    return re.match("^[-+]?\d{0,10}$", newval) is not None


# windows funcs
# (gv = given value; dv = default values)
def create_dv_window(name, size, func, file_name):
    dv_window = Tk()
    dv_window.title(name)
    dv_window.geometry(size)
    first_val = read_file(file_name)[0]
    second_val = read_file(file_name)[1]
    label_a = ttk.Label(dv_window, text="a = " + first_val).pack(anchor=NW, padx=6, pady=6)
    label_b = ttk.Label(dv_window, text="b = " + second_val).pack(anchor=NW, padx=6, pady=6)
    ans = func(int(first_val), int(second_val))
    if ans[1] == True:
        label_ans = ttk.Label(dv_window, text="Відповідь: " + str(ans[0])).pack(anchor=NW, padx=6, pady=0)
    else:
        label_ans = ttk.Label(dv_window, text=str(ans[0])).pack(anchor=NW, padx=6, pady=0)
    dv_window.mainloop()


def create_gv_window(name, size, func):
    def get_value():
        ans = func(num1.get(), num2.get())
        if ans[1] == True:
            label_ans = ttk.Label(gv_window, text="Відповідь: " + str(ans[0])).pack(anchor=NW, padx=6, pady=0)
        else:
            label_ans = ttk.Label(gv_window, text=str(ans[0])).pack(anchor=NW, padx=6, pady=0)

    gv_window = Tk()
    gv_window.title(name)
    gv_window.geometry(size)
    label_a = ttk.Label(gv_window, text="a = ").pack(anchor=NW, padx=6, pady=6)
    num1 = IntVar(gv_window)
    num2 = IntVar(gv_window)
    check = (gv_window.register(check_valid), "%P")
    entry_a = Entry(gv_window, textvariable=num1, validate="key", validatecommand=check).pack(anchor=NW, padx=6, pady=6)
    label_b = ttk.Label(gv_window, text="b = ").pack(anchor=NW, padx=6, pady=6)
    entry_b = Entry(gv_window, textvariable=num2, validate="key", validatecommand=check).pack(anchor=NW, padx=6, pady=6)
    save_a_b = ttk.Button(gv_window, text="ANSWER", command=get_value).pack(anchor=NW, padx=5, pady=5)
    gv_window.mainloop()


# main window
window_names = ["Linear Algorithm (default values)", "Linear Algorithm (given values)",
                "Ramified Algorithm (default values)", "Ramified Algorithm (given values)",
                "Cyclic Algorithm (default values)", "Cyclic Algorithm (given values)"]
window_size = "430x210"
file_names = ["data/linear_a.txt", "data/ramified_a.txt", "data/cyclic_a.txt"]

menu = Tk()
menu.title("MENU")
menu.geometry("430x400")

label1 = ttk.Label(menu, text="Linear Algorithm").grid(row=0, column=0, columnspan=2, padx=5, pady=10)
btn_dv1 = ttk.Button(menu, text="Сalculate algorithm by default values",
                     command=partial(create_dv_window, window_names[0], window_size, lf.linear_algorithm, file_names[0]))
btn_dv1.grid(row=1, column=0, padx=5, pady=5)
btn_gv1 = ttk.Button(menu, text="Сalculate algorithm from given values",
                     command=partial(create_gv_window, window_names[1], window_size, lf.linear_algorithm))
btn_gv1.grid(row=2, column=0, padx=5, pady=5)
img_1 = ImageTk.PhotoImage(Image.open("data/n1.png").resize((147, 105)))
label_i1 = Label(image=img_1).grid(row=1, column=1, rowspan=2, padx=5, pady=5)

label2 = ttk.Label(menu, text="Ramified Algorithm").grid(row=3, column=0, columnspan=2, padx=5, pady=10)
btn_dv2 = ttk.Button(menu, text="Сalculate algorithm by default values",
                     command=partial(create_dv_window, window_names[2], window_size, lf.ramified_algorithm, file_names[1]))
btn_dv2.grid(row=4, column=0, padx=5, pady=5)
btn_gv2 = ttk.Button(menu, text="Сalculate algorithm from given values",
                     command=partial(create_gv_window, window_names[3], window_size, lf.ramified_algorithm))
btn_gv2.grid(row=5, column=0, padx=5, pady=5)
img_2 = ImageTk.PhotoImage(Image.open("data/n2.png").resize((150, 23)))
label_i2 = Label(image=img_2).grid(row=4, column=1, rowspan=2, padx=5, pady=5)

label3 = ttk.Label(menu, text="Cyclic Algorithm").grid(row=6, column=0, columnspan=2, padx=5, pady=10)
btn_dv3 = ttk.Button(menu, text="Сalculate algorithm by default values",
                     command=partial(create_dv_window, window_names[4], window_size, lf.cyclic_algorithm, file_names[2]))
btn_dv3.grid(row=7, column=0, padx=5, pady=5)
btn_gv3 = ttk.Button(menu, text="Сalculate algorithm from given values",
                     command=partial(create_gv_window, window_names[5], window_size, lf.cyclic_algorithm))
btn_gv3.grid(row=8, column=0, padx=5, pady=5)
img_3 = ImageTk.PhotoImage(Image.open("data/n3.png").resize((123, 48)))
label_i3 = Label(image=img_3).grid(row=7, column=1, rowspan=2, padx=5, pady=5)

menu.mainloop()
