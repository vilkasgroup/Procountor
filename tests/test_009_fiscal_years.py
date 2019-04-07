import unittest
from tests import TestClient


class TestClientFiscalYears(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientFiscalYears, self).__init__(*args, **kwargs)

    def test_001_get_fiscal_years(self):
        response = self.client.get_fiscal_years()
        self.assertEqual(response['status'], 200)
        self.assertIsInstance(response['content']['fiscalYears'], list)

if __name__ == '__main__':
    unittest.main()