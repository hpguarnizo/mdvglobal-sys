# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-04 12:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0002_auto_20170704_1255'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ciudad',
            name='pais',
        ),
        migrations.DeleteModel(
            name='Ciudad',
        ),
        migrations.DeleteModel(
            name='Pais',
        ),
    ]
