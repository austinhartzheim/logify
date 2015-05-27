# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='shopify_id',
            field=models.BigIntegerField(unique=True, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='shopify_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='customertag',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
