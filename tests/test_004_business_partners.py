import unittest
import os
from tests import TestClient


class TestClientBusinessPartners(TestClient):

    # For testing get business partner
    test_partner_id = None

    def __init__(self, *args, **kwargs):
        super(TestClientBusinessPartners, self).__init__(*args, **kwargs)
        self.__class__.test_partner_id = os.getenv('PROCOUNTOR_BUSINESS_PARTNERS_PARTNER_ID', None)

    def test_001_get_business_patners(self):
        response = self.client.get_business_partners()
        self.assertEqual(response['status'], 200)
        self.assertIsNotNone(response['content'])

    def test_002_get_business_partner(self):
        if self.__class__.test_partner_id:
            response = self.client.get_business_partner(self.__class__.test_partner_id)
            self.assertEqual(response['status'], 200)
            self.assertEqual(response['content']['id'], int(self.__class__.test_partner_id))

    def test_003_update_business_partner(self):
        # TODO: Create tests for update business partner
        pass

    def test_004_get_business_partner_details(self):
        response = self.client.get_business_partner_details()
        self.assertEqual(response['status'], 200)
        self.assertIsNotNone(response['content']['personId']) 

if __name__ == '__main__':
    unittest.main()