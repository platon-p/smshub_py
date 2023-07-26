from .wrapper import SmsHubWrapper
from .exceptions import NoCountryException

__countries_id = {0: 'RU', 1: 'UA', 2: 'KZ', 3: 'CN', 4: 'PH', 5: 'MM', 6: 'ID', 7: 'MY', 8: 'KE', 9: 'TZ', 10: 'VN',
                  11: 'KP', 12: 'US', 13: 'IL', 14: 'HK', 15: 'PL', 16: 'GB', 18: 'CG', 19: 'NG', 21: 'EG', 22: 'IN',
                  23: 'IE', 24: 'KH', 25: 'LA', 26: 'HT', 27: 'CI', 28: 'GM', 29: 'RS', 30: 'YE', 31: 'ZA', 32: 'RO',
                  33: 'CO', 34: 'EE', 36: 'CA', 37: 'MA', 38: 'GH', 39: 'AR', 40: 'UZ', 41: 'CM', 42: 'TD', 43: 'DE',
                  44: 'LT', 45: 'HR', 46: 'SE', 47: 'IQ', 48: 'NL', 49: 'LV', 50: 'AT', 51: 'BY', 52: 'TH', 53: 'SA',
                  54: 'MX', 55: 'TW', 56: 'ES', 57: 'IR', 58: 'DZ', 60: 'BD', 61: 'SN', 62: 'TR', 63: 'CZ', 64: 'LK',
                  65: 'PE', 66: 'PK', 67: 'NZ', 68: 'GN', 69: 'ML', 70: 'VE', 72: 'MN', 73: 'BR', 74: 'AF', 75: 'UG',
                  76: 'AO', 77: 'CY', 78: 'FR', 79: 'PG', 80: 'MZ', 81: 'NP', 85: 'MD', 87: 'PY', 88: 'HN', 89: 'TN',
                  90: 'NI', 92: 'BO', 94: 'GT', 95: 'ОАЭ', 96: 'ZW', 98: 'SD', 101: 'SV', 102: 'LY', 103: 'JM',
                  104: 'TT', 105: 'EC', 109: 'DO', 110: 'SY', 114: 'MR', 115: 'SL', 116: 'JO', 117: 'PT', 120: 'BJ',
                  121: 'BN', 123: 'BW', 126: 'DM', 128: 'GE', 129: 'GR', 131: 'GY', 135: 'LR', 142: 'SR', 143: 'TJ',
                  146: 'RE', 148: 'AM', 150: 'CG', 152: 'BF', 153: 'LB', 154: 'GA', 157: 'MU', 158: 'BT', 159: 'MV',
                  161: 'TM', 172: 'DK', 179: 'AW', 187: 'США', 189: 'FJ', 195: 'BM'}

__id_countries = {v: k for k, v in __countries_id.items()}


def find_min_prices(client: SmsHubWrapper, service: str, count: int = None) -> list[tuple[float, str, int]]:
    """
    :param client: SmsHubClient wrapper object
    :param service: Service code
    :param count: Results count (optional)
    :return: List of tuples (price, country ID, numbers quantity)
    """
    ans = []
    for country, val in client.get_prices(service).items():
        if service in val.keys():
            ans.extend([(float(i[0]), country, i[1]) for i in val[service].items()])
    return sorted(ans, key=lambda x: x[0])[:count]


def id_to_country(id_: int) -> str:
    """
    :param id_: Country ID on SmsHub
    :return: ISO 3166-1 alpha-2 country code
    """
    try:
        return __id_countries[id_]
    except KeyError:
        raise NoCountryException(str(id_))


def country_to_id(alpha_2: str) -> int:
    """
    :param alpha_2: ISO 3166-1 alpha-2 country code
    :return: Country ID on SmsHub
    """
    try:
        return __countries_id[alpha_2]
    except KeyError:
        raise NoCountryException(alpha_2)
