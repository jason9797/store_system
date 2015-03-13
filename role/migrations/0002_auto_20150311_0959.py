# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u89d2\u8272',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '\u7528\u6237\u89d2\u8272\u5173\u7cfb'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(to='role.Role'),
            preserve_default=True,
        ),
    ]
