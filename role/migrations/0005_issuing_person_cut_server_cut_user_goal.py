# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('role', '0004_auto_20150331_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issuing_person_cut',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cut_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=2, blank=True, null=True, verbose_name=b'\xe6\x8f\x90\xe6\x88\x90\xe7\xb3\xbb\xe6\x95\xb0')),
                ('issuing_person', models.ForeignKey(verbose_name=b'\xe5\x87\xba\xe5\x8d\x95\xe4\xba\xba', to='role.Issuing_person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='server_cut',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cut_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=2, blank=True, null=True, verbose_name=b'\xe6\x8f\x90\xe6\x88\x90\xe7\xb3\xbb\xe6\x95\xb0')),
                ('server', models.ForeignKey(verbose_name=b'\xe5\xae\xa2\xe6\x9c\x8d', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='user_goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goal_quantity', models.IntegerField(null=True, verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe9\x87\x8f', blank=True)),
                ('goal_money', models.DecimalField(decimal_places=2, default=0, max_digits=7, blank=True, null=True, verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe6\x88\x90\xe4\xba\xa4\xe9\xa2\x9d')),
                ('goal_chosen', models.BooleanField(default=0, verbose_name=b'0:\xe5\x87\xba\xe5\x8d\x95\xe9\x87\x8f,1:\xe7\x9b\xae\xe6\xa0\x87\xe9\xa2\x9d')),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
