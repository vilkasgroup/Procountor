import unittest
import os
from tests import TestClient


class TestClientBankStatements(TestClient):
    # TODO: Test for put banstatement

    # For testing get bank statements
    test_start_date = None
    test_end_date = None

    def __init__(self, *args, **kwargs):
        super(TestClientBankStatements, self).__init__(*args, **kwargs)
        self.__class__.test_start_date = os.getenv('PROCOUNTOR_BANK_START_DATE', None)
        self.__class__.test_end_date = os.getenv('PROCOUNTOR_BANK_END_DATE', None)

    def test_001_get_bank_statements(self):
        """ Test getting bank statemens from API """
        if self.__class__.test_start_date and self.__class__.test_end_date:
            dates = {
                'startDate': self.__class__.test_start_date,
                'endDate': self.__class__.test_end_date,
            }
            response = self.client.get_bank_statements(**dates)
            self.assertEqual(response['status'], 200)
            self.assertIsNotNone(response['content'])

    def test_002_delete_products_from_bank_statement(self):
        # TODO: Create test for product bank statement
        # statementId = 1234
        # eventId = 4321

        # response = self.client.delete_products_from_bank_statement(statementId, eventId)
        # self.assertEqual(response['state'], 403)
        pass

    def test_003_products_to_bank_statement(self):
        # TODO: Create test for product to bank statement
        pass

    def test_100_error_because_dates_are_invalidate(self):
      """
      Error becausestart and end date are not dates 
      """

      response = self.client.get_bank_statements(startDate='aa', endDate='bb')
      self.assertNotEqual(response['status'], 200)

if __name__ == '__main__':
    unittest.main()
