import requests
import json
import hashlib

# URL для авторизации и вызова методов
url = 'https://services.fedresurs.ru/SignificantEvents/MessagesServiceDemo2/v1/'

# Логин и пароль для авторизации
login = 'demo'
password = 'Ax!761BN'
session = requests.Session()

# Функция для проверки и очистки введенного ИНН
def process_inn():
    while True:
        inn = input('Введите ИНН (от 10 до 15 цифр): ')
        inn = ''.join([ch for ch in inn if ch.isdigit()]) # Удаление всех символов из строки, оставление только цифр
        if 10 <= len(inn) <= 15:
            return inn
        print('Введите число, состоящий из 10-15 цифр')

# Хэширование пароля
password_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()

# Параметры запроса на авторизацию
params = {'login': login, 'passwordHash': password_hash}

# Отправка POST-запроса для получения авторизационного токена
response = session.post(url + 'auth', data=json.dumps(params), headers={'Content-Type': 'application/json'})

# Извлечение токена из ответа
if response.status_code == requests.codes.ok:
    token = response.json()
    session.headers.update({'Authorization': 'Bearer ' + token['jwt']})
    print('Токен получен')
else:
    print('Не удалось получить токен авторизации. Код ошибки: %d' % response.status_code)
    token = ''
    headers = {}

inn = process_inn()
# 'participant.type': ['Company', 'IndividualEntrepreneur', 'Person', 'Appraiser'],
query = {
    'messageTypes': ['AnyOther', 'FinancialLeaseContract'],
    'participant.type': ['Company', 'IndividualEntrepreneur', 'Person', 'Appraiser'],
    'participant.code': inn,
    'limit': 20,
    'offset': 0
}

# Отправка запроса на контур

response = session.get(url + 'messages', params=query)
print(response.url)
print(response.status_code)
print(response.json())
