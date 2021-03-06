# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-11 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import s3direct.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pay', '0002_auto_20170711_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaContenido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Contenido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
                ('descripcion', models.TextField()),
                ('imagen', s3direct.fields.S3DirectField(blank=True, null=True)),
                ('archivo', s3direct.fields.S3DirectField(blank=True, null=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('acceso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pay.Plan')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenido.CategoriaContenido')),
            ],
        ),
        migrations.CreateModel(
            name='TipoContenido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='contenido',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenido.TipoContenido'),
        ),
    ]
