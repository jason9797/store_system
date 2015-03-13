# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20150306_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='jointime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 9, 32, 6, 955256, tzinfo=utc), verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='jointime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 9, 32, 17, 948030, tzinfo=utc), verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='jointime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 9, 32, 30, 345907, tzinfo=utc), verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
    ]
