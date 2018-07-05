# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-27 02:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_auto_20180323_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='tipo_tiempo_residencia',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'MESES'), (1, 'A\xd1OS')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='tiempo_residencia',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
