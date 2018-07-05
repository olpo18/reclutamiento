# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
# models
from maestros.models import *
from contratistas.models import *
# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from maestros.helpers import get_file_path

class Role(models.Model):
	PROYECTO = 1
	CONTRATISTA_PRINCIPAL = 2
	CONTRATISTA = 3
	SUB_CONTRATISTA = 4
	POSTULANTE = 5
	ROLE_CHOICES = (
		(PROYECTO, 'Proyecto'),
		(CONTRATISTA_PRINCIPAL, 'Contratista Principal'),
		(CONTRATISTA, 'Contratista'),
		(SUB_CONTRATISTA, 'Sub Contratista'),
		(POSTULANTE, 'Postulante'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	rol = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=False, blank=False)

class UserAsociacion(models.Model):
	user = models.ForeignKey(User)
	proyecto = models.ForeignKey(Proyecto, null=True, blank=True)
	contratista_principal = models.ForeignKey(ContratistaPrincipal, null=True, blank=True)
	contratista = models.ForeignKey(Contratista, null=True, blank=True)
	sub_contratista = models.ForeignKey(SubContratista, null=True, blank=True)

	def clean(self):
		if not hasattr(self.user, 'role'):
			raise ValidationError({'user' : _('El usuario no tiene un rol asociado.')})
		else:
			if self.user.role.rol == Role.SUB_CONTRATISTA and self.sub_contratista is None:
				raise ValidationError({'sub_contratista' : _('Asignale una sub_contratista')})
			elif self.user.role.rol == Role.CONTRATISTA and self.contratista is None:
				raise ValidationError({'sub_contratista' : _('Asignale una contratista')})

	class Meta:
		verbose_name = "Asociacion de usuario"
		verbose_name_plural = "Asociacion de usuario"
		unique_together = ('user','proyecto','contratista_principal','contratista','sub_contratista')

class Persona(models.Model):
	ESTADO_CIVIL_SOLTERO = 0
	ESTADO_CIVIL_CASADO = 1
	GENERO_MASCULINO = 0
	GENERO_FEMENINO = 1
	MANO_OBRA_NO_CALIFICADO = 0
	MANO_OBRA_CALIFICADO = 1
	MESES = 0
	ANNIOS = 1

	CHOICES_ESTADOS_CIVIL = ((ESTADO_CIVIL_SOLTERO, 'SOLTERO'), (ESTADO_CIVIL_CASADO, 'CASADO'))
	CHOICES_GENEROS = ((GENERO_MASCULINO, 'MASCULINO'), (GENERO_FEMENINO, 'FEMENINO'))
	CHOICES_MANO_OBRA = ((MANO_OBRA_NO_CALIFICADO, 'NO CALIFICADO'), (MANO_OBRA_CALIFICADO, 'CALIFICADO'))
	CHOICES_TIPO_TIEMPO_RESIDENCIA = ((MESES, 'MESES'), (ANNIOS, u'AÑOS'))

	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	user_add = models.ForeignKey(User, null=True, blank=True, related_name='user_add' )
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	email = models.EmailField(max_length=200, null=True, blank=True)
	nombres = models.CharField(max_length=255, null=True, blank=True)
	apellidos = models.CharField(max_length=255, null=True, blank=True)
	fecha_nacimiento = models.DateField(null=True, blank=True)
	departamento_nacimiento = models.ForeignKey(PEQ_MAE_departamentos, null=True, blank=True)
	provincia_nacimiento = models.ForeignKey(PEQ_MAE_provincias, null=True, blank=True)
	distrito_nacimiento = models.ForeignKey(PEQ_MAE_distritos, null=True, blank=True)
	departamento_residencia = models.ForeignKey(PEQ_MAE_departamentos, related_name='departamento_residencia', null=True, blank=True)
	provincia_residencia = models.ForeignKey(PEQ_MAE_provincias, related_name='provincia_residencia', null=True, blank=True)
	distrito_residencia = models.ForeignKey(PEQ_MAE_distritos, related_name='distrito_residencia', null=True, blank=True)
	direccion = models.CharField(max_length=255, null=True, blank=True)
	tiempo_residencia = models.PositiveIntegerField(null=True, blank=True, default=0)
	tipo_tiempo_residencia = models.SmallIntegerField(choices=CHOICES_TIPO_TIEMPO_RESIDENCIA, null=True, blank=True, default=0)
	nacionalidad = models.CharField(max_length=255, null=True, blank=True)
	estado_civil = models.SmallIntegerField(choices=CHOICES_ESTADOS_CIVIL, null=False, blank=True, default=0)
	genero = models.SmallIntegerField(choices=CHOICES_GENEROS, null=False, blank=True, default=0)
	mano_obra = models.SmallIntegerField(choices=CHOICES_MANO_OBRA, null=False, blank=True, default=0)
	tipo_documento = models.ForeignKey(PEQ_MAE_tipos_documento, null=True, blank= True)
	numero_documento = models.CharField(max_length=20, null=False, blank=False, unique=True)
	numero_licencia_conducir = models.CharField(max_length=255, null=True, blank=True)
	telefono_fijo = models.CharField(max_length=255, null=True, blank=True)
	celular = models.CharField(max_length=255, null=True, blank=True)
	celular_dos = models.CharField(max_length=255, null=True, blank=True)
	discapacitado = models.BooleanField(default=False)
	verificado = models.BooleanField(default=False)
	declaro = models.BooleanField(default=False)
	imagen = models.FileField(upload_to='personas/', null=True, blank=True)
	tipo_discapacidad = models.ForeignKey(PEQ_MAE_tipos_discapacidad, null=True, blank=True)
	ingles = models.ForeignKey(PEQ_MAE_ingles, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Persona"
		verbose_name_plural = "Personas"
		permissions = (
			("read_persona", "Puede ver personas"),
			("verificar_persona", "Puede verificar personas"),
		)

	def __unicode__(self):
		return '%s' % self.nombres +' '+ self.apellidos

	def delete(self, *args, **kwargs):
		self.user.delete()
		return super(self.__class__, self).delete(*args, **kwargs)

class InformacionEducativa(models.Model):
	persona = models.ForeignKey(Persona)
	centro_estudio = models.ForeignKey(PEQ_MAE_centros_estudio, null=False, blank=False)
	nombre = models.CharField(max_length=255, null=True, blank=True)
	grado = models.ForeignKey(PEQ_MAE_grado, null=False, blank= False)
	estado_grado = models.ForeignKey(PEQ_MAE_estado_grado, null=False, blank=False)
	familia_carrera = models.ForeignKey(PEQ_MAE_familia_carreras, null=True, blank= True)
	carrera = models.ForeignKey(PEQ_MAE_carreras, null=True, blank= True)
	fecha_inicio = models.DateField(null=False, blank=False)
	fecha_fin = models.DateField(null=True, blank=True)
	hasta_actualidad = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Información educativa"
		verbose_name_plural = "Información educativa"

	def __unicode__(self):
		return '%s' % self.nombre

class InformacionLaboral(models.Model):
	persona = models.ForeignKey(Persona)
	empresa = models.ForeignKey(PEQ_MAE_empresas, null=True, blank=True)
	nombre = models.CharField(max_length=255, null=True, blank=True)
	familia_puesto = models.ForeignKey(PEQ_MAE_familia_puesto, null=False, blank= False)
	especialidad = models.ForeignKey(PEQ_MAE_familia, null=False, blank= False)
	sub_especialidad = models.ForeignKey(PEQ_MAE_sub_especialidad, null=True, blank= True)
	rango = models.ForeignKey(PEQ_MAE_rangos, null=True, blank= True)
	fecha_inicio = models.DateField(null=False, blank=False)
	fecha_fin = models.DateField(null=True, blank=True)
	hasta_actualidad = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Información laboral"
		verbose_name_plural = "Información laboral"

	def __unicode__(self):
		return '%s' % self.persona

# documento = models.FileField(upload_to=get_path_for_persona_documento)
# def get_path_for_persona_documento(instance, filename):
# 	return get_file_path('documentos/', filename)

class DocumentosPersonal(models.Model):
	persona = models.ForeignKey(Persona)
	tipo = models.ForeignKey(PEQ_MAE_tipos_documento_personales, null=False, blank=False)
	nombre = models.CharField(max_length=255, null=True, blank=True)
	documento = models.FileField(upload_to=get_file_path)

	class Meta:
		verbose_name = "Documento personal"
		verbose_name_plural = "Documentos personales"
		unique_together = ('persona','tipo')

	def __unicode__(self):
		return '%s' % self.nombre

class CursosPostulantes(models.Model):
	persona = models.ForeignKey(Persona)
	tipo = models.ForeignKey(PEQ_MAE_tipo_cursos, null=False, blank=False)
	nombre = models.ForeignKey(PEQ_MAE_cursos, null=False, blank=False)
	descripcion = models.CharField(max_length=250, null=True, blank=True)
	fecha_inicio = models.DateField(null=False, blank=False)
	fecha_fin = models.DateField(null=True, blank=True)
	hasta_actualidad = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Cursos del postulante'

class Bloqueados(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	numero_documento = models.CharField(max_length=255, null=False, blank=False)
	nombres = models.CharField(max_length=255, null=True, blank=True)
	apellidos = models.CharField(max_length=255, null=True, blank=True)
	direccion = models.CharField(max_length=255, null=True, blank=True)
	celular = models.CharField(max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Bloqueados"
		verbose_name_plural = "Bloqueados"

	def __unicode__(self):
		return '%s' % self.numero_documento
