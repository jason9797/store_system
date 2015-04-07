# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_auto_20150324_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='stock_channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe8\xbf\x9b\xe8\xb4\xa7\xe6\xb8\xa0\xe9\x81\x93', blank=True, to='stock.Stock_Channel', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe7\xb1\xbb\xe5\x88\xab', blank=True, to='stock.Stock_Type', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stock_management',
            name='mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe5\x87\xba\xe5\x85\xa5\xe6\x96\xb9\xe5\xbc\x8f', blank=True, to='stock.Stock_Mode', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stock_management',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81', blank=True, to='order.Product', null=True),
            preserve_default=True,
        ),
    ]
