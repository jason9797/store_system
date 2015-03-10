# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('detail', models.CharField(max_length=100, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('price', models.DecimalField(verbose_name=b'\xe5\x8d\x95\xe4\xbb\xb7', max_digits=6, decimal_places=2)),
                ('quantity', models.IntegerField(verbose_name=b'\xe6\x95\xb0\xe9\x87\x8f')),
            ],
            options={
                'verbose_name': '\u539f\u6599',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stock_Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=100, verbose_name=b'\xe5\x85\xac\xe5\x8f\xb8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('person', models.CharField(max_length=50, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe7\xa0\x81', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
            ],
            options={
                'verbose_name': '\u539f\u6599\u6e20\u9053',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stock_Management',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stock_mode', models.BooleanField(verbose_name=b'\xe5\x87\xba/\xe5\x85\xa5\xe5\xba\x93')),
            ],
            options={
                'verbose_name': '\u5e93\u5b58\u7ba1\u7406',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stock_Mode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('method', models.CharField(max_length=200, verbose_name=b'\xe6\x96\xb9\xe5\xbc\x8f')),
                ('description', models.CharField(max_length=100, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0')),
            ],
            options={
                'verbose_name': '\u51fa\u5165\u65b9\u5f0f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stock_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=50, verbose_name=b'\xe7\xb1\xbb\xe5\x88\xab\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u539f\u6599\u7c7b\u522b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='stock_management',
            name='mode',
            field=models.ForeignKey(verbose_name=b'\xe5\x87\xba\xe5\x85\xa5\xe6\x96\xb9\xe5\xbc\x8f', to='stock.Stock_Mode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stock_management',
            name='stock',
            field=models.ForeignKey(verbose_name=b'\xe5\x8e\x9f\xe6\x96\x99', to='stock.Stock'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stock',
            name='stock_channel',
            field=models.ForeignKey(verbose_name=b'\xe8\xbf\x9b\xe8\xb4\xa7\xe6\xb8\xa0\xe9\x81\x93', to='stock.Stock_Channel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stock',
            name='stock_type',
            field=models.ForeignKey(verbose_name=b'\xe7\xb1\xbb\xe5\x88\xab', to='stock.Stock_Type'),
            preserve_default=True,
        ),
    ]
