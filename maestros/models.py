# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# CAPACITACIONES
class PEQ_MAE_capacitaciones(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=200, null=False, blank=False, unique=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Capacitacion"
		verbose_name_plural = "Capacitaciones"

	def __unicode__(self):
		return '%s' % self.descripcion

# NIVELES DE INGLES
class PEQ_MAE_ingles(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=200, null=False, blank=False, unique=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Ingles"
		verbose_name_plural = "Ingles"

	def __unicode__(self):
		return '%s' % self.descripcion

# TIPO DE ATENCIÓN
class PEQ_MAE_tipo_atencion(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=200, null=False, blank=False, unique=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Tipo de atención"
		verbose_name_plural = "Tipos de atenciones"

	def __unicode__(self):
		return '%s' % self.descripcion

# CRITERIOS DE APROBACION
class PEQ_MAE_criterios_aprobacion(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=700, null=False, blank=False)
	alias = models.CharField(max_length=25, null=False, blank=False, unique=True)
	orden = models.IntegerField(null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Criterios de Aprobación"
		verbose_name_plural = "Criterios de Aprobación"

	def __unicode__(self):
		return '%s' % self.descripcion

# RANGO SELECCION
class PEQ_MAE_rango_seleccion(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=700, null=False, blank=False)
	orden = models.PositiveIntegerField(null=True, blank=True, default=0)
	minimo = models.PositiveIntegerField(null=True, blank=True)
	maximo = models.PositiveIntegerField(null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Porcentaje postulante"
		verbose_name_plural = "Porcentajes postulante"

	def __unicode__(self):
		return '%s' % self.descripcion

# DOCUMENTACION
class PEQ_MAE_documentacion(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=200, null=False, blank=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Tipo Documentación"
		verbose_name_plural = "Tipo Documentación"

	def __unicode__(self):
		return '%s' % self.descripcion

# CURSOS
class PEQ_MAE_cursos(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=700, null=False, blank=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Cursos"
		verbose_name_plural = "Cursos"

	def __unicode__(self):
		return '%s' % self.descripcion

# TIPOS DE DOCUMENTOS PERSONALES
class PEQ_MAE_tipos_documento_personales(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=700, null=False, blank=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Tipos de documentos personales"
		verbose_name_plural = "Tipos de documentos personales"

	def __unicode__(self):
		return '%s' % self.descripcion

# DETALLE DOCUMENTACION
class PEQ_MAE_detalle_documentacion(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	tipo = models.ForeignKey(PEQ_MAE_documentacion)
	descripcion = models.CharField(max_length=700, null=False, blank=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Detalle Documentación"
		verbose_name_plural = "Detalle Documentación"

	def __unicode__(self):
		return '%s' % self.descripcion

# REQUISITOS
class PEQ_MAE_requisitos(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(max_length=700, null=False, blank=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Requisitos Convocatoria"
		verbose_name_plural = "Requisitos Convocatoria"

	def __unicode__(self):
		return '%s' % self.descripcion

# DURACION CONTRATO
class PEQ_MAE_duracion_contrato(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Duración Contrato"
		verbose_name_plural = "Duracion Contrato"

	def __unicode__(self):
		return '%s' % self.descripcion

# REMUNERACION
class PEQ_MAE_remuneracion(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Remuneracion"
		verbose_name_plural = "Remuneraciones"

	def __unicode__(self):
		return '%s' % self.descripcion

# RANGOS
class PEQ_MAE_rangos(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	orden = models.PositiveIntegerField(null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Rango"
		verbose_name_plural = "Rangos"

	def __unicode__(self):
		return '%s' % self.descripcion

# ESTADOS DE POSTULACION
class PEQ_MAE_estados_postulacion(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	alias = models.CharField(max_length=255, null=True, blank=True)
	orden = models.PositiveIntegerField(null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Estado de postulación"
		verbose_name_plural = "Estados de postulación"

	def __unicode__(self):
		return '%s' % self.descripcion
# EMPRESAS
class PEQ_MAE_empresas(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Empresa"
		verbose_name_plural = "Empresas"

	def __unicode__(self):
		return '%s' % self.descripcion

# CENTROS DE ESTUDIOS
class PEQ_MAE_centros_estudio(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Centro de estudios"
		verbose_name_plural = "Centro de estudios"

	def __unicode__(self):
		return '%s' % self.descripcion

# TIPOS DE DISCAPACIDAD
class PEQ_MAE_tipos_discapacidad(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Tipos de discapacidad"
		verbose_name_plural = "Tipos de discapacidad"

	def __unicode__(self):
		return '%s' % self.descripcion

# TIPOS DE DOCUMENTO
class PEQ_MAE_tipos_documento(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Tipo de documento"
		verbose_name_plural = "Tipos de documento"

	def __unicode__(self):
		return '%s' % self.descripcion

# PUESTOS
class PEQ_MAE_familia_puesto(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	orden = models.IntegerField(null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Familia Puesto"
		verbose_name_plural = "Familia Puestos"

	def __unicode__(self):
		return '%s' % self.descripcion

# ESPECIALIDADES
class PEQ_MAE_familia(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	orden = models.IntegerField(null=True, blank=True, default=0)
	familia_puesto = models.ForeignKey(PEQ_MAE_familia_puesto, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Especialidad"
		verbose_name_plural = "Especialidades"

	def __unicode__(self):
		return '%s' % self.descripcion

# PUESTOS
class PEQ_MAE_familia_carreras(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	orden = models.IntegerField(null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Familia carreras"
		verbose_name_plural = "Familia carreras"

	def __unicode__(self):
		return '%s' % self.descripcion

# ESPECIALIDADES
class PEQ_MAE_carreras(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	familia_carrera = models.ForeignKey(PEQ_MAE_familia_carreras, null=True, blank=True)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	orden = models.IntegerField(null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Carrera"
		verbose_name_plural = "Carreras"

	def __unicode__(self):
		return '%s' % self.descripcion

# SUB ESPECIALIDADES
class PEQ_MAE_sub_especialidad(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	especialidad = models.ForeignKey(PEQ_MAE_familia, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Sub especialidad"
		verbose_name_plural = "Sub especialidades"

	def __unicode__(self):
		return '%s' % self.descripcion

# FAMILIA GRADOS
class PEQ_MAE_familia_grado(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	orden = models.IntegerField(null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Familia Grado"
		verbose_name_plural = "Familia Grados"

	def __unicode__(self):
		return '%s' % self.descripcion

# GRADO
class PEQ_MAE_grado(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	orden = models.IntegerField(null=True, blank=True, default=0)
	familia = models.ForeignKey(PEQ_MAE_familia_grado, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Grado"
		verbose_name_plural = "Grados"

	def __unicode__(self):
		return '%s' % self.descripcion

# TIEMPO DE EXPERINCIA
class PEQ_MAE_tiempo_experiencia(models.Model):
	MES = 1
	ANNIO = 0

	TIPOS = ( (MES, 'MES'), (ANNIO, u'AÑO'))
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	tiempo = models.IntegerField()
	tipo = models.SmallIntegerField(choices=TIPOS, null=False, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Tiempo de experiencia"
		verbose_name_plural = "Tiempo de experiencia"

	def __unicode__(self):
		return '%s' % self.tiempo +' '+self.get_tipo_display()


# ESTADO DE GRADOS
class PEQ_MAE_estado_grado(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	orden = models.IntegerField(null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Estado Grado"
		verbose_name_plural = "Estados Grado"

	def __unicode__(self):
		return '%s' % self.descripcion

# TAGS
class PEQ_MAE_tags(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Tag"
		verbose_name_plural = "Tags"

	def __unicode__(self):
		return '%s' % self.descripcion

# CURSOS O CAPACITACIONES
class PEQ_MAE_tipo_cursos(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Tipo Cursos"
		verbose_name_plural = "Tipo Cursos"

	def __unicode__(self):
		return '%s' % self.descripcion

# LUGARES
class PEQ_MAE_lugares(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Lugar"
		verbose_name_plural = "Lugares"

	def __unicode__(self):
		return '%s' % self.descripcion

# DEPARTAMENTOS
class PEQ_MAE_departamentos(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Departamento"
		verbose_name_plural = "Departamentos"

	def __unicode__(self):
		return '%s' % self.descripcion

# PROVINCIAS
class PEQ_MAE_provincias(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	departamento = models.ForeignKey(PEQ_MAE_departamentos, null=False, blank=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Provincia"
		verbose_name_plural = "Provincias"

	def __unicode__(self):
		return '%s' % self.descripcion

# DISTRITOS
class PEQ_MAE_distritos(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	provincia = models.ForeignKey(PEQ_MAE_provincias, null=False, blank=False)
	descripcion = models.CharField(max_length=255, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Distrito"
		verbose_name_plural = "Distritos"

	def __unicode__(self):
		return '%s' % self.descripcion

# ESTADOS DE CONVOCATORIA
class PEQ_MAE_estados_convocatoria(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	descripcion = models.CharField(unique=True ,max_length=255, null=False, blank=False)
	orden = models.IntegerField(null=True, blank=True, default=0)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	estado = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Estado convocatoria"
		verbose_name_plural = "Estados convocatoria"

	def __unicode__(self):
		return '%s' % self.descripcion
