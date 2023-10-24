from django.test import TestCase

from delivery import serializers as srlzs
from delivery.fake import DeliveryFaker


class TestService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.faker = DeliveryFaker()
        super().setUpClass()

    def test_create_package_ser(self):
        data = {
            "name": "package 1",
            "cost": 20,
            "type": 1,
            "weight": 10
        }
        ser = srlzs.CreatePackage(data=data)
        ser.is_valid(raise_exception=True)
        session = self.client.session
        session.save()
        ser.save(session_id=session.session_key)
