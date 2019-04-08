import unittest
from tests import TestClient


class TestClientCOA(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientCOA, self).__init__(*args, **kwargs)

    def test_001_get_business_patners(self):
        response = self.client.get_coa()
        self.assertEqual(response['status'], 200)
        self.assertIsNotNone(response['content'])
        self.assertIs(type(response['content']['ledgerAccounts']), list)

if __name__ == '__main__':
    unittest.main()