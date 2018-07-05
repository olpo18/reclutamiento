# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
# MODELS
from .models import *
# Register your models here.
@admin.register(Convocatoria)
class ConvocatoriaAdmin(admin.ModelAdmin):
	list_display = ('uuid','nombre','codigo','remuneracion','contratista','fecha_inicio','fecha_fin')
	search_fields = ['nombre','codigo']
	list_filter = ('contratista',)

@admin.register(ConvocatoriaPuesto)
class ConvocatoriaPuestoAdmin(admin.ModelAdmin):
	list_display = ('uuid','convocatoria','rango','especialidad','familia_puesto','duracion_contrato','cantidad_vacantes')
	search_fields = ['convocatoria__nombre','convocatoria__codigo','rango__descripcion','especialidad__descripcion','familia_puesto__descripcion']

@admin.register(PEQ_INT_convocatoria_academico)
class ConvocatoriaAcademicoAdmin(admin.ModelAdmin):
	list_display = ('convocatoria_puesto','familia_carrera','carrera','grado','estado_grado','porcentaje_cumplimiento')
	search_fields = ['convocatoria_puesto__convocatoria__nombre','convocatoria_puesto__convocatoria__codigo', 'familia_carrera__descripcion', 'carrera__descripcion', 'grado__descripcion']

@admin.register(PEQ_INT_convocatoria_experiencia)
class ConvocatoriaExperienciaAdmin(admin.ModelAdmin):
	list_display = ('convocatoria_puesto','especialidad','familia_puesto','experiencia','porcentaje_cumplimiento')
	search_fields = ['convocatoria_puesto__convocatoria__nombre','convocatoria_puesto__convocatoria__codigo','especialidad__descripcion','familia_puesto__descripcion']

@admin.register(PEQ_INT_convocatoria_cursos)
class ConvocatoriaCursosAdmin(admin.ModelAdmin):
	list_display = ('convocatoria_puesto','tipo','nombre','descripcion','porcentaje_cumplimiento')
	search_fields = ['convocatoria_puesto__convocatoria__nombre','convocatoria_puesto__convocatoria__codigo','tipo__descripcion','nombre__descripcion']

@admin.register(PEQ_INT_estado_convocatoria)
class EstadoConvocatoriaAdmin(admin.ModelAdmin):
	list_display = ('uuid','convocatoria','estado','fecha_inicio','fecha_fin','activo')
	search_fields = ['convocatoria__nombre','convocatoria__codigo']

@admin.register(PostulacionConvocatoria)
class ConvocatoriaPostulacionAdmin(admin.ModelAdmin):
	list_display = ('convocatoria_puesto','persona','rango','codigo_postulacion','tipo_ingreso')
	search_fields = ['convocatoria_puesto__convocatoria__nombre','convocatoria_puesto__convocatoria__codigo','persona__numero_documento','persona__nombres','persona__apellidos']

@admin.register(PEQ_INT_estado_postulacion)
class EstadoPostulacionAdmin(admin.ModelAdmin):
	list_display = ('postulacion','estado','fecha')
	search_fields = ['postulacion__convocatoria_puesto__convocatoria__nombre','postulacion__convocatoria_puesto__convocatoria__codigo','postulacion__persona__numero_documento','postulacion__persona__nombres','postulacion__persona__apellidos']

@admin.register(DocumentoPostulacion)
class DocumentoPostulacionAdmin(admin.ModelAdmin):
	list_display = ('detalle_documento','estado_postulacion','documento','fecha_creacion')
	

@admin.register(PlantillaCriteriosAvanzados)
class PlantillasCriterioAdmin(admin.ModelAdmin):
	list_display = ('descripcion',)

@admin.register(ConvocatoriaTags)
class ConvocatoriaTagsAdmin(admin.ModelAdmin):
	list_display = ('convocatoria_puesto','persona','display_tags')

	def display_tags(self, instance):
		return ', '.join([ tag.descripcion for tag in instance.tags.all() ])
	display_tags.short_description = 'Tags'
