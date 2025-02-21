import sys

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QListWidget, QInputDialog


def userVerification(login, password):
    with open("data.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ')
            if len(parts) < 2:
                continue  # Пропустить некорректные строки
            loginInDB = parts[0]
            passwordInDB = parts[1]
            extraData = ' '.join(parts[2:]) if len(parts) > 2 else "00000"
            if login == loginInDB:
                if extraData[0] == "1" and password == passwordInDB:
                    return False, "Пользователь заблокирован"
                if passwordInDB == "":  # Пустой пароль
                    updatePassword(login, "", password)
                    return True, "Успешная регистрация, " + login
                elif password == passwordInDB:
                    return True, "Успешный вход"
        return False, "Неверный логин/пароль"


def updatePassword(login, oldPassword, newPassword):
    with open("data.txt", 'r') as file:
        lines = file.readlines()

    with open("data.txt", 'w') as file:
        for line in lines:
            parts = line.strip().split(' ')
            if len(parts) < 2:
                file.write(line)  # Пропустить некорректные строки
                continue
            loginInDB = parts[0]
            passwordInDB = parts[1]
            extraData = ' '.join(parts[2:]) if len(parts) > 2 else "00000"

            if login == loginInDB and (oldPassword == passwordInDB or passwordInDB == ""):
                file.write(f"{login} {newPassword} {extraData}\n")
            else:
                file.write(line)


def addUser(login):
    with open("data.txt", 'a') as file:
        file.write(f"{login}  0\n")  # Пустой пароль и флаг 0


def toggleUserBlock(login):
    with open("data.txt", 'r') as file:
        lines = file.readlines()

    with open("data.txt", 'w') as file:
        for line in lines:
            parts = line.strip().split(' ')
            if len(parts) < 2:
                file.write(line)  # Пропустить некорректные строки
                continue
            loginInDB = parts[0]
            passwordInDB = parts[1]
            extraData = ' '.join(parts[2:]) if len(parts) > 2 else "00000"

            if login == loginInDB:
                newFlag = "1" if extraData[0] == "0" else "0"
                file.write(f"{login} {passwordInDB} {newFlag}\n")
            else:
                file.write(line)


def passwordParams(password):
    flags = ['0', '0', '0', '0']

    for c in password:
        if c.islower():
            flags[0] = '1'
        if c.isupper():
            flags[1] = '1'
        if c.isdigit():
            flags[2] = '1'
        if not (c.islower() or c.isupper() or c.isdigit()):
            flags[3] = '1'

    return ''.join(flags)

class VerificationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.failedAttempts = 0  # Счетчик неудачных попыток
        self.setWindowTitle("Верификация")

        self.loginLabel = QLabel("Логин:")
        self.loginInput = QLineEdit()
        self.passwordLabel = QLabel("Пароль:")
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)

        self.loginButton = QPushButton("Войти")
        self.loginButton.clicked.connect(self.loginClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.loginLabel)
        layout.addWidget(self.loginInput)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordInput)
        layout.addWidget(self.loginButton)

        self.setLayout(layout)

    def loginClicked(self):
        login = self.loginInput.text()
        password = self.passwordInput.text()

        success, message = userVerification(login, password)
        if success:
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

        layout.addWidget(self.mainLabel)
        layout.addWidget(self.oldPasswordLabel)
        layout.addWidget(self.oldPasswordInput)
        layout.addWidget(self.newPasswordLabel)
        layout.addWidget(self.newPasswordInput)
        layout.addWidget(self.acceptPasswordButton)

        self.setLayout(layout)

    def newPasswordClicked(self):
        oldPassword = self.oldPasswordInput.text()
        newPassword = self.newPasswordInput.text()

        if not oldPassword or not newPassword:
            QMessageBox.warning(self, "Ошибка", "Поля не могут быть пустыми!")
            return

        if " " in newPassword:
            QMessageBox.warning(self, "Ошибка", "Новый пароль не может содержать пробелы!")
            return

        if not userVerification(self.username, oldPassword)[0]:
            QMessageBox.warning(self, "Ошибка", "Старый пароль неверный!")
            return

        updatePassword(self.username, oldPassword, newPassword)
        QMessageBox.information(self, "Успех", "Пароль успешно изменен!")


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

        self.changePasswordButton = QPushButton("Сменить пароль")
        self.changePasswordButton.clicked.connect(self.changePassword)

        layout.addWidget(self.userList)
        layout.addWidget(self.addUserButton)
        layout.addWidget(self.toggleBlockButton)
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
            addUser(login)
            self.loadUsers()

    def toggleUserBlock(self):
        selectedUser = self.userList.currentItem()
        if selectedUser:
            login = selectedUser.text().split(' - ')[0]
            toggleUserBlock(login)
            self.loadUsers()

    def changePassword(self):
        self.passwordWindow = MainUserWindow("ADMIN")
        self.passwordWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Создание файла при первом запуске
    try:
        with open("data.txt", 'x') as file:
            file.write("ADMIN  0\n")
    except FileExistsError:
        pass

    window = VerificationWindow()
    window.show()

    sys.exit(app.exec())
