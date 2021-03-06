# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-17 06:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import maestros.helpers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maestros', '0001_initial'),
        ('contratistas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bloqueados',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('numero_documento', models.CharField(max_length=255)),
                ('nombres', models.CharField(blank=True, max_length=255, null=True)),
                ('apellidos', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('celular', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Bloqueados',
                'verbose_name_plural': 'Bloqueados',
            },
        ),
        migrations.CreateModel(
            name='DocumentosPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('documento', models.FileField(upload_to=maestros.helpers.get_file_path)),
            ],
            options={
                'verbose_name': 'Documento personal',
                'verbose_name_plural': 'Documentos personales',
            },
        ),
        migrations.CreateModel(
            name='InformacionEducativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('hasta_actualidad', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_carreras')),
                ('centro_estudio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_centros_estudio')),
                ('estado_grado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_estado_grado')),
                ('familia_carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_familia_carreras')),
                ('grado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_grado')),
            ],
            options={
                'verbose_name': 'Informaci\xf3n educativa',
                'verbose_name_plural': 'Informaci\xf3n educativa',
            },
        ),
        migrations.CreateModel(
            name='InformacionLaboral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('hasta_actualidad', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_empresas')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_familia')),
                ('familia_puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_familia_puesto')),
            ],
            options={
                'verbose_name': 'Informaci\xf3n laboral',
                'verbose_name_plural': 'Informaci\xf3n laboral',
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('nombres', models.CharField(blank=True, max_length=255, null=True)),
                ('apellidos', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('tiempo_residencia', models.PositiveIntegerField(blank=True, null=True)),
                ('nacionalidad', models.CharField(blank=True, max_length=255, null=True)),
                ('estado_civil', models.SmallIntegerField(blank=True, choices=[(0, 'SOLTERO'), (1, 'CASADO')], default=0)),
                ('genero', models.SmallIntegerField(blank=True, choices=[(0, 'MASCULINO'), (1, 'FEMENINO')], default=0)),
                ('mano_obra', models.SmallIntegerField(blank=True, choices=[(0, 'NO CALIFICADO'), (1, 'CALIFICADO')], default=0)),
                ('numero_documento', models.CharField(max_length=10, unique=True)),
                ('numero_licencia_conducir', models.CharField(blank=True, max_length=255, null=True)),
                ('telefono_fijo', models.CharField(blank=True, max_length=255, null=True)),
                ('celular', models.CharField(blank=True, max_length=255, null=True)),
                ('celular_dos', models.CharField(blank=True, max_length=255, null=True)),
                ('discapacitado', models.BooleanField(default=False)),
                ('verificado', models.BooleanField(default=False)),
                ('imagen', models.FileField(blank=True, null=True, upload_to='personas/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('departamento_nacimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_departamentos')),
                ('departamento_residencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departamento_residencia', to='maestros.PEQ_MAE_departamentos')),
                ('distrito_nacimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_distritos')),
                ('distrito_residencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='distrito_residencia', to='maestros.PEQ_MAE_distritos')),
                ('provincia_nacimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_provincias')),
                ('provincia_residencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provincia_residencia', to='maestros.PEQ_MAE_provincias')),
                ('tipo_discapacidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_tipos_discapacidad')),
                ('tipo_documento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_tipos_documento')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_add', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_add', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'permissions': (('read_persona', 'Puede ver personas'), ('verificar_persona', 'Puede verificar personas')),
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.PositiveSmallIntegerField(choices=[(1, 'Proyecto'), (2, 'Contratista Principal'), (3, 'Contratista'), (4, 'Sub Contratista'), (5, 'Postulante')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAsociacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contratista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contratistas.Contratista')),
                ('contratista_principal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contratistas.ContratistaPrincipal')),
                ('proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contratistas.Proyecto')),
                ('sub_contratista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contratistas.SubContratista')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Asociacion de usuario',
                'verbose_name_plural': 'Asociacion de usuario',
            },
        ),
        migrations.AddField(
            model_name='informacionlaboral',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Persona'),
        ),
        migrations.AddField(
            model_name='informacionlaboral',
            name='rango',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_rangos'),
        ),
        migrations.AddField(
            model_name='informacionlaboral',
            name='sub_especialidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_sub_especialidad'),
        ),
        migrations.AddField(
            model_name='informacioneducativa',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Persona'),
        ),
        migrations.AddField(
            model_name='documentospersonal',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Persona'),
        ),
        migrations.AddField(
            model_name='documentospersonal',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestros.PEQ_MAE_tipos_documento_personales'),
        ),
        migrations.AlterUniqueTogether(
            name='userasociacion',
            unique_together=set([('user', 'proyecto', 'contratista_principal', 'contratista', 'sub_contratista')]),
        ),
    ]
