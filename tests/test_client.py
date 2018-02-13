import os
import unittest
import datetime
import json
from time import sleep
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

    # def test_send_one_time_pass(self):
    #     """ Test sending one time password for currently logged in user via SMS """
    #     response = self.client.send_one_time_pass()
    #     self.assertIsNotNone(response)
    #     sleep(600)

    def test_get_user_profile(self):
        """ Test getting user profile based on user ID """
        userId = 27584
        response = self.client.get_user_profile(userId)
        self.assertIsNotNone(response)
        print(response)

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
        j = json.loads(response)
        self.assertIsNotNone(j['vatInformation'][0]['country'])

    def test_get_vats_country(self):
        """ get VAT percentages available for the given country """
        response = self.client.get_vats_country('FI')
        j = json.loads(response)
        self.assertIn(24.0, j['vatPercentages'])

    def test_get_invoices(self):
        data = {
            "status": "UNFINISHED",
            "startDate": "2018-02-10",
            "endDate": "2018-02-18",
            "types": "TRAVEL_INVOICE,PURCHASE_INVOICE",
            #"orderById": "asc",
            "orderByDate": "asc"
        }

        response = self.client.get_invoices(8203820, **data)

        self.assertIsNotNone(response)

    def test_get_invoice(self):
        invoiceId = 8204221
        response = self.client.get_invoice(invoiceId)
        j = json.loads(response)
        self.assertEqual(j['id'], invoiceId)

    # def test_invoice(self):
    #     date = str(datetime.date.today())
    #     dueDate = str(datetime.date.today() + datetime.timedelta(weeks=2))
    #     data = {
    #         "type": "PURCHASE_INVOICE",
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
    #     print("POST INVOICE")
    #     post_response = self.client.post_invoice(**data)
    #
    #     j = json.loads(post_response)
    #     self.assertIsNotNone(j['id'])
    #     invoiceId = j['id']
    #     print(invoiceId)
    #
    #
    #     print("Send to CIRCULATION")
    #     circulation_response = self.client.send_invoice_to_circulation(invoiceId)
    #     self.assertEqual(circulation_response, 200)
    #
    #     print("VERIFY")
    #     verify_response = self.client.verify_invoice(invoiceId)
    #     self.assertEqual(verify_response, 200)
    #
    #     print("APPROVE")
    #     approve_response = self.client.approve_invoice(invoiceId)
    #     self.assertEqual(approve_response, 200)

        # otp = "dyrn"
        # data = {
        #     "paymentData": [
        #         {
        #             "invoiceId": invoiceId,
        #             "payDate": date
        #         }
        #     ],
        #     "oneTimePassword": otp
        # }
        # pay_response = self.client.pay_invoice(**data)
        # self.assertIsNotNone(pay_response)

    def test_get_currencies(self):
        response = self.client.get_currencies()

        j = json.loads(response)
        currencies = j['currencies']
        self.assertIn("EUR", currencies)

    def test_get_exchange_rate(self):
        data = {
            'baseCurrency': 'DKK',
            'currency': 'EUR',
            'day': '2017-12-07',
            'rateType': 'PROCOUNTOR_ACCOUNTING_EXCHANGE_RATE',
        }

        response = self.client.get_exchange_rate(**data)
        j = json.loads(response)
        self.assertEqual(j['currency'], 'EUR')

    def test_get_latest_currency_rate(self):
        response = self.client.get_latest_currency_rate(1)

        self.assertIsNotNone(response)

    def test_get_dimensions(self):
        response = self.client.get_dimensions()
        j = json.loads(response)
        self.assertIsNotNone(j[0]['id'])

    def test_get_dimension(self):
        dimensionId = 86160
        response = self.client.get_dimension(dimensionId)
        j = json.loads(response)
        self.assertIsNotNone(j['id'])

    def test_get_fiscal_years(self):
        response = self.client.get_fiscal_years()
        self.assertIsNotNone(response)

    def test_get_ledger_receipts(self):
        data = {
            "startDate": "2018-02-12",
            "endDate": "2018-02-14",
            "types": "PURCHASE_INVOICE",
            "orderById": "asc",
        }
        previousId = 13787852
        response = self.client.get_ledger_receipts(previousId, **data)
        j = json.loads(response)
        if data['orderById'] is "desc":
            self.assertLess(j['results'][0]['receiptId'], previousId)
        elif data['orderById'] is "asc":
            self.assertGreater(j['results'][0]['receiptId'], previousId)

    def test_get_ledger_receipt(self):
        receiptId = 13787902
        response = self.client.get_ledger_receipt(receiptId)
        j = json.loads(response)
        self.assertEqual(j['receiptId'], receiptId)

    # def test_update_ledger_receipt(self):
    #     data = {
    #         "vatStatus": 1,
    #     }
    #
    #     response = self.client.update_ledger_receipt(13787902, **data)
    #     self.assertIsNotNone(response)
    #     print(response)

    def test_get_coa(self):
        response = self.client.get_coa()
        j = json.loads(response)
        self.assertIs(type(j['ledgerAccounts']), list)

    def test_get_business_partner(self):
        partnerId = 1517286
        response = self.client.get_business_partner(partnerId)
        j = json.loads(response)
        self.assertEqual(j['id'], partnerId)

    def test_get_business_partner_details(self):
        response = self.client.get_business_partner_details()
        j = json.loads(response)
        self.assertIsNotNone(j['personId'])

    def test_get_bank_statements(self):
        startDate = "2018-02-01"
        endDate = "2018-02-14"

        response = self.client.get_bank_statements(startDate, endDate)
        self.assertIsNotNone(response)

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
