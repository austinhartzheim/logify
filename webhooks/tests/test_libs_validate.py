import unittest
import django.test
from webhooks.libs.validate import ValidateShopifyWebhookRequest
from webhooks.tests import utils


class TestValidateShopifyWebhookRequestInvalidData(unittest.TestCase):
    '''
    Test that the ValidateShopifyWebhookRequest decorator properly
    prevents execution from ever reaching the internal function.
    '''
    siteid = 'abcd'
    
    #: Headers to be individually omitted when testing validation.
    headers = ('HTTP_X_SHOPIFY_SHOP_DOMAIN', 'HTTP_X_REQUEST_ID',
               'HTTP_X_SHOPIFY_TOPIC', 'HTTP_X_SHOPIFY_HMAC_SHA256')
    
    #: An incorrect HMAC value to test HMAC validation
    bad_hmac = '0000000000000000000000000000000000000000000='
    
    def setUp(self):
        
        @ValidateShopifyWebhookRequest
        def dummy_view(*args, **kwargs):
            '''
            Raise an exception if this "view" is ever executed. The
            validation decorator should prevent this "view" from
            being executed.
            '''
            raise Exception('This function should not have been called')
            
        self.view = dummy_view
        
    def test_get_request(self):
        '''
        Check that the validator rejects HTTP GET and PUT requests.
        '''
        factory = django.test.RequestFactory()
        
        request = factory.get('/')
        response = self.view(request, self.siteid)
        
        self.assertEqual(response.status_code, 405,
                         'Not returning 405 to notify of POST requirement.')
        
        request = factory.put('/')
        response = self.view(request, self.siteid)
        
        self.assertEqual(response.status_code, 405,
                         'Not returning 405 to notify of PUT requirement.')
        
    def test_missing_individual_headers(self):
        '''
        Check that missing Shopify headers result in an HTTP 400 Bad
        Request response.
        '''
        path = '/webhooks/shopify/%s/order_create' % self.siteid
        for header in self.headers:
            factory = utils.ShopifyRequestFactory(omit=(header,))
            
            request = factory.create_shopify_webhook_request(path, data={})
            response = self.view(request, self.siteid)
            
            self.assertEqual(response.status_code, 400)

    def test_incorrect_content_type_header(self):
        '''
        Check that Content-Type headers other than application/json are
        rejected by the validator.
        '''
        path = '/webhooks/shopify/%s/order_create' % self.siteid
        override_headers = {'content_type': 'text/plain'}
        
        for header in self.headers:
            factory = utils.ShopifyRequestFactory(override=override_headers)
            
            request = factory.create_shopify_webhook_request(path, data={})
            response = self.view(request, self.siteid)
            
            self.assertEqual(response.status_code, 400)
            
    def test_incorrect_hmac_header(self):
        '''
        Check that the HMAC validation code is properly executing and
        returning an HTTP 403 Forbidden response.
        '''
        path = '/webhooks/shopify/%s/order_create' % self.siteid
        override_headers = {'HTTP_X_SHOPIFY_HMAC_SHA256': self.bad_hmac}
        
        for header in self.headers:
            factory = utils.ShopifyRequestFactory(override=override_headers)
            
            request = factory.create_shopify_webhook_request(path, data={})
            response = self.view(request, self.siteid)
            
            self.assertEqual(response.status_code, 403,
                             'Bad HMAC did not result in forbidden response')