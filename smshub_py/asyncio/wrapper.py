from typing import Optional
import aiohttp

from .. import exceptions
from ..status import STATUS_WAIT_RETRY, STATUS_OK


class AsyncSmsHubWrapper:
    base_url = 'https://www.smshub.org/stubs/handler_api.php'

    def __init__(self, key: str, proxy: Optional[str] = None):
        """
        Asynchronous wrapper for SmsHub API
        :param key: API Key for SmsHub
        :param proxy: protocol://ip:port OR protocol://user:password@ip:port
        """
        self.key = key
        self.proxy = proxy

    def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        return

    @staticmethod
    async def _process_status(r: aiohttp.ClientResponse):
        if await r.text() == 'BAD_KEY':
            raise exceptions.BadApiKey
        elif await r.text() == 'ERROR_SQL':
            raise exceptions.SqlError
        elif await r.text() == 'NO_NUMBERS':
            raise exceptions.NoNumbers
        elif await r.text() == 'NO_BALANCE':
            raise exceptions.NoBalance
        elif await r.text() == 'WRONG_SERVICE':
            raise exceptions.WrongService
        elif await r.text() == 'NO_ACTIVATION':
            raise exceptions.NoActivation

    async def get_balance(self) -> float:
        """
        Get balance value
        :return: Balance value
        """
        async with aiohttp.request('GET', self.base_url, params={'api_key': self.key, 'action': 'getBalance'},
                                   proxy=self.proxy) as req:
            await self._process_status(req)
            return float((await req.text()).replace('ACCESS_BALANCE:', ''))

    async def get_number_status(self, country: Optional[int] = '', operator: Optional[str] = '') -> dict[str, int]:
        """
        Request for quantity available numbers
        :param country: Country ID
        :param operator: Operator code
        :return: `Dict` service - numbers quantity
        """
        async with aiohttp.request('GET', self.base_url, params={
            'api_key': self.key,
            'action': 'getNumbersStatus',
            'country': country,
            'operator': operator
        }, proxy=self.proxy) as req:
            await self._process_status(req)
            return await req.json()

    async def get_number(self, service: str, operator: Optional[str] = '', country: Optional[int] = '') -> (
            int, int):
        """
        Request for using number
        :param service: Service code
        :param operator: Operator code
        :param country: Country ID
        :return: Activation ID and phone number
        """
        async with aiohttp.request('GET', self.base_url, params={
            'api_key': self.key,
            'action': 'getNumber',
            'service': service,
            'operator': operator,
            'country': country
        }, proxy=self.proxy) as req:
            await self._process_status(req)
            return tuple(map(int, (await req.text()).split(':')[1:]))

    async def set_status(self, id_: int, status: int) -> str:
        """
        Set current status of activation
        :param id_: Activation ID
        :param status: Status ID
        :return: Status message
        """
        async with aiohttp.request('GET', self.base_url, params={
            'api_key': self.key,
            'action': 'setStatus',
            'id': id_,
            'status': status
        }, proxy=self.proxy) as req:
            await self._process_status(req)
            return await req.text()

    async def get_status(self, id_: int) -> (int, int):
        """
        Get status of activation
        :param id_: Activation ID
        :return: Status message, with code if possible
        """
        async with aiohttp.request('GET', self.base_url, params={
            'api_key': self.key,
            'action': 'getStatus',
            'id': id_
        }, proxy=self.proxy) as req:
            await self._process_status(req)
            if (await req.text()).startswith(STATUS_WAIT_RETRY) or (await req.text()).startswith(STATUS_OK):
                status, code = (await req.text()).split(':')
                return status, code
            return await req.text(), 0

    async def get_prices(self, service: Optional[str] = '', country: Optional[int] = '') -> \
            dict[str, dict[str, dict[str, int]]]:
        """
        Get all prices
        :param service: Service code
        :param country: Country ID
        :return: `Dict` with prices
        """
        async with aiohttp.request('GET', self.base_url, params={
            'api_key': self.key,
            'action': 'getPrices',
            'service': service,
            'country': country,
        }, proxy=self.proxy) as req:
            await self._process_status(req)
            return await req.json()
