# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-17 06:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20180317_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cursospostulantes',
            name='nombre',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_cursos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cursospostulantes',
            name='tipo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_tipo_cursos'),
            preserve_default=False,
        ),
    ]
