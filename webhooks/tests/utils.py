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

    def __init__(self, omit=[], override={}):
        '''
        :param iterable omit: An iterable object of headers to omit.
          Note that only explicitly added for the Shopify emulation
          can be omitted.
        :param dict override: A dictionary of (header, value) pairs
          that will be used to override the default header values.
        '''
        self.omit = omit
        self.override = override
        self.factory = django.test.RequestFactory()

    def create_shopify_webhook_request(self, path, data, topic='/'):
        '''
        Create a Shopify webhook request for testing purposes. The
        returned request object will have headers and a Sha256 HMAC as
        if it was a real webhook request.
        
        :param str path: The path which the emulated request would have
          if it actually reached the view.
        :param dict data: This dict will be converted to a JSON string,
          used to compute the HMAC, and used as the request body.
        :param str topic: The topic for the Shopify-Topic header. This
          has a form such as "customers/create".
        :returns: a Django request object containing the given data;
          this can be passed to a view to simulate an actual request.
        '''
        # Calculate the HMAC
        datastr = json.dumps(data)
        hmac256 = self.compute_hmac(datastr, private_settings.SHARED_SECRET)

        # Define headers to add to the request
        headers = {
            'HTTP_X_REQUEST_ID': uuid.uuid4(),  # Generate a UUID
            'HTTP_X_SHOPIFY_HMAC_SHA256': hmac256,
            'HTTP_X_SHOPIFY_TOPIC': topic,
            'HTTP_X_SHOPIFY_SHOP_DOMAIN': 'example.myshopify.com',
            'content_type': 'application/json'
        }

        # Omit headers
        for header in self.omit:
            if header in headers:
                headers.pop(header)

        # Override headers
        for header, value in self.override.items():
            headers[header] = value

        # Create the POST request
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

    def customer_create(self, path, data):
        topic = 'customers/create'
        return self.create_shopify_webhook_request(path, data, topic)

    def customer_enable(self, path, data):
        topic = 'customer/enable'
        return self.create_shopify_webhook_request(path, data, topic)

    def customer_update(self, path, data):
        topic = 'customers/update'
        return self.create_shopify_webhook_request(path, data, topic)

    def customer_delete(self, path, data):
        topic = 'customers/delete'
        return self.create_shopify_webhook_request(path, data, topic)

    def shop_update(self, path, data):
        topic = 'shop/update'
        return self.create_shopify_webhook_request(path, data, topic)
