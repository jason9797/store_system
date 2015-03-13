# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20150306_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='jointime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 9, 32, 37, 2234, tzinfo=utc), verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock_channel',
            name='jointime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 9, 32, 43, 98837, tzinfo=utc), verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock_management',
            name='jointime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 9, 32, 55, 619307, tzinfo=utc), verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
    ]
