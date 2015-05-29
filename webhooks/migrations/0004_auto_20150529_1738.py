# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0003_auto_20150529_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='google_apps_domain',
            field=models.TextField(default=None, null=True),
        ),
    ]
