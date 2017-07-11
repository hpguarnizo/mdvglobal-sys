# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-10 03:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0005_auto_20170706_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='evento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evento.Evento'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='ciudad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.Region'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='codigo',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='estado',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='evento.EstadoEntrada'),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='nombre',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
