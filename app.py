import requests
import json
import hashlib

# URL для авторизации и вызова методов
url = 'https://services.fedresurs.ru/SignificantEvents/MessagesServiceDemo2/v1/'

# Логин и пароль для авторизации
login = 'demo'
password = 'Ax!761BN'

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
response = requests.post(url + 'auth', data=json.dumps(params), headers={'Content-Type': 'application/json'})

# Извлечение токена из ответа
if response.status_code == requests.codes.ok:
    token = response.json()
    headers = {'Authorization': 'Bearer ' + token['jwt']}
    print('Токен получен')
else:
    print('Не удалось получить токен авторизации. Код ошибки: %d' % response.status_code)
    token = ''
    headers = {}

inn = process_inn()

query = {
    'messageTypes': 'AnyOther',
    'messageTypes': 'FinancialLeaseContract',
    'participant.type': 'LegalEntity',
    'participant.code': '364113334012',
    'limit': 20,
    'offset': 0
}

response = requests.get(url + 'messages', headers=headers, params=query)
response.raise_for_status()
if response.status_code == requests.codes.ok:
    messages = response.json()['messages']
    if messages:
        for message in messages:
            print(message['guid'])
            print(message['participants'])
            print(message['datePublish'])
            print(message['messageType']['name'])
    else:
        print('Сообщения не найдены')
else:
    print('Не удалось получить список сообщений. Код ошибки: %d' % response.status_code)
