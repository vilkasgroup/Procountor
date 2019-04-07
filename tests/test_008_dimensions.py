import os
import unittest
from tests import TestClient


class TestClientDimensions(TestClient):

    test_dimension_id = None

    def __init__(self, *args, **kwargs):
        super(TestClientDimensions, self).__init__(*args, **kwargs)
        self.__class__.test_dimension_id = os.getenv('PROCOUNTOR_DIMENSION_DIMENSION_ID', None)

    def test_001_get_dimensions(self):
        response = self.client.get_dimensions()
        self.assertEqual(response['status'], 200)
        self.assertIsInstance(response['content'][0]['id'], int)

    def test_002_update_dimension(self):
        # TODO: Crate a test for update_dimension
        pass

    def test_003_get_dimension(self):
        if self.__class__.test_dimension_id:
            response = self.client.get_dimension(self.__class__.test_dimension_id)
            self.assertEqual(response['status'], 200)
            self.assertIsInstance(response['content']['id'], int)

    def test_004_create_dimension_item(self):
        # TODO: Create a test for create_dimension_item
        pass

    def test_005_update_dimension_item(self):
        # TODO: Create a test for update_dimension_item
        pass

if __name__ == '__main__':
    unittest.main()