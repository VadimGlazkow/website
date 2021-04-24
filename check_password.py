def check_password(password):
    if len(password) > 8:
        return 'Длина меньше 8 символов'
    if not [None for letter in password if letter in '0123456789']:
        return 'В пароле нет цифр'
    if not [None for letter in password if letter.islower()]:
        return 'Пароль не имеет букв нижнего регистра'
    if not [None for letter in password if letter.isupper()]:
        return 'Пароль не имеет букв верхнего регистра'


p = check_password('qweGrt7y')
print(p)



