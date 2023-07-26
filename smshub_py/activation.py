from typing import Optional
import time

from .wrapper import SmsHubWrapper
from .status import *
from .exceptions import IncorrectResponse, TimeoutException


class SmsActivation:
    def __init__(self, api_key: str, service: str, operator: Optional[str] = None, country: Optional[int] = None):
        """
        Provides convenient operations with activation on SmsHub
        :param api_key: API key for SmsHub
        :param service: Service code
        :param operator: Operator name
        :param country: Country ID
        """
        self.wrapper = SmsHubWrapper(key=api_key)
        self.service = service
        self.operator = operator
        self.country_code = country
        self.activation_id, self.phone = self.wrapper.get_number(service, operator, country)
        self.code = None
        self.status = None
        self.update_status()

    def sms_sent(self):
        """
        Say SmsHub that your SMS was sent
        """
        r = self.wrapper.set_status(self.activation_id, status=SMS_SENT)
        if r != ACCESS_READY:
            raise IncorrectResponse(ACCESS_READY, r)

    def cancel(self):
        """
        Cancel activation
        """
        r = self.wrapper.set_status(self.activation_id, status=CANCEL)
        if r != ACCESS_CANCEL:
            raise IncorrectResponse(ACCESS_CANCEL, r)

    def retry(self):
        """
        Ask for receiving another SMS
        """
        r = self.wrapper.set_status(self.activation_id, status=SMS_RETRY)
        if r != ACCESS_RETRY_GET:
            raise IncorrectResponse(ACCESS_RETRY_GET, r)

    def finish(self):
        """
        Finish activation
        """
        r = self.wrapper.set_status(self.activation_id, status=SMS_ACCEPTED)
        if r != ACCESS_ACTIVATION:
            raise IncorrectResponse(ACCESS_ACTIVATION, r)

    def update_status(self):
        """
        Get current activation status from SmsHub
        """
        s = self.wrapper.get_status(self.activation_id)
        self.status = s[0]
        if s[0] == STATUS_OK or s[0] == STATUS_WAIT_RETRY:
            self.code = s[1]

    def wait_for_sms(self, interval: int = 1, timeout: int = 120):
        """
        Wait until new SMS got on SmsHub
        :param interval: Interval of requests (Seconds)
        :param timeout: Timeout (Seconds). When time is off :class:`TimeoutException` will be raised
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            last_time = time.time()
            self.update_status()
            if self.status == STATUS_OK:
                break
            time.sleep(abs(interval - (time.time() - last_time) * (interval > (time.time() - last_time))))
        else:
            raise TimeoutException
