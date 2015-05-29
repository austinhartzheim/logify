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

SHOP_FIELDS_DIRECT_COPY = [
    'address1',
    'city',
    'country',
    'country_code',
    'country_name',
    'county_taxes',
    # 'created_at',
    'currency',
    'customer_email',
    'domain',
    'eligible_for_payments',
    'email',
    'google_apps_domain',
    'google_apps_login_enabled',
    'has_storefront',
    'iana_timezone',
    # 'id',
    'latitude',
    'longitude',
    'money_format',
    'money_in_emails_format',
    'money_with_currency_format',
    'money_with_currency_in_emails_format',
    'myshopify_domain',
    'name',
    'password_enabled',
    'phone',
    'plan_display_name',
    'plan_name',
    'primary_locale',
    'primary_location_id',
    'province',
    'province_code',
    'requires_extra_payments_agreement',
    'shop_owner',
    'source',
    'tax_shipping',
    'taxes_included',
    'timezone',
    'zip'
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
    pass

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_customer_disable(request, siteid):
    pass

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

    for fieldname in CUSTOMER_FIELDS_DIRECT_COPY:
        if fieldname in data:
            setattr(customer, fieldname, data[fieldname])

    # TODO: parse created_at
    # TODO: parse updated_at

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

    for fieldname in SHOP_FIELDS_DIRECT_COPY:
        if fieldname in data:
            setattr(shop, fieldname, data[fieldname])

    # TODO: parse created_at

    shop.save()
    return django.http.HttpResponse()

@csrf_exempt
@validate.ValidateShopifyWebhookRequest
def shopify_refund_create(request, siteid):
    pass
