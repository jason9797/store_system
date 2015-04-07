# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import order.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_historicalcustomerfile_historicalorderfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_info',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Customer', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='issuing_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='role.Issuing_person', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Customer_Level', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customerfile',
            name='file',
            field=models.FileField(upload_to=b'customer/%Y/%m/%d', validators=[order.models.validate_file_extension]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Customer', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='issuing_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='role.Issuing_person', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Product', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Order_State', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stock_product',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.Product', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stock_product',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='stock.Stock', null=True),
            preserve_default=True,
        ),
    ]
