from hashlib import sha256
import base64
import hmac

import django.http
from logify import private_settings


class ValidateShopifyWebhookRequest():
    def __init__(self, view):
        self.view = view

    def __call__(self, request, siteid, *args, **kwargs):
        '''
        Check that `request` is a POST request that contains the
        headers to indicate that it is a Shopify webhook request. Also
        check that the HMAC is valid.
        
        If the request is valid, then call the view with the `request`
        and `siteid` as parameters. 
        '''
        # Check that the request is using the POST method
        if request.method != 'POST':
            return django.http.HttpResponseNotAllowed(['POST'])

        # Check that the headers exist.
        if 'HTTP_X_SHOPIFY_SHOP_DOMAIN' not in request.META:
            return django.http.HttpResponseBadRequest('missing X-Shopify-Shop-Domain')
        if 'HTTP_X_REQUEST_ID' not in request.META:
            return django.http.HttpResponseBadRequest('missing X-Request-Id')
        if 'HTTP_X_SHOPIFY_TOPIC' not in request.META:
            return django.http.HttpResponseBadRequest('missing X-Shopify-Topic')
        if 'HTTP_X_SHOPIFY_HMAC_SHA256' not in request.META:
            return django.http.HttpResponseBadRequest('missing X-Shopify-Hmac-Sha256')
        if 'CONTENT_TYPE' not in request.META:
            return django.http.HttpResponseBadRequest('missing Content-Type')
        if request.META['CONTENT_TYPE'] != 'application/json':
            return django.http.HttpResponseBadRequest('bad Content-Type')

        # Check that the HMAC is valid
        if not self.validate_shopify_webhook_hmac(request):
            return django.http.HttpResponseForbidden('Invalid HMAC')

        # The checks pass; forward the request to the view
        return self.view(request, siteid, *args, **kwargs)

    def validate_shopify_webhook_hmac(self, request):
        '''
        Check that the necessary headers are included on the request and
        verify the SHA256-HMAC with our shared secret.
        
        :param django.http.HttpRequest request: A Django request object
          that contains the headers, POST data, etc.
        :returns: a boolean value; `true` indicates a valid request;
          `false` indicates an invalid request
        '''
        if 'HTTP_X_SHOPIFY_HMAC_SHA256' not in request.META:
            return False

        shared_secret = private_settings.SHARED_SECRET.encode('utf8')
        digest = hmac.new(shared_secret, request.body, sha256).digest()
        digest = base64.b64encode(digest).decode('utf8')

        return self.__safe_compare(digest, request.META['HTTP_X_SHOPIFY_HMAC_SHA256'])

    @staticmethod
    def __safe_compare(a, b):
        '''
        Attempt to use hmac.compare_digest(), which is available in
        Python 3.3+. If that fails, iterate over the entire digest to
        detect a difference; only return after iterating over the
        entire digest to avoid a timing attack.
        '''
        # TODO: implement the manual comparison in a low-level language
        #   Python might optimize the comparison loop
        try:
            return hmac.safe_compare(a, b)
        except AttributeError:
            if len(a) != len(b):
                return False

            result = True
            count = 0  # Hack to prevent optimization
            for i in range(0, len(a)):
                if a[i] != b[i]:
                    result = False
                count += 1
            return result
