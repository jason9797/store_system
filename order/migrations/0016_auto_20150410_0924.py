# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_auto_20150408_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_level',
            name='name',
            field=models.CharField(default='ceshi1', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalcustomer_level',
            name='name',
            field=models.CharField(default='ceshi2', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer_level',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalcustomer_level',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')]),
            preserve_default=True,
        ),
    ]
