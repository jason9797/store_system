# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0003_auto_20150312_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalContact_info',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('address', models.CharField(max_length=30, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('customer_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u8054\u7cfb\u65b9\u5f0f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalCustomer',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('sex', models.BooleanField(default=True, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab')),
                ('level_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('jointime', models.DateTimeField(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u5ba2\u6237',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalCustomer_Level',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('level', models.IntegerField(default=1, choices=[(1, b'vip'), (2, b'vvip'), (3, b'vvvip')])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u5ba2\u6237\u6c34\u5e73',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalOrder',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('delivery_no', models.CharField(default=b'', max_length=30, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x8d\x95\xe5\x8f\xb7')),
                ('fact_money', models.DecimalField(default=0, verbose_name=b'\xe5\xae\x9e\xe6\x94\xb6\xe9\x87\x91\xe9\xa2\x9d', max_digits=4, decimal_places=2)),
                ('customer_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('issuing_person_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('product_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('state_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('jointime', models.DateTimeField(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u8ba2\u5355',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalOrder_State',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u8ba2\u5355\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('price', models.DecimalField(verbose_name=b'\xe4\xbb\xb7\xe9\x92\xb1', max_digits=6, decimal_places=2)),
                ('delivery_type', models.CharField(max_length=100, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe7\xb1\xbb\xe5\x9e\x8b', blank=True)),
                ('jointime', models.DateTimeField(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u4ea7\u54c1',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalStock_Product',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('quantity', models.DecimalField(verbose_name=b'\xe7\xb3\xbb\xe6\x95\xb0', max_digits=4, decimal_places=2)),
                ('delivery_bill', models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xbf\x90\xe8\xb4\xb9')),
                ('product_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('stock_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u4ea7\u54c1\u539f\u6599\u5173\u7cfb',
            },
            bases=(models.Model,),
        ),
    ]
