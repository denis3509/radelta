"""
(!) import delivery.exchangerate inside test functions
for proper decorator patching
"""
from unittest.mock import patch, Mock

from django.test import TestCase

from delivery.fake import DeliveryFaker
from radelta.tests.test_cache import dummy_decorator


class TestService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.faker = DeliveryFaker()
        super().setUpClass()
        cls.create_package_post = {
            "name": "package 1",
            "cost": 20,
            "type": 1,
            "weight": 10
        }

    @patch("delivery.exchangerate.ExchangeRate.fetch")
    def test_constructor(self, fetch):
        from delivery.exchangerate import ExchangeRate
        ExchangeRate('RUB')
        fetch.assert_called()

    @patch("radelta.caching.memoize_with_expiration", dummy_decorator)
    @patch("requests.get")
    def test_fetch_1(self, get):
        from delivery.exchangerate import ExchangeRate, DataError, LoadError
        """test fetch call inside constructor"""
        mock_resp = Mock()

        mock_resp.status_code = 200
        mock_resp.json.return_value = None
        get.return_value = mock_resp
        with self.assertRaises(DataError):
            ExchangeRate('RUB')

        mock_resp.status_code = 400
        with self.assertRaises(LoadError):
            ExchangeRate('RUB')

        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            'field': 'invalid_response'
        }
        ex_rate = ExchangeRate('RUB')
        with self.assertRaises(DataError):
            ex_rate.get_by_code('USD')