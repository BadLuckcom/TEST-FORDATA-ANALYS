# -*- coding: utf-8 -*-
"""Тестовое задание №3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1S34xqyze1zt-oOt61aeBUphd-MeGWYq8
"""

import json
from datetime import datetime, timedelta

def check_client_eligibility(client_data: dict) -> bool:
    birth_date = datetime.fromisoformat(client_data["birthDate"].replace("Z", ""))
    passport_issued_at = datetime.fromisoformat(client_data["passport"]["issuedAt"].replace("Z", ""))
    current_date = datetime.now()
    age = (current_date - birth_date).days // 365

    # Проверка 1: Минимальный возраст (не менее 20 лет)
    if age < 20:
        return False

    # Проверка 2: Действительность паспорта
    age_20_date = birth_date + timedelta(days=365*20)
    age_45_date = birth_date + timedelta(days=365*45)

    if (age >= 20 and passport_issued_at < age_20_date) or (age >= 45 and passport_issued_at < age_45_date):
        return False

    # Проверка 3: Кредитная история
    overdue_count = 0  # Количество кредитов с просрочкой более 15 дней

    for credit in client_data["creditHistory"]:
        credit_type = credit["type"].lower()
        overdue_days = credit["numberOfDaysOnOverdue"]
        current_overdue = credit["currentOverdueDebt"] > 0

        if "кредитная карта" in credit_type:
            if current_overdue or overdue_days > 30:
                return False
        else:
            if current_overdue or overdue_days > 60:
                return False
            if overdue_days > 15:
                overdue_count += 1

    # Проверка количества кредитов с просрочкой более 15 дней
    if overdue_count > 2:
        return False

    return True

client_json = '''{
    "firstName": "Иван",
    "middleName": "Иванович",
    "lastName": "Иванов",
    "birthDate": "1969-12-31T21:00:00.000Z",
    "citizenship": "РФ",
    "passport": {
        "series": "12 34",
        "number": "123456",
        "issuedAt": "2023-03-11T21:00:00.000Z",
        "issuer": "УФМС",
        "issuerСode": "123-456"
    },
    "creditHistory": [
        {
            "type": "Кредит наличными",
            "currency": "RUB",
            "issuedAt": "2003-02-27T21:00:00.000Z",
            "rate": 0.13,
            "loanSum": 100000,
            "term": 12,
            "repaidAt": "2004-02-27T21:00:00.000Z",
            "currentOverdueDebt": 0,
            "numberOfDaysOnOverdue": 0,
            "remainingDebt": 0,
            "creditId": "25e8a350-fbbc-11ee-a951-0242ac120002"
        },
        {
            "type": "Кредитная карта",
            "currency": "RUB",
            "issuedAt": "2009-03-27T21:00:00.000Z",
            "rate": 0.24,
            "loanSum": 30000,
            "term": 3,
            "repaidAt": "2009-06-29T20:00:00.000Z",
            "currentOverdueDebt": 0,
            "numberOfDaysOnOverdue": 2,
            "remainingDebt": 0,
            "creditId": "81fb1ff6-fbbc-11ee-a951-0242ac120002"
        },
        {
            "type": "Кредит наличными",
            "currency": "RUB",
            "issuedAt": "2009-02-27T21:00:00.000Z",
            "rate": 0.09,
            "loanSum": 200000,
            "term": 24,
            "repaidAt": "2011-03-02T21:00:00.000Z",
            "currentOverdueDebt": 0,
            "numberOfDaysOnOverdue": 3,
            "remainingDebt": 0,
            "creditId": "c384eea2-fbbc-11ee-a951-0242ac120002"
        },
        {
            "type": "Кредит наличными",
            "currency": "RUB",
            "issuedAt": "2024-05-15T21:00:00.000Z",
            "rate": 0.13,
            "loanSum": 200000,
            "term": 36,
            "repaidAt": null,
            "currentOverdueDebt": 10379,
            "numberOfDaysOnOverdue": 15,
            "remainingDebt": 110000,
            "creditId": "ebeddfde-fbbc-11ee-a951-0242ac120002"
        }
    ]
}'''

client_data = json.loads(client_json)
print(check_client_eligibility(client_data))

"""Логика работы функции
Функция анализирует JSON-объект с информацией о клиенте и его кредитной истории. Она выполняет три проверки:

Минимальный возраст

Вычисляется возраст клиента на текущую дату.
Если возраст меньше 20 лет – отказ.
Проверка действительности паспорта

Если клиенту больше 20 лет, паспорт должен быть выдан после достижения 20 лет.
Если клиенту больше 45 лет, паспорт должен быть выдан после достижения 45 лет.
Если одно из условий не выполняется – отказ.
Проверка кредитной истории

Для всех типов кредитов проверяется наличие непогашенной просроченной задолженности.
Для кредитных карт отказ происходит, если была просрочка более 30 дней.
Для обычных кредитов отказ происходит, если была просрочка более 60 дней или более двух кредитов с просрочкой >15 дней.
Если клиент проходит все проверки, функция возвращает True, иначе False.

{
  "firstName": "Иван",
  "middleName": "Иванович",
  "lastName": "Иванов",
  "birthDate": "2000-01-15T00:00:00.000Z",
  "citizenship": "РФ",
  "passport": {
    "series": "12 34",
    "number": "123456",
    "issuedAt": "2021-01-20T00:00:00.000Z",
    "issuer": "УФМС",
    "issuerСode": "123-456"
  },
  "creditHistory": [
    {
      "type": "Кредит наличными",
      "currency": "RUB",
      "issuedAt": "2022-06-01T00:00:00.000Z",
      "rate": 0.13,
      "loanSum": 50000,
      "term": 12,
      "repaidAt": null,
      "currentOverdueDebt": 0,
      "numberOfDaysOnOverdue": 0,
      "remainingDebt": 25000,
      "creditId": "123456789"
    }
  ]
}

Результат выполнения функции:
✅ Вывод: True (Клиент успешно прошел все проверки).
"""