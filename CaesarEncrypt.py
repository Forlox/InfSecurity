def encryptCaesar(text, k):
    result = []
    for c in text:
        if c.isalpha():
            # Для английских букв
            if c.islower() and ord(c) >= ord('a') and ord(c) <= ord('z'):
                base = ord('a')
                drift = (ord(c) - base + k) % 26
                result.append(chr(base + drift))
            elif c.isupper() and ord(c) >= ord('A') and ord(c) <= ord('Z'):
                base = ord('A')
                drift = (ord(c) - base + k) % 26
                result.append(chr(base + drift))
            # Для русских букв
            elif c.islower() and ord(c) >= ord('а') and ord(c) <= ord('я'):
                base = ord('а')
                drift = (ord(c) - base + k) % 32
                result.append(chr(base + drift))
            elif c.isupper() and ord(c) >= ord('А') and ord(c) <= ord('Я'):
                base = ord('А')
                drift = (ord(c) - base + k) % 32
                result.append(chr(base + drift))
        else:
            result.append(c)
    return ''.join(result)

def decryptCaesar(text, k):
    return encryptCaesar(text, -k)


if __name__ == "__main__":
    while True:
        print("\n1 - шифрование, 2 - дешифрование")
        mode = int(input("Выберите режим: "))

        if mode == 1:
            print("= Шифрование файла =")
            inputFile = "text.txt"
        elif mode == 2:
            print("= Расшифровка файла =")
            inputFile = "encC_text.txt"
        else:
            break

        k = int(input("Смещение K: "))

        try:
            with open(inputFile, 'r') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"Ошибка: файл {inputFile} не найден!")
            continue

        if mode == 1:
            encText = encryptCaesar(text, k)
            outputFile = f"encC_{inputFile}"
        elif mode == 2:
            encText = decryptCaesar(text, k)
            outputFile = f"decC_{inputFile}"

        with open(outputFile, 'w') as file:
            file.write(encText)
        print(f"Текст сохранен в {outputFile}")

        print("\nПервые строки файлов:")
        filesToCheck = ["text.txt", "encC_text.txt", "decC_encC_text.txt"]
        for filename in filesToCheck:
            try:
                with open(filename, 'r') as file:
                    firstLine = file.readline().strip()
                    print(f"{filename}: {firstLine}")
            except FileNotFoundError:
                print(f"{filename}:\tфайл не найден")