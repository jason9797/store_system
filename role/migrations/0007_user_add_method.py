# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('role', '0006_auto_20150417_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_add_method',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
    ]
