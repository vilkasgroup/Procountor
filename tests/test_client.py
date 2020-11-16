import unittest
import os
from procountor.client import Client


class TestClient(unittest.TestCase):

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

    def __init__(self, *args, **kwargs):
        """ Initialize Procountor client. Requires the following environment
        variables PROCOUNTOR_API_KEY, PROCOUNTOR_CLIENT_ID, PROCOUNTOR_CLIENT_SECRET, PROCOUNTOR_REDIRECT_URI and PROCOUNTOR_API_VERSION. """

        super(TestClient, self).__init__(*args, **kwargs)
        self.client = Client(
            api_key = os.environ['PROCOUNTOR_API_KEY'],
            client_id = os.environ['PROCOUNTOR_CLIENT_ID'],
            client_secret = os.environ['PROCOUNTOR_CLIENT_SECRET'],
            redirect_uri = os.environ['PROCOUNTOR_REDIRECT_URI'],
            test_mode = True,
            api_version = os.environ['PROCOUNTOR_API_VERSION']
        )

if __name__ == '__main__':
    unittest.main()