import base64
import hashlib
import hmac
import json
import time
import uuid

import django.test
from logify import private_settings


class ShopifyRequestFactory():
    '''
    Emulate Shopify webhook requests.
    '''
    
    def __init__(self):
        self.factory = django.test.RequestFactory()
    
    def create_shopify_webhook_request(self, path, data):
        '''
        Create a Shopify webhook request for testing purposes. The
        returned request object will have headers and a Sha256 HMAC as
        if it was a real webhook request.
        
        :param :class:`django.test.RequestFactory` factory: A Django
          RequestFactory for generating the request object.
        :param dict data: This dict will be converted to a JSON string,
          used to compute the HMAC, and used as the request body.
        :returns: a Django request object containing the given data;
          this can be passed to a view to simulate an actual request.
        '''
        datastr = json.dumps(data)
        hmac256 = self.compute_hmac(datastr, private_settings.SHARED_SECRET)
        
        headers = {
            'HTTP_X_REQUEST_ID': uuid.uuid4(),  # Generate a UUID
            'HTTP_X_SHOPIFY_HMAC_SHA256': hmac256,
            'HTTP_X_SHOPIFY_TOPIC': 'customers/update',
            'HTTP_X_SHOPIFY_SHOP_DOMAIN': 'example.myshopify.com',
            'content_type': 'application/json'
        }
        
        return self.factory.post(path, datastr, **headers)
        
        
    def compute_hmac(self, data, shared_secret):
        '''
        Calculate the HMAC for `data` and `shared_secret`. Theese
        parameters can be supplied as `str` or `bytes` objects. If a
        string is passed, it will be encoded using utf8.
        
        :param bytes data: The data of the request.
        :param bytes secret_key: The secret key
        '''
        # Convert `data` and `secret_key` to bytes if necessary.
        if isinstance(data, str):
            data = data.encode('utf8')
        if isinstance(shared_secret, str):
            shared_secret = shared_secret.encode('utf8')
            
        # Compute the digest
        digest = hmac.new(shared_secret, data, hashlib.sha256).digest()
        return base64.b64encode(digest).decode('utf8')