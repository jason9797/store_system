# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import order.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('role', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=30, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('default', models.BooleanField(default=False, verbose_name=b'\xe9\xbb\x98\xe8\xae\xa4\xe6\x96\xb9\xe5\xbc\x8f')),
            ],
            options={
                'verbose_name': '\u8054\u7cfb\u65b9\u5f0f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('sex', models.BooleanField(default=True, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab')),
                ('jointime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u5ba2\u6237',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer_Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer', models.CharField(max_length=50, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('content', models.CharField(max_length=255, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('add_user', models.CharField(max_length=50, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe4\xba\xba')),
                ('alert_time', models.DateTimeField(verbose_name=b'\xe6\x8f\x90\xe9\x86\x92\xe6\x97\xb6\xe9\x97\xb4')),
                ('alert_state', models.BooleanField(default=0, verbose_name=b'\xe6\x8f\x90\xe9\x86\x92\xe7\x8a\xb6\xe6\x80\x81')),
                ('task_id', models.CharField(max_length=b'100', null=True, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1id', blank=True)),
                ('jointime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
                ('alert_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe6\x8f\x90\xe9\x86\x92\xe4\xba\xba', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u5ba2\u6237\u63d0\u9192',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer_Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=1, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '\u5ba2\u6237\u6c34\u5e73',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\xa0\x87\xe9\xa2\x98')),
                ('file', models.FileField(upload_to=b'customer/%Y/%m/%d', validators=[order.models.validate_file_extension])),
                ('jointime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u5ba2\u6237\u5bfc\u5165',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalContact_info',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('address', models.CharField(max_length=30, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('customer_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('default', models.BooleanField(default=False, verbose_name=b'\xe9\xbb\x98\xe8\xae\xa4\xe6\x96\xb9\xe5\xbc\x8f')),
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
                ('user_id', models.IntegerField(db_index=True, null=True, blank=True)),
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
                ('level', models.IntegerField(default=1, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('name', models.CharField(max_length=100)),
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
            name='HistoricalOrder',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('delivery_no', models.CharField(default=b'', max_length=30, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x8d\x95\xe5\x8f\xb7')),
                ('fact_money', models.DecimalField(default=0, verbose_name=b'\xe5\xae\x9e\xe6\x94\xb6\xe9\x87\x91\xe9\xa2\x9d', max_digits=4, decimal_places=2)),
                ('customer_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('issuing_person_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('product_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('state_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('remark', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
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
                ('level', models.IntegerField(null=True, verbose_name=b'\xe7\xba\xa7\xe5\x88\xab', blank=True)),
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
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('price', models.DecimalField(verbose_name=b'\xe4\xbb\xb7\xe9\x92\xb1', max_digits=6, decimal_places=2)),
                ('delivery_type', models.CharField(max_length=100, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe7\xb1\xbb\xe5\x9e\x8b', blank=True)),
                ('detail', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
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
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivery_no', models.CharField(default=b'', max_length=30, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x8d\x95\xe5\x8f\xb7')),
                ('fact_money', models.DecimalField(default=0, verbose_name=b'\xe5\xae\x9e\xe6\x94\xb6\xe9\x87\x91\xe9\xa2\x9d', max_digits=4, decimal_places=2)),
                ('remark', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('jointime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Customer', null=True)),
                ('issuing_person', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='role.Issuing_person', null=True)),
            ],
            options={
                'verbose_name': '\u8ba2\u5355',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order_all_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_no', models.IntegerField(null=True, verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95id', blank=True)),
                ('delivery_no', models.CharField(default=b'', max_length=30, null=True, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x8d\x95\xe5\x8f\xb7', blank=True)),
                ('fact_money', models.CharField(max_length=10, null=True, verbose_name=b'\xe5\xae\x9e\xe6\x94\xb6\xe9\x87\x91\xe9\xa2\x9d', blank=True)),
                ('customer_id', models.IntegerField(null=True, verbose_name=b'\xe9\xa1\xbe\xe5\xae\xa2id', blank=True)),
                ('customer_name', models.CharField(max_length=100, null=True, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('customer_sex', models.BooleanField(default=True, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7\xe6\x80\xa7\xe5\x88\xab')),
                ('customer_level', models.IntegerField(default=1, null=True, blank=True)),
                ('customer_level_name', models.CharField(max_length=100, null=True, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7\xe7\xad\x89\xe7\xba\xa7\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('user_first_name', models.CharField(max_length=100, null=True, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xae\xa2\xe6\x9c\x8d\xe5\xa7\x93\xe5\x90\x8d', blank=True)),
                ('user_username', models.CharField(max_length=100, null=True, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xae\xa2\xe6\x9c\x8d\xe8\xb4\xa6\xe5\x8f\xb7', blank=True)),
                ('user_group_name', models.CharField(max_length=100, null=True, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xae\xa2\xe6\x9c\x8d\xe8\xa7\x92\xe8\x89\xb2', blank=True)),
                ('address', models.CharField(max_length=100, null=True, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80', blank=True)),
                ('phone_number', models.CharField(max_length=20, null=True, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', blank=True)),
                ('issuing_person', models.CharField(max_length=100, null=True, verbose_name=b'\xe5\x87\xba\xe5\x8d\x95\xe4\xba\xba', blank=True)),
                ('product_name', models.CharField(max_length=100, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('product_price', models.CharField(max_length=10, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc', blank=True)),
                ('product_delivery_type', models.CharField(max_length=100, null=True, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('state_name', models.CharField(max_length=100, null=True, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('state_level', models.IntegerField(null=True, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe7\xad\x89\xe7\xba\xa7', blank=True)),
                ('remark', models.CharField(max_length=100, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('jointime', models.DateTimeField(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u8be6\u60c5',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order_Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=255, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('jointime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95\xe5\x8f\xb7', blank=True, to='order.Order', null=True)),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u7eaa\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order_State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('level', models.IntegerField(null=True, verbose_name=b'\xe7\xba\xa7\xe5\x88\xab', blank=True)),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\xa0\x87\xe9\xa2\x98')),
                ('file', models.FileField(upload_to=b'order/%Y/%m/%d', validators=[order.models.validate_file_extension])),
                ('jointime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u5bfc\u5165',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('price', models.DecimalField(verbose_name=b'\xe4\xbb\xb7\xe9\x92\xb1', max_digits=6, decimal_places=2)),
                ('delivery_type', models.CharField(max_length=100, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe7\xb1\xbb\xe5\x9e\x8b', blank=True)),
                ('detail', models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('jointime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u4ea7\u54c1',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stock_Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(verbose_name=b'\xe7\xb3\xbb\xe6\x95\xb0', max_digits=4, decimal_places=2)),
                ('delivery_bill', models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xbf\x90\xe8\xb4\xb9')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Product', null=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='stock.Stock', null=True)),
            ],
            options={
                'verbose_name': '\u4ea7\u54c1\u539f\u6599\u5173\u7cfb',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.ManyToManyField(to='stock.Stock', through='order.Stock_Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Product', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Order_State', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Customer_Level', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact_info',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Customer', null=True),
            preserve_default=True,
        ),
    ]
