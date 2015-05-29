# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0004_auto_20150529_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last_order_name',
            field=models.TextField(null=True),
        ),
    ]
