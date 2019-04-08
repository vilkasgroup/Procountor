import unittest
from tests import TestClient


class TestClientBankAccounts(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientBankAccounts, self).__init__(*args, **kwargs)

    def test_001_get_bank_accounts(self):
        """ Test getting bank accounts from API """
        response = self.client.get_bank_accounts()
        self.assertEqual(response['status'], 200)
        self.assertIsNotNone(response['content'])

    def test_100_error_if_page_size_under_one(self):
      """
      Error because page size cannot be under 1 
      """

      response = self.client.get_bank_accounts(size=0)
      self.assertNotEqual(response['status'], 200)

if __name__ == '__main__':
    unittest.main()
