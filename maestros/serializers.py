from rest_framework import serializers
# MODELS
from .models import PEQ_MAE_familia, PEQ_MAE_sub_especialidad, PEQ_MAE_grado, PEQ_MAE_detalle_documentacion, PEQ_MAE_rangos, PEQ_MAE_familia_puesto, PEQ_MAE_carreras, PEQ_MAE_provincias, PEQ_MAE_distritos, PEQ_MAE_centros_estudio

class FamiliaEspecialidadSerializer(serializers.ModelSerializer):

	class Meta:
		model = PEQ_MAE_familia_puesto
		fields = ('uuid', 'descripcion')

class CentroEstudioSerializer(serializers.ModelSerializer):

	class Meta:
		model = PEQ_MAE_centros_estudio
		fields = ('uuid', 'descripcion')

class EspecialidadSerializer(serializers.ModelSerializer):

	familia_puesto = FamiliaEspecialidadSerializer() 

	class Meta:
		model = PEQ_MAE_familia
		fields = ('uuid', 'descripcion', 'familia_puesto')

class CarrerasSerializer(serializers.ModelSerializer):

	class Meta:
		model = PEQ_MAE_carreras
		fields = ('uuid', 'descripcion')

class SubEspecialidadSerializer(serializers.ModelSerializer):

	class Meta:
		model = PEQ_MAE_sub_especialidad
		fields = ('uuid', 'descripcion')

class SearchSubEspecialidadSerializer(serializers.ModelSerializer):

	especialidad = EspecialidadSerializer()

	class Meta:
		model = PEQ_MAE_sub_especialidad
		fields = ('uuid', 'descripcion', 'especialidad')

class GradoSerializer(serializers.ModelSerializer):

	class Meta:
		model = PEQ_MAE_grado
		fields = ('uuid', 'descripcion')

class RangoSerializer(serializers.ModelSerializer):

	class Meta:
		model = PEQ_MAE_rangos
		fields = ('uuid', 'descripcion')

class DetalleDocumentacionSerializer(serializers.ModelSerializer):

	class Meta:
		model = PEQ_MAE_detalle_documentacion
		fields = ('uuid', 'descripcion')