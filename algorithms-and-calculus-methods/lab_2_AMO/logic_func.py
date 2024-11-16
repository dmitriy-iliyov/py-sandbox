from datetime import datetime
import random
import re


def make_random_array(size):
    try:
        _size = int(size)
        _array = [random.randint(-1000, 1000) for i in range(_size)]
        return _array
    except:
        _array = [random.randint(-1000, 1000) for i in range(random.randint(10, 100))]
        return _array


def generate_arrays(func, count_array, arreys_length, file_name):
    _arrays_stats = func(count_array, arreys_length)
    _count = _arrays_stats[0]
    _length = _arrays_stats[1]
    if _count == 0:
        _count = random.randint(1, 10)
    if len(_length) < _count:
        difference = _count - len(_length)
        for i in range(difference):
            _arrays_stats[1].append(str(random.randint(10, 10000)))
        for i in range(_count):
            write_file(file_name, make_random_array(_length[i]))
    else:
        for i in range(_count):
            write_file(file_name, make_random_array(_length[i]))


def selection_sort_min(array):
    start_time = datetime.now()
    size = len(array)
    for i in range(size):
        _min = array[i]
        min_index = i
        for j in range(i, size):
            if array[j] < _min:
                _min = array[j]
                min_index = j
        array[min_index] = array[i]
        array[i] = _min
    current_time = datetime.now() - start_time
    return array, pick_out_int(current_time)


def pick_out_int(value):
    digits = re.findall(r'\d+', str(value))
    digits = [int(i) for i in digits]
    return digits[len(digits)-1]


def write_file(name, data):
    file = open(name, 'a')
    str1 = str(data).replace('[', '')
    written_str = str1.replace(']', '')
    file.write(written_str+"\n")
    file.close()


def write_file_2_file(written_file_name, readed_file_name):
    sort_stats = []
    for i in read_file(readed_file_name):
        sort_stats.append(selection_sort_min(i))
    for i in sort_stats:
        write_file(written_file_name, i[0])
        write_file(written_file_name, len(i[0]))
        write_file(written_file_name, i[1])


def read_file(name):
    file = open(name, 'r')
    lines = [line.strip() for line in file]
    array_arrays = []
    for i in range(0, len(lines)):
        array_arrays.append([int(item) for item in lines[i].split(", ")])
    file.close()
    return array_arrays


def clear_file(name):
    file = open(name, 'w')
    file.close()
