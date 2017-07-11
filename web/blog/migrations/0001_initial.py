# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-27 14:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeValidatorBlog',
            fields=[
                ('code', models.CharField(max_length=40, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=60)),
                ('confirmed', models.NullBooleanField(default=False)),
                ('subscribe_email', models.NullBooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='codevalidatorblog',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Subscriber'),
        ),
    ]
