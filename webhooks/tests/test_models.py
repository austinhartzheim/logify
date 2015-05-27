from django.test import TestCase
from webhooks import models


class TestCustomer(TestCase):
    '''
    Test the methods of the Customer class.
    '''
    def test_str(self):
        customer = models.Customer()
        customer.first_name = 'Jim'
        customer.shopify_id = 0
        customer.orders_count = 0
        customer.state = 'disabled'

        self.assertIn('Jim', str(customer),
                      'The __str__ method does not contain the first name')

class TestCustomerTag(TestCase):
    '''
    Test the methods of the CustomerTag class.
    '''
    def test_get_or_create(self):
        tag1 = models.CustomerTag.get_or_create('hello')
        tag2 = models.CustomerTag.get_or_create('hello')

        self.assertEqual(tag1.pk, tag2.pk,
                         'Duplicate tag created by get_or_create method')

    def test_str(self):
        tag = models.CustomerTag.get_or_create('hello')
        self.assertIn('hello', str(tag),
                      'The __str__ method does not contain the tag name')
