import unittest
from tests import TestClient


class TestClientUsers(TestClient):

    userId = None # Saves userid for tests

    def __init__(self, *args, **kwargs):
        super(TestClientUsers, self).__init__(*args, **kwargs)

    def test_001_get_users(self):
        """ Test getting user information from API """
        response = self.client.get_users()
        self.assertEqual(response['status'], 200)
        self.assertIsInstance(response['content']['userId'], int)
        self.__class__.userId = response['content']['userId']

    def test_002_update_user(self):
        # TODO: Write test for update user
        pass

    def test_003_user_transaction_confirm(self):
        # TODO: Write test for user_transaction_confirm
        pass

    def test_004_send_one_time_pass(self):
        """ Test sending one time password for currently logged in user via SMS """
        response = self.client.send_one_time_pass()
        # After the first test status code is 429 if not waited 10 minutes
        if response['status'] != 200:
            self.assertEqual(response['status'], 429)
        else:
            self.assertEqual(response['status'], 200)

    def test_005_get_user_profile(self):
        """ Test getting user profile based on user ID """
        response = self.client.get_user_profile(self.__class__.userId)
        self.assertEqual(response['status'], 200)
        self.assertIsNotNone(response['content']['firstname'])

if __name__ == '__main__':
    unittest.main()
