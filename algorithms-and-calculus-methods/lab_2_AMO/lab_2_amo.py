from tkinter import *
from tkinter import ttk
from functools import partial
import matplotlib.pyplot as plt
import re
import logic_func as lf


def check_valid_1(value):
    return re.match("^\d{0,4}$", value) is not None


def check_valid_2(value):
    return re.match("^[\d{0,5}\s]+$", value) is not None


def get_value(arr_c, arr_l):
    _arr_c = int(arr_c.get())
    _arr_l = str(arr_l.get()).split(' ')
    print(_arr_l)
    return _arr_c, _arr_l


def make_graph(file_name):
    _array = lf.read_file(file_name)
    _array_arrays = []
    _arrays_lenght = []
    _arrays_sort_time = []
    new_array = []
    for i in range(len(_array)):
        if i % 3 != 0:
            new_array.append(_array[i])
        else:
            _array_arrays.append(_array[i])
    for i in range(len(new_array)):
        if i % 2 == 0:
            _arrays_lenght.append(new_array[i][0])
        else:
            _arrays_sort_time.append(new_array[i][0]/(10**6))
    plt.title('Testing Sort by choice algorythm')
    plt.xlabel('Length of array')
    plt.ylabel('Sorting time, s')
    teor_times = [len(sample) ** 2 / 100000000 for sample in _array_arrays]
    plt.plot(lf.selection_sort_min(_arrays_lenght)[0], lf.selection_sort_min(teor_times)[0], color='red', linewidth=1)
    plt.plot(lf.selection_sort_min(_arrays_lenght)[0], lf.selection_sort_min(_arrays_sort_time)[0], color='orange', linewidth=1)
    plt.show()


#10 10 10 10 100 100 100 100 1000 1000 1000 1000 10000 10000 10000 10000
#10 20 500 100 200 300 2000 1000 3000 10000
#10 20 30 40 50 60 70 80 90 100
file_names = ["data/array.txt", "data/sorted_array.txt"]

menu = Tk()
menu.title("MENU")
menu.geometry("340x155")
menu.configure(bg='#ECECEC')
label1 = ttk.Label(menu, width=30, text="Введіть кількість массивів:").grid(row=0, column=0, columnspan=2, sticky=W, pady=5)
label2 = ttk.Label(menu, width=31, text="Введіть розміри массивів через пробіл:").grid(row=1, column=0, columnspan=2, sticky=W, pady=5)
_arrays_count = IntVar(menu)
_arrays_lens = StringVar(menu)
check1 = (menu.register(check_valid_1), "%P")
check2 = (menu.register(check_valid_2), "%P")
entry1 = ttk.Entry(menu, width=9, textvariable=_arrays_count, validate="all", validatecommand=check1).grid(row=0, column=2, sticky=W, pady=5)
entry2 = ttk.Entry(menu, width=41, textvariable=_arrays_lens, validate="all", validatecommand=check2).grid(row=2, column=0, columnspan=3, sticky=W, pady=5)
save_btn = ttk.Button(menu, width=6, text="Save",
                      command=partial(get_value, _arrays_count, _arrays_lens))
save_btn.grid(row=1, column=2, sticky=W, padx=1, pady=1)
set_arrays_btn = ttk.Button(menu, width=15, text="Generate arrays",
                            command=partial(lf.generate_arrays, get_value, _arrays_count, _arrays_lens, file_names[0]))
set_arrays_btn.grid(row=3, column=0, sticky=W, padx=1, pady=1)
set_rand_array_btn = ttk.Button(menu, width=18.5, text="Generate random arrays", command=partial(lf.generate_arrays, get_value, _arrays_count, _arrays_lens, file_names[0]))
set_rand_array_btn.grid(row=3, column=1, columnspan=2, sticky=W, padx=2, pady=1)
write_btn = ttk.Button(menu, width=15, text="Sort and write to file",
                       command=partial(lf.write_file_2_file, file_names[1], file_names[0]))
write_btn.grid(row=4, column=0, sticky=W, padx=1, pady=1)
graph_btn = ttk.Button(menu, width=18, text="Generate graph", command=partial(make_graph, file_names[1]))
graph_btn.grid(row=4, column=1, columnspan=2, sticky=W, padx=1, pady=1)
lf.clear_file(file_names[0])
lf.clear_file(file_names[1])
menu.mainloop()
