from datetime import timedelta

from django.test import TestCase

from core import caching


def dummy_decorator(*args, **kwargs):
    print("dummy decorator called")

    def wrapper(fn):
        def wrapped(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapped

    return wrapper


class TestCache(TestCase):
    def test_calc_expiration_date(self):
        time_delta = timedelta(days=1)
        dt_args = {'hour': 1, 'minute': 1, 'second': 1, 'microsecond': 1}
        dt = caching.calc_expiration_date(time_delta, dt_args)
        self.assertEqual(dt.hour, 1)
        self.assertEqual(dt.minute, 1)
        self.assertEqual(dt.second, 1)
        self.assertEqual(dt.microsecond, 1)

    def test_memoize(self):
        pass
