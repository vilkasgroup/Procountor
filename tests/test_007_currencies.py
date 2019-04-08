import unittest
from tests import TestClient


class TestClientCurrencies(TestClient):

    """ rate_type value
     1 - Procountor Accounting Exchange Rate
     2 - Average Rate
     3 - Buy Rate
     4 - Sell Rate
     5 - Cash Buy Rate
     6 - Cash sale exchange rate
    """
    rate_type = 1

    def __init__(self, *args, **kwargs):
        super(TestClientCurrencies, self).__init__(*args, **kwargs)

    def test_001_get_currencies(self):
        response = self.client.get_currencies()

        self.assertEqual(response['status'], 200)
        self.assertIn("EUR", response['content']['currencies'])

    def test_002_get_currency(self):
        response = self.client.get_currency()

        self.assertEqual(response['status'], 200)

    def test_003_get_exchange_rate(self):
        data = {
            'baseCurrency': 'DKK',
            'currency': 'EUR',
            'day': '2017-12-07',
            'rateType': 'PROCOUNTOR_ACCOUNTING_EXCHANGE_RATE',
        }

        response = self.client.get_exchange_rate(**data)
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['content']['currency'], 'EUR')

    def test_004_get_latest_currency_rate(self):
        response = self.client.get_latest_currency_rate(rateType=self.__class__.rate_type)
        self.assertEqual(response['status'], 200)

if __name__ == '__main__':
    unittest.main()