# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20150331_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='issuing_person',
        ),
        migrations.RemoveField(
            model_name='historicalcustomer',
            name='issuing_person_id',
        ),
    ]
