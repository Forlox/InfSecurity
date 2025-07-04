import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QListWidget, QInputDialog
import dataDefs as d
from PasswordAnalisys import alphabet_strength, enumtime, calcSeconds

class VerificationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.s = 5
        self.m = 1
        self.u = 1

        self.failedAttempts = 0
        self.setWindowTitle("Верификация")

        self.loginLabel = QLabel("Логин:")
        self.loginInput = QLineEdit("")
        self.passwordLabel = QLabel("Пароль:")
        self.passwordInput = QLineEdit()
        # self.passwordInput.setEchoMode(QLineEdit.Password)

        self.loginButton = QPushButton("Войти")
        self.loginButton.clicked.connect(self.loginClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.loginLabel)
        layout.addWidget(self.loginInput)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordInput)
        layout.addWidget(self.loginButton)

        self.checkPasswordButton = QPushButton("Проверка введённого пароля")
        self.checkPasswordButton.clicked.connect(self.checkPasswordClicked)
        self.passwordAnalisysLabel = QLabel("")

        layout.addWidget(self.checkPasswordButton)
        layout.addWidget(self.passwordAnalisysLabel)

        self.setLayout(layout)

    # def bruteClicked(self):
    #     login = self.loginInput.text()
    #
    #     try:
    #         password = d.getPassword(login)
    #         if password is None:
    #             raise ValueError
    #     except Exception:
    #         QMessageBox.critical(self, "Ошибка", f"Пользователь '{login}' не найден.")
    #         return
    #
    #     print(f"Password to brute: {password}")
    #
    #     attemptsBook, timeBook = BruteForce.bruteByBook(login)
    #
    #     result_text = ""
    #
    #     if attemptsBook != -1:
    #         speedBook = attemptsBook / timeBook if timeBook > 0 else 0
    #         result_text += (
    #             f"Пароль найден в словаре за {attemptsBook} попыток\n"
    #             f"Прошло времени: {timeBook:.2f} сек\n"
    #             f"Средняя скорость подбора в сек: {speedBook:.2f}\n"
    #         )
    #     else:
    #         result_text += "Пароль не найден в словаре\n"
    #
    #
    #     maxLen = len(password)
    #     strength = 95
    #     attemptsBrute, timeBrute = BruteForce.bruteForce(login, 'aA1/', maxLen, strength)
    #
    #     if attemptsBrute != -1:
    #         speedBrute = attemptsBrute / timeBrute if timeBrute > 0 else 0
    #         result_text += (
    #             "========================\n"
    #             f"Пароль подобран за {attemptsBrute} попыток\n"
    #             f"Прошло времени: {timeBrute:.2f} сек\n"
    #             f"Средняя скорость перебора в сек: {speedBrute:.2f}\n"
    #         )
    #     else:
    #         result_text += "Пароль не удалось подобрать полным перебором\n"
    #
    #     QMessageBox.information(self, "Результаты брутфорса", result_text)

    def checkPasswordClicked(self):
        password = self.passwordInput.text()
        self.passwordAnalisysLabel.setText(enumtime(self.s,self.m,self.u, alphabet_strength(password)**len(password)))

    def loginClicked(self):
        login = self.loginInput.text()
        password = self.passwordInput.text()

        # Проверка на пустые поля
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Поля не могут быть пустыми!")
            return

        success, message = d.userVerification(login, password)
        if success:
            # Если пароль пустой (первый вход), проверяем флаги
            userData = d.getUserData(login)
            if userData and userData[1] == "":
                flags = d.getFlags(login)
                if flags != d.passwordFlags(password):
                    QMessageBox.warning(self, "Ошибка", "Пароль не соответствует требованиям.")
                    return
            ############
            QMessageBox.information(self, "Успех", message)
            if login == "ADMIN":
                self.mainWindow = MainADMINWindow()
            else:
                self.mainWindow = MainUserWindow(login)
            self.mainWindow.show()
            self.close()
        else:
            if message == "Пользователь заблокирован":
                QMessageBox.warning(self, "Ошибка", message)
                sys.exit()  # Завершаем программу при блокировке
            else:
                self.failedAttempts += 1
                if self.failedAttempts >= 3:
                    QMessageBox.critical(self, "Ошибка", "Превышено количество попыток.")
                    sys.exit()
                else:
                    self.loginButton.setText(f"Неверный логин/пароль ({self.failedAttempts}/3)")

class MainUserWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(username)
        layout = QVBoxLayout()

        self.mainLabel = QLabel("Смена пароля")
        self.oldPasswordLabel = QLabel("Старый пароль:")
        self.oldPasswordInput = QLineEdit()
        self.oldPasswordInput.setEchoMode(QLineEdit.Password)
        self.newPasswordLabel = QLabel("Новый пароль:")
        self.newPasswordInput = QLineEdit()
        self.newPasswordInput.setEchoMode(QLineEdit.Password)
        self.acceptPasswordButton = QPushButton("Сменить пароль")
        self.acceptPasswordButton.clicked.connect(self.newPasswordClicked)

        # Метка для отображения разрешённых и запрещённых символов
        self.allowedCharsLabel = QLabel("")
        self.updateAllowedCharsLabel()  # Обновляем метку при инициализации

        layout.addWidget(self.mainLabel)
        layout.addWidget(self.oldPasswordLabel)
        layout.addWidget(self.oldPasswordInput)
        layout.addWidget(self.newPasswordLabel)
        layout.addWidget(self.newPasswordInput)
        layout.addWidget(self.acceptPasswordButton)
        layout.addWidget(self.allowedCharsLabel)

        self.setLayout(layout)

    def updateAllowedCharsLabel(self):
        flags = d.getFlags(self.username)
        allowed = []
        forbidden = []

        if flags[0] == '1':
            allowed.append("нижний регистр")
        else:
            forbidden.append("нижний регистр")

        if flags[1] == '1':
            allowed.append("верхний регистр")
        else:
            forbidden.append("верхний регистр")

        if flags[2] == '1':
            allowed.append("цифры")
        else:
            forbidden.append("цифры")

        if flags[3] == '1':
            allowed.append("специальные символы")
        else:
            forbidden.append("специальные символы")

        self.allowedCharsLabel.setText(
            f"Требования к паролю: {', '.join(allowed) if allowed else 'нет'}\n"
            f"Запрещено в пароле: {', '.join(forbidden) if forbidden else 'нет'}"
        )

    def newPasswordClicked(self):
        oldPassword = self.oldPasswordInput.text()
        newPassword = self.newPasswordInput.text()

        if not oldPassword or not newPassword:
            QMessageBox.warning(self, "Ошибка", "Поля не могут быть пустыми!")
            return

        if " " in newPassword:
            QMessageBox.warning(self, "Ошибка", "Новый пароль не может содержать пробелы!")
            return

        if not d.userVerification(self.username, oldPassword)[0]:
            QMessageBox.warning(self, "Ошибка", "Старый пароль неверный!")
            return

        # Проверка нового пароля на соответствие флагам
        flags = d.getFlags(self.username)
        if flags != d.passwordFlags(newPassword):
            QMessageBox.warning(self, "Ошибка", "Новый пароль не соответствует требованиям.")
            return

        d.updatePassword(self.username, oldPassword, newPassword)
        QMessageBox.information(self, "Успех", "Пароль успешно изменен!")


class changePassFlagsWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Ограничения на пароли")
        lay = QVBoxLayout()

        self.label1 = QLabel("Логин пользователя:")
        self.input = QLineEdit()
        self.input.setText(username)  # Устанавливаем выбранного пользователя
        self.input.setReadOnly(True)  # Запрещаем редактирование

        self.userStatusLabel = QLabel("Флаги пароля:")
        self.label2 = QLabel("Статус флагов:")

        # Метки для отображения статуса флагов
        self.flagLowerStatus = QLabel("Нижний регистр: -")
        self.flagUpperStatus = QLabel("Верхний регистр: -")
        self.flagDigitStatus = QLabel("Цифры: -")
        self.flagSpecialStatus = QLabel("Специальные символы: -")

        # Кнопки для изменения флагов
        self.buttonFlagLower = QPushButton("Нижний регистр")
        self.buttonFlagLower.clicked.connect(lambda: self.changeFlags(0))
        self.buttonFlagUpper = QPushButton("Верхний регистр")
        self.buttonFlagUpper.clicked.connect(lambda: self.changeFlags(1))
        self.buttonFlagDigit = QPushButton("Цифры")
        self.buttonFlagDigit.clicked.connect(lambda: self.changeFlags(2))
        self.buttonFlagSpecial = QPushButton("Специальные символы")
        self.buttonFlagSpecial.clicked.connect(lambda: self.changeFlags(3))

        lay.addWidget(self.label1)
        lay.addWidget(self.input)
        lay.addWidget(self.userStatusLabel)
        lay.addWidget(self.label2)
        lay.addWidget(self.flagLowerStatus)
        lay.addWidget(self.flagUpperStatus)
        lay.addWidget(self.flagDigitStatus)
        lay.addWidget(self.flagSpecialStatus)
        lay.addWidget(self.buttonFlagLower)
        lay.addWidget(self.buttonFlagUpper)
        lay.addWidget(self.buttonFlagDigit)
        lay.addWidget(self.buttonFlagSpecial)

        self.setLayout(lay)
        self.updateUserStatus()  # Инициализация статуса при запуске

    def updateUserStatus(self):
        username = self.input.text()
        userData = d.getUserData(username)

        if userData:
            flags = d.getFlags(username)
            self.userStatusLabel.setText(f"Флаги пароля: {flags}")
            self.enableButtons(True)  # Включаем кнопки, если пользователь найден
            self.updateFlagStatuses(flags)  # Обновляем статусы флагов
        else:
            self.userStatusLabel.setText("Пользователь не найден")
            self.enableButtons(False)  # Отключаем кнопки, если пользователь не найден
            self.clearFlagStatuses()  # Очищаем статусы флагов

    def enableButtons(self, enabled):
        self.buttonFlagLower.setEnabled(enabled)
        self.buttonFlagUpper.setEnabled(enabled)
        self.buttonFlagDigit.setEnabled(enabled)
        self.buttonFlagSpecial.setEnabled(enabled)

    def updateFlagStatuses(self, flags):
        self.flagLowerStatus.setText(f"Нижний регистр: {'Включен' if flags[0] == '1' else 'Отключен'}")
        self.flagUpperStatus.setText(f"Верхний регистр: {'Включен' if flags[1] == '1' else 'Отключен'}")
        self.flagDigitStatus.setText(f"Цифры: {'Включен' if flags[2] == '1' else 'Отключен'}")
        self.flagSpecialStatus.setText(f"Специальные символы: {'Включен' if flags[3] == '1' else 'Отключен'}")

    def changeFlags(self, flagPos):
        username = self.input.text()
        userData = d.getUserData(username)

        if userData:
            flags = list(d.getFlags(username))  # Преобразуем строку флагов в список
            if 0 <= flagPos < len(flags):
                flags[flagPos] = '1' if flags[flagPos] == '0' else '0'  # Меняем флаг на противоположный
                userData[3] = ''.join(flags)
                d.writeUserData(userData)
                self.updateUserStatus()  # Обновляем статус после изменения флагов


class MainADMINWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADMIN")
        layout = QVBoxLayout()

        self.userList = QListWidget()
        self.loadUsers()

        self.addUserButton = QPushButton("Добавить пользователя")
        self.addUserButton.clicked.connect(self.addUser)

        self.toggleBlockButton = QPushButton("Заблокировать/Разблокировать")
        self.toggleBlockButton.clicked.connect(self.toggleUserBlock)

        self.changePassFlagsButton = QPushButton("Изменение параметров пароля")
        self.changePassFlagsButton.clicked.connect(self.changePassFlags)

        self.changePasswordButton = QPushButton("Сменить пароль")
        self.changePasswordButton.clicked.connect(self.changePassword)

        layout.addWidget(self.userList)
        layout.addWidget(self.addUserButton)
        layout.addWidget(self.toggleBlockButton)
        layout.addWidget(self.changePassFlagsButton)
        layout.addWidget(self.changePasswordButton)

        self.setLayout(layout)

    def loadUsers(self):
        self.userList.clear()  # Очистка списка перед загрузкой
        with open("data.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(' ')
                if len(parts) < 2:
                    continue  # Пропустить некорректные строки
                status = "Заблокирован" if len(parts) > 2 and parts[2] == "1" else "Активен"
                self.userList.addItem(f"{parts[0]} - {status}")

    def addUser(self):
        login, ok = QInputDialog.getText(self, 'Добавить пользователя', 'Введите логин:')
        if ok and login:
            d.addUser(login)
            self.loadUsers()

    def toggleUserBlock(self):
        selectedUser = self.userList.currentItem()
        if selectedUser:
            login = selectedUser.text().split(' - ')[0]
            if login == "ADMIN":
                QMessageBox.warning(self, "Ошибка", "Невозможно заблокировать ADMIN.")
                return
            d.toggleUserBlock(login)
            self.loadUsers()

    def changePassFlags(self):
        selectedUser = self.userList.currentItem()
        if selectedUser:
            username = selectedUser.text().split(' - ')[0]
            self.flagsWindow = changePassFlagsWindow(username)
            self.flagsWindow.show()

    def changePassword(self):
        self.passwordWindow = MainUserWindow("ADMIN")
        self.passwordWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Создание файла при первом запуске
    try:
        with open("data.txt", 'x') as file:
            file.write("ADMIN  0 1111\n")
    except FileExistsError:
        pass

    window = VerificationWindow()
    window.show()

    sys.exit(app.exec())