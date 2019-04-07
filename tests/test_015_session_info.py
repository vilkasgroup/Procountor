import unittest
from tests import TestClient


class TestClientSessionInfo(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientSessionInfo, self).__init__(*args, **kwargs)

    def test_001_get_session_info(self):
        response = self.client.get_session_info()
        self.assertEqual(response['status'], 200)
        self.assertIsNotNone(response['content'])
        self.assertIs(type(response['content']['companyId']), int)

if __name__ == '__main__':
    unittest.main()