# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock_management',
            name='stock_mode',
            field=models.BooleanField(default=True, verbose_name=b'\xe5\x87\xba/\xe5\x85\xa5\xe5\xba\x93'),
            preserve_default=True,
        ),
    ]
