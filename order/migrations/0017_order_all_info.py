# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_auto_20150410_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_all_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_no', models.IntegerField(verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95id')),
                ('delivery_no', models.CharField(default=b'', max_length=30, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x8d\x95\xe5\x8f\xb7')),
                ('fact_money', models.DecimalField(default=0, verbose_name=b'\xe5\xae\x9e\xe6\x94\xb6\xe9\x87\x91\xe9\xa2\x9d', max_digits=4, decimal_places=2)),
                ('customer_name', models.CharField(max_length=100, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7\xe5\x90\x8d\xe7\xa7\xb0')),
                ('customer_sex', models.BooleanField(default=True, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7\xe6\x80\xa7\xe5\x88\xab')),
                ('customer_level', models.IntegerField(default=1)),
                ('customer_level_name', models.CharField(max_length=100, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7\xe7\xad\x89\xe7\xba\xa7\xe5\x90\x8d\xe7\xa7\xb0')),
                ('user_first_name', models.CharField(max_length=100, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xae\xa2\xe6\x9c\x8d\xe5\xa7\x93\xe5\x90\x8d')),
                ('user_username', models.CharField(max_length=100, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xae\xa2\xe6\x9c\x8d\xe8\xb4\xa6\xe5\x8f\xb7')),
                ('user_group_name', models.CharField(max_length=100, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xae\xa2\xe6\x9c\x8d\xe8\xa7\x92\xe8\x89\xb2')),
                ('address', models.CharField(max_length=100, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80')),
                ('phone_number', models.CharField(max_length=20, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81')),
                ('issuing_person', models.CharField(max_length=100, verbose_name=b'\xe5\x87\xba\xe5\x8d\x95\xe4\xba\xba')),
                ('product_name', models.CharField(max_length=100, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x90\x8d\xe7\xa7\xb0')),
                ('product_price', models.DecimalField(default=0, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc', max_digits=4, decimal_places=2)),
                ('product_delivery_type', models.CharField(max_length=100, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x90\x8d\xe7\xa7\xb0')),
                ('state_name', models.CharField(max_length=100, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8d\xe7\xa7\xb0')),
                ('state_level', models.IntegerField(verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe7\xad\x89\xe7\xba\xa7')),
                ('remark', models.CharField(max_length=100, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8')),
                ('jointime', models.DateTimeField(verbose_name=b'\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u8be6\u60c5',
            },
            bases=(models.Model,),
        ),
    ]
