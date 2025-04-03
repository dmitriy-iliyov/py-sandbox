import time
import matplotlib
from matplotlib import pyplot as plt
import ciphers
from ciphers import WheatstoneCipher, AffineCipher, DoubleAffineCipher, RC4, DoubleRC4, VigenereCipher

matplotlib.use('TkAgg')


def plot(e_time, d_time):
    x_values = [i * 10 for i in range(1, len(e_time) + 1)]
    plt.figure(figsize=(10, 5))
    plt.plot(x_values, e_time, label="Encoding Time")
    plt.plot(x_values, d_time, label="Decoding Time")
    plt.xlabel("Message Length (characters)")
    plt.ylabel("Time (seconds)")
    plt.title("Encoding vs Decoding Time")
    plt.legend()
    plt.grid(True)
    plt.show()


ukrainian_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

with open('/Users/sayner/github_repos/py-sandbox/cryptography/input_data.txt') as f:
    test_data = []
    for l in f:
        l = l.lower()
        l = l.strip()
        for c in l:
            test_data.append(c)

rc4 = RC4(16, "eirj209rh3d1", return_type='str')
message = "тестове повідомлення"
m_bits = rc4.encode(message)
print(m_bits)
decode = rc4.decode(m_bits)
print(decode)

drc4 = DoubleRC4(16, 1234341598172, 8, "[eplefkwn2342korgjierjwepo4ve[ko1r", return_type='str')
message = "тестове повідомлення"
m_bits = drc4.encode(message)
print(m_bits)
decode = drc4.decode(m_bits)
print(decode)

encoding_time_list = []
decoding_time_list = []
drc4 = DoubleRC4(16, 123434159812, 8, "[eplefkwn2kfowejihfepwf", return_type='str')
message = ''
for i in range(0, len(test_data), 100):
    message += ''.join(test_data[i: i + 100])
    start_time = time.perf_counter()
    encoded_message = drc4.encode(message)
    end_time = time.perf_counter()
    encoding_time_list.append(end_time - start_time)

    start_time = time.perf_counter()
    decoded_message = drc4.decode(encoded_message)
    end_time = time.perf_counter()
    decoding_time_list.append(end_time - start_time)

plot(encoding_time_list, decoding_time_list)

for _, i in enumerate(encoding_time_list):
    if _ % 10 == 0:
        print(_, str(round(i, 6)) + ' secs')

for _, i in enumerate(decoding_time_list):
    if _ % 10 == 0:
        print(_, str(round(i, 6)) + ' secs')
