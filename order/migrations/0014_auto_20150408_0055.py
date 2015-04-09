# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_auto_20150408_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder_state',
            name='level',
            field=models.IntegerField(default=1, verbose_name=b'\xe7\xba\xa7\xe5\x88\xab'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_state',
            name='level',
            field=models.IntegerField(default=1, verbose_name=b'\xe7\xba\xa7\xe5\x88\xab'),
            preserve_default=False,
        ),
    ]
