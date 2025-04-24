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
    """Определение длины ключа методом индекса совпадений"""

    def ic(text):
        freq = {}
        for c in text:
            freq[c] = freq.get(c, 0) + 1
        total = len(text)
        if total < 2:
            return 0
        return sum([count * (count - 1) for count in freq.values()]) / (total * (total - 1))

    # Нормальный IC (индекс совпадений) для английского языка
    english_ic = 0.0667

    bestLen = 1
    bestDiff = float('inf')

    for length in range(1, max_len + 1):
        total_ic = 0.0
        # Создаем length групп символов
        groups = [''] * length
        for i, c in enumerate(ciphertext):
            groups[i % length] += c

        # Вычисляем средний IC для всех групп
        valid_groups = 0
        avg_ic = 0.0
        for group in groups:
            if len(group) > 1:
                group_ic = ic(group)
                avg_ic += group_ic
                valid_groups += 1

        if valid_groups == 0:
            continue

        avg_ic /= valid_groups
        diff = abs(avg_ic - english_ic)

        if diff < bestDiff:
            bestDiff = diff
            bestLen = length

    return bestLen


def keyDecrypt(ciphertext, key_length):
    # Разделяем текст на группы по ключу
    groups = [''] * key_length
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            groups[i % key_length] += c

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
    key_len = len(key)
    key_index = 0

    for c in ciphertext:
        if c.isalpha():
            shift = ord(key[key_index % key_len]) - ord('a')
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

    # Проверяем, все ли символы в ключе одинаковые
    if all(c == key[0] for c in key):
        print("Шифротекст Цезаря")
        keyC = ord(key[0]) - ord('a')
        print(f"Ключ К: {keyC}")
    else:
        print("Шифротекст Виженера")
        print(f"Ключ: {key}")

    decryptedText = decryptVigenere(ciphertext, key)
    write_file("Decrypted.txt", decryptedText)
    print("Текст расшифрован и сохранен в Decrypted.txt")
