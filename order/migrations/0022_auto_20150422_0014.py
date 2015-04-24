# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_auto_20150421_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_all_info',
            name='fact_money',
            field=models.CharField(max_length=10, null=True, verbose_name=b'\xe5\xae\x9e\xe6\x94\xb6\xe9\x87\x91\xe9\xa2\x9d', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='product_price',
            field=models.CharField(max_length=10, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc', blank=True),
            preserve_default=True,
        ),
    ]
