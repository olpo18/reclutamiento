# -*- coding: utf-8 -*-
from rest_framework import serializers
# MODELS
from .models import Persona, InformacionLaboral

from datetime import datetime

now = datetime.now().date()

class InformacionEducativaSerializer(serializers.ModelSerializer):

	centro_estudio = serializers.SerializerMethodField()
	grado = serializers.SerializerMethodField()
	estado_grado = serializers.SerializerMethodField()
	carrera = serializers.SerializerMethodField()
	familia_carrera = serializers.SerializerMethodField()
	fecha_inicio = serializers.SerializerMethodField()

	def get_centro_estudio(self, obj):
		return obj.centro_estudio.descripcion.upper() if obj.centro_estudio else ''

	def get_grado(self, obj):
		return obj.grado.descripcion.upper() if obj.grado else ''

	def get_estado_grado(self, obj):
		return obj.estado_grado.descripcion.upper() if obj.estado_grado else ''

	def get_carrera(self, obj):
		return obj.carrera.descripcion.upper() if obj.carrera else ''

	def get_familia_carrera(self, obj):
		return obj.familia_carrera.descripcion.upper() if obj.familia_carrera else ''

	def get_fecha_inicio(self, obj):
		tiempo_meses = 0
		if obj.hasta_actualidad:
			if obj.fecha_inicio:
				tiempo_meses = (now - obj.fecha_inicio).days/30
		elif obj.fecha_inicio and obj.fecha_fin:
			tiempo_meses = (obj.fecha_fin - obj.fecha_inicio).days/30
		annios = tiempo_meses / 12
		meses = tiempo_meses % 12
		return ( u'{0} AÑOS '.format(annios) if annios > 0 else '' ) + (str(meses)+' MESES' if meses > 0 else '')

	class Meta:
		model = InformacionLaboral
		fields = ('centro_estudio', 'nombre', 'grado', 'estado_grado', 'carrera', 'familia_carrera','fecha_inicio', 'fecha_fin','hasta_actualidad')

class InformacionLaboralSerializer(serializers.ModelSerializer):

	rango = serializers.SerializerMethodField()
	empresa = serializers.SerializerMethodField()
	especialidad = serializers.SerializerMethodField()
	familia_puesto = serializers.SerializerMethodField()
	fecha_inicio = serializers.SerializerMethodField()

	def get_rango(self, obj):
		return obj.rango.descripcion.upper() if obj.rango else ''

	def get_empresa(self, obj):
		return obj.empresa.descripcion.upper() if obj.empresa else ''

	def get_especialidad(self, obj):
		return obj.especialidad.descripcion.upper() if obj.especialidad else ''

	def get_familia_puesto(self, obj):
		return obj.familia_puesto.descripcion.upper() if obj.familia_puesto else ''

	def get_fecha_inicio(self, obj):
		tiempo_meses = 0
		if obj.hasta_actualidad:
			if obj.fecha_inicio:
				tiempo_meses = (now - obj.fecha_inicio).days/30
		elif obj.fecha_inicio and obj.fecha_fin:
			tiempo_meses = (obj.fecha_fin - obj.fecha_inicio).days/30
		annios = tiempo_meses / 12
		meses = tiempo_meses % 12
		return ( u'{0} AÑOS '.format(annios) if annios > 0 else '' ) + (str(meses)+' MESES' if meses > 0 else '')

	class Meta:
		model = InformacionLaboral
		fields = ('empresa', 'nombre', 'especialidad', 'rango','familia_puesto', 'fecha_inicio', 'fecha_fin','hasta_actualidad')

class PersonaSerializer(serializers.ModelSerializer):

	estado_civil = serializers.SerializerMethodField()
	genero = serializers.SerializerMethodField()
	tipo_documento = serializers.SerializerMethodField()
	tipo_discapacidad = serializers.SerializerMethodField()

	def get_estado_civil(self, obj):
		return obj.get_estado_civil_display()

	def get_genero(self, obj):
		return obj.get_genero_display()

	def get_tipo_documento(self, obj):
		return obj.tipo_documento.descripcion if obj.tipo_documento else ''

	def get_tipo_discapacidad(self, obj):
		return obj.tipo_discapacidad.descripcion if obj.tipo_discapacidad else ''

	class Meta:
		model = Persona
		fields = ('uuid','email','nombres','apellidos','fecha_nacimiento','direccion','tiempo_residencia','nacionalidad','estado_civil','genero','tipo_documento','numero_documento','numero_licencia_conducir','telefono_fijo','celular','celular_dos','discapacitado','imagen','tipo_discapacidad' )