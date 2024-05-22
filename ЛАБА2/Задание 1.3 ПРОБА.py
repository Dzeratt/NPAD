string = input("Введите последовательность целых чисел через пробел: ")
words = []
word = ""

for char in string:
    if char == " ":
        words.append(int(word))
        word = ""
    else:
        word += char

if word:
    words.append(int(word))

total_sum = 0
index = 0

while index < len(words):
    total_sum += words[index]
    index += 1

print("Сумма всех чисел в последовательности:", total_sum)
print("Количество чисел в последовательности:", index)
