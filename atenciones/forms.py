# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
# models
from .models import *
from datetime import datetime
# AUTOCOMPLETE
from dal import autocomplete

class AtencionForm(forms.ModelForm):

	fecha = forms.DateField(label='Fecha', widget=forms.TextInput(attrs={'class' : 'form-control datepicker', 'type':'text', 'type':'date', 'id': 'fecha_inicio', 'autocomplete': 'off'}))
	hora_inicio = forms.TimeField(label='Hora inicio', widget=forms.TimeInput(attrs={'class' : 'form-control input-mask', 'data-mask' : '00:00:00', 'placeholder':'ej: 18:06', 'autocomplete':'off','type':'text'}))

	class Meta:
		model = Atenciones
		fields = ('persona','tipo','capacitacion','fecha','hora_inicio')
		widgets = {
			'tipo': forms.Select(attrs={'class': 'normal__select'}),
			'capacitacion': forms.Select(attrs={'class': 'normal__select'}),
			'persona': autocomplete.ModelSelect2(url='persona-autocomplete')
		}

	def clean(self):
		cleaned_data = super(AtencionForm, self).clean()
		if(cleaned_data.get('tipo').descripcion.lower() == u'postulación a capacitaciones'):
			self.add_error('capacitacion', 'Campo Obligatorio.') if not cleaned_data.get('capacitacion') else ''
		else:
			cleaned_data['capacitacion'] = None

class FinalizarAtencionForm(forms.ModelForm):

	observaciones = forms.CharField(label='Descripción', required=False,widget=forms.Textarea(attrs={'class' : 'form-control', 'rows':'4'}))
	hora_fin = forms.TimeField(label='Hora Fin', widget=forms.TimeInput(attrs={'class' : 'form-control input-mask', 'data-mask' : '00:00:00', 'placeholder':'ej: 18:06', 'autocomplete':'off','type':'text'}))
	fecha_finalizacion = forms.DateField(label='Fecha', widget=forms.TextInput(attrs={'class' : 'form-control datepicker', 'type':'text', 'type':'date', 'id': 'fecha_inicio', 'autocomplete': 'off'}))

	class Meta:
		model = Atenciones
		fields = ('observaciones','hora_fin','fecha_finalizacion')