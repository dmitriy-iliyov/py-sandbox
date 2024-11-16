import math


def function(x):
    # return 1/(1+math.e**(-x))
    return math.sin(x)


class Interpolation:

    def __init__(self, number_line):
        self.__a = number_line[0]
        self.__b = number_line[1]
        self.n = 33
        self.__default_x = []
        self.__default_y = []
        self.__interpolate_x = []
        self.__auxiliary_y = []
        self.__interpolate_y = []

    def default_func(self):
        h = (self.__b - self.__a)/(self.n * 10)
        for i in range(self.n * 10):
            self.__default_x.append(self.__a + h * i)
            self.__default_y.append(function(self.__a + h * i))
        return self.__default_x, self.__default_y

    def lagrange_polynomial(self, x):
        p = self.__auxiliary_y.copy()
        for i in range(self.n - 1):
            for j in range(i + 1, self.n):
                p[j] = ((x - self.__interpolate_x[i]) * p[j] - (x - self.__interpolate_x[j]) * p[i]) / (self.__interpolate_x[j] - self.__interpolate_x[i])
        return p[self.n - 1]

    def interpolated_func(self):
        h = (self.__b - self.__a)/(self.n - 1)
        for i in range(self.n):
            self.__interpolate_x.append(self.__a + h * i)
            self.__auxiliary_y.append(function(self.__a + h * i))
        for i in range(self.n):
            self.__interpolate_y.append(self.lagrange_polynomial(self.__interpolate_x[i]))
        return self.__interpolate_x, self.__interpolate_y

    def interpolation_error(self):
        d = []
        for i in range(self.n*10):
            d.append(abs(self.__default_y[i] - self.lagrange_polynomial(self.__default_x[i])))
        return self.__default_x, d
