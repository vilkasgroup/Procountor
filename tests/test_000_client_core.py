import unittest
from tests import TestClient
from procountor.client import Client


class TestClientClient(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientClient, self).__init__(*args, **kwargs)

    def test_0001_init(self):
        """ Testing that client has required params """
        self.assertIsInstance(self.client, Client)
        self.assertIsNotNone(self.client.username)
        self.assertIsNotNone(self.client.password)
        self.assertIsNotNone(self.client.company_id)
        self.assertIsNotNone(self.client.client_id)
        self.assertIsNotNone(self.client.client_secret)
        self.assertIsNotNone(self.client.redirect_uri)
        self.assertEqual(self.client.test_mode, True)
        self.assertIsNotNone(self.client.access_token)
        self.assertIsNotNone(self.client.refresh_token)

    def test_0002_get_tokens(self):
        tokens = self.client._get_tokens()
        self.assertIsNotNone(tokens['access_token'])
        self.assertIsNotNone(tokens['refresh_token'])

        invalidate_token = self.client.invalidate_token()
        self.assertEqual(invalidate_token['status'], 200)

    def test_0003_refresh_access_token(self):
        response = self.client.refresh_access_token()
        self.assertIsNotNone(response)

    def test_0004_headers(self):
        response = self.client._headers("GET", "users")
        self.assertEqual(response['authorization'], "Bearer {}".format(self.client.access_token))

if __name__ == '__main__':
    unittest.main()
