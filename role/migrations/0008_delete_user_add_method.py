# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0007_user_add_method'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User_add_method',
        ),
    ]
