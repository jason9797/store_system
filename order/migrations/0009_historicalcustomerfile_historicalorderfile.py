# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import order.models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0008_customerfile_orderfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCustomerFile',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\xa0\x87\xe9\xa2\x98')),
                ('file', models.TextField(max_length=100, validators=[order.models.validate_file_extension])),
                ('jointime', models.DateTimeField(verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u5ba2\u6237\u5bfc\u5165',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalOrderFile',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\xa0\x87\xe9\xa2\x98')),
                ('file', models.TextField(max_length=100, validators=[order.models.validate_file_extension])),
                ('jointime', models.DateTimeField(verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u8ba2\u5355\u5bfc\u5165',
            },
            bases=(models.Model,),
        ),
    ]
