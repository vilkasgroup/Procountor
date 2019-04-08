import os
import unittest
from tests import TestClient

# TODO: Write tests for invoice methods

class TestClientInvoices(TestClient):

    test_get_invoices_params = {
        'startDate': None,
        'endDate': None,
    }
    test_get_invoice_id = None

    def __init__(self, *args, **kwargs):
        super(TestClientInvoices, self).__init__(*args, **kwargs)
        self.__class__.test_get_invoices_params['startDate'] = os.getenv('PROCOUNTOR_INVOICE_INVOICES_PARAMS_STARTDATE', None)
        self.__class__.test_get_invoices_params['endDate'] = os.getenv('PROCOUNTOR_INVOICE_INVOICES_PARAMS_ENDDATE', None)
        self.__class__.test_get_invoice_id = os.getenv('PROCOUNTOR_INVOICE_INVOICE_ID', None)

    def test_001_get_invoices(self):
        data = self.__class__.test_get_invoices_params

        if data['startDate'] and data['endDate']:
            response = self.client.get_invoices(**data)

            self.assertEqual(response['status'], 200)
            self.assertIsInstance(response['content']['results'], list)

    def test_002_get_invoice(self):
        invoiceId = self.__class__.test_get_invoice_id
        if invoiceId:
            response = self.client.get_invoice(invoiceId)
            self.assertEqual(response['status'], 200)
            self.assertEqual(response['content']['id'], int(invoiceId))

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

    #     post_response = self.client.post_invoice(**data)

    #     self.assertIsNotNone(post_response[1]['id'])
    #     invoiceId = post_response[1]['id']

    #     # TODO fix this (something goes wrong when trying send to circulation)
    #     circulation_response = self.client.send_invoice_to_circulation(invoiceId)
    #     self.assertEqual(circulation_response, 403)

    #     verify_response = self.client.verify_invoice(invoiceId)
    #     self.assertEqual(verify_response, 200)

    #     approve_response = self.client.approve_invoice(invoiceId)
    #     self.assertEqual(approve_response, 200)

    #     otp = "dyrn"
    #     pay_data = {
    #         "paymentData": [
    #             {
    #                 "invoiceId": invoiceId,
    #                 "payDate": date
    #             }
    #         ],
    #         "oneTimePassword": otp
    #     }
    #     pay_response = self.client.pay_invoice(**pay_data)
    #     self.assertEqual(pay_response, 401)


if __name__ == '__main__':
    unittest.main()