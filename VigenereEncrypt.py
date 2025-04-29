import random
from CaesarEncrypt import encryptCaesar, decryptCaesar


def detectAlphabet(text):
    ru_chars = set('абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    en_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    ru_count = sum(1 for c in text if c in ru_chars)
    en_count = sum(1 for c in text if c in en_chars)

    if ru_count > en_count:
        return 'ru'
    else: return 'eng'  # по умолчанию английский


def printSquare(lang):
    if lang == 'ru':
        alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    elif lang == 'eng':
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    langSize = len(alphabet)

    for shift in range(langSize):
        for chr in alphabet:
            print(encryptCaesar(chr, shift), end=' ')
        print()


def getShiftK(keyChar, alphabet, alphabet_mode=1):
    """Возвращает сдвиг для символа ключа с выбранным режимом алфавита"""
    if alphabet_mode == 2:
        return random.randint(0, len(alphabet) - 1) # Cлучайный сдвиг для каждого символа ключа
    else:
        return alphabet.index(keyChar)


def encryptVigenere(text, key, lang, alphabet_mode=1):
    encrypted = []
    key_index = 0

    if lang == 'ru':
        alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    else:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    key = key.upper()

    for char in text:
        if char.upper() in alphabet:
            shift = getShiftK(key[key_index % len(key)], alphabet, alphabet_mode) #key_id % len(key) - зацикливание по позиции ключа
            encrypted_chr = encryptCaesar(char, shift)
            encrypted.append(encrypted_chr)
            key_index += 1
        else:
            encrypted.append(char)

    return ''.join(encrypted)


def decryptVigenere(text, key, lang):
    decrypted = []
    key_id = 0

    if lang == 'ru':
        alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    else:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    key = key.upper()

    for char in text:
        if char.upper() in alphabet:
            shift = getShiftK(key[key_id % len(key)], alphabet, 1)
            decrypted_char = decryptCaesar(char, shift)
            decrypted.append(decrypted_char)
            key_id += 1
        else:
            decrypted.append(char)

    return ''.join(decrypted)


if __name__ == "__main__":
    while True:
        print("1 - Шифрование Виженера")
        print("2 - Дешифрование Виженера")
        print("3 - Показать квадрат Виженера")

        # mode = int(input("Выберите режим: "))
        mode = 1
        if mode not in (1, 2, 3):
            break
        elif mode == 3:
            inputFile = "text.txt"
            with open(inputFile, 'r') as f:
                text = f.read()
            lang = detectAlphabet(text)
            print("Квадрат Виженера:")
            printSquare(lang)
            continue

        inputFile = "text.txt" if mode == 1 else "encV_text.txt"

        try:
            with open(inputFile, 'r') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"Ошибка: файл {inputFile} не найден!")
            continue

        lang = detectAlphabet(text)
        print(f"Язык: {lang}")

        if mode==1:
            print("Выберите режим алфавита:")
            print("1 - По порядку")
            print("2 - Случайным образом ")
            # alphabetMod = int(input())
            alphabetMod = 1
        if alphabetMod not in (1, 2):
            break

        key = input(f"Введите ключ (только буквы {lang} языка): ").strip()
        while not key.isalpha():
            print("Ключ должен содержать только буквы!")
            key = input("Введите ключ (только буквы): ").strip()

        if mode == 1:
            encrypted = encryptVigenere(text, key, lang, alphabetMod)
            outputFile = f"encC_{inputFile}"
            with open(outputFile, 'w') as file:
                file.write(encrypted)
            print(f"Текст зашифрован и сохранен в {outputFile}")
        else:
            decrypted = decryptVigenere(text, key, lang)
            outputFile = f"decC_{inputFile}"
            with open(outputFile, 'w') as file:
                file.write(decrypted)
            print(f"Текст расшифрован и сохранен в {outputFile}")

        print()
        print("Первые строки файлов:")
        filesToCheck = ["text.txt", "encC_text.txt", "decC_encC_text.txt"]
        for filename in filesToCheck:
            try:
                with open(filename, 'r') as file:
                    firstLine = file.readline().strip()
                    print(f"{filename}: {firstLine}")
            except FileNotFoundError:
                print(f"{filename}:\tфайл не найден")
        print()