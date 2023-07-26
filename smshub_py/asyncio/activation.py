from typing import Optional
import time
import asyncio

from .wrapper import AsyncSmsHubWrapper
from ..status import *
from ..exceptions import IncorrectResponse, TimeoutException


class AsyncSmsActivation:
    def __init__(self, api_key: str, service: str, operator: Optional[str] = '', country: Optional[int] = '',
                 proxy: Optional[str] = None):
        """
        Provides convenient asynchronous operations with activation on SmsHub
        :param api_key: API key for SmsHub
        :param service: Service code
        :param operator: Operator name
        :param country: Country ID
        :param proxy: protocol://ip:port OR protocol://user:password@ip:port
        """
        self.wrapper = AsyncSmsHubWrapper(key=api_key, proxy=proxy)
        self.service = service
        self.operator = operator
        self.country_code = country
        self.code = None
        self.status = None
        self.activation_id, self.phone = None, None

    async def init_(self):
        self.activation_id, self.phone = await self.wrapper.get_number(self.service, self.operator, self.country_code)
        await self.update_status()

    async def __aenter__(self):
        await self.init_()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return

    async def sms_sent(self):
        """
        Say SmsHub that your SMS was sent
        """
        r = await self.wrapper.set_status(self.activation_id, status=SMS_SENT)
        if r != ACCESS_READY:
            raise IncorrectResponse(ACCESS_READY, r)

    async def cancel(self):
        """
        Cancel activation
        """
        r = await self.wrapper.set_status(self.activation_id, status=CANCEL)
        if r != ACCESS_CANCEL:
            raise IncorrectResponse(ACCESS_CANCEL, r)

    async def retry(self):
        """
        Ask for receiving another SMS
        """
        r = await self.wrapper.set_status(self.activation_id, status=SMS_RETRY)
        if r != ACCESS_RETRY_GET:
            raise IncorrectResponse(ACCESS_RETRY_GET, r)

    async def finish(self):
        """
        Finish activation
        """
        r = await self.wrapper.set_status(self.activation_id, status=SMS_ACCEPTED)
        if r != ACCESS_ACTIVATION:
            raise IncorrectResponse(ACCESS_ACTIVATION, r)

    async def update_status(self):
        """
        Get current activation status from SmsHub
        """
        s = await self.wrapper.get_status(self.activation_id)
        self.status = s[0]
        if s[0] == STATUS_OK or s[0] == STATUS_WAIT_RETRY:
            self.code = s[1]

    async def wait_for_sms(self, interval: int = 1, timeout: int = 120):
        """
        Asynchronous wait until new SMS got on SmsHub
        :param interval: Interval of requests (Seconds)
        :param timeout: Timeout (Seconds). When time is off :class:`TimeoutException` will be raised
        """
        try:
            async with asyncio.timeout(timeout):
                while True:
                    last_time = time.time()
                    await self.update_status()
                    if self.status == STATUS_OK:
                        break
                    await asyncio.sleep(
                        abs(interval - (time.time() - last_time) * (interval > (time.time() - last_time))))
        except asyncio.TimeoutError:
            raise TimeoutException
