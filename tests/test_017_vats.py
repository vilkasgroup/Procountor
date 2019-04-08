import unittest
from tests import TestClient


class TestClientVats(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientVats, self).__init__(*args, **kwargs)

    def test_000_get_vats(self):
        """ get VAT percentages for the current company """
        response = self.client.get_vats()
        self.assertEqual(response['status'], 200)
        self.assertIsNotNone(response['content']['vatInformation'][0]['country'])

    def test_001_get_vats_country(self):
        """ get VAT percentages available for the given country """
        response = self.client.get_vats_country(countryCode='FI')
        self.assertEqual(response['status'], 200)
        self.assertIn(24.0, response['content']['vatPercentages'])



if __name__ == '__main__':
    unittest.main()
