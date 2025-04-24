import matplotlib.pyplot as plt


class FrequencyOfLetters:
    def __init__(self):
        self.filename = "1984.txt"
        self.chrsCount = {}
        self.chrsFrq = {}
        self.total_chars = 0

    def chrsFrequencyBook(self):
        self.chrsCount = {}
        self.total_chars = 0

        with open(self.filename, 'r') as file:
            for line in file:
                for c in line.lower():
                    if c.isalpha() or c.isspace():
                        if c in self.chrsCount:
                            self.chrsCount[c] += 1
                        else:
                            self.chrsCount[c] = 1
                        self.total_chars += 1

        self.chrsFrq = {char: count / self.total_chars for char, count in self.chrsCount.items()}
        return self.chrsFrq

    def printStats(self):
        if not self.chrsCount or not self.chrsFrq:
            self.chrsFrequencyBook()  # Если словари пустые, сначала вызываем подсчёт

        print("Символ | Количество | Процент")
        print("-----------------------------")
        for char in sorted(self.chrsCount.keys()):
            print(f"'{char}': \t {self.chrsCount[char]:6d} \t {self.chrsFrq[char] * 100:.2f}%")

    def plot10Chrs(self):
        if not self.chrsCount:
            self.chrsFrequencyBook()  # Если словарь пуст, сначала вызываем подсчёт

        top_chars = sorted(self.chrsCount.items(), key=lambda x: x[1], reverse=True)[:10]
        chars, counts = zip(*top_chars)

        plt.figure(figsize=(10, 5))
        plt.bar(chars, counts, color='skyblue')
        plt.title("Топ-10 самых частых символов")
        plt.xlabel("Символ")
        plt.ylabel("Количество")
        plt.show()


if __name__ == "__main__":
    analyzer = FrequencyOfLetters("1984.txt")

    chrsFrq = analyzer.chrsFrequencyBook()
    print("Словарь вероятностей символов:", chrsFrq)

    print("\nСтатистика символов:")
    analyzer.printStats()

    print("\nПостроение диаграммы...")
    analyzer.plot10Chrs()