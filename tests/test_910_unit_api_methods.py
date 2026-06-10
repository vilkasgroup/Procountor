"""Offline unit tests for :mod:`procountor.api_methods`.

Each test mocks ``Client.request`` and asserts that the high-level helper
delegates with the correct HTTP method and endpoint. This pins down the URL
construction without touching the network.
"""

import unittest
from unittest import mock

from tests.test_client import build_mock_client


class ApiMethodDelegationTests(unittest.TestCase):
    def setUp(self):
        self.client = build_mock_client()
        patcher = mock.patch.object(
            self.client, "request", return_value={"status": 200, "content": {}}
        )
        self.mock_request = patcher.start()
        self.addCleanup(patcher.stop)

    def assert_called_with_positional(self, method, endpoint):
        self.mock_request.assert_called_once()
        args, _ = self.mock_request.call_args
        self.assertEqual(args[0], method)
        self.assertEqual(args[1], endpoint)

    def test_get_attachment(self):
        self.client.get_attachment(123)
        self.assert_called_with_positional("GET", "attachments/123")

    def test_delete_attachment(self):
        self.client.delete_attachment(123)
        self.assert_called_with_positional("DELETE", "attachments/123")

    def test_get_bank_accounts_no_params(self):
        self.client.get_bank_accounts()
        self.assert_called_with_positional("GET", "bankaccounts")

    def test_get_bank_accounts_with_params(self):
        self.client.get_bank_accounts(size=5)
        self.assert_called_with_positional("GET", "bankaccounts?size=5")

    def test_get_business_partners(self):
        self.client.get_business_partners()
        self.assert_called_with_positional("GET", "businesspartners")

    def test_get_business_partner(self):
        self.client.get_business_partner(42)
        self.assert_called_with_positional("GET", "businesspartners/42")

    def test_get_coa(self):
        self.client.get_coa()
        self.assert_called_with_positional("GET", "coa")

    def test_get_company(self):
        self.client.get_company()
        self.assert_called_with_positional("GET", "company")

    def test_get_currencies(self):
        self.client.get_currencies()
        self.assert_called_with_positional("GET", "currencies")

    def test_get_fiscal_years(self):
        self.client.get_fiscal_years()
        self.assert_called_with_positional("GET", "fiscalyears")

    def test_get_invoice(self):
        self.client.get_invoice(7)
        self.assert_called_with_positional("GET", "invoices/7")

    def test_get_invoices_with_params(self):
        self.client.get_invoices(startDate="2024-01-01")
        self.assert_called_with_positional("GET", "invoices?startDate=2024-01-01")

    def test_get_payment(self):
        self.client.get_payment(99)
        self.assert_called_with_positional("GET", "payments/99")

    def test_delete_payment(self):
        self.client.delete_payment(99)
        self.assert_called_with_positional("DELETE", "payments/99")

    def test_get_session_info(self):
        self.client.get_session_info()
        self.assert_called_with_positional("GET", "sessioninfo")

    def test_get_users(self):
        self.client.get_users()
        self.assert_called_with_positional("GET", "users")

    def test_get_user_profile(self):
        self.client.get_user_profile(11)
        self.assert_called_with_positional("GET", "users/profiles/11")

    def test_send_one_time_pass(self):
        self.client.send_one_time_pass()
        self.assert_called_with_positional("GET", "users/otp")


if __name__ == "__main__":
    unittest.main()
