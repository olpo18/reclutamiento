# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid
from maestros.models import *
from maestros.helpers import get_file_path
from contratistas.models import Contratista
from usuarios.models import Persona
# Create your models here.
class Observaciones(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=300, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

class Convocatoria(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, null=True, blank=True)
	nombre = models.CharField(max_length=255, null=True, blank=True)
	numero = models.IntegerField(null=True, blank=True)
	codigo = models.CharField(max_length=255, null=True, blank=True, unique=True)
	remuneracion = models.ForeignKey(PEQ_MAE_remuneracion, null=True, blank=True)
	contratista = models.ForeignKey(Contratista, null=False, blank=False)
	lugar = models.ForeignKey(PEQ_MAE_lugares, null=False, blank= False)
	condiciones_adicionales = models.CharField(max_length=1000, null=True, blank=True)
	activo = models.BooleanField(default=True)
	fecha_inicio = models.DateField(null=False, blank=False)
	fecha_fin = models.DateField(null=False, blank=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Convocatoria"
		verbose_name_plural = "Convocatorias"
		permissions = (
			("read_convocatoria", "Puede ver convocatorias"),
			("autorizar_convocatoria", "Puede autorizar convocatoria"),
			("iniciar_convocatoria", "Puede iniciar convocatoria"),
		)

	def __unicode__(self):
		return '{0} {1}'.format(self.nombre, self.codigo)

class ConvocatoriaPuesto(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	convocatoria = models.ForeignKey(Convocatoria)
	especialidad = models.ForeignKey(PEQ_MAE_familia, null=False, blank= False)
	familia_puesto = models.ForeignKey(PEQ_MAE_familia_puesto, null=False, blank= False)
	sub_especialidad = models.ForeignKey(PEQ_MAE_sub_especialidad, null=True, blank= True)
	rango = models.ForeignKey(PEQ_MAE_rangos, null=False, blank= False)
	duracion_contrato = models.ForeignKey(PEQ_MAE_duracion_contrato, null=False, blank= False)
	cantidad_vacantes = models.PositiveIntegerField(null=False, blank=False)
	edad_minima = models.PositiveIntegerField(null=False, blank=False)
	edad_maxima = models.PositiveIntegerField(null=False, blank=False)
	requisitos = models.ManyToManyField(PEQ_MAE_requisitos)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Convocatorias Puesto'
		unique_together = ('convocatoria','especialidad','familia_puesto','sub_especialidad','rango')

	def __unicode__(self):
		return '{0} - {1}'.format(self.convocatoria.nombre, self.especialidad.descripcion)	

NORMAL = 0
CRITERIO = 1
# Aplica para la parte académica, experiencia, cursos y documentos
CHOICES_TIPOS_REGISTRO = (
	(NORMAL, 'normal'),
	(CRITERIO, 'criterio'),
)

class PEQ_INT_convocatoria_academico(models.Model):
	convocatoria_puesto = models.ForeignKey(ConvocatoriaPuesto)
	familia_carrera = models.ForeignKey(PEQ_MAE_familia_carreras, null=True, blank= True)
	carrera = models.ForeignKey(PEQ_MAE_carreras, null=True, blank=True)
	grado = models.ForeignKey(PEQ_MAE_grado, null=False, blank= False)
	estado_grado = models.ForeignKey(PEQ_MAE_estado_grado, null=False, blank=False)
	indispensable = models.BooleanField(default=False)
	porcentaje_cumplimiento = models.PositiveIntegerField(null=True, blank=True, default=0)
	tipo_registro = models.PositiveSmallIntegerField(choices=CHOICES_TIPOS_REGISTRO, null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Convocatorias Académico'
		unique_together = ('convocatoria_puesto', 'familia_carrera', 'carrera', 'grado','estado_grado')
		permissions = (
			("add_criterio_academico", "Puede agregar criterio academico"),
		)
			
class PEQ_INT_convocatoria_experiencia(models.Model):
	convocatoria_puesto = models.ForeignKey(ConvocatoriaPuesto)
	familia_puesto = models.ForeignKey(PEQ_MAE_familia_puesto, null=False, blank=False)
	especialidad = models.ForeignKey(PEQ_MAE_familia, null=False, blank= False)
	sub_especialidad = models.ForeignKey(PEQ_MAE_sub_especialidad, null=True, blank=True)
	rango = models.ForeignKey(PEQ_MAE_rangos, null=True, blank= True)
	experiencia = models.ForeignKey(PEQ_MAE_tiempo_experiencia, verbose_name='Tiempo',null=False, blank= False)
	porcentaje_cumplimiento = models.PositiveIntegerField(null=True, blank=True, default=0)
	tipo_registro = models.PositiveSmallIntegerField(choices=CHOICES_TIPOS_REGISTRO, null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Convocatorias Experiencia"
		unique_together = ('convocatoria_puesto', 'especialidad', 'familia_puesto', 'sub_especialidad','rango','tipo_registro')
		permissions = (
			("add_criterio_laboral", "Puede agregar criterio laboral"),
		)

class PEQ_INT_convocatoria_cursos(models.Model):
	convocatoria_puesto = models.ForeignKey(ConvocatoriaPuesto, null=False, blank=False)
	tipo = models.ForeignKey(PEQ_MAE_tipo_cursos, null=True, blank=True)
	nombre = models.ForeignKey(PEQ_MAE_cursos, null=True, blank=True)
	descripcion = models.CharField(max_length=250, null=True, blank=True)
	indispensable = models.BooleanField(default=False)
	porcentaje_cumplimiento = models.PositiveIntegerField(null=True, blank=True, default=0)
	tipo_registro = models.PositiveSmallIntegerField(choices=CHOICES_TIPOS_REGISTRO, null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Convocatorias curso'
		unique_together = ('convocatoria_puesto','tipo','nombre','tipo_registro')
		permissions = (
			("add_criterio_curso", "Puede agregar criterio de cursos"),
		)

class PEQ_INT_convocatoria_documentos(models.Model):
	convocatoria_puesto = models.ForeignKey(ConvocatoriaPuesto, null=False, blank=False)
	tipo_documento = models.ForeignKey(PEQ_MAE_documentacion, null=False, blank=False)
	detalle_documento = models.ForeignKey(PEQ_MAE_detalle_documentacion, null=False, blank=False)
	indispensable = models.BooleanField(default=False)
	porcentaje_cumplimiento = models.PositiveIntegerField(null=True, blank=True)
	tipo_registro = models.PositiveSmallIntegerField(choices=CHOICES_TIPOS_REGISTRO, null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Convocatorias curso'
		unique_together = ('convocatoria_puesto','detalle_documento','tipo_registro')	

class PEQ_INT_estado_convocatoria(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	convocatoria = models.ForeignKey(Convocatoria, null=False, blank= False)
	estado = models.ForeignKey(PEQ_MAE_estados_convocatoria, null=False, blank= False)
	fecha_inicio = models.DateField(null=True, blank=True)
	fecha_fin = models.DateField(null=True, blank=True)
	fecha_comite = models.DateField(null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	activo = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Estado Convocatorias"
		unique_together = ('convocatoria', 'estado')
		
	def __unicode__(self):
		return '%s' % self.convocatoria.nombre

class PostulacionConvocatoria(models.Model):
	convocatoria_puesto = models.ForeignKey(ConvocatoriaPuesto, null=True, blank= True)
	rango = models.ForeignKey(PEQ_MAE_rango_seleccion, null=True, blank=True)
	persona = models.ForeignKey(Persona, null=False, blank= False)
	tipo_ingreso = models.CharField(max_length=250, null=True, blank=True)
	codigo_postulacion = models.CharField(max_length=100, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Convocatorias Postulante'
		unique_together = ('convocatoria_puesto','persona')
		permissions = (
			("read_postulaciones", "Puede ver postulaciones"),
		)

	def __unicode__(self):
		return '{0} - {1}'.format(self.convocatoria_puesto.convocatoria.nombre or '', self.persona.nombres+' '+self.persona.apellidos)

class PEQ_INT_estado_postulacion(models.Model):
	postulacion = models.ForeignKey(PostulacionConvocatoria, null=False, blank=False)
	estado = models.ForeignKey(PEQ_MAE_estados_postulacion, null=False, blank=False)
	llamado = models.BooleanField(default=False)
	quiero_participar = models.BooleanField(default=False)
	entrevista = models.BooleanField(default=False)
	apto = models.BooleanField(default=False)
	visitado = models.BooleanField(default=False)
	verificado = models.BooleanField(default=False)
	observaciones = models.ManyToManyField(Observaciones, blank=True)
	fecha = models.DateField(null=True, blank=True, auto_now_add=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Estado Postulacion'
		unique_together = ('postulacion','estado')
		permissions = (
			("add_preseleccionados", "Puede preseleccionar postulantes"),
			("add_aprobados", "Puede aprobar postulantes"),
			("add_seleccionarpreseleccionado", "Puede seleccionar postulantes preseleccionados"),
			("add_tramitedocumentario", "Puede agregar tramite documentario"),
			("read_verificaciondomiciliaria", "Puede ver verificacion domiciliaria"),
			("read_contactabilidad", "Puede ver cantactabilidad"),
			("read_preseleccionados", "Puede ver preseleccionados"),
			("read_seleccionados", "Puede ver seleccionados"),
			("read_aprobados", "Puede ver aprobados"),
		)

class DocumentoPostulacion(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	detalle_documento = models.ForeignKey(PEQ_MAE_detalle_documentacion, null=False, blank=False)
	estado_postulacion = models.ForeignKey(PEQ_INT_estado_postulacion, null=False, blank=False)
	documento = models.FileField(upload_to='documentos/', null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Documentos Postulacion'
		unique_together = ('detalle_documento','estado_postulacion')

class PasesIngreso(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	persona = models.ForeignKey(Persona)
	convocatoria_puesto = models.ForeignKey(ConvocatoriaPuesto)
	criterio_aprobacion = models.ForeignKey(PEQ_MAE_criterios_aprobacion)
	boleta_de_pago = models.FileField(upload_to=get_file_path, null=True, blank=True)
	pdt = models.FileField(upload_to=get_file_path, null=True, blank=True)
	registro_informacion_laboral = models.FileField(upload_to=get_file_path, null=True, blank=True)
	carnet_extranjeria = models.FileField(upload_to=get_file_path, null=True, blank=True)
	tramite_calidad_migratoria = models.FileField(upload_to=get_file_path, null=True, blank=True)
	orden_servicio = models.FileField(upload_to=get_file_path, null=True, blank=True)

	class Meta:
		unique_together = ('persona','convocatoria_puesto')

class ConvocatoriaTags(models.Model):
	convocatoria_puesto = models.ForeignKey(ConvocatoriaPuesto, null=True, blank=True)
	persona = models.ForeignKey(Persona, null=False, blank= False)
	tags = models.ManyToManyField(PEQ_MAE_tags)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Convocatoria Tag'

# CRITERIOS AVANZADOS
class PlantillaCriteriosAvanzados(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=200, null=False, blank=False, unique=True)
	academico = models.ManyToManyField(PEQ_INT_convocatoria_academico, blank=True)
	experiencia = models.ManyToManyField(PEQ_INT_convocatoria_experiencia, blank=True)
	cursos = models.ManyToManyField(PEQ_INT_convocatoria_cursos, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Criterios Avanzados"
		verbose_name_plural = "Criterios Avanzados"

	def __unicode__(self):
		return '%s' % self.descripcion
