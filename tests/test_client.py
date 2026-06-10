import os
import unittest
from unittest import mock

from procountor.client import Client


#: Environment variables required to talk to the real Procountor API.
INTEGRATION_ENV = (
    "PROCOUNTOR_API_KEY",
    "PROCOUNTOR_CLIENT_ID",
    "PROCOUNTOR_CLIENT_SECRET",
    "PROCOUNTOR_REDIRECT_URI",
    "PROCOUNTOR_API_VERSION",
)

#: Run the live integration tests only when explicitly opted in *and* every
#: required credential is present. Otherwise the whole integration suite is
#: skipped so the tests run offline (e.g. in CI) without false passes.
RUN_INTEGRATION = os.getenv("PROCOUNTOR_RUN_INTEGRATION") == "1" and all(
    os.getenv(name) for name in INTEGRATION_ENV
)

#: Token handed out by the mocked OAuth call used in unit tests.
TEST_ACCESS_TOKEN = "test-access-token"


def build_mock_client(**overrides):
    """Construct a :class:`Client` without performing a real token request.

    ``Client.__init__`` normally calls ``_get_token`` which makes a live HTTP
    request. Here we patch it to set a dummy access token instead, so the
    client can be exercised entirely offline.
    """

    def fake_get_token(self):
        self.access_token = TEST_ACCESS_TOKEN
        return TEST_ACCESS_TOKEN

    params = {
        "api_key": "test-api-key",
        "client_id": "test-client-id",
        "client_secret": "test-client-secret",
        "redirect_uri": "https://example.com/callback",
        "test_mode": True,
        "api_version": "supported",
    }
    params.update(overrides)

    with mock.patch.object(Client, "_get_token", fake_get_token):
        return Client(**params)


class TestClient(unittest.TestCase):
    """Base class for the live integration tests.

    The historical test suite talks to the real Procountor test API and needs
    credentials supplied through the ``PROCOUNTOR_*`` environment variables.
    Those tests are skipped unless ``PROCOUNTOR_RUN_INTEGRATION=1`` and the
    credentials are present, which keeps the default ``pytest`` run fast and
    network-free. Offline logic is covered by the unit tests instead.
    """

    # Set the first item from query set during tests
    userId = None
    productId = None

    # Settings for tests
    country_code = "FI"
    product_groups = "PURCHASE"
    vat_in = 24.0
    get_invoice_params = {
        'startDate': '2019-02-01',
        'endDate': '2019-02-01',
    }
    get_invoice_id = 8204221
    get_dimension_id = 86160

    def setUp(self):
        if not RUN_INTEGRATION:
            self.skipTest(
                "Live Procountor integration tests skipped. Set "
                "PROCOUNTOR_RUN_INTEGRATION=1 together with the PROCOUNTOR_* "
                "credentials to run them."
            )

        self.client = Client(
            api_key=os.environ["PROCOUNTOR_API_KEY"],
            client_id=os.environ["PROCOUNTOR_CLIENT_ID"],
            client_secret=os.environ["PROCOUNTOR_CLIENT_SECRET"],
            redirect_uri=os.environ["PROCOUNTOR_REDIRECT_URI"],
            test_mode=True,
            api_version=os.environ["PROCOUNTOR_API_VERSION"],
        )


if __name__ == '__main__':
    unittest.main()
