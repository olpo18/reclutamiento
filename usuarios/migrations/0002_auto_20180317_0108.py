# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-17 06:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maestros', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CursosPostulantes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('nombre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_cursos')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Persona')),
                ('tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_tipo_cursos')),
            ],
            options={
                'verbose_name': 'Cursos del postulante',
            },
        ),
        migrations.AlterUniqueTogether(
            name='cursospostulantes',
            unique_together=set([('persona', 'tipo', 'nombre')]),
        ),
    ]
