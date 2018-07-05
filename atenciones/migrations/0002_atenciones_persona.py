# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-18 05:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0012_persona_ingles'),
        ('atenciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='atenciones',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.Persona'),
        ),
    ]
