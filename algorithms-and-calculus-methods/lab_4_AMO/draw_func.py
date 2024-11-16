import logic_func as lf
from tkinter import *
from tkinter import ttk
from functools import partial
import matplotlib.pyplot as plt
import re


def draw_graph(data_1, data_2, graph_name, color, borders=None):
    arr_x = []
    arr_y = []
    plt.title(graph_name)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis(borders)
    for i in range(borders[0], borders[1] + 1):
        arr_x.append(i)
        arr_y.append(0)
    plt.plot(arr_x, arr_y, color="black", linewidth=1)
    arr_x.clear()
    arr_y.clear()
    for i in range(borders[2], borders[3] + 1):
        arr_x.append(0)
        arr_y.append(i)
    plt.plot(arr_x, arr_y, color="black", linewidth=1)
    plt.plot(data_1, data_2, color=color, linewidth=1)
    plt.grid(True)


def my_graph(interval):
    x = []
    y = []
    a = int(get_value(interval)[0])
    b = int(get_value(interval)[1])
    i = a
    while i <= b:
        x.append(i)
        y.append(lf.__function(i))
        i += 0.001
    borders = [-10, 10, -10, 10]
    plt.figure(figsize=(5, 7))
    plt.subplot(211)
    draw_graph(x, y, "Графік функції", "red", borders)
    plt.subplot(212)
    borders = [a, b, lf.__function(a), lf.__function(b)]
    draw_graph(x, y, "Приближено", "red", borders)
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, hspace=0.3, wspace=0.)
    plt.show()


def check_valid(value):
    return re.match("^[-+?\d{0,5}\s]+$", value) is not None


def get_value(interval):
    _interval = str(interval.get()).split(' ')
    return _interval


def make_lable(menu, interval):
    label2 = ttk.Label(menu, width=30, text="x:      " + str(lf.tangent_method(interval))).grid(row=1, column=0, sticky=W, pady=5)


def draw_menu():
    menu = Tk()
    menu.title("MENU")
    menu.geometry("440x70")
    menu.configure(bg='#ECECEC')
    label1 = ttk.Label(menu, width=15, text="Введіть проміжок:").grid(row=0, column=0, sticky=W, pady=5)
    _interval = StringVar(menu)
    check1 = (menu.register(check_valid), "%P")
    entry1 = ttk.Entry(menu, width=11, textvariable=_interval, validate="all", validatecommand=check1).grid(row=0,
                                                                                             column=1, sticky=W, pady=5)
    btn2 = ttk.Button(menu, width=8, text="Find value", command=partial(make_lable, menu, _interval))
    btn2.grid(row=0, column=2, sticky=W, padx=1, pady=1)
    btn1 = ttk.Button(menu, width=8, text="Draw graph", command=partial(my_graph, _interval))
    btn1.grid(row=1, column=2, sticky=W, padx=1, pady=1)
    menu.mainloop()
