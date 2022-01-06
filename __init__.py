from typing import Optional, Union

import requests
from .errors import *


class Client:
    url = 'https://smshub.org/stubs/handler_api.php'

    def __init__(self, key: str):
        self.key = key

    def get_balance(self) -> float:
        req = requests.get(self.url, params={'api_key': self.key, 'action': 'getBalance'})
        return float(req.text.replace('ACCESS_BALANCE:', ''))

    def get_number_status(self, country: Optional[int] = None, operator: Optional[str] = None) -> dict[str, int]:
        req = requests.get(self.url, params={
            'api_key': self.key,
            'action': 'getNumbersStatus',
            'country': country,
            'operator': operator,
        })
        if req.text == 'BAD_KEY':
            raise BadKeyError('Неверный API-ключ')
        elif req.text == 'ERROR_SQL':
            raise ErrorSql('Ошибка сервера')
        return req.json()

    def get_number(self, service: str, operator: Optional[str] = None, country: Optional[int] = None) -> (int, int):
        req = requests.get(self.url, params={
            'api_key': self.key,
            'action': 'getNumber',
            'service': service,
            'operator': operator,
            'country': country,
        })
        if req.text == 'NO_NUMBERS':
            raise NoNumbers('Нет номеров с заданными параметрами, попробуйте позже, или поменяйте оператора, страну.')
        elif req.text == 'NO_BALANCE':
            raise NoBalance('Закончились деньги на API-ключе')
        elif req.text == 'WRONG_SERVICE':
            raise WrongService('Не верный идентификатор сервиса')
        else:
            return tuple(map(int, req.text.split(':')[1:]))

    def set_status(self, id_: int, status: int) -> str:
        req = requests.get(self.url, params={
            'api_key': self.key,
            'action': 'setStatus',
            'id': id_,
            'status': status,
        })
        return req.text

    def get_status(self, id_: int) -> Union[str, tuple[int, int]]:
        req = requests.get(self.url, params={
            'api_key': self.key,
            'action': 'getStatus',
            'id': id_,
        })
        if req.text == 'NO_ACTIVATION':
            raise NoActivation('id активации не существует')
        elif req.text == 'ERROR_SQL':
            raise ErrorSql('Ошибка базы SQL-сервера')
        elif req.text.startswith('STATUS_WAIT_RETRY') or req.text.startswith('STATUS_OK'):
            status, code = req.text.split(':')
            return status, code
        return req.text

    def get_prices(self, service: str = None, country: int = None) -> dict[str, dict[str, dict[str, int]]]:
        req = requests.get(self.url, params={
            'api_key': self.key,
            'action': 'getPrices',
            'service': service,
            'country': country,
        })
        return req.json()


class Utils:
    id_to_country_name_dict = {0: 'Россия', 1: 'Украина', 2: 'Казахстан', 3: 'Китай', 4: 'Филиппины', 5: 'Мьянма',
                               6: 'Индонезия', 7: 'Малайзия', 8: 'Кения', 9: 'Танзания', 10: 'Вьетнам',
                               11: 'Кыргызстан', 12: 'США (виртуальные)', 13: 'Израиль', 14: 'Гонконг', 15: 'Польша',
                               16: 'Англия', 18: 'Дем.Конго', 19: 'Нигерия', 21: 'Египет', 22: 'Индия', 23: 'Ирландия',
                               24: 'Камбоджа', 25: 'Лаос', 26: 'Гаити', 27: "Кот д'Ивуар", 28: 'Гамбия', 29: 'Сербия',
                               30: 'Йемен', 31: 'Южная Африка', 32: 'Румыния', 33: 'Колумбия', 34: 'Эстония',
                               36: 'Канада', 37: 'Марокко', 38: 'Гана', 39: 'Аргентина', 40: 'Узбекистан',
                               41: 'Камерун', 42: 'Чад', 43: 'Германия', 44: 'Литва', 45: 'Хорватия', 46: 'Швеция',
                               47: 'Ирак', 48: 'Нидерланды', 49: 'Латвия', 50: 'Австрия', 51: 'Беларусь', 52: 'Таиланд',
                               53: 'Сауд. Аравия', 54: 'Мексика', 55: 'Тайвань', 56: 'Испания', 57: 'Иран', 58: 'Алжир',
                               60: 'Бангладеш', 61: 'Сенегал', 62: 'Турция', 63: 'Чехия', 64: 'Шри-Ланка', 65: 'Перу',
                               66: 'Пакистан', 67: 'Новая Зеландия', 68: 'Гвинея', 69: 'Мали', 70: 'Венесуэла',
                               72: 'Монголия', 73: 'Бразилия', 74: 'Афганистан', 75: 'Уганда', 76: 'Ангола', 77: 'Кипр',
                               78: 'Франция', 79: 'Папуа-Новая Гвинея', 80: 'Мозамбик', 81: 'Непал', 85: 'Молдова',
                               87: 'Парагвай', 88: 'Гондурас', 89: 'Тунис', 90: 'Никарагуа', 92: 'Боливия',
                               94: 'Гватемала', 95: 'ОАЭ', 96: 'Зимбабве', 98: 'Судан', 101: 'Сальвадор', 102: 'Ливия',
                               103: 'Ямайка', 104: 'Тринидад и Тобаго', 105: 'Эквадор', 109: 'Доминиканская Республика',
                               110: 'Сирия', 114: 'Мавритания', 115: 'Сьерра-Леоне', 116: 'Иордания', 117: 'Португалия',
                               120: 'Бенин', 121: 'Бруней', 123: 'Ботсвана', 126: 'Доминика', 128: 'Грузия',
                               129: 'Греция', 131: 'Гайана', 135: 'Либерия', 142: 'Суринам', 143: 'Таджикистан',
                               146: 'Реюньон', 148: 'Армения', 150: 'Конго', 152: 'Буркина-Фасо', 153: 'Ливан',
                               154: 'Габон', 157: 'Маврикий', 158: 'Бутан', 159: 'Мальдивы', 161: 'Туркменистан',
                               172: 'Дания', 179: 'Аруба', 187: 'США', 189: 'Фиджи', 195: 'Бермуды'}
    country_name_to_id_dict = {'Россия': 0, 'Украина': 1, 'Казахстан': 2, 'Китай': 3, 'Филиппины': 4, 'Мьянма': 5,
                               'Индонезия': 6, 'Малайзия': 7, 'Кения': 8, 'Танзания': 9, 'Вьетнам': 10,
                               'Кыргызстан': 11, 'США (виртуальные)': 12, 'Израиль': 13, 'Гонконг': 14, 'Польша': 15,
                               'Англия': 16, 'Дем.Конго': 18, 'Нигерия': 19, 'Египет': 21, 'Индия': 22, 'Ирландия': 23,
                               'Камбоджа': 24, 'Лаос': 25, 'Гаити': 26, "Кот д'Ивуар": 27, 'Гамбия': 28, 'Сербия': 29,
                               'Йемен': 30, 'Южная Африка': 31, 'Румыния': 32, 'Колумбия': 33, 'Эстония': 34,
                               'Канада': 36, 'Марокко': 37, 'Гана': 38, 'Аргентина': 39, 'Узбекистан': 40,
                               'Камерун': 41, 'Чад': 42, 'Германия': 43, 'Литва': 44, 'Хорватия': 45, 'Швеция': 46,
                               'Ирак': 47, 'Нидерланды': 48, 'Латвия': 49, 'Австрия': 50, 'Беларусь': 51, 'Таиланд': 52,
                               'Сауд. Аравия': 53, 'Мексика': 54, 'Тайвань': 55, 'Испания': 56, 'Иран': 57, 'Алжир': 58,
                               'Бангладеш': 60, 'Сенегал': 61, 'Турция': 62, 'Чехия': 63, 'Шри-Ланка': 64, 'Перу': 65,
                               'Пакистан': 66, 'Новая Зеландия': 67, 'Гвинея': 68, 'Мали': 69, 'Венесуэла': 70,
                               'Монголия': 72, 'Бразилия': 73, 'Афганистан': 74, 'Уганда': 75, 'Ангола': 76, 'Кипр': 77,
                               'Франция': 78, 'Папуа-Новая Гвинея': 79, 'Мозамбик': 80, 'Непал': 81, 'Молдова': 85,
                               'Парагвай': 87, 'Гондурас': 88, 'Тунис': 89, 'Никарагуа': 90, 'Боливия': 92,
                               'Гватемала': 94, 'ОАЭ': 95, 'Зимбабве': 96, 'Судан': 98, 'Сальвадор': 101, 'Ливия': 102,
                               'Ямайка': 103, 'Тринидад и Тобаго': 104, 'Эквадор': 105, 'Доминиканская Республика': 109,
                               'Сирия': 110, 'Мавритания': 114, 'Сьерра-Леоне': 115, 'Иордания': 116, 'Португалия': 117,
                               'Бенин': 120, 'Бруней': 121, 'Ботсвана': 123, 'Доминика': 126, 'Грузия': 128,
                               'Греция': 129, 'Гайана': 131, 'Либерия': 135, 'Суринам': 142, 'Таджикистан': 143,
                               'Реюньон': 146, 'Армения': 148, 'Конго': 150, 'Буркина-Фасо': 152, 'Ливан': 153,
                               'Габон': 154, 'Маврикий': 157, 'Бутан': 158, 'Мальдивы': 159, 'Туркменистан': 161,
                               'Дания': 172, 'Аруба': 179, 'США': 187, 'Фиджи': 189, 'Бермуды': 195}

    def __init__(self, client: Client):
        self.client = client

    def find_min_prices(self, service: str, count: int = None) -> list[tuple[float, str, int]]:
        """
        :param service: название сервиса
        :param count: количество результатов к выдаче (опционально)
        :return: элементы, содержащие стоимость, код страны и количество симок
        """
        ans = []
        for country, val in self.client.get_prices(service).items():
            if service in val.keys():
                ans.extend([(float(i[0]), country, i[1]) for i in val[service].items()])
        return sorted(ans, key=lambda x: x[0])[:count]

    def id_to_country_name(self, id_: int) -> str:
        return self.id_to_country_name_dict[id_]

    def country_name_to_id(self, country: str) -> int:
        return self.country_name_to_id_dict[country]