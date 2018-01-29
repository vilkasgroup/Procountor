import os
import unittest
from procountor.client import Client

class TestClient(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        """ Initialize Procountor client. Requires the following environment
        variables PROCOUNTOR_USERNAME, PROCOUNTOR_PASSWORD, PROCOUNTOR_COMPANY_ID, PROCOUNTOR_CLIENT_ID, PROCOUNTOR_CLIENT_SECRET and PROCOUNTOR_REDIRECT_URI. """

        super(TestClient, self).__init__(*args, **kwargs)
        self.client = Client(
            username = os.environ['PROCOUNTOR_USERNAME'],
            password = os.environ['PROCOUNTOR_PASSWORD'],
            company_id = os.environ['PROCOUNTOR_COMPANY_ID'],
            client_id = os.environ['PROCOUNTOR_CLIENT_ID'],
            client_secret = os.environ['PROCOUNTOR_CLIENT_SECRET'],
            redirect_uri = os.environ['PROCOUNTOR_REDIRECT_URI'],
            access_token = os.environ['PROCOUNTOR_ACCESS_TOKEN'],
            refresh_token = os.environ['PROCOUNTOR_REFRESH_TOKEN'],
        )

    # def test_init(self):
    #     """ Testing that client has required params """
    #     self.assertIsNotNone(self.client)
    #     self.assertIsNotNone(self.client.username)
    #     self.assertIsNotNone(self.client.password)
    #     self.assertIsNotNone(self.client.company_id)
    #     self.assertIsNotNone(self.client.client_id)
    #     self.assertIsNotNone(self.client.client_secret)
    #     self.assertIsNotNone(self.client.redirect_uri)
    #

    def test_get_users(self):
        """ Test getting user information from API """
        response = self.client.get_users()
        print(response)
        self.assertIsNotNone(response)

    # def test_send_one_time_pass(self):
    #     """ Test sending one time password for currently logged in user via SMS """
    #     response = self.client.send_one_time_pass()
    #     print(response)
    #     self.assertIsNotNone(response)
    #
    def test_get_user_profile(self):
        """ Test getting user profile based on user ID """
        userId = 1517286
        response = self.client.get_user_profile(userId)
        print(response)
        self.assertIsNotNone(response)

    def test_get_products(self):
        """ Test getting all products from API """

        data = {
            "previousId": "",
            "limit": "",
            "group": "",
            "type": "PURCHASE"
        }

        response = self.client.get_products()
        print(response)
        self.assertIsNotNone(response)

    def test_get_product(self):
        """ Test getting info of one product """
        productId = 723460
        response = self.client.get_product(productId)
        print(response)
        self.assertIsNotNone(response)

    def test_get_product_groups(self):
        """ Test getting product groups (by product type) """

        data = {
            "productType": "PURCHASE",
        }

        response = self.client.get_product_groups("PURCHASE")
        print(response)
        self.assertIsNotNone(response)

    # def test_get_vats(self):
    #     response = self.client.get_vats()
    #     print(response)
    #     self.assertIsNotNone(response)
    #
    # def test_get_vats_country(self):
    #     data = {'countryCode':'FI'}
    #     response = self.client.get_vats_coutry('FI')
    #     print(response)
    #     self.assertIsNotNone(response)

    def test_get_invoices(self):
        data = {
            "status": "",
            "startDate": "",
            "endDate": "",
            "types":"PURCHASE_INVOICE,SALES_INVOICE",
            "orderById": "asc",
            #"orderByDate": ""
        }

        response = self.client.get_invoices(0, **data)
        print(response)
        self.assertIsNotNone(response)

    def test_get_invoice(self):
        response = self.client.get_invoice(8203037)
        print(response)
        self.assertIsNotNone(response)

    # def test_get_ledger_receipt(self):
    #     response = self.client.get_ledger_receipt(13786856)
    #     print(response)

    def test_get_attachment(self):
        response = self.client.get_attachment(1528)
        print(response)
        self.assertIsNotNone(response)

    # def test_post_attachment(self):
    #     meta = {
    #         "name": "test.txt",
    #         "referenceType": "INVOICE",
    #         "referenceId": 8197608,
    #     }
    #
    #     filename = "/Users/joonasmaliniemi/Desktop/test.txt"
    #     response = self.client.post_attachment(meta, filename)
    #     print(response)

    # def test_delete_attachment(self):
    #     attachmentId = 1486
    #     response = self.client.delete_attachment(attachmentId)
    #     print(response)

    # def test_post_invoice(self):
    #     data = {
    #         "type": "SALES_INVOICE",
    #         "status": "UNFINISHED",
    #         "date": "2017-01-22",
    #         "counterParty": {
    #             "counterPartyAddress": {
    #                 "name": "Testi Mies 2"
    #             }
    #         },
    #         "paymentInfo": {
    #             "paymentMethod": "BANK_TRANSFER",
    #             "currency": "EUR",
    #             "dueDate": "2018-01-17",
    #             "currencyRate": 1,
    #             "bankAccount": {
    #                 "accountNumber" : os.environ['PROCOUNTOR_TEST_IBAN']
    #             }
    #         },
    #         "extraInfo": {
    #             "accountingByRow": False,
    #             "unitPricesIncludeVat": False
    #         },
    #         "discountPercent": 0,
    #         "invoiceRows": [
    #             {
    #                 "product": "Purkki",
    #                 "quantity": 1,
    #                 "unit": "PIECE",
    #                 "unitPrice": 2.50,
    #                 "discountPercent" : 10,
    #                 "vatPercent": 24
    #             }
    #         ],
    #         "invoiceChannel": "NO_SENDING",
    #         "language" : "FINNISH"
    #     }
    #
    #     response = self.client.post_invoice(**data)
    #     print(response)
    #     self.assertIsNotNone(response)

    # def test_get_currencies(self):
    #     response = self.client.get_currencies()
    #     print(response)
    #     self.assertIsNotNone(response)
    #
    # def test_get_exchange_rate(self):
    #     data = {
    #         'baseCurrency': 'DKK',
    #         'currency': 'EUR',
    #         'day': '2017-12-07',
    #         'rateType': 'PROCOUNTOR_ACCOUNTING_EXCHANGE_RATE',
    #     }
    #
    #     response = self.client.get_exchange_rate(**data)
    #     print(response)
    #     self.assertIsNotNone(response)
    #
    # def test_get_latest_currency_rate(self):
    #     response = self.client.get_latest_currency_rate(1)
    #     print(response)
    #     self.assertIsNotNone(response)
    #
    # def test_get_dimensions(self):
    #     response = self.client.get_dimensions()
    #     print(response)
    #     self.assertIsNotNone(response)
    #
    # def test_get_dimension(self):
    #     dimensionId = 86160
    #     response = self.client.get_dimension(dimensionId)
    #     print(response)
    #     self.assertIsNotNone(response)

    def test_get_bank_statements(self):
        startDate = "2017-12-01"
        endDate = "2018-01-23"

        response = self.client.get_bank_statements(startDate, endDate)
        print(response)

    def test_delete_products_from_bank_statement(self):
        statementId = 1234
        eventId = 4321

        response = self.client.delete_products_from_bank_statement(statementId, eventId)
        print(response)

if __name__ == '__main__':
    unittest.main()
