a=int(input("Введите первое число: "))
b=int(input("Введите второе число: "))
c=int(input("Введите третье число: "))
mass = [a,b,c]

print(f"Минимальное из введенных: {min(mass)}")

for i in mass:
    if i >= 1 and i <=50:
        print(f"Числo в диапозоне [1,50]: {i}")
