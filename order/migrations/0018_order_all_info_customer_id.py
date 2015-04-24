# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_order_all_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_all_info',
            name='customer_id',
            field=models.IntegerField(default=1, verbose_name=b'\xe9\xa1\xbe\xe5\xae\xa2id'),
            preserve_default=False,
        ),
    ]
