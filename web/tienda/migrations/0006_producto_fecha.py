# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-11 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_auto_20170711_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='fecha',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
