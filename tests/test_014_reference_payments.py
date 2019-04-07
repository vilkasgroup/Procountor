from tests import TestClient


class TestClientProduct(TestClient):

    def __init__(self, *args, **kwargs):
        super(TestClientProduct, self).__init__(*args, **kwargs)

    def test_001_get_reference_payments(self):
        """ get all products from API """

        response = self.client.get_reference_payments()
        self.assertEqual(response['status'], 200)

        if response['content']['meta']['resultCount'] > 0:
          self.assertIsInstance(response['content']['results'], list)

if __name__ == '__main__':
    unittest.main()