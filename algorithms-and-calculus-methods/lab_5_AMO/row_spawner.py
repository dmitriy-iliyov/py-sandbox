import component as components
import f_memb as fm


class SlarSpawner:
    def __init__(self):
        self.__row_number = 0
        self.__x_arr = []
        self.__components_arr = []
        self.__com_values = []
        self.__free_memb_arr = []
        self.__free_memb_values = []
        self.__file_names = ["user_coef.txt", "user_free_memb.txt"]

    def spawn(self, window, i):
        self.__row_number = i
        for i in range(1, i + 1):
            if i == self.__row_number:
                self.__x_arr.append("x" + str(i) + "  = ")
            else:
                self.__x_arr.append("x" + str(i) + "  + ")
        for i in range(self.__row_number):
            for j in range(self.__row_number):
                _c = components.Component(window)
                self.__components_arr.append(_c)
                _c.cmponent(i, j * 2, self.__x_arr[j])
                if j + 1 == self.__row_number:
                    _fm = fm.FreeMember(window)
                    self.__free_memb_arr.append(_fm)
                    _fm.free_member(i, j * 2 + 2)

    def __to_str(self, _list):
        str1 = str(_list).replace('[', '')
        written_str = str1.replace(']', '')
        written_str2 = written_str.replace(',', '')
        return written_str2

    def write_com_values(self):
        self.__com_values = [list() for i in range(self.__row_number)]
        try:
            file = open(self.__file_names[0], 'a')
            for i in range(self.__row_number):
                for j in range(self.__row_number):
                    index = i*self.__row_number+j
                    if j != self.__row_number-1:
                        file.write(str(self.__components_arr[index].value.get())+" ")
                    else:
                        file.write(str(self.__components_arr[index].value.get()))
                file.write("\n")
            file.close()
        except:
            print("Vallue Error: values dosen't exist")

    def write_free_values(self):
        try:
            for i in range(self.__row_number):
                self.__free_memb_values.append(int(self.__free_memb_arr[i].value.get()))
            file = open(self.__file_names[1], 'a')
            _str = self.__to_str(self.__free_memb_values)
            file.write(_str + "\n")
            file.close()
        except:
            print("Vallue Error: values dosen't exist")
