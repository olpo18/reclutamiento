from rest_framework import serializers
# MODELS
from .models import Observaciones

class ObservacionesSerializer(serializers.ModelSerializer):

	fecha_creacion = serializers.DateTimeField(format="%d-%m-%Y")

	class Meta:
		model = Observaciones
		fields = ('uuid', 'descripcion','fecha_creacion')