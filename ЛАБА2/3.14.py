import numpy as np

N = int(input("Введите размер одномерного массива: "))

array = np.random.randint(1, 100, N)
print(array)

min_index = array.argmin()
max_index = array.argmax()

array[min_index], array[max_index] = array[max_index], array[min_index]

average_number = array.mean()
print("Среднее арифметическое всех чисел в массиве:", average_number)

array[array > average_number] = 1

print("Полученный массив после замены:", array)
