# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-04 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.City'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.City'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='descripcion',
            field=models.TextField(),
        ),
    ]
