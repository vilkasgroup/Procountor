import unittest
from tests import TestClient

# TODO: Write tests for Payments

class TestClientPayments(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientPayments, self).__init__(*args, **kwargs)

if __name__ == '__main__':
    unittest.main()