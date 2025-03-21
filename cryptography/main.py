from ciphers import WheatstoneCipher, AffineCipher, DoubleAffineCipher


ukrainian_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
english_alphabet = "abcdefghijklmnopqrstuvwxyz"


# wc = WheatstoneCipher(ukrainian_alphabet, 5)
# message = "тестове повідомлення"
# e_message = wc.encode(message)
# print(e_message)
# n_message = wc.decode(e_message)
# print(n_message)

# print(len(ukrainian_alphabet))
# ac = AffineCipher(ukrainian_alphabet, 5, 7)
# message = "тестове повідомлення"
# message = message.replace(' ', '')
# print(message)
# e_m = ac.encode(message)
# print(e_m)
# n_m = ac.decode(e_m)
# print(n_m)

dac = DoubleAffineCipher(ukrainian_alphabet, 5, 7, 4, 3)
message = "тестове повідомлення"
message = message.replace(' ', '')
print(message)
e_m = dac.encode(message)
print(e_m)
n_m = dac.decode(e_m)
print(n_m)
