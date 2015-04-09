# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20150408_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorder_state',
            name='level',
            field=models.IntegerField(null=True, verbose_name=b'\xe7\xba\xa7\xe5\x88\xab', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_state',
            name='level',
            field=models.IntegerField(null=True, verbose_name=b'\xe7\xba\xa7\xe5\x88\xab', blank=True),
            preserve_default=True,
        ),
    ]
