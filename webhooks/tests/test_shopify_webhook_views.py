import json
from decimal import Decimal
from django.test import TestCase
from webhooks import views, models
from webhooks.tests import utils


class TesteShopifyMinimalData(TestCase):
    '''
    Test that the minimal amount of data Shopify will allow is still
    handled correctly by the views.
    '''
    # TODO: Determine the minimal data allowed for each view; this will
    #   require experimenting with their web interface
    # TODO: Implement tests which give this minimal level of data.
    pass


class TestShopifyWebHooksTestData(TestCase):
    '''
    Test the Shopify webhooks against the data sent to the webhook by
    Shopify's "send test notification" button.
    
    The test requests include null in their ID fields; we can drop
    these requests.
    '''
    @classmethod
    def setUpClass(cls):
        cls.siteid = 'abcd'  # TODO: generate a random site ID

    def setUp(self):
        self.factory = utils.ShopifyRequestFactory()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_shopify_order_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_updated(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_paid(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_cancelled(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_fulfilled(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_product_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_product_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_product_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_cart_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_cart_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_collection_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_collection_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_collection_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_group_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_group_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_group_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_checkout_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_checkout_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_checkout_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_fulfillment_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_fulfillment_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_create(self):
        # TODO: create a util function to create requests with valid HMACs
        path = '/webhooks/shopify/%s/order_create' % self.siteid
        data = {"accepts_marketing":True,
                "created_at":None,
                "email":"bob@biller.com",
                "first_name":"Bob",
                "id":None,
                "last_name":"Biller",
                "last_order_id":None,
                "multipass_identifier":None,
                "note":"This customer loves ice cream",
                "orders_count":0,
                "state":"disabled",
                "tax_exempt":False,
                "total_spent":"0.00",
                "updated_at":None,
                "verified_email":True,
                "tags":"",
                "last_order_name":None,
                "addresses":[]
        }
        request = self.factory.create_shopify_webhook_request(path, data)
        response = views.shopify_customer_create(request, self.siteid)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')
        self.assertEqual(len(models.Customer.objects.all()), 0,
                         'Test requests should not be added.')


    def test_shopify_customer_enable(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_disable(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_shop_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_refund_create(self):
        self.skipTest("Test not implemented")


class TesetShopifyWebHooksValidData(TestCase):
    '''
    Perform tests under normal use cases just to make sure we don't
    miss them between the minimalist tests and the absurd extremes.
    '''
    @classmethod
    def setUpClass(cls):
        cls.siteid = 'abcd'  # TODO: generate a random site ID

    def setUp(self):
        self.factory = utils.ShopifyRequestFactory()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_shopify_order_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_updated(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_paid(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_cancelled(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_fulfilled(self):
        self.skipTest("Test not implemented")

    def test_shopify_order_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_product_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_product_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_product_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_cart_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_cart_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_collection_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_collection_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_collection_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_group_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_group_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_group_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_checkout_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_checkout_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_checkout_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_fulfillment_create(self):
        self.skipTest("Test not implemented")

    def test_shopify_fulfillment_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_create(self):
        # TODO: create a util function to create requests with valid HMACs
        path = '/webhooks/shopify/%s/order_create' % self.siteid
        data = {"accepts_marketing":False,
                "created_at":"2015-05-27T19:12:18+01:00",
                "email":"testme@example.com",
                "first_name":"Test",
                "id":553412611,
                "last_name":"Customer",
                "last_order_id":None,
                "multipass_identifier":None,
                "note":"",
                "orders_count":0,
                "state":"disabled",
                "tax_exempt":False,
                "total_spent":"0.00",
                "updated_at":"2015-05-27T19:12:19+01:00",
                "verified_email":True,
                "tags":"",
                "last_order_name":None,
                "default_address":{
                    "address1":"",
                    "address2":"",
                    "city":"",
                    "company":"",
                    "country":"United States",
                    "first_name":"Test",
                    "id":638359939,
                    "last_name":"Customer",
                    "phone":"",
                    "province":"Alabama",
                    "zip":"",
                    "name":"Test Customer",
                    "province_code":"AL",
                    "country_code":"US",
                    "country_name":"United States",
                    "default":True},
                "addresses":[
                    {"address1":"",
                     "address2":"",
                     "city":"",
                     "company":"",
                     "country":"United States",
                     "first_name":"Test",
                     "id":638359939,
                     "last_name":"Customer",
                     "phone":"",
                     "province":"Alabama",
                     "zip":"",
                     "name":"Test Customer",
                     "province_code":"AL",
                     "country_code":"US",
                     "country_name":"United States",
                     "default":True}
                ]
        }
        request = self.factory.create_shopify_webhook_request(path, data)
        response = views.shopify_customer_create(request, self.siteid)
        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        customer_objects = models.Customer.objects.all()
        self.assertEqual(len(customer_objects), 1,
                         'View did not create a new Customer object')

        customer = customer_objects[0]
        self.assertEqual(customer.shopify_id, data['id'],
                         'The created customer has an incorrect shopify_id')
        self.assertEqual(customer.note, data['note'],
                         'The created customer does not have an empty note')
        self.assertEqual(customer.total_spent, Decimal(data['total_spent']),
                         'The created customer has an incorrect total_spent')

        # TODO: add tests for the address fields when address parsing is
        #   complete in the view.


    def test_shopify_customer_enable(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_disable(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_delete(self):
        self.skipTest("Test not implemented")

    def test_shopify_shop_update(self):
        self.skipTest("Test not implemented")

    def test_shopify_refund_create(self):
        self.skipTest("Test not implemented")


class TestShopifyWebHooksAbsurdData(TestCase):
    '''
    Shopify doesn't validate the input data, so we need to accept
    everything they can throw at us, including absurdly large values.
    '''
    pass  # TODO: implement tests


class TestShopifyWebHooksInvalidHmac(TestCase):
    '''
    Send webhook requests with invalid HMACs; test that the view
    returns a non-200 HTTP status code (indicating an error to
    Shopify, which causes the webhook to be re-sent).
    '''
    pass
