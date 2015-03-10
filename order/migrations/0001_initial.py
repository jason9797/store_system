# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0001_initial'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=30, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
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
                ('sex', models.BooleanField(verbose_name=b'\xe6\x80\xa7\xe5\x88\xab')),
            ],
            options={
                'verbose_name': '\u5ba2\u6237',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer_Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=1, choices=[(1, b'vip'), (2, b'vvip'), (3, b'vvvip')])),
            ],
            options={
                'verbose_name': '\u5ba2\u6237\u6c34\u5e73',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivery_no', models.CharField(default=b'', max_length=30, verbose_name=b'\xe5\xbf\xab\xe9\x80\x92\xe5\x8d\x95\xe5\x8f\xb7')),
                ('fact_money', models.DecimalField(default=0, verbose_name=b'\xe5\xae\x9e\xe6\x94\xb6\xe9\x87\x91\xe9\xa2\x9d', max_digits=4, decimal_places=2)),
                ('customer', models.ForeignKey(to='order.Customer')),
                ('issuing_person', models.ForeignKey(to='role.Issuing_person')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order_State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u72b6\u6001',
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
                ('product', models.ForeignKey(to='order.Product')),
                ('stock', models.ForeignKey(to='stock.Stock')),
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
            field=models.ForeignKey(to='order.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(to='order.Order_State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='level',
            field=models.ForeignKey(to='order.Customer_Level'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact_info',
            name='customer',
            field=models.ForeignKey(to='order.Customer'),
            preserve_default=True,
        ),
    ]
