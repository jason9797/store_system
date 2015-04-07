# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20150320_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_info',
            name='default',
            field=models.BooleanField(default=False, verbose_name=b'\xe9\xbb\x98\xe8\xae\xa4\xe6\x96\xb9\xe5\xbc\x8f'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalcontact_info',
            name='default',
            field=models.BooleanField(default=False, verbose_name=b'\xe9\xbb\x98\xe8\xae\xa4\xe6\x96\xb9\xe5\xbc\x8f'),
            preserve_default=True,
        ),
    ]
