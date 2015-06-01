import json
from decimal import Decimal
from django.test import TestCase
from webhooks import views, models
from webhooks.tests import utils


class ShopifyViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.siteid = 'abcd'  # TODO: generate a random site ID

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.factory = utils.ShopifyRequestFactory()

    def _check_copy_field_validity(self, obj, data):
        '''
        Loop through all the fields listed in object.DIRECT_COPY_FIELDS and
        check if the object has these attributes and that they match the
        data contained in the `data` parameter.
         
        :param :class:`django.db.models.Model` obj: the object to check
          the DIRECT_COPY_FIELDS attributes on.
        :param dict data: a dictionary object containing the values that
          the object should have as properties.
        '''
        for fieldname in obj.DIRECT_COPY_FIELDS:
            self.assertEqual(getattr(obj, fieldname), data[fieldname],
                             'Object has an invalid %s value' % fieldname)


class TestShopifyCustomerCreate(ShopifyViewTest):
    '''
    Test that the shopify_customer_create view behaves correctly.
    '''
    def test_with_test_data(self):
        '''
        Send the same data sent by Shopify's test webhook button and
        monitor for proper behavior.
        '''
        path = '/webhooks/shopify/%s/customer_create' % self.siteid
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
        request = self.factory.customer_create(path, data)
        response = views.shopify_customer_create(request, self.siteid)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')
        self.assertEqual(len(models.Customer.objects.all()), 0,
                         'Test requests should not be added.')

    def test_with_valid_data(self):
        '''
        Test the view with actual data to confirm that a customer
        object is created in the database. Also check that using
        a modified form of the same data results in a second, distinct
        object in the database.
        '''
        path = '/webhooks/shopify/%s/customer_create' % self.siteid
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
        request = self.factory.customer_create(path, data)
        response = views.shopify_customer_create(request, self.siteid)
        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        customer_objects = models.Customer.objects.all()
        self.assertEqual(len(customer_objects), 1,
                         'View did not create a new Customer object')

        customer = customer_objects[0]
        self.assertEqual(customer.shopify_id, data['id'],
                         'The created customer has an incorrect shopify_id')
        self._check_copy_field_validity(customer, data)
        self.assertEqual(customer.total_spent, Decimal(data['total_spent']),
                         'The created customer has an incorrect total_spent')

        # Modify `data` and create a second customer.
        data['first_name'] = 'Test2'
        data['email'] = 'testyou@example.com'
        data['id'] = 553412612
        data['tags'] = 'hello, world'

        request = self.factory.customer_create(path, data)
        response = views.shopify_customer_create(request, self.siteid)
        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        customer = models.Customer.objects.get(shopify_id=data['id'])
        self._check_copy_field_validity(customer, data)

        tags_as_str = []
        for tag in customer.tags.all():
            tags_as_str.append(tag.name)

        self.assertIn('hello', tags_as_str,
                      'The created customer is missing a tag')
        self.assertIn('world', tags_as_str,
                      'The created customer is missing a tag')

        # TODO: add tests for the address fields when address parsing is
        #   complete in the view.


class TestShopifyCustomerUpdate(ShopifyViewTest):
    '''
    Test that the shopify_customer_udpate view behaves correctly.
    '''
    def test_with_test_data(self):
        path = '/webhooks/shopify/%s/customer_update' % self.siteid
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
        request = self.factory.customer_update(path, data)
        response = views.shopify_customer_update(request, self.siteid)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')
        self.assertEqual(len(models.Customer.objects.all()), 0,
                         'Test requests should not be added')

    def test_shopify_customer_update(self):
        '''
        Check that this view will create a new customer object with the
        given data if a customer does not currently exist. If a
        customer with he given ID already exists, test that it is then
        updated with the modified data.
        '''
        # Test creation of unknown customers
        path = '/webhooks/shopify/%s/customer_update' % self.siteid
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
                "updated_at":"2015-05-27T21:30:34+01:00",
                "verified_email":True,
                "tags":"hello, secondtag, shorttag, world",
                "last_order_name":None,
                "default_address": {
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
                    "default":True
                }, "addresses":[
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
                     "default":True
                    }
                ]
        }
        request = self.factory.customer_update(path, data)
        response = views.shopify_customer_update(request, self.siteid)
        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        customers = models.Customer.objects.all()
        self.assertEqual(len(customers), 1,
                         'Customer update resulted in incorrect object count')

        customer = customers[0]
        self._check_copy_field_validity(customer, data)

        tags_as_str = []
        for tag in customer.tags.all():
            tags_as_str.append(tag.name)

        self.assertIn('hello', tags_as_str,
                      'The created customer is missing a tag')
        self.assertIn('world', tags_as_str,
                      'The created customer is missing a tag')

        # Test that existing customers are properly updated.
        data['email'] = 'updatedemail@example.com'
        data['tags'] = 'tag1, tag2'

        request = self.factory.customer_update(path, data)
        response = views.shopify_customer_update(request, self.siteid)
        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

        customers = models.Customer.objects.all()
        self.assertEqual(len(customers), 1,
                         'Customer update resulted in incorrect object count')

        customer = customers[0]
        self._check_copy_field_validity(customer, data)

        tags_as_str = []
        for tag in customer.tags.all():
            tags_as_str.append(tag.name)

        self.assertIn('tag1', tags_as_str,
                      'The created customer is missing a tag')
        self.assertIn('tag2', tags_as_str,
                      'The created customer is missing a tag')
        self.assertNotIn('hello', tags_as_str,
                         'Old tag not deleted during update')
        self.assertNotIn('world', tags_as_str,
                         'Old tag not deleted during update')


class TestShopifyCustomerDelete(ShopifyViewTest):
    '''
    Test that the shopify_customer_delete view behaves correctly.
    '''
    def test_with_test_data(self):
        '''
        Send the data from Shopify's test webhook button and monitor
        for correct behavior.
        '''
        path = '/webhooks/shoify/%s/customer_delete' % self.siteid
        data = {"id":None,
                "addresses":[]
        }
        request = self.factory.customer_delete(path, data)
        response = views.shopify_customer_delete(request, self.siteid)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')

    def test_shopify_customer_delete(self):
        '''
        Test the view with actual data to ensure proper functionality.
        This view is tested for both existing and non-existing customer
        objects.
        '''
        # Test deletion with an existing customer
        customer = models.Customer()
        customer.shopify_id = 534645123
        customer.save()

        path = '/webhooks/shopify/%s/customer_delete' % self.siteid
        data = {'id': customer.shopify_id}
        request = self.factory.customer_delete(path, data)
        response = views.shopify_customer_delete(request, self.siteid)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')
        self.assertEqual(len(models.Customer.objects.all()), 0,
                         'Customer not correctly deleted')

        # Reply the delete to test when customer does not exist
        response = views.shopify_customer_delete(request, self.siteid)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')
        self.assertEqual(len(models.Customer.objects.all()), 0,
                         'The last object should have been deleted')


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

    def test_shopify_customer_enable(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_disable(self):
        self.skipTest("Test not implemented")

    def test_shopify_shop_update(self):
        # Test shop creation
        path = '/webhooks/shopify/%s/shop_update' % self.siteid
        data = {"address1":"190 MacLaren Street",
                "city":"Houston",
                "country":"US",
                "created_at":None,
                "customer_email":None,
                "domain":None,
                "email":"super@supertoys.com",
                "id":None,
                "latitude":None,
                "longitude":None,
                "name":"Super Toys",
                "phone":"3213213210",
                "primary_locale":"en",
                "primary_location_id":None,
                "province":"Tennessee",
                "source":None,
                "zip":"37178",
                "country_code":"US",
                "country_name":"United States",
                "currency":"USD",
                "timezone":"(GMT-05:00) Eastern Time (US \u0026 Canada)",
                "iana_timezone":None,
                "shop_owner":"N\/A",
                "money_format":"$ {{amount}}",
                "money_with_currency_format":"$ {{amount}} USD",
                "province_code":"TN",
                "taxes_included":None,
                "tax_shipping":None,
                "county_taxes":None,
                "plan_display_name":None,
                "plan_name":None,
                "myshopify_domain":None,
                "google_apps_domain":None,
                "google_apps_login_enabled":None,
                "money_in_emails_format":"${{amount}}",
                "money_with_currency_in_emails_format":"${{amount}} USD",
                "eligible_for_payments":True,
                "requires_extra_payments_agreement":False,
                "password_enabled":None,
                "has_storefront":False
        }
        request = self.factory.shop_update(path, data)
        response = views.shopify_shop_update(request, self.siteid)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')
        shops = models.Shop.objects.all()
        self.assertEqual(len(shops), 0,
                         'The test request should not create a shop')

    def test_shopify_refund_create(self):
        self.skipTest("Test not implemented")


class TestShopifyWebHooksValidData(TestCase):
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

    def test_shopify_customer_enable(self):
        self.skipTest("Test not implemented")

    def test_shopify_customer_disable(self):
        self.skipTest("Test not implemented")

    def test_shopify_shop_update(self):
        '''
        Test that this view creates a new shop in the case that the
        shop to be updated does not exist. If the shop does exist,
        check that it is updated.
        '''
        path = '/webhooks/shopify/%s/shop_update' % self.id
        data = {"address1":"121 West Sprint Street",
                "city":"Appleton",
                "country":"US",
                "created_at":"2015-05-19T17:45:19+01:00",
                "customer_email":'sales@example.com',
                "domain":"example.myshopify.com",
                "email":"test@example.com",
                "id":8711838,
                "latitude":12.4567,
                "longitude":-80.1234,
                "name":"My First Test Store",
                "phone":"",
                "primary_locale":"en",
                "primary_location_id":None,
                "province":"Wisconsin",
                "source":"learn-more",
                "zip":"12345",
                "country_code":"US",
                "country_name":"United States",
                "currency":"USD",
                "timezone":"(GMT+00:00) London",
                "iana_timezone":"Europe\/London",
                "shop_owner":"Austin Hartzheim",
                "money_format":"$ {{amount}}",
                "money_with_currency_format":"$ {{amount}} USD",
                "province_code":"WI",
                "taxes_included":False,
                "tax_shipping":None,
                "county_taxes":None,
                "plan_display_name":"affiliate",
                "plan_name":"affiliate",
                "myshopify_domain":"example.myshopify.com",
                "google_apps_domain":None,
                "google_apps_login_enabled":None,
                "money_in_emails_format":"${{amount}}",
                "money_with_currency_in_emails_format":"${{amount}} USD",
                "eligible_for_payments":True,
                "requires_extra_payments_agreement":False,
                "password_enabled":True,
                "has_storefront":True
        }
        request = self.factory.shop_update(path, data)
        response = views.shopify_shop_update(request, self.siteid)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error')
        shops = models.Shop.objects.all()
        self.assertEqual(len(shops), 1, 'One shop should exist')
        shop = shops[0]

        self.assertEqual(shop.shopify_id, data['id'],
                         'Created shop has incorrect shopify_id value')
        self.__check_copy_field_validity(shop, data)

        # Test shop update
        data['city'] = 'New York'
        data['shop_owner'] = 'Bob Smith'

        request = self.factory.shop_update(path, data)
        response = views.shopify_shop_update(request, self.siteid)

        self.assertEqual(response.status_code, 200,
                         'View returned an HTTP error code')
        shops = models.Shop.objects.all()
        self.assertEqual(len(shops), 1, 'One shop should exist')
        shop = shops[0]
        self.assertEqual(shop.shopify_id, data['id'],
                         'Created shop has an incorrect shopify_id')
        self.__check_copy_field_validity(shop, data)

    def test_shopify_refund_create(self):
        self.skipTest("Test not implemented")

    def __check_copy_field_validity(self, obj, data):
        '''
        Loop through all the fields listed in object.DIRECT_COPY_FIELDS and
        check if the object has these attributes and that they match the
        data contained in the `data` parameter.
         
        :param :class:`django.db.models.Model` obj: the object to check
          the DIRECT_COPY_FIELDS attributes on.
        :param dict data: a dictionary object containing the values that
          the object should have as properties.
        '''
        for fieldname in obj.DIRECT_COPY_FIELDS:
            self.assertEqual(getattr(obj, fieldname), data[fieldname],
                             'Object has an invalid %s value' % fieldname)


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
