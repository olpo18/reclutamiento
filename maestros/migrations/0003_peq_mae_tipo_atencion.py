# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-26 04:43
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('maestros', '0002_auto_20180321_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='PEQ_MAE_tipo_atencion',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200, unique=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Tipo de atenci\xf3n',
                'verbose_name_plural': 'Tipos de atenciones',
            },
        ),
    ]
