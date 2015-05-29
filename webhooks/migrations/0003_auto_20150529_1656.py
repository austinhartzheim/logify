# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0002_auto_20150527_1803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('shopify_id', models.BigIntegerField(unique=True)),
                ('name', models.TextField(blank=True)),
                ('has_storefront', models.BooleanField(default=False)),
                ('myshopify_domain', models.TextField(blank=True, null=True)),
                ('created_at', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254)),
                ('customer_email', models.EmailField(blank=True, max_length=254)),
                ('shop_owner', models.TextField()),
                ('password_enabled', models.BooleanField(default=False)),
                ('domain', models.TextField(null=True)),
                ('province_code', models.CharField(max_length=2)),
                ('zip', models.TextField(blank=True)),
                ('country_code', models.CharField(max_length=2)),
                ('country', models.TextField(default='US')),
                ('primary_locale', models.CharField(max_length=10)),
                ('primary_location_id', models.BigIntegerField(null=True)),
                ('province', models.TextField()),
                ('city', models.TextField()),
                ('address1', models.TextField()),
                ('phone', models.TextField()),
                ('country_name', models.TextField()),
                ('latitude', models.FloatField(null=True, default=None)),
                ('longitude', models.FloatField(null=True, default=None)),
                ('timezone', models.TextField(default='(GMT-05:00) Eastern Time (US & Canada)')),
                ('iana_timezone', models.TextField(null=True)),
                ('plan_name', models.CharField(null=True, max_length=25)),
                ('plan_display_name', models.CharField(max_length=25)),
                ('source', models.TextField(null=True, default=None)),
                ('county_taxes', models.NullBooleanField(default=None)),
                ('tax_shipping', models.NullBooleanField(default=None)),
                ('taxes_included', models.NullBooleanField(default=None)),
                ('currency', models.CharField(max_length=3)),
                ('money_in_emails_format', models.TextField(default='${{amount}}')),
                ('money_with_currency_in_emails_format', models.TextField(default='${{amount}} USD')),
                ('money_with_currency_format', models.TextField(default='$ {{amount}} USD')),
                ('money_format', models.TextField(default='$ {{amount}}')),
                ('google_apps_login_enabled', models.NullBooleanField(default=None)),
                ('google_apps_domain', models.TextField()),
                ('requires_extra_payments_agreement', models.BooleanField(default=False)),
                ('eligible_for_payments', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='orders_count',
            field=models.IntegerField(default=0),
        ),
    ]
