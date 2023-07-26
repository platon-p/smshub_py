from typing import Optional
import httpx

from . import exceptions
from .status import STATUS_WAIT_RETRY, STATUS_OK


class SmsHubWrapper:
    base_url = 'https://smshub.org/stubs/handler_api.php'

    def __init__(self, key: str, proxy: Optional[str] = None):
        """
        Wrapper for SmsHub API
        :param key: API Key for SmsHub
        :param proxy: protocol://ip:port OR protocol://user:password@ip:port
        """
        self.key = key
        self.proxy = proxy

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
        req = httpx.get(self.base_url, params={'api_key': self.key, 'action': 'getBalance'}, proxies=self.proxy)
        self._process_status(req)
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
            'operator': operator
        }, proxies=self.proxy)
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
            'country': country
        }, proxies=self.proxy)
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
            'status': status
        }, proxies=self.proxy)
        self._process_status(req)
        return req.text

    def get_status(self, id_: int) -> (int, int):
        """
        Get status of activation
        :param id_: Activation ID
        :return: Status message, with code if possible
        """
        req = httpx.get(self.base_url, params={
            'api_key': self.key,
            'action': 'getStatus',
            'id': id_
        }, proxies=self.proxy)
        self._process_status(req)
        if req.text.startswith(STATUS_WAIT_RETRY) or req.text.startswith(STATUS_OK):
            status, code = req.text.split(':')
            return status, code
        return req.text, 0

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
            'country': country
        }, proxies=self.proxy)
        self._process_status(req)
        return req.json()
