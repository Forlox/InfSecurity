def dataToMas():
    with open("data.txt", 'r') as file:
        lines = file.readlines()
        data = []
        for line in lines:
            parts = line.strip().split(' ')
            data.append(parts)
        return data

def getUserData(username):
    data = dataToMas()
    for user in data:
        if user[0] == username:
            return user
    return None

def writeUserData(userMas):
    data = dataToMas()
    with open("data.txt", 'w') as file:
        for user in data:
            if user[0] == userMas[0]:
                file.write(' '.join(userMas) + '\n')
            else:
                file.write(' '.join(user) + '\n')

def getPassword(username):
    return getUserData(username)[1]

def getFlags(username):
    userData = getUserData(username)
    if userData and len(userData) > 3:
        return userData[3]
    return "0000"

def userVerification(login, password):
    with open("data.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ')
            if len(parts) < 2:
                continue  # Пропустить некорректные строки
            loginInDB = parts[0]
            passwordInDB = parts[1]
            blockFlag = parts[2] if len(parts) > 2 else "0"
            flags = parts[3] if len(parts) > 3 else "0000"
            if login == loginInDB:
                if blockFlag == "1" and password == passwordInDB:
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
            blockFlag = parts[2] if len(parts) > 2 else "0"
            flags = parts[3] if len(parts) > 3 else "0000"

            if login == loginInDB and (oldPassword == passwordInDB or passwordInDB == ""):
                file.write(f"{login} {newPassword} {blockFlag} {flags}\n")
            else:
                file.write(line)


def addUser(username):
    with open("data.txt", 'a') as file:
        file.write(f"{username}  0 1111\n")

def toggleUserBlock(username):
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
            blockFlag = parts[2] if len(parts) > 2 else "0"
            flags = parts[3] if len(parts) > 3 else "0000"

            if username == loginInDB:
                newFlag = "1" if blockFlag == "0" else "0"
                file.write(f"{username} {passwordInDB} {newFlag} {flags}\n")
            else:
                file.write(line)


def passwordFlags(password):
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