# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_order_all_info_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_all_info',
            name='address',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='customer_id',
            field=models.IntegerField(null=True, verbose_name=b'\xe9\xa1\xbe\xe5\xae\xa2id', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='customer_level',
            field=models.IntegerField(default=1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='customer_level_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7\xe7\xad\x89\xe7\xba\xa7\xe5\x90\x8d\xe7\xa7\xb0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='customer_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7\xe5\x90\x8d\xe7\xa7\xb0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='delivery_no',
            field=models.CharField(default=b'', max_length=30, null=True, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x8d\x95\xe5\x8f\xb7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='fact_money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, blank=True, null=True, verbose_name=b'\xe5\xae\x9e\xe6\x94\xb6\xe9\x87\x91\xe9\xa2\x9d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='issuing_person',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe5\x87\xba\xe5\x8d\x95\xe4\xba\xba', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='order_no',
            field=models.IntegerField(null=True, verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95id', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='product_delivery_type',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x90\x8d\xe7\xa7\xb0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='product_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x90\x8d\xe7\xa7\xb0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='product_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, blank=True, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='remark',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='state_level',
            field=models.IntegerField(null=True, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe7\xad\x89\xe7\xba\xa7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='state_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8d\xe7\xa7\xb0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='user_first_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xae\xa2\xe6\x9c\x8d\xe5\xa7\x93\xe5\x90\x8d', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='user_group_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xae\xa2\xe6\x9c\x8d\xe8\xa7\x92\xe8\x89\xb2', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order_all_info',
            name='user_username',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xae\xa2\xe6\x9c\x8d\xe8\xb4\xa6\xe5\x8f\xb7', blank=True),
            preserve_default=True,
        ),
    ]
