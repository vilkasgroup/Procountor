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



if __name__ == '__main__':
    unittest.main()
