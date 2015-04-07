# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import order.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20150323_0945'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\xa0\x87\xe9\xa2\x98')),
                ('file', models.FileField(upload_to=b'/customer/%Y/%m/%d', validators=[order.models.validate_file_extension])),
                ('jointime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u5ba2\u6237\u5bfc\u5165',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\xa0\x87\xe9\xa2\x98')),
                ('file', models.FileField(upload_to=b'/order/%Y/%m/%d', validators=[order.models.validate_file_extension])),
                ('jointime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u5bfc\u5165',
            },
            bases=(models.Model,),
        ),
    ]
