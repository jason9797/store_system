# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('role', '0003_historicalissuing_person_historicalrole_historicaluserprofile'),
        ('order', '0004_historicalcontact_info_historicalcustomer_historicalcustomer_level_historicalorder_historicalorder_s'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='issuing_person',
            field=models.ForeignKey(default=1, to='role.Issuing_person'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalcustomer',
            name='issuing_person_id',
            field=models.IntegerField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalcustomer',
            name='user_id',
            field=models.IntegerField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
