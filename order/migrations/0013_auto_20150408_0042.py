# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_auto_20150407_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='remark',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='remark',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True),
            preserve_default=True,
        ),
    ]
