# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-29 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maestros', '0003_peq_mae_tipo_atencion'),
    ]

    operations = [
        migrations.AddField(
            model_name='peq_mae_provincias',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
