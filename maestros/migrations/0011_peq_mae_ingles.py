# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-15 21:17
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('maestros', '0010_auto_20180502_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='PEQ_MAE_ingles',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200, unique=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Ingles',
                'verbose_name_plural': 'Ingles',
            },
        ),
    ]
