# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-03 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('convocatorias', '0011_auto_20180402_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peq_int_convocatoria_academico',
            name='carrera',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_carreras'),
        ),
        migrations.AlterField(
            model_name='peq_int_convocatoria_academico',
            name='familia_carrera',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_familia_carreras'),
        ),
    ]
