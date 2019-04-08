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
        variables PROCOUNTOR_USERNAME, PROCOUNTOR_PASSWORD, PROCOUNTOR_COMPANY_ID, PROCOUNTOR_CLIENT_ID, PROCOUNTOR_CLIENT_SECRET and PROCOUNTOR_REDIRECT_URI. """

        super(TestClient, self).__init__(*args, **kwargs)
        self.client = Client(
            username = os.environ['PROCOUNTOR_USERNAME'],
            password = os.environ['PROCOUNTOR_PASSWORD'],
            company_id = os.environ['PROCOUNTOR_COMPANY_ID'],
            client_id = os.environ['PROCOUNTOR_CLIENT_ID'],
            client_secret = os.environ['PROCOUNTOR_CLIENT_SECRET'],
            redirect_uri = os.environ['PROCOUNTOR_REDIRECT_URI'],
            test_mode = True,
        )

if __name__ == '__main__':
    unittest.main()