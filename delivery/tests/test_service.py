from decimal import Decimal
from unittest.mock import patch, call

from django.test import TestCase

from delivery import service
from delivery.fake import DeliveryFaker


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

    def test_calculate_cost(self):
        result = service.calculate_cost(Decimal('1'), Decimal('1'), Decimal('1'))
        self.assertEqual(Decimal('0.51'), result)

    @patch("delivery.service.calculate_cost")
    @patch("delivery.exchangerate.ExchangeRate.get_by_code")
    @patch("delivery.exchangerate.ExchangeRate.fetch")
    def test_update_pkg_delivery_cost(self, fetch, get_by_code, calculate_cost):
        pkg = self.faker.package(self.client.session.session_key)
        calculate_cost.return_value = Decimal('1')
        get_by_code.return_value = Decimal('1')
        service.update_pkg_delivery_cost(pkg)

    @patch("delivery.service.update_pkg_delivery_cost")
    def test_update_delivery_costs(self, update_pkg_delivery_cost):
        pkg1 = self.faker.package(self.client.session.session_key)
        pkg2 = self.faker.package(self.client.session.session_key,
                                  delivery_cost=Decimal('100'))
        service.update_delivery_costs()
        calls = [call(pkg1, save=False)]
        update_pkg_delivery_cost.assert_has_calls(calls)

    @patch("delivery.service.update_pkg_delivery_cost")
    def test_register_package(self, update_pkg_delivery_cost):
        service.register_package(self.create_package_post,
                                 self.client.session.session_key)
        update_pkg_delivery_cost.assert_called()
