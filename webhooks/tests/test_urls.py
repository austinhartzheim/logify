import django.test


class TestUrls(django.test.TestCase):
    '''
    Some simple tests to prevent total breakage of the routing setup.
    '''

    def test_shopify_customer_create(self):
        client = django.test.Client()
        response = client.get('/webhooks/shopify/123/customer_create')
        self.assertEqual(response.status_code, 405)
        response = client.post('/webhooks/shopify/123/customer_create')
        self.assertEqual(response.status_code, 400)

    def test_404(self):
        '''
        Test that invalid URLs return a 404 response.
        '''
        client = django.test.Client()
        response = client.get('/webhooks/this_should_404')
        self.assertEqual(response.status_code, 404)