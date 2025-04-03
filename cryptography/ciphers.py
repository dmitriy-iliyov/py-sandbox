import math
import string
from abc import ABC, abstractmethod
from collections import defaultdict, Counter
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
        self.__small_punctuation_string = " ,.?!:;—-()'\""
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
        self.__alphabet = alphabet + " ,.?!:;—-()'\""

        self.__a = a
        self.__b = b
        self.__m = len(self.__alphabet)

        self.__inverse_a = self.__mod_inverse(self.__a, self.__m)

        self.__cipher_map = {self.__alphabet[i]: i for i in range(len(self.__alphabet))}
        self.__reverse_cipher_map = {i: self.__alphabet[i] for i in range(len(self.__alphabet))}

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


class RC4(Cipher, ABC):
    def __init__(self, n, key, converted_type='byte', return_type='byte'):
        self.__S_size = 2 ** n
        self.__S = np.zeros((self.__S_size,), dtype=np.uint8)
        self.__key_block = np.zeros((self.__S_size,), dtype=np.uint8)
        key = str(key).encode('utf-8')
        for i in range(self.__S_size):
            self.__S[i] = i
            self.__key_block[i] = key[i % len(key)]
        j = 0
        for i in range(self.__S_size):
            j = (j + self.__S[i] + self.__key_block[i]) % self.__S_size
            self.__S[i], self.__S[j] = self.__S[j], self.__S[i]
        self.__c_type = converted_type
        self.__r_type = return_type

    def encode(self, message):
        message_bytes = message
        if self.__c_type == 'byte':
            message_bytes = message.encode('utf-8')
        key_stream = self.__generate_key_stream(len(message_bytes))
        encoded_message_bytes = np.bitwise_xor(np.frombuffer(message_bytes, dtype=np.uint8), key_stream)
        return encoded_message_bytes.tobytes()

    def decode(self, encoded_message):
        encoded_message_bytes = np.frombuffer(encoded_message, dtype=np.uint8)
        key_stream = self.__generate_key_stream(len(encoded_message_bytes))
        decoded_message_bytes = np.bitwise_xor(encoded_message_bytes, key_stream)
        if self.__r_type == 'str':
            return decoded_message_bytes.tobytes().decode('utf-8')
        return decoded_message_bytes.tobytes()

    def __generate_key_stream(self, length):
        S = np.copy(self.__S)
        i = 0
        j = 0
        key_stream = np.zeros(length, dtype=np.uint8)

        for k in range(length):
            i = (i + 1) % self.__S_size
            j = (j + S[i]) % self.__S_size
            S[i], S[j] = S[j], S[i]
            t = (int(S[i]) + int(S[j])) % self.__S_size
            key_stream[k] = S[t]

        return key_stream


class DoubleRC4(Cipher, ABC):

    def __init__(self, n1, key1, n2, key2, return_type='byte'):
        self.__first_cipher = RC4(n1, key1, return_type=return_type)
        self.__second_cipher = RC4(n2, key2, converted_type='none')

    def encode(self, message):
        first_iteration = self.__first_cipher.encode(message)
        return self.__second_cipher.encode(first_iteration)

    def decode(self, encoded_message):
        first_iteration = self.__second_cipher.decode(encoded_message)
        return self.__first_cipher.decode(first_iteration)


class VigenereCipher(Cipher, ABC):

    def __init__(self, alphabet, key):
        self.__alphabet_len = len(alphabet)
        self.__alphabet = alphabet
        self.__tabular_recta = np.empty((self.__alphabet_len, self.__alphabet_len), dtype=np.str_)
        for i in range(self.__alphabet_len):
            for j in range(self.__alphabet_len):
                self.__tabular_recta[i, j] = alphabet[(j + i) % self.__alphabet_len]
        self.__key = key

    def encode(self, message):
        encoded_message = []
        key_repeated = (self.__key * (len(message) // len(self.__key))) + self.__key[:len(message) % len(self.__key)]

        for i in range(len(message)):
            message_idx = self.__alphabet.index(message[i])
            key_idx = self.__alphabet.index(key_repeated[i])
            encoded_message.append(str(self.__tabular_recta[key_idx, message_idx]))
        return ''.join(encoded_message)

    def decode(self, encoded_message):
        decoded_message = []
        key_repeated = ((self.__key * (len(encoded_message) // len(self.__key)))
                        + self.__key[:len(encoded_message) % len(self.__key)])

        for i in range(len(encoded_message)):
            encoded_idx = self.__alphabet.index(encoded_message[i])
            key_idx = self.__alphabet.index(key_repeated[i])
            decoded_idx = (encoded_idx - key_idx) % self.__alphabet_len
            decoded_message.append(self.__alphabet[decoded_idx])

        return ''.join(decoded_message)


def kasiski_analysis(ciphertext):
    substrings = defaultdict(list)
    for i in range(len(ciphertext) - 3):
        substring = ciphertext[i:i + 4]
        substrings[substring].append(i)

    distances = []
    for substring, positions in substrings.items():
        if len(positions) > 1:
            for i in range(1, len(positions)):
                distances.append(positions[i] - positions[i - 1])

    return distances


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def get_possible_key_lengths(distances):
    gcds = []
    for i in range(len(distances) - 1):
        gcds.append(gcd(distances[i], distances[i + 1]))
    return gcds


def frequency_analysis(text):
    return dict(Counter(text))


def get_shift_from_frequencies(text, expected_frequency):
    frequencies = frequency_analysis(text)
    most_common_char = max(frequencies, key=frequencies.get)
    shift = (ord(most_common_char) - ord(expected_frequency)) % 26
    return shift


def break_vigenere_cipher(ciphertext, key_length):
    groups = ['' for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        groups[i % key_length] += char

    key = ''
    for group in groups:
        shift = get_shift_from_frequencies(group, 'e')
        key += chr(shift + ord('A'))

    return key