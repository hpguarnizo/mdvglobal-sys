# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-08 14:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import s3direct.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities_light', '0006_compensate_for_0003_bytestring_bug'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.CharField(max_length=256)),
                ('total', models.FloatField()),
                ('ciudad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.City')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.FloatField()),
                ('cantidad', models.IntegerField()),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.Compra')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
                ('descripcion', models.TextField()),
                ('precio', models.FloatField()),
                ('archivo', s3direct.fields.S3DirectField(blank=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.CategoriaProducto')),
            ],
        ),
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Enviado',
            fields=[
                ('estadocompra_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tienda.EstadoCompra')),
            ],
            bases=('tienda.estadocompra',),
        ),
        migrations.CreateModel(
            name='Incompleta',
            fields=[
                ('estadocompra_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tienda.EstadoCompra')),
            ],
            bases=('tienda.estadocompra',),
        ),
        migrations.CreateModel(
            name='Pagado',
            fields=[
                ('estadocompra_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tienda.EstadoCompra')),
            ],
            bases=('tienda.estadocompra',),
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.TipoProducto'),
        ),
        migrations.AddField(
            model_name='detallecompra',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.Producto'),
        ),
        migrations.AddField(
            model_name='compra',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.EstadoCompra'),
        ),
        migrations.AddField(
            model_name='compra',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.Region'),
        ),
        migrations.AddField(
            model_name='compra',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
