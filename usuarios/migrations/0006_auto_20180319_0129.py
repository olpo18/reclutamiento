# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-19 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_auto_20180317_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='numero_documento',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
