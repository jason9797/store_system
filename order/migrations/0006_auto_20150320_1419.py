# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20150317_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='issuing_person',
            field=models.ForeignKey(to='role.Issuing_person', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='issuing_person',
            field=models.ForeignKey(to='role.Issuing_person', null=True),
            preserve_default=True,
        ),
    ]
