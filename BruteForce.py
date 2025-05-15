import PasswordAnalisys
import time
from dataDefs import getPassword


def checkPassword(login, password):
    return password == getPassword(login)


def сменаРаскладки(text):
    eng = "qwertyuiop[]asdfghjkl;'zxcvbnm,.`"
    ru = "йцукенгшщзхъфывапролджэячсмитьбюё"
    result = []

    for char in text:
        if char in eng:
            i = eng.index(char)
            result.append(ru[i])
        elif char in ru:
            i = ru.index(char)
            result.append(eng[i])
        else:
            result.append(char)
    return ''.join(result)


def bruteByBook(login):
    start_time = time.time()
    attempts = 0

    with open("Пароли.txt", 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            attempts += 1
            if checkPassword(login, line):
                elapsed_time = time.time() - start_time
                return attempts, elapsed_time

            # Пропускаем смену раскладки если только цифры
            if line.isdigit():
                continue

            attempts += 1
            if checkPassword(login, сменаРаскладки(line)):
                elapsed_time = time.time() - start_time
                return attempts, elapsed_time

    elapsed_time = time.time() - start_time
    return -1, elapsed_time


def bruteForce(login, chrs, maxLen, strength):
    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    specials = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`\'"\\'

    alphabet = ''
    if strength == 95:
        alphabet = lower + upper + numbers + specials
    elif strength == 36:  # буквы + цифры
        alphabet = (lower if any(c.islower() for c in chrs) else '') + \
                   (upper if any(c.isupper() for c in chrs) else '') + \
                   numbers
    elif strength == 52:  # буквы
        alphabet = lower + upper
    elif strength == 26:  # строчные или заглавные
        alphabet = lower if any(c.islower() for c in chrs) else upper
    elif strength == 10:  # цифры
        alphabet = numbers
    elif strength == 33:  # спецсимволы
        alphabet = specials

    attempt = 0
    startTime = time.time()

    for length in range(1, maxLen + 1):
        indexes = [0] * length

        while True:
            current = ''.join([alphabet[i] for i in indexes])
            attempt += 1

            if attempt % 100000 == 0:
                print(f"Попытка {attempt}: проверяем '{current}'")

            if checkPassword(login, current):
                endTime = time.time()
                totalTime = endTime - startTime
                return attempt, totalTime

            # Переход к следующей комбинации
            i = length - 1
            while i >= 0:
                if indexes[i] < len(alphabet) - 1:
                    indexes[i] += 1
                    break
                else:
                    indexes[i] = 0
                    i -= 1
            else:
                break

    endTime = time.time()
    totalTime = endTime - startTime
    return -1, totalTime


if __name__ == "__main__":
    login = "ADMIN"
    password = getPassword(login)
    maxLen = len(password)
    strength = PasswordAnalisys.alphabet_strength(password)
    print(f"Пароль '{password}', макс длина: {maxLen}, мощность алфавита: {strength}")

    attempts, brute_time = bruteForce(login, password, maxLen, strength)
    attemptsBook, timeBook = bruteByBook(login)

    if attemptsBook != -1:
        print(f"Пароль найден в словаре за {attemptsBook} попыток")
        print(f"Затрачено времени: {timeBook:.2f} сек")
    else:
        print("Пароль не найден в словаре")

    if attempts != -1:
        print(f"Пароль подобран за {attempts} попыток")
        print(f"Затрачено времени: {brute_time:.2f} сек")