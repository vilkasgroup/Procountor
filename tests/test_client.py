import os
import unittest
import datetime
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

    def test_init(self):
        """ Testing that client has required params """
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(self.client.username)
        self.assertIsNotNone(self.client.password)
        self.assertIsNotNone(self.client.company_id)
        self.assertIsNotNone(self.client.client_id)
        self.assertIsNotNone(self.client.client_secret)
        self.assertIsNotNone(self.client.redirect_uri)

    def test_refresh_access_token(self):
        response = self.client.refresh_access_token(self.client.refresh_token)
        self.assertIsNotNone(response)

    def test_get_users(self):
        """ Test getting user information from API """
        response = self.client.get_users()
        self.assertIsNotNone(response)
        print(response)

    # def test_send_one_time_pass(self):
    #     """ Test sending one time password for currently logged in user via SMS """
    #     response = self.client.send_one_time_pass()
    #     self.assertIsNotNone(response)

    # def test_get_user_profile(self):
    #     """ Test getting user profile based on user ID """
    #     userId = 14438
    #     response = self.client.get_user_profile(userId)
    #     self.assertIsNotNone(response)

    def test_get_products(self):
        """ get all products from API """

        response_all = self.client.get_products()
        self.assertIsNotNone(response_all)

        """ get products with limit """

        data = {
            "previousId": "",
            "limit": "2",
            "group": "",
            "type": "PURCHASE"
        }

        response_limit = self.client.get_products(**data)
        self.assertIsNotNone(response_limit)

    def test_get_product(self):
        """ get info of one product """
        productId = 723460
        response = self.client.get_product(productId)

        self.assertIsNotNone(response)

    def test_get_product_groups(self):
        """ get product groups (by product type) """

        data = {
            "productType": "PURCHASE",
        }

        response = self.client.get_product_groups("PURCHASE")
        self.assertIsNotNone(response)

    def test_get_vats(self):
        """ get VAT percentages for the current company """
        response = self.client.get_vats()

        self.assertIsNotNone(response)

    def test_get_vats_country(self):
        """ get VAT percentages available for the given country """
        response = self.client.get_vats_country('FI')

        self.assertIsNotNone(response)

    def test_get_invoices(self):
        # data = {
        #     "status": "",
        #     "startDate": "",
        #     "endDate": "",
        #     "types":"TRAVEL_INVOICE",
        #     #"orderById": "asc",
        #     "orderByDate": ""
        # }

        response = self.client.get_invoices(0)

        self.assertIsNotNone(response)

    def test_get_invoice(self):
        response = self.client.get_invoice(8203037)

        self.assertIsNotNone(response)
        #print(response)

    # def test_post_invoice(self):
    #     date = str(datetime.date.today())
    #     dueDate = str(datetime.date.today() + datetime.timedelta(weeks=2))
    #     data = {
    #         "type": "TRAVEL_INVOICE",
    #         "status": "UNFINISHED",
    #         "date": date,
    #         "counterParty": {
    #             "counterPartyAddress": {
    #                 "name": "Testi Mies"
    #             }
    #         },
    #         "paymentInfo": {
    #             "paymentMethod": "BANK_TRANSFER",
    #             "currency": "EUR",
    #             "dueDate": dueDate,
    #             "currencyRate": 1,
    #             "bankAccount": {
    #                 "accountNumber": "FI7276549406033672",
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
    #
    #     self.assertIsNotNone(response)

    def test_approve_invoice(self):
        pass

    def test_send_invoice_to_circulation(self):
        invoiceId = 8203716
        response = self.client.send_invoice_to_circulation(invoiceId)
        self.assertIsNotNone(response)
        print(response)


    def test_verify_invoice(self):
        pass

    def test_pay_invoice(self):
        pass

    def test_get_currencies(self):
        response = self.client.get_currencies()

        self.assertIsNotNone(response)

    def test_get_exchange_rate(self):
        data = {
            'baseCurrency': 'DKK',
            'currency': 'EUR',
            'day': '2017-12-07',
            'rateType': 'PROCOUNTOR_ACCOUNTING_EXCHANGE_RATE',
        }

        response = self.client.get_exchange_rate(**data)

        self.assertIsNotNone(response)

    def test_get_latest_currency_rate(self):
        response = self.client.get_latest_currency_rate(1)

        self.assertIsNotNone(response)

    def test_get_dimensions(self):
        response = self.client.get_dimensions()

        self.assertIsNotNone(response)

    def test_get_dimension(self):
        dimensionId = 86160
        response = self.client.get_dimension(dimensionId)

        self.assertIsNotNone(response)

    def test_get_fiscal_years(self):
        response = self.client.get_fiscal_years()
        self.assertIsNotNone(response)

    def test_get_ledger_receipts(self):
        response = self.client.get_ledger_receipts(0)
        self.assertIsNotNone(response)

    def test_get_ledger_receipt(self):
        response = self.client.get_ledger_receipt(13786856)
        self.assertIsNotNone(response)

    def test_update_ledger_receipt(self):
        pass

    def test_get_coa(self):
        response = self.client.get_coa()
        self.assertIsNotNone(response)

    def test_get_business_partner(self):
        pass

    def test_get_bank_statements(self):
        # startDate = "2017-12-01"
        # endDate = "2018-01-23"
        #
        # response = self.client.get_bank_statements(startDate, endDate)
        pass

    def test_delete_products_from_bank_statement(self):
        # statementId = 1234
        # eventId = 4321
        #
        # response = self.client.delete_products_from_bank_statement(statementId, eventId)
        pass

    def test_put_products_to_bank_statement(self):
        pass

    def test_get_attachment(self):
        response = self.client.get_attachment(1528)

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
    #     self.assertIsNotNone(response)
    #     attachmentId = response['id']
    #     responseDelete = self.client.delete_attachment(attachmentId)
    #     self.assertIsNotNone(responseDelete)

if __name__ == '__main__':
    unittest.main()
