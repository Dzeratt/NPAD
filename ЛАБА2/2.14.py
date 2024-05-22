inputstring = input("Введите произвольную строку: ")

word = ""
words = []

for char in inputstring:
    if char == " ":
        if word:
            words.append(word)
            word = ""
    else:
        word += char

if word:
    words.append(word)

print(words)

for word in words:
    if (word[0] == "а" or word[0] == "А") and (word[-1] == "х" or word[-1] == "Х"):
        print(word)
