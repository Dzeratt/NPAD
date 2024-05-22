a=int(input("Введите первое число: "))
b=int(input("Введите второе число: "))
c=int(input("Введите третье число: "))
mass = [a,b,c]
print(f"Минимальное из введенных: {min(mass)}")

for i in mass:
    if i >= 1 and i <=50:
        print(i)


m = float(input("Введите вещественное число m: "))

for num in (1,11,1):
    print(m*num)