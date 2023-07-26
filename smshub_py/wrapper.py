from typing import Optional, Union
import httpx

from . import exceptions


class SmsHubWrapper:
    base_url = 'https://smshub.org/stubs/handler_api.php'

    def __init__(self, key: str):
        self.key = key

    @staticmethod
    def _process_status(r: httpx.Response):
        if r.text == 'BAD_KEY':
            raise exceptions.BadApiKey
        elif r.text == 'ERROR_SQL':
            raise exceptions.SqlError
        elif r.text == 'NO_NUMBERS':
            raise exceptions.NoNumbers
        elif r.text == 'NO_BALANCE':
            raise exceptions.NoBalance
        elif r.text == 'WRONG_SERVICE':
            raise exceptions.WrongService
        elif r.text == 'NO_ACTIVATION':
            raise exceptions.NoActivation

    def get_balance(self) -> float:
        """
        Get balance value
        :return: Balance value
        """
        req = httpx.get(self.base_url, params={'api_key': self.key, 'action': 'getBalance'})
        return float(req.text.replace('ACCESS_BALANCE:', ''))

    def get_number_status(self, country: Optional[int] = None, operator: Optional[str] = None) -> dict[str, int]:
        """
        Request for quantity available numbers
        :param country: Country ID
        :param operator: Operator code
        :return: `Dict` service - numbers quantity
        """
        req = httpx.get(self.base_url, params={
            'api_key': self.key,
            'action': 'getNumbersStatus',
            'country': country,
            'operator': operator,
        })
        self._process_status(req)
        return req.json()

    def get_number(self, service: str, operator: Optional[str] = None, country: Optional[int] = None) -> (int, int):
        """
        Request for using number
        :param service: Service code
        :param operator: Operator code
        :param country: Country ID
        :return: Activation ID and phone number
        """
        req = httpx.get(self.base_url, params={
            'api_key': self.key,
            'action': 'getNumber',
            'service': service,
            'operator': operator,
            'country': country,
        })
        self._process_status(req)
        return tuple(map(int, req.text.split(':')[1:]))

    def set_status(self, id_: int, status: int) -> str:
        """
        Set current status of activation
        :param id_: Activation ID
        :param status: Status ID
        :return: Status message
        """
        req = httpx.get(self.base_url, params={
            'api_key': self.key,
            'action': 'setStatus',
            'id': id_,
            'status': status,
        })
        return req.text

    def get_status(self, id_: int) -> Union[str, tuple[int, int]]:
        """
        Get status of activation
        :param id_: Activation ID
        :return: Status message, with code if possible
        """
        req = httpx.get(self.base_url, params={
            'api_key': self.key,
            'action': 'getStatus',
            'id': id_,
        })
        self._process_status(req)
        if req.text.startswith('STATUS_WAIT_RETRY') or req.text.startswith('STATUS_OK'):
            status, code = req.text.split(':')
            return status, code
        return req.text

    def get_prices(self, service: str = None, country: int = None) -> dict[str, dict[str, dict[str, int]]]:
        """
        Get all prices
        :param service: Service code
        :param country: Country ID
        :return: `Dict` with prices
        """
        req = httpx.get(self.base_url, params={
            'api_key': self.key,
            'action': 'getPrices',
            'service': service,
            'country': country,
        })
        return req.json()


class Utils:
    __id_to_country_name_dict = {0: 'Россия', 1: 'Украина', 2: 'Казахстан', 3: 'Китай', 4: 'Филиппины', 5: 'Мьянма',
                                 6: 'Индонезия', 7: 'Малайзия', 8: 'Кения', 9: 'Танзания', 10: 'Вьетнам',
                                 11: 'Кыргызстан', 12: 'США (виртуальные)', 13: 'Израиль', 14: 'Гонконг', 15: 'Польша',
                                 16: 'Англия', 18: 'Дем.Конго', 19: 'Нигерия', 21: 'Египет', 22: 'Индия',
                                 23: 'Ирландия',
                                 24: 'Камбоджа', 25: 'Лаос', 26: 'Гаити', 27: "Кот д'Ивуар", 28: 'Гамбия', 29: 'Сербия',
                                 30: 'Йемен', 31: 'Южная Африка', 32: 'Румыния', 33: 'Колумбия', 34: 'Эстония',
                                 36: 'Канада', 37: 'Марокко', 38: 'Гана', 39: 'Аргентина', 40: 'Узбекистан',
                                 41: 'Камерун', 42: 'Чад', 43: 'Германия', 44: 'Литва', 45: 'Хорватия', 46: 'Швеция',
                                 47: 'Ирак', 48: 'Нидерланды', 49: 'Латвия', 50: 'Австрия', 51: 'Беларусь',
                                 52: 'Таиланд',
                                 53: 'Сауд. Аравия', 54: 'Мексика', 55: 'Тайвань', 56: 'Испания', 57: 'Иран',
                                 58: 'Алжир',
                                 60: 'Бангладеш', 61: 'Сенегал', 62: 'Турция', 63: 'Чехия', 64: 'Шри-Ланка', 65: 'Перу',
                                 66: 'Пакистан', 67: 'Новая Зеландия', 68: 'Гвинея', 69: 'Мали', 70: 'Венесуэла',
                                 72: 'Монголия', 73: 'Бразилия', 74: 'Афганистан', 75: 'Уганда', 76: 'Ангола',
                                 77: 'Кипр',
                                 78: 'Франция', 79: 'Папуа-Новая Гвинея', 80: 'Мозамбик', 81: 'Непал', 85: 'Молдова',
                                 87: 'Парагвай', 88: 'Гондурас', 89: 'Тунис', 90: 'Никарагуа', 92: 'Боливия',
                                 94: 'Гватемала', 95: 'ОАЭ', 96: 'Зимбабве', 98: 'Судан', 101: 'Сальвадор',
                                 102: 'Ливия',
                                 103: 'Ямайка', 104: 'Тринидад и Тобаго', 105: 'Эквадор',
                                 109: 'Доминиканская Республика',
                                 110: 'Сирия', 114: 'Мавритания', 115: 'Сьерра-Леоне', 116: 'Иордания',
                                 117: 'Португалия',
                                 120: 'Бенин', 121: 'Бруней', 123: 'Ботсвана', 126: 'Доминика', 128: 'Грузия',
                                 129: 'Греция', 131: 'Гайана', 135: 'Либерия', 142: 'Суринам', 143: 'Таджикистан',
                                 146: 'Реюньон', 148: 'Армения', 150: 'Конго', 152: 'Буркина-Фасо', 153: 'Ливан',
                                 154: 'Габон', 157: 'Маврикий', 158: 'Бутан', 159: 'Мальдивы', 161: 'Туркменистан',
                                 172: 'Дания', 179: 'Аруба', 187: 'США', 189: 'Фиджи', 195: 'Бермуды'}
    __country_name_to_id_dict = {v: k for k, v in __id_to_country_name_dict.items()}

    def __init__(self, client: SmsHubWrapper):
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
        return self.__id_to_country_name_dict[id_]

    def country_name_to_id(self, country: str) -> int:
        return self.__country_name_to_id_dict[country]
