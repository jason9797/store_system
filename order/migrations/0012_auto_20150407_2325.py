# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import order.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20150404_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='detail',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderfile',
            name='file',
            field=models.FileField(upload_to=b'order/%Y/%m/%d', validators=[order.models.validate_file_extension]),
            preserve_default=True,
        ),
    ]
