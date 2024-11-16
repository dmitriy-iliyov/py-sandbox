import math


def linear_algorithm(a, b):
    y = math.sqrt(math.sin(a / 6) + math.cos(b / 6)) + math.sqrt(2 * math.sin(a / 6) * math.cos(b / 6))
    return y, True


def ramified_algorithm(k, x):
    try:
        y = k * x ** 2 * math.log(k * x) + math.sqrt(x)
        return y, True
    except ValueError:
        error = "Підлогарифмічний вираз k * x набуває недопустимого значення."
        return error, False


def cyclic_algorithm(n, b):
    if n > 0:
        summ = 0
        mult = 1
        for a in range(1, n + 1):
            if a == 4:
                break
            for k in range(1, a + 1):
                summ += a ** k + b / k
            mult *= summ
            summ = 0
        return mult, True
    else:
        error = "Значення n недопустиме."
        return error, False