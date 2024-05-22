sequence = list(map(int, input("Введите последовательность целых чисел через пробел: ").split()))

total_sum = 0
index = 0

while index < len(sequence):
    total_sum += sequence[index]
    index += 1

print("Сумма всех чисел в последовательности:", total_sum)
print("Количество чисел в последовательности:", index)