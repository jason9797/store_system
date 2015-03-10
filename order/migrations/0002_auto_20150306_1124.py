# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='sex',
            field=models.BooleanField(default=True, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab'),
            preserve_default=True,
        ),
    ]
