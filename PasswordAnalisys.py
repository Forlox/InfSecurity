import math

def alphabet_strength(password):
    lower = upper = special = number = False

    for c in password:
        if c.islower(): lower = True
        elif c.isupper(): upper = True
        elif c.isdigit(): number = True
        else: special = True

    if lower and upper and number and special: return 95
    elif (lower or upper) and number: return 36
    elif lower and upper: return 52
    elif lower or upper: return 26
    elif number: return 10
    elif special: return 33


def enumtime(s, m, u, attempts):
    pauseCount = math.floor((attempts-1) / m)
    timeCalculate = attempts/s + pauseCount*u

    years = int(timeCalculate / (365 * 24 * 3600))
    timeCalculate-= years * (365 * 24 * 3600)

    months = int(timeCalculate / (30 * 24 * 3600))
    timeCalculate -= months * (30 * 24 * 3600)

    days = int(timeCalculate / (24 * 3600))
    timeCalculate -= days * (24 * 3600)

    hours = int(timeCalculate / 3600)
    timeCalculate -= hours * 3600

    minutes = int(timeCalculate / 60)
    timeCalculate -= minutes * 60

    seconds = int(timeCalculate)

    print(f"Время перебора: {years} лет {months} месяцев {days} дней {hours} часов {minutes} минут {seconds} секунд")


if __name__ == "__main__":
    while True:
        password = input("password: ")
        n = alphabet_strength(password)
        l = len(password)
        print(f"Мощность алфавита: {n}")
        print(f"Длина пароля: {l}")
        print(f"Количество возможных комбинаций: {n**l}")

        s = float(input("Скорость перебора паролей в секунду s: "))
        m = float(input("Количество неправильных попыток перед паузой m: "))
        u = float(input("Длительность паузы в секундах u: "))

        enumtime(s, m, u, n**l)
