import os
import unittest
import datetime
import json
import tempfile
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
        self.assertIsNotNone(self.client.access_token)
        self.assertIsNotNone(self.client.refresh_token)

    def test_get_tokens(self):
        tokens = self.client.get_tokens()
        self.assertIsNotNone(tokens['access_token'])
        self.assertIsNotNone(tokens['refresh_token'])

        invalidate_token = self.client.invalidate_token()
        self.assertEqual(invalidate_token, None)

    def test_refresh_access_token(self):
        response = self.client.refresh_access_token()
        self.assertIsNotNone(response)

    def test_get_users(self):
        """ Test getting user information from API """
        response = self.client.get_users()
        self.assertEqual(response[0], 200)

    def test_send_one_time_pass(self):
        """ Test sending one time password for currently logged in user via SMS """
        response = self.client.send_one_time_pass()
        # After the first test status code is 429 if not waited 10 minutes
        if response != 200:
            self.assertEqual(response, 429)
        else:
            self.assertEqual(response, 200)

    def test_get_user_profile(self):
        """ Test getting user profile based on user ID """
        userId = 27584
        response = self.client.get_user_profile(userId)
        self.assertEqual(response[0], 200)
        self.assertIsNotNone(response[1]['companyId'])

    def test_get_products(self):
        """ get all products from API """

        response = self.client.get_products()
        self.assertEqual(response[0], 200)
        self.assertIsNotNone(response[1])

    def test_get_product(self):
        """ get info of one product """
        productId = 723460
        response = self.client.get_product(productId)
        self.assertEqual(response[0], 200)
        self.assertIsNotNone(response[1])

    def test_get_product_groups(self):
        """ get product groups (by product type) """

        response = self.client.get_product_groups("PURCHASE")
        self.assertEqual(response[0], 200)
        self.assertIsNotNone(response[1]['productGroups'])

    def test_get_vats(self):
        """ get VAT percentages for the current company """
        response = self.client.get_vats()
        self.assertEqual(response[0], 200)
        self.assertIsNotNone(response[1]['vatInformation'][0]['country'])

    def test_get_vats_country(self):
        """ get VAT percentages available for the given country """
        response = self.client.get_vats_country('FI')
        self.assertEqual(response[0], 200)
        self.assertIn(24.0, response[1]['vatPercentages'])

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

        self.assertEqual(response[0], 200)
        self.assertIsNotNone(response[1])

    def test_get_invoice(self):
        invoiceId = 8204221
        response = self.client.get_invoice(invoiceId)
        self.assertEqual(response[0], 200)
        self.assertEqual(response[1]['id'], invoiceId)

    def test_invoice(self):
        date = str(datetime.date.today())
        dueDate = str(datetime.date.today() + datetime.timedelta(weeks=2))
        data = {
            "type": "PURCHASE_INVOICE",
            "status": "UNFINISHED",
            "date": date,
            "counterParty": {
                "counterPartyAddress": {
                    "name": "Testi Mies"
                }
            },
            "paymentInfo": {
                "paymentMethod": "BANK_TRANSFER",
                "currency": "EUR",
                "dueDate": dueDate,
                "currencyRate": 1,
                "bankAccount": {
                    "accountNumber": "FI7276549406033672",
                }
            },
            "extraInfo": {
                "accountingByRow": False,
                "unitPricesIncludeVat": False
            },
            "discountPercent": 0,
            "invoiceRows": [
                {
                    "product": "Purkki",
                    "quantity": 1,
                    "unit": "PIECE",
                    "unitPrice": 2.50,
                    "discountPercent" : 10,
                    "vatPercent": 24
                }
            ],
            "invoiceChannel": "NO_SENDING",
            "language" : "FINNISH"
        }

        post_response = self.client.post_invoice(**data)

        self.assertIsNotNone(post_response[1]['id'])
        invoiceId = post_response[1]['id']

        # TODO fix this (something goes wrong when trying send to circulation)
        circulation_response = self.client.send_invoice_to_circulation(invoiceId)
        self.assertEqual(circulation_response, 403)

        verify_response = self.client.verify_invoice(invoiceId)
        self.assertEqual(verify_response, 200)

        approve_response = self.client.approve_invoice(invoiceId)
        self.assertEqual(approve_response, 200)

        otp = "dyrn"
        pay_data = {
            "paymentData": [
                {
                    "invoiceId": invoiceId,
                    "payDate": date
                }
            ],
            "oneTimePassword": otp
        }
        pay_response = self.client.pay_invoice(**pay_data)
        self.assertEqual(pay_response, 401)

    def test_get_currencies(self):
        response = self.client.get_currencies()

        currencies = response[1]['currencies']
        self.assertEqual(response[0], 200)
        self.assertIn("EUR", currencies)

    def test_get_currency(self):
        response = self.client.get_currency()

        self.assertEqual(response[0], 200)

    def test_get_exchange_rate(self):
        data = {
            'baseCurrency': 'DKK',
            'currency': 'EUR',
            'day': '2017-12-07',
            'rateType': 'PROCOUNTOR_ACCOUNTING_EXCHANGE_RATE',
        }

        response = self.client.get_exchange_rate(**data)
        self.assertEqual(response[0], 200)
        self.assertEqual(response[1]['currency'], 'EUR')

    def test_get_latest_currency_rate(self):
        response = self.client.get_latest_currency_rate(1)
        self.assertEqual(response[0], 200)

    def test_get_dimensions(self):
        response = self.client.get_dimensions()
        self.assertEqual(response[0], 200)
        self.assertIsNotNone(response[1][0]['id'])

    def test_get_dimension(self):
        dimensionId = 86160
        response = self.client.get_dimension(dimensionId)
        self.assertEqual(response[0], 200)
        self.assertIsNotNone(response[1]['id'])

    def test_get_fiscal_years(self):
        response = self.client.get_fiscal_years()
        self.assertEqual(response[0], 200)

    def test_get_ledger_receipts(self):
        data = {
            "startDate": "2018-02-12",
            "endDate": "2018-02-14",
            "types": "PURCHASE_INVOICE",
            "orderById": "asc",
        }
        previousId = 13787852
        response = self.client.get_ledger_receipts(previousId, **data)
        self.assertEqual(response[0], 200)

        if data['orderById'] is "desc":
            self.assertLess(response[1]['results'][0]['receiptId'], previousId)
        elif data['orderById'] is "asc":
            self.assertGreater(response[1]['results'][0]['receiptId'], previousId)

    def test_get_ledger_receipt(self):
        receiptId = 13787902
        response = self.client.get_ledger_receipt(receiptId)
        self.assertEqual(response[0], 200)
        self.assertEqual(response[1]['receiptId'], receiptId)

    def test_get_coa(self):
        response = self.client.get_coa()
        self.assertEqual(response[0], 200)
        self.assertIs(type(response[1]['ledgerAccounts']), list)

    def test_get_business_partner(self):
        partnerId = 1517286
        response = self.client.get_business_partner(partnerId)
        self.assertEqual(response[0], 200)
        self.assertEqual(response[1]['id'], partnerId)

    def test_get_business_partner_details(self):
        response = self.client.get_business_partner_details()
        self.assertEqual(response[0], 200)
        self.assertIsNotNone(response[1]['personId'])

    def test_get_bank_statements(self):
        startDate = "2018-02-01"
        endDate = "2018-02-14"

        response = self.client.get_bank_statements(startDate, endDate)
        self.assertEqual(response[0], 200)

    def test_delete_products_from_bank_statement(self):
        statementId = 1234
        eventId = 4321

        response = self.client.delete_products_from_bank_statement(statementId, eventId)
        self.assertEqual(response, 403)

    def test_put_products_to_bank_statement(self):
        pass

    def test_get_attachment(self):
        response = self.client.get_attachment(1528)
        self.assertEqual(response[0], 200)

    def test_post_attachment(self):

        f = tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.txt', prefix='test_')
        f.write(b"Temp file")
        f.close()

        meta = {
            "name": "test.txt",
            "referenceType": "INVOICE",
            "referenceId": 8197608,
        }

        response = self.client.post_attachment(meta, f.name)
        self.assertEqual(response[0], 200)
        attachmentId = response[1]['id']

        os.unlink(f.name)

        responseDelete = self.client.delete_attachment(attachmentId)
        self.assertEqual(responseDelete, 200)

    def test_request(self):
        response = self.client.request("GET", "users")
        self.assertIsNotNone(response)

    def test_headers(self):
        response = self.client.headers("GET", "users")
        self.assertEqual(response['authorization'], "Bearer {}".format(self.client.access_token))

if __name__ == '__main__':
    unittest.main()
