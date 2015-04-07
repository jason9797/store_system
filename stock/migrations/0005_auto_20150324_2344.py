# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20150323_0945'),
        ('stock', '0004_historicalstock_historicalstock_channel_historicalstock_management_historicalstock_mode_historicalst'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalstock_management',
            name='stock_id',
        ),
        migrations.RemoveField(
            model_name='stock_management',
            name='stock',
        ),
        migrations.AddField(
            model_name='historicalstock_management',
            name='product_id',
            field=models.IntegerField(db_index=True, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stock_management',
            name='product',
            field=models.ForeignKey(default=1, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81', to='order.Product'),
            preserve_default=False,
        ),
    ]
