# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0003_auto_20150312_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalStock',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('detail', models.CharField(max_length=100, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('price', models.DecimalField(verbose_name=b'\xe5\x8d\x95\xe4\xbb\xb7', max_digits=6, decimal_places=2)),
                ('quantity', models.IntegerField(verbose_name=b'\xe6\x95\xb0\xe9\x87\x8f')),
                ('stock_type_id', models.IntegerField(db_index=True, null=True, verbose_name=b'\xe7\xb1\xbb\xe5\x88\xab', blank=True)),
                ('stock_channel_id', models.IntegerField(db_index=True, null=True, verbose_name=b'\xe8\xbf\x9b\xe8\xb4\xa7\xe6\xb8\xa0\xe9\x81\x93', blank=True)),
                ('jointime', models.DateTimeField(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u539f\u6599',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalStock_Channel',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('company', models.CharField(max_length=100, verbose_name=b'\xe5\x85\xac\xe5\x8f\xb8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('person', models.CharField(max_length=50, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('jointime', models.DateTimeField(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u539f\u6599\u6e20\u9053',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalStock_Management',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('stock_mode', models.BooleanField(default=True, verbose_name=b'\xe5\x87\xba/\xe5\x85\xa5\xe5\xba\x93')),
                ('stock_id', models.IntegerField(db_index=True, null=True, verbose_name=b'\xe5\x8e\x9f\xe6\x96\x99', blank=True)),
                ('mode_id', models.IntegerField(db_index=True, null=True, verbose_name=b'\xe5\x87\xba\xe5\x85\xa5\xe6\x96\xb9\xe5\xbc\x8f', blank=True)),
                ('jointime', models.DateTimeField(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u5e93\u5b58\u7ba1\u7406',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalStock_Mode',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('method', models.CharField(max_length=200, verbose_name=b'\xe6\x96\xb9\xe5\xbc\x8f')),
                ('description', models.CharField(max_length=100, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u51fa\u5165\u65b9\u5f0f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalStock_Type',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('type_name', models.CharField(max_length=50, verbose_name=b'\xe7\xb1\xbb\xe5\x88\xab\xe5\x90\x8d\xe7\xa7\xb0')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical \u539f\u6599\u7c7b\u522b',
            },
            bases=(models.Model,),
        ),
    ]
