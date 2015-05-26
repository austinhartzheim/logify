# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shopify_id', models.BigIntegerField(null=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('verified_email', models.BooleanField(default=False)),
                ('first_name', models.TextField(blank=True)),
                ('last_name', models.TextField(blank=True)),
                ('note', models.TextField(blank=True)),
                ('last_order_id', models.BigIntegerField(null=True)),
                ('orders_count', models.IntegerField()),
                ('total_spent', models.DecimalField(default=0, max_digits=9, decimal_places=2)),
                ('state', models.CharField(max_length=20)),
                ('tax_exempt', models.BooleanField(default=False)),
                ('accepts_marketing', models.BooleanField(default=False)),
                ('multipass_identifier', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shopify_id', models.BigIntegerField()),
                ('default', models.BooleanField(default=False)),
                ('name', models.TextField(blank=True)),
                ('first_name', models.TextField(blank=True)),
                ('last_name', models.TextField(blank=True)),
                ('company', models.TextField(blank=True)),
                ('address1', models.TextField(blank=True)),
                ('address2', models.TextField(blank=True)),
                ('city', models.TextField(blank=True)),
                ('country', models.CharField(max_length=50)),
                ('country_code', models.CharField(max_length=2)),
                ('country_name', models.CharField(max_length=50)),
                ('province', models.TextField(blank=True)),
                ('province_code', models.CharField(max_length=2)),
                ('zip', models.TextField(blank=True)),
                ('phone', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='addresses',
            field=models.ManyToManyField(to='webhooks.CustomerAddress'),
        ),
        migrations.AddField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(to='webhooks.CustomerTag'),
        ),
    ]
