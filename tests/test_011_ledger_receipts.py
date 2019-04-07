import unittest
from tests import TestClient

# TODO: Write tests for LedgerReceipts

class TestClientLedgerReceipts(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientLedgerReceipts, self).__init__(*args, **kwargs)

    # def test_get_ledger_receipts(self):
    #     data = {
    #         "previousId": 13787852,
    #         "startDate": "2018-02-12",
    #         "endDate": "2018-02-14",
    #         "types": "PURCHASE_INVOICE",
    #         "orderById": "asc",
    #     }

    #     response = self.client.get_ledger_receipts(**data)
    #     self.assertEqual(response['status'], 200)

    # def test_get_ledger_receipt(self):
    #     receiptId = 13787902
    #     response = self.client.get_ledger_receipt(receiptId)
    #     self.assertEqual(response['status'], 200)
    #     self.assertEqual(response['content']['receiptId'], receiptId)

if __name__ == '__main__':
    unittest.main()