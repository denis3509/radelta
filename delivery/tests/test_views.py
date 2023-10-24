from django.test import TestCase

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

    def test_create_package(self):
        response = self.client.post('/api/delivery/package/', self.create_package_post)
        self.assertEqual(response.status_code, 201)

    def test_get_package(self):
        pkg = self.faker.package(session_key=self.client.session.session_key)
        response = self.client.get(f'/api/delivery/package/{pkg.id}/')
        self.assertEqual(response.status_code, 200)

    def test_list_package_types(self):
        response = self.client.get('/api/delivery/package-type-list/')
        self.assertEqual(response.status_code, 200)

    def test_list_package(self):
        response = self.client.get('/api/delivery/package-list/', params={
            'types': '1,2'
        })

        self.assertEqual(response.status_code, 200)
