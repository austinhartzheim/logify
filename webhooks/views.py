import json
from decimal import Decimal

from django.shortcuts import render
import django.http
from django.views.decorators.csrf import csrf_exempt
from webhooks.models import *
from webhooks.libs import validate

CUSTOMER_FIELDS_DIRECT_COPY = [
    'accepts_marketing',
    # created_at
    'email',
    'first_name',
    # 'id',
    'last_name',
    'last_order_id',
    'multipass_identifier',
    'note',
    'orders_count',
    'state',
    'tax_exempt',
    # total_spent
    # updated_at
    'verified_email',
    # tags
    'last_order_name',
    # addresses
]


@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_order_create(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_order_updated(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_order_paid(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_order_cancelled(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_order_fulfilled(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_order_delete(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_product_create(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_product_update(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_product_delete(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_cart_create(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_cart_update(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_collection_create(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_collection_update(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_collection_delete(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_group_create(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_group_update(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_group_delete(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_checkout_create(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_checkout_update(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_checkout_delete(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_fulfillment_create(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_fulfillment_update(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_create(request, siteid):

    data = json.loads(request.body.decode('utf8'))
    if data['id'] == None:  # Test request
        return django.http.HttpResponse()
    customer = Customer()
    customer.shopify_id = data['id']

    for fieldname in CUSTOMER_FIELDS_DIRECT_COPY:
        if fieldname in data:
            setattr(customer, fieldname, data[fieldname])

    # TODO: parse created_at
    # TODO: parse updated_at

    if 'total_spent' in data:
        customer.total_spent = Decimal(data['total_spent'])

    if 'tags' in data:
        tags = data['tags'].split()
        for tag in tags:
            customer.tags.add(CustomerTag.get_or_create(tag))

    # TODO: handle addresses

    customer.save()

    return django.http.HttpResponse()

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_enable(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_disable(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_update(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_delete(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_shop_update(request, siteid):
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_refund_create(request, siteid):
    pass
