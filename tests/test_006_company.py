import unittest
from tests import TestClient


class TestClientCompany(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientCompany, self).__init__(*args, **kwargs)

    def test_001_get_company(self):
        """
        Test get_company api call
        """
        response = self.client.get_company()
        self.assertEqual(response['status'], 200)
        self.assertIsNotNone(response['content'])
        self.assertIsInstance(response['content']['id'], int)

    def test_002_update_company(self):
        """
        TODO: Test for update company
        """
        pass


if __name__ == '__main__':
    unittest.main()