from django.db import models


# class Order(models.Model):
#     pass
#
#
# class Product(models.Model):
#     pass
#
#
# class Cart(models.Model):
#     pass
#
#
# class Collection(models.Model):
#     pass


class Customer(models.Model):
    shopify_id = models.BigIntegerField(unique=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    email = models.EmailField(blank=True)
    verified_email = models.BooleanField(default=False)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)

    note = models.TextField(blank=True)
    last_order_id = models.BigIntegerField(null=True)
    orders_count = models.IntegerField(default=0)
    total_spent = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    tags = models.ManyToManyField('CustomerTag')

    state = models.CharField(max_length=20)  # disabled, etc.
    tax_exempt = models.BooleanField(default=False)

    accepts_marketing = models.BooleanField(default=False)
    multipass_identifier = models.TextField(null=True)

    addresses = models.ManyToManyField('CustomerAddress')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class CustomerTag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_or_create(cls, name):
        '''
        Find a tag with the specified name in the database or create a
        new tag with that name. Return the tag in either case.
        
        :param str name: The name of the tag to be found/created.
        :returns: a :class:`CustomerTag` object with the specified `name`.
        '''
        try:
            obj = cls.objects.get(name=name)
        except cls.DoesNotExist:
            obj = CustomerTag()
            obj.name = name
            obj.save()
        return obj

    def __str__(self):
        return self.name


class CustomerAddress(models.Model):
    shopify_id = models.BigIntegerField(unique=True)

    default = models.BooleanField(default=False)

    name = models.TextField(blank=True)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    company = models.TextField(blank=True)
    address1 = models.TextField(blank=True)
    address2 = models.TextField(blank=True)
    city = models.TextField(blank=True)
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=50)
    province = models.TextField(blank=True)
    province_code = models.CharField(max_length=2)
    zip = models.TextField(blank=True)

    phone = models.TextField(blank=True)

    def __str__(self):
        return '%s, %s, %s, "%s"' % (self.country_code, self.province_code,
                                     self.city, self.name)


# class Checkout(models.Model):
#     pass
#
#
# class Fulfillment(models.Model):
#     pass
#
#
# class Customer(models.Model):
#     pass
#
#
class Shop(models.Model):
    shopify_id = models.BigIntegerField(unique=True)

    # Basic data
    name = models.TextField(blank=True)
    has_storefront = models.BooleanField(default=False)
    myshopify_domain = models.TextField(blank=True, null=True)
    created_at = models.TextField(null=True)

    #: The contact email address for the shop
    email = models.EmailField()
    #: The customer support email for the shop
    customer_email = models.EmailField(blank=True)

    shop_owner = models.TextField()
    #: Indicates if the store front is password protected
    password_enabled = models.BooleanField(default=False)
    domain = models.TextField(null=True)

    # Location information
    province_code = models.CharField(max_length=2)
    zip = models.TextField(blank=True)
    country_code = models.CharField(max_length=2)
    country = models.TextField(default='US')
    primary_locale = models.CharField(max_length=10)
    primary_location_id = models.BigIntegerField(null=True)
    province = models.TextField()
    city = models.TextField()
    address1 = models.TextField()
    phone = models.TextField()
    country_name = models.TextField()
    latitude = models.FloatField(default=None, null=True)
    longitude = models.FloatField(default=None, null=True)
    timezone = models.TextField(default='(GMT-05:00) Eastern Time (US & Canada)')
    #: https://www.iana.org/time-zones
    iana_timezone = models.TextField(null=True)

    # Plan information
    plan_name = models.CharField(max_length=25, null=True)
    plan_display_name = models.CharField(max_length=25)
    #: Referral code
    source = models.TextField(default=None, null=True)

    # Taxes
    county_taxes = models.NullBooleanField(default=None)
    tax_shipping = models.NullBooleanField(default=None)
    taxes_included = models.NullBooleanField(default=None)

    # Currency/format strings
    currency = models.CharField(max_length=3)
    money_in_emails_format = models.TextField(default='${{amount}}')
    money_with_currency_in_emails_format = models.TextField(default='${{amount}} USD')
    money_with_currency_format = models.TextField(default='$ {{amount}} USD')
    money_format = models.TextField(default='$ {{amount}}')

    # Google Apps settings
    google_apps_login_enabled = models.NullBooleanField(default=None, null=True)
    google_apps_domain = models.TextField(default=None, null=True)

    # Other
    requires_extra_payments_agreement = models.BooleanField(default=False)
    eligible_for_payments = models.BooleanField(default=True)
