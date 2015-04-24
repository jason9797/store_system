# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0005_issuing_person_cut_server_cut_user_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuing_person_cut',
            name='jointime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 17, 3, 33, 29, 611487, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server_cut',
            name='jointime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 17, 3, 33, 37, 427673, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
