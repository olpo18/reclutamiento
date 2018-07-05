# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# MODELS
from .models import PEQ_MAE_familia, PEQ_MAE_sub_especialidad, PEQ_MAE_grado, PEQ_MAE_detalle_documentacion, PEQ_MAE_departamentos, PEQ_MAE_provincias, PEQ_MAE_distritos
# SERIALIZERS
from .serializers import *
# REST FRAMEWORK
from rest_framework import generics
# AUTOCOMPLETE
from dal import autocomplete

# Create your views here.
class EspecialidadesByFamiliaList(generics.ListAPIView):
	serializer_class = EspecialidadSerializer

	def get_queryset(self):
		queryset = PEQ_MAE_familia.objects.all()
		familia_uuid = self.request.query_params.get('familia', None)
		if familia_uuid is not None:
			queryset = queryset.filter(familia_puesto__uuid=familia_uuid).order_by('descripcion')
		return queryset

class SubEspecialidadesByFamiliaList(generics.ListAPIView):
	serializer_class = SubEspecialidadSerializer

	def get_queryset(self):
		queryset = PEQ_MAE_sub_especialidad.objects.all()
		especialidad_uuid = self.request.query_params.get('especialidad', None)
		if especialidad_uuid is not None:
			queryset = queryset.filter(especialidad__uuid=especialidad_uuid).order_by('descripcion')
		return queryset

class GradosByFamiliaList(generics.ListAPIView):
	serializer_class = GradoSerializer

	def get_queryset(self):
		queryset = PEQ_MAE_grado.objects.all()
		familia_uuid = self.request.query_params.get('familia', None)
		if familia_uuid is not None:
			queryset = queryset.filter(familia__uuid=familia_uuid).order_by('descripcion')
		return queryset

class CarrerasByFamiliaList(generics.ListAPIView):
	serializer_class = CarrerasSerializer

	def get_queryset(self):
		queryset = PEQ_MAE_carreras.objects.all()
		familia_uuid = self.request.query_params.get('familia', None)
		if familia_uuid is not None:
			queryset = queryset.filter(familia_carrera__uuid=familia_uuid).order_by('descripcion')
		return queryset		

class DetalleByTipoDocumentoList(generics.ListAPIView):
	serializer_class = DetalleDocumentacionSerializer

	def get_queryset(self):
		queryset = PEQ_MAE_detalle_documentacion.objects.all()
		tipo_uuid = self.request.query_params.get('tipo', None)
		if tipo_uuid is not None:
			queryset = queryset.filter(tipo__uuid=tipo_uuid)
		return queryset

class DepartamentosAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = PEQ_MAE_departamentos.objects.all().order_by('descripcion')
        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)
        return qs

class ProvinciasAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = PEQ_MAE_provincias.objects.all().order_by('descripcion')
        departamento = self.forwarded.get('departamento_nacimiento', None) or self.forwarded.get('departamento_residencia', None)
        if departamento:
            qs = qs.filter(departamento=departamento)
        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)
        return qs

class DistritosAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = PEQ_MAE_distritos.objects.all().order_by('descripcion')
        provincia = self.forwarded.get('provincia_nacimiento', None) or self.forwarded.get('provincia_residencia', None)
        if provincia:
            qs = qs.filter(provincia=provincia)
        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)
        return qs

# Error Pages
def handler403(request):
    return render(request, 'error_pages/403.html', status=404)

def handler404(request):
    return render(request, 'error_pages/404.html', status=404)

def handler500(request):
    return render(request, 'error_pages/500.html', status=500)