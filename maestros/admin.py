# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(PEQ_MAE_sub_especialidad, PEQ_MAE_tipo_cursos, PEQ_MAE_lugares, PEQ_MAE_tipos_documento, PEQ_MAE_tipos_discapacidad, PEQ_MAE_centros_estudio, PEQ_MAE_empresas, PEQ_MAE_tags, PEQ_MAE_remuneracion, PEQ_MAE_duracion_contrato, PEQ_MAE_requisitos, PEQ_MAE_documentacion, PEQ_MAE_detalle_documentacion, PEQ_MAE_departamentos, PEQ_MAE_provincias, PEQ_MAE_distritos, PEQ_MAE_cursos, PEQ_MAE_tipos_documento_personales, PEQ_MAE_tipo_atencion, PEQ_MAE_ingles, PEQ_MAE_capacitaciones)
class PEQ_MAE_Admin(admin.ModelAdmin):
    readonly_fields = ('uuid',)
    list_display = ('uuid','descripcion')
    search_fields = ['descripcion',]

@admin.register(PEQ_MAE_rangos, PEQ_MAE_grado, PEQ_MAE_estado_grado, PEQ_MAE_estados_postulacion, PEQ_MAE_familia, PEQ_MAE_criterios_aprobacion, PEQ_MAE_rango_seleccion, PEQ_MAE_familia_puesto, PEQ_MAE_familia_carreras, PEQ_MAE_carreras, PEQ_MAE_familia_grado, PEQ_MAE_estados_convocatoria)
class PEQ_MAE_OrdenAdmin(admin.ModelAdmin):
	list_display = ('uuid','descripcion','orden')
	search_fields = ['descripcion',]

class PEQ_MAE_TiempoExperienciaAdmin(admin.ModelAdmin):
	list_display = ('uuid','tiempo','tipo')
