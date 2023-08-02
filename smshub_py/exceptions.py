class BadApiKey(Exception):
    pass


class SqlError(Exception):
    pass


class NoBalance(Exception):
    pass


class NoNumbers(Exception):
    pass


class WrongService(Exception):
    pass


class NoActivation(Exception):
    pass


class IncorrectResponse(Exception):
    def __init__(self, needed: str, got: str):
        super().__init__(f"Invalid responce. Needed \'{needed}\' got \'{got}\'")


class TimeoutException(Exception):
    pass


# Country errors
class NoCountryException(Exception):
    pass
