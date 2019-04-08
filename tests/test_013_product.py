import os
from tests import TestClient


class TestClientProduct(TestClient):

    # for testing
    test_product_group = None

    the_first_productId = None

    def __init__(self, *args, **kwargs):
        super(TestClientProduct, self).__init__(*args, **kwargs)
        self.__class__.test_product_group = os.getenv('PROCOUNTOR_PRODUCT_PRODUCT_GROUP', None)

    def test_001_get_products(self):
        """ get all products from API """

        response = self.client.get_products()
        self.assertEqual(response['status'], 200)
        self.assertIsInstance(response['content']['products'], list)
        self.__class__.the_first_productId = response['content']['products'][0]['id']

    def test_002_get_product(self):
        """ get info of one product """
        response = self.client.get_product(self.__class__.the_first_productId)
        self.assertEqual(response['status'], 200)
        self.assertIsNotNone(response['content'])

    def test_003_get_product_groups(self):
        """ get product groups (by product type) """

        if self.__class__.test_product_group:
            response = self.client.get_product_groups(productType=self.__class__.test_product_group)
            self.assertEqual(response['status'], 200)
            self.assertIsInstance(response['content'], list)

if __name__ == '__main__':
    unittest.main()