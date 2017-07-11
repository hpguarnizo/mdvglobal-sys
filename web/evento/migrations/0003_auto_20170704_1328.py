# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-04 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0002_auto_20170704_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='asistentes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='evento',
            name='ciudad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.City'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='cupo',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evento',
            name='direccion',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
