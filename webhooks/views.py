import json
from decimal import Decimal

from django.shortcuts import render
import django.http
from django.views.decorators.csrf import csrf_exempt
import dateutil.parser

from webhooks.models import *
from webhooks.libs import validate

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
    '''
    Test if a customer with the same shopify_id already exists. If one
    does, then return a 200 response. If one does not, then create it.
    '''
    data = json.loads(request.body.decode('utf8'))
    if data['id'] == None:  # Test request
        return django.http.HttpResponse()

    # Test if customer already exists
    try:
        customer = Customer.objects.get(shopify_id=data['id'])
        return django.http.HttpResponse()
    except Customer.DoesNotExist:
        pass

    # Create a new customer
    customer = Customer()
    customer.shopify_id = data['id']

    for fieldname in Customer.DIRECT_COPY_FIELDS:
        if fieldname in data:
            setattr(customer, fieldname, data[fieldname])

    customer.created_at = dateutil.parser.parse(data['created_at'])
    customer.updated_at = dateutil.parser.parse(data['updated_at'])

    if 'total_spent' in data:
        customer.total_spent = Decimal(data['total_spent'])

    # TODO: handle addresses

    customer.save()  # Customer must be saved before using ManyToMany fields

    if 'tags' in data and data['tags']:
        tags = data['tags'].split(', ')
        for tag in tags:
            customer.tags.add(CustomerTag.get_or_create(tag))
        customer.save()

    return django.http.HttpResponse()

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_enable(request, siteid):
    '''
    If the given customer ID already exists, enable that customer
    object. If the ID does not exist, then create a new customer
    object with the given data.
    '''
    data = json.loads(request.body.decode('utf8'))
    if data['id'] == None:  # Test request
        return django.http.HttpResponse()

    try:
        customer = Customer.objects.get(shopify_id=data['id'])
    except Customer.DoesNotExist:
        return shopify_customer_create(request, siteid)

    customer.state = 'enabled'
    customer.updated_at = dateutil.parser.parse(data['updated_at'])
    customer.save()

    return django.http.HttpResponse()

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_disable(request, siteid):
    '''
    If the given customer ID already exists, disable that customer
    object. If the ID does not exist, then create a new customer
    object with the given data.
    '''

    data = json.loads(request.body.decode('utf8'))
    if data['id'] == None:  # Test request
        return django.http.HttpResponse()

    try:
        customer = Customer.objects.get(shopify_id=data['id'])
    except Customer.DoesNotExist:
        return shopify_customer_create(request, siteid)

    customer.state = 'disabled'
    customer.updated_at = dateutil.parser.parse(data['updated_at'])
    customer.save()

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_update(request, siteid):
    '''
    If the given customer ID already exists, update the data for that
    customer object. If the customer ID does not exist, then create a
    new customer object with the given data.
    '''

    data = json.loads(request.body.decode('utf8'))
    if data['id'] == None:  # Test request
        return django.http.HttpResponse()

    try:
        customer = Customer.objects.get(shopify_id=data['id'])
    except Customer.DoesNotExist:
        return shopify_customer_create(request, siteid)

    for fieldname in Customer.DIRECT_COPY_FIELDS:
        if fieldname in data:
            setattr(customer, fieldname, data[fieldname])

    customer.created_at = dateutil.parser.parse(data['created_at'])
    customer.updated_at = dateutil.parser.parse(data['updated_at'])

    if 'total_spent' in data:
        customer.total_spent = Decimal(data['total_spent'])

    # TODO: handle addresses

    customer.save()

    if 'tags' in data and data['tags']:
        customer.tags.clear()
        tags = data['tags'].split(', ')
        for tag in tags:
            customer.tags.add(CustomerTag.get_or_create(tag))
        customer.save()

    return django.http.HttpResponse()

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_delete(request, siteid):
    '''
    If the given customer ID already exists, delete it. If it cannot be
    found, do nothing.
    '''
    data = json.loads(request.body.decode('utf8'))
    if data['id'] == None:  # Test request
        return django.http.HttpResponse()

    try:
        customer = Customer.objects.get(shopify_id=data['id'])
        customer.delete()
    except Customer.DoesNotExist:
        pass

    return django.http.HttpResponse()

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_shop_update(request, siteid):

    data = json.loads(request.body.decode('utf8'))
    if data['id'] is None:  # Test request
        return django.http.HttpResponse()

    try:
        shop = Shop.objects.get(shopify_id=data['id'])
    except Shop.DoesNotExist:
        shop = Shop()
        shop.shopify_id = data['id']

    for fieldname in Shop.DIRECT_COPY_FIELDS:
        if fieldname in data:
            setattr(shop, fieldname, data[fieldname])

    shop.created_at = dateutil.parser.parse(data['created_at'])

    shop.save()
    return django.http.HttpResponse()

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_refund_create(request, siteid):
    pass
