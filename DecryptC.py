from FrequencyOfLetters import FrequencyOfLetters

frequency = FrequencyOfLetters()
chrsFreq = frequency.chrsFrequencyBook()


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().lower()


def write_file(filename, text):
    with open(filename, 'w') as file:
        file.write(text)


def keyLen(ciphertext, max_len=20):
    """Определение длины ключа методом индекса совпадений с подробным выводом"""

    def ic(text):
        freq = {}
        for c in text:
            freq[c] = freq.get(c, 0) + 1
        total = len(text)
        if total < 2:
            return 0
        return sum([count * (count - 1) for count in freq.values()]) / (total * (total - 1))

    # Нормальный IC для английского языка
    englishIC = 0.0667


    bestLen = 1
    bestDiff = float('inf')

    print("Длина\tСредний IC\tРазница")

    for length in range(1, max_len + 1):
        groups = [''] * length
        for i, c in enumerate(ciphertext):
            groups[i % length] += c

        validGroups = 0
        avgIC = 0.0
        for group in groups:
            if len(group) > 1:
                group_ic = ic(group)
                avgIC += group_ic
                validGroups += 1

        if validGroups == 0:
            continue

        avgIC /= validGroups
        diff = abs(avgIC - englishIC)

        print(f"\t{length}\t{avgIC:.8f}\t{diff:.8f}")

        if diff < bestDiff:
            bestDiff = diff
            bestLen = length

    print()
    print(f"Наиболее вероятная длина ключа: {bestLen} (разница c английским: {bestDiff:8f})")
    print()
    return bestLen


def keyDecrypt(ciphertext, keyLen):
    # Разделяем текст на группы по ключу
    groups = [''] * keyLen
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            groups[i % keyLen] += c

    key = []
    for group in groups:
        # Для каждой группы находим сдвиг по частотному анализу
        freqs = letterFreq(group)
        bestShift = 0
        bestScore = float('inf')

        # Пробуем все возможные сдвиги (0-25)
        for shift in range(26):
            score = 0
            for c in freqs:
                decrypted_char = chr(((ord(c) - ord('a') - shift) % 26) + ord('a'))
                score += abs(freqs[c] - chrsFreq.get(decrypted_char, 0))

            if score < bestScore:
                bestScore = score
                bestShift = shift

        key.append(chr(bestShift + ord('a')))

    return ''.join(key)


def letterFreq(text):
    freq = {}
    total = 0
    for c in text:
        if c.isalpha():
            freq[c] = freq.get(c, 0) + 1
            total += 1

    return {k: v / total for k, v in freq.items()}


def decryptVigenere(ciphertext, key):
    decrypted = []
    keyLen = len(key)
    key_index = 0

    for c in ciphertext:
        if c.isalpha():
            shift = ord(key[key_index % keyLen]) - ord('a')
            decrypted_char = chr(((ord(c) - ord('a') - shift) % 26) + ord('a'))
            decrypted.append(decrypted_char)
            key_index += 1
        else:
            decrypted.append(c)

    return ''.join(decrypted)


if __name__ == "__main__":
    ciphertext = read_file("encC_text.txt")
    encText = ''.join(c for c in ciphertext if c.isalpha())
    key_length = keyLen(encText)
    key = keyDecrypt(encText, key_length)

    if all(c == key[0] for c in key):
        print("Шифротекст Цезаря")
        print(f"Ключ К: {ord(key[0]) - ord('a')}")
    else:
        print("Шифротекст Виженера")
        print(f"Ключ: {key}")

    decryptedText = decryptVigenere(ciphertext, key)
    write_file("Decrypted.txt", decryptedText)
    print("Текст расшифрован и сохранен в Decrypted.txt")
