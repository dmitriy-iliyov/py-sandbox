import math
import string
from abc import ABC, abstractmethod

import numpy as np


class Cipher(ABC):

    @abstractmethod
    def encode(self, message):
        pass

    @abstractmethod
    def decode(self, encoded_message):
        pass


class WheatstoneCipher(Cipher, ABC):

    def __init__(self, alphabet, filler_letter_id, punctuation=False, full_punctuation=False):
        self.__alphabet = alphabet
        if len(alphabet) - 1 < filler_letter_id:
            raise IndexError
        self.__filler_letter = alphabet[filler_letter_id]
        self.__small_punctuation_string = " ,.?!:;—()[]{}«»"
        self.__m1 = self.__generate_matrix(self.__alphabet, punctuation=punctuation, full_punctuation=full_punctuation)
        self.__m2 = self.__generate_matrix(self.__alphabet, punctuation=punctuation, full_punctuation=full_punctuation)

    def encode(self, message):
        encoded_message = ""

        if len(message) % 2 != 0:
            message += self.__filler_letter

        for char_id in range(0, len(message), 2):
            bigram = message[char_id: char_id + 2]
            encoded_message += self.__parse_bigram(bigram)
        return encoded_message

    def decode(self, encoded_message):
        message = ""
        for char_id in range(0, len(encoded_message), 2):
            bigram = encoded_message[char_id: char_id + 2]
            message += self.__parse_bigram(bigram)
        return message

    def __parse_bigram(self, bigram):
        indexes = np.where(self.__m1 == bigram[0])
        b_1_r = indexes[0][0]
        b_0_c = indexes[1][0]
        indexes = np.where(self.__m2 == bigram[1])
        b_0_r = indexes[0][0]
        b_1_c = indexes[1][0]
        return self.__m1[b_0_r, b_0_c] + self.__m2[b_1_r, b_1_c]

    def __generate_matrix(self, alphabet, punctuation=False, full_punctuation=False):
        matrix = []

        if full_punctuation:
            alphabet = alphabet + string.punctuation + ' '
        elif punctuation:
            alphabet = alphabet + self.__small_punctuation_string
        else:
            alphabet += ' '
        matrix_size = self.__calculate_matrix_size(len(alphabet))

        char_id = 0
        for i in range(matrix_size):
            row = []
            for j in range(matrix_size):
                if char_id < len(alphabet):
                    row.append(alphabet[char_id])
                    char_id += 1
                else:
                    row.append(string.punctuation[matrix_size ** 2 - i * j])
            matrix.append(row)
        matrix = np.array(matrix, dtype='U1')
        return np.random.permutation(matrix.flatten()).reshape(matrix.shape)

    def __calculate_matrix_size(self, alphabet_size):
        length = math.sqrt(alphabet_size)
        rows = math.ceil(length)
        return rows


class AffineCipher(Cipher, ABC):

    def __init__(self, alphabet, a, b):
        self.__alphabet = alphabet

        self.__a = a
        self.__b = b
        self.__m = len(alphabet)

        self.__inverse_a = self.__mod_inverse(self.__a, self.__m)

        self.__cipher_map = {alphabet[i]: i for i in range(len(alphabet))}
        self.__reverse_cipher_map = {i: alphabet[i] for i in range(len(alphabet))}

    def encode(self, message):
        encoded_message = ""
        for char in message:
            char_id = self.__cipher_map[char]
            encoded_char_id = self.__encode_func(char_id)
            encoded_message += self.__reverse_cipher_map[encoded_char_id]
        return encoded_message

    def __encode_func(self, x):
        return divmod((self.__a * x + self.__b), self.__m)[1]

    def decode(self, encoded_message):
        message = ""
        for char in encoded_message:
            encoded_char_id = self.__cipher_map[char]
            char_id = self.__decode_func(encoded_char_id)
            message += self.__reverse_cipher_map[char_id]
        return message

    def __decode_func(self, x):
        return divmod((self.__inverse_a * (x - self.__b)), self.__m)[1]

    def __mod_inverse(self, a, m):
        g, x, y = self.__extended_gcd(a, m)
        if g != 1:
            return None
        else:
            return x % m

    def __extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        g, x1, y1 = self.__extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y


class DoubleAffineCipher(Cipher, ABC):

    def __init__(self, alphabet, a1, b1, a2, b2):
        self.__first_cipher = AffineCipher(alphabet, a1, b1)
        self.__second_cipher = AffineCipher(alphabet, a2, b2)

    def encode(self, message):
        first_iteration_result = self.__first_cipher.encode(message)
        return self.__second_cipher.encode(first_iteration_result)

    def decode(self, encoded_message):
        first_iteration_result = self.__second_cipher.decode(encoded_message)
        return self.__first_cipher.decode(first_iteration_result)