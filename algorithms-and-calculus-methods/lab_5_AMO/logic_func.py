

class SLARsolver:

    def __init__(self):
        self.__coeficient_matrix = []
        self.__free_members = []
        self.__equation_count = 0
        self.__file_names = ["coef.txt", "free_memb.txt", "user_coef.txt", "user_free_memb.txt"]
        self.answers = []

    def __read_file(self, name):
        file = open(name, 'r')
        _matrix = []
        for line in file:
            _matrix.append(line.split(' '))
        file.close()
        new_matrix, new_line = [], []
        if len(_matrix) > 1:
            for line in _matrix:
                for i in line:
                    new_line.append(float(i))
                new_matrix.append(new_line)
                new_line = []
            return new_matrix
        else:
            for line in _matrix:
                for i in line:
                    new_matrix.append(float(i))
            return new_matrix

    def __get_file_data(self):
        self.__coeficient_matrix = self.__read_file(self.__file_names[0])
        self.__free_members = self.__read_file(self.__file_names[1])
        self.__equation_count = len(self.__coeficient_matrix)

    def __get_user_data(self):
        self.__coeficient_matrix = self.__read_file(self.__file_names[2])
        self.__free_members = self.__read_file(self.__file_names[3])
        self.__equation_count = len(self.__coeficient_matrix)

    def clear_user_files(self):
        file = open(self.__file_names[2], 'w')
        file.close()
        file = open(self.__file_names[3], 'w')
        file.close()

    def __swap_rows(self, A, B, row1, row2):
        A[row1], A[row2] = A[row2], A[row1]
        B[row1], B[row2] = B[row2], B[row1]

    def __divide_row(self, A, B, row, divider):
        A[row] = [a / divider for a in A[row]]
        B[row] /= divider

    def __combine_rows(self, A, B, row, source_row, weight):
        A[row] = [(a + k * weight) for a, k in zip(A[row], A[source_row])]
        B[row] += B[source_row] * weight

    def gauss_method(self, flag):
        if flag == 1:
            self.__get_user_data()
        else:
            self.__get_file_data()
        column = 0
        while (column < len(self.__free_members)):
            current_row = None
            for r in range(column, len(self.__coeficient_matrix)):
                if current_row is None or abs(self.__coeficient_matrix[r][column]) > abs(self.__coeficient_matrix[current_row][column]):
                    current_row = r
            if current_row is None:
                return None
            if current_row != column:
                self.__swap_rows(self.__coeficient_matrix, self.__free_members, current_row, column)
            self.__divide_row(self.__coeficient_matrix, self.__free_members, column, self.__coeficient_matrix[column][column])
            for r in range(column + 1, len(self.__coeficient_matrix)):
                self.__combine_rows(self.__coeficient_matrix, self.__free_members, r, column, - self.__coeficient_matrix[r][column])
            column += 1
        self.answers = [0 for b in self.__free_members]
        for i in range(len(self.__free_members) - 1, -1, -1):
            self.answers[i] = self.__free_members[i] - sum(x * a for x, a in zip(self.answers[(i + 1):], self.__coeficient_matrix[i][(i + 1):]))
        print(self.answers)
