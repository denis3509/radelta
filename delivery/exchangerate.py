from datetime import timedelta
from decimal import Decimal

import requests

from core import caching
from core.logging import get_logger
from delivery import exceptions as exc


class ExchangeRatesError(exc.DeliveryError):
    pass


class LoadError(ExchangeRatesError):
    pass


class DataError(ExchangeRatesError):
    pass


def next_day_expires():
    """create expiration time at next day at 00:00:00 """
    time_delta = timedelta(days=1)
    dt_args = {'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0}
    return caching.calc_expiration_date(time_delta, dt_args)


logger = get_logger()


class ExchangeRate:
    def __init__(self, currency: str):
        self.rates = None
        self.currency = currency
        self.rates = self.fetch()

    @caching.memoize_with_expiration(next_day_expires)
    def fetch(self):
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        if response.status_code == 200:
            data = response.json()
            if not data:
                raise DataError("Empty response")
            return data
        else:
            raise LoadError(f"Unable to load rates: resource respond with status {response.status_code}")

    def get_by_code(self, code: str) -> Decimal:
        try:
            logger.info(self.rates['Valute'][code])
            return Decimal(str(self.rates['Valute'][code]['Value']))
        except (KeyError, TypeError) as e:
            raise DataError("Invalid rates format") from e
