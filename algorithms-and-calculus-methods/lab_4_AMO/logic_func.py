from scipy.misc import derivative
import draw_func as df


def __floater(x):
    return float('{:.3f}'.format(x))


def __function(x):
    return x ** 3 + 10 * x - 9
    # return x ** 3 + 3 * x ** 2 + 12 * x + 8
    # return math.cos(x)
    # return x ** 2 - math.cos(math.pi * x)
    # return x ** 2 - math.sin(math.pi * x)


def __derivative_function(x, numder=None):
    return __floater(derivative(__function, x, dx=1e-6, n=numder))


def __part_of_tangent_method(x0):
    x = [x0]
    i = 0
    while True:
        x.append(x[i] - __function(x[i]) / __derivative_function(x[i], 1))
        i += 1
        if abs(x[i] - x[i-1]) < 0.0001:
            return __floater(x[i])


def tangent_method(interval):
    a = int(df.get_value(interval)[0])
    b = int(df.get_value(interval)[1])
    f1 = __derivative_function(1, 1)
    f2 = __derivative_function(1, 1)
    if f1 > 0 and f2 > 0 or f1 < 0 and f2 < 0:
        x0 = __part_of_tangent_method(b)
        if a < x0 < b:
            return x0
        else:
            return "Функція не перетинає вісь х"
    elif f1 > 0 and f2 < 0 or f1 < 0 and f2 > 0:
        x0 = __part_of_tangent_method(b)
        if a < x0 < b:
            return x0
        else:
            return "Функція не перетинає вісь х"

