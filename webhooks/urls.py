from django.conf.urls import patterns, url

urlpatterns = patterns('webhooks.views',
    url(r'^shopify/(?P<siteid>[\w]+)/customer_create', 'shopify_customer_create')
)
