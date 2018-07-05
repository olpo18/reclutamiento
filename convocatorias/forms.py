# -*- coding: utf-8 -*-
from django import forms

from .models import Convocatoria, ConvocatoriaPuesto,PEQ_INT_convocatoria_academico, PEQ_INT_convocatoria_experiencia, PEQ_INT_convocatoria_cursos, PEQ_INT_convocatoria_documentos
from contratistas.models import Contratista
from maestros.models import PEQ_MAE_requisitos
# AUTOCOMPLETE
from dal import autocomplete

class ConvocatoriaForm(forms.ModelForm):
	error_css_class = 'error'
	required_css_class = 'required'

	nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	codigo = forms.CharField(label=u'Código', widget=forms.TextInput(attrs={'class' : 'form-control', 'readonly':'true'}))
	# remuneracion = forms.IntegerField(label=u'Remuneración', error_messages={'invalid': 'Ingresar solo numeros.'},widget=forms.TextInput(attrs={'class' : 'form-control'}))
	fecha_inicio = forms.DateField(label='Inicio', widget=forms.TextInput(attrs={'class' : 'form-control datepicker', 'id':'fecha_inicio'}))
	fecha_fin = forms.DateField(label='Fin', widget=forms.TextInput(attrs={'class' : 'form-control datepicker', 'id':'fecha_fin'}))
	condiciones_adicionales = forms.CharField(label='Condiciones Adicionales', widget=forms.Textarea(attrs={'class' : 'form-control', 'rows':'5'}))
	# requisitos_funciones = forms.CharField(label='Requisitos', widget=forms.Textarea(attrs={'class' : 'form-control', 'rows':'5'}))

	class Meta:
		model = Convocatoria
		fields = ('nombre','codigo','remuneracion','contratista','lugar','fecha_inicio','fecha_fin','condiciones_adicionales')
		widgets = {
			'contratista': forms.Select(attrs={'class': 'normal__select'}),
			'lugar': forms.Select(attrs={'class': 'normal__select'}),
			'remuneracion': forms.Select(attrs={'class': 'normal__select'}),
		}

class ConvocatoriaPuestoForm(forms.ModelForm):
	cantidad_vacantes = forms.IntegerField(label='Vacantes', error_messages={'invalid': 'Ingresar solo numeros.'},widget=forms.NumberInput(attrs={'class' : 'form-control'}))
	edad_minima = forms.IntegerField(label='Edad Mín.', error_messages={'invalid': 'Ingresar solo numeros.'},widget=forms.NumberInput(attrs={'class' : 'form-control'}))
	edad_maxima = forms.IntegerField(label='Edad Max.', error_messages={'invalid': 'Ingresar solo numeros.'},widget=forms.NumberInput(attrs={'class' : 'form-control'}))

	class Meta:
		model = ConvocatoriaPuesto
		fields = ('familia_puesto','especialidad','sub_especialidad','rango','cantidad_vacantes','duracion_contrato','edad_minima','edad_maxima')
		widgets = {
			'familia_puesto': forms.Select(attrs={'class': 'normal__select'}),
			'especialidad': autocomplete.ModelSelect2(url='especialidades-autocomplete', forward=['familia_puesto']),
			'sub_especialidad': autocomplete.ModelSelect2(url='sub-especialidades-autocomplete', forward=['especialidad']),
			'rango': forms.Select(attrs={'class': 'normal__select'}),
			'duracion_contrato': forms.Select(attrs={'class': 'normal__select'}),
		}

	def clean(self):
		cleaned_data = super(ConvocatoriaPuestoForm, self).clean()
		edad_minima = int(cleaned_data.get("edad_minima"))
		edad_maxima = int(cleaned_data.get("edad_maxima"))
		# validate edad
		self.add_error('edad_maxima', "Edad Máxima debe ser mayor") if edad_maxima < edad_minima else ''

class ConvocatoriaAcademicoForm(forms.ModelForm):

	class Meta:
		model = PEQ_INT_convocatoria_academico
		fields = ('grado','estado_grado','familia_carrera','carrera','indispensable')
		widgets = {
			'familia_carrera': forms.Select(attrs={'class': 'normal__select'}),
			'carrera': autocomplete.ModelSelect2(url='carreras-autocomplete', forward=['familia_carrera']),
			'grado': forms.Select(attrs={'class': 'normal__select'}),
			'estado_grado': forms.Select(attrs={'class': 'normal__select'})
		}

class ConvocatoriaExperienciaForm(forms.ModelForm):

	class Meta:
		model = PEQ_INT_convocatoria_experiencia
		fields = ('familia_puesto','especialidad','sub_especialidad','rango','experiencia')
		widgets = {
			'familia_puesto': forms.Select(attrs={'class': 'normal__select'}),
			'especialidad': autocomplete.ModelSelect2(url='especialidades-autocomplete', forward=['familia_puesto']),
			'sub_especialidad': autocomplete.ModelSelect2(url='sub-especialidades-autocomplete', forward=['especialidad']),
			'rango': forms.Select(attrs={'class': 'normal__select'}),
			'experiencia': forms.Select(attrs={'class': 'normal__select'})
		}

class ConvocatoriaCursosForm(forms.ModelForm):

	descripcion = forms.CharField(label='Descripción', required=True,widget=forms.Textarea(attrs={'class' : 'form-control', 'rows':'3'}))

	class Meta:
		model = PEQ_INT_convocatoria_cursos
		fields = ('tipo','nombre','descripcion','indispensable')
		widgets = {
			'tipo' : forms.Select(attrs={'class': 'normal__select','required':'required'}),
			'nombre' : autocomplete.ModelSelect2(url='nombre-curso-autocomplete'),
		}

class ConvocatoriaDocumentosForm(forms.ModelForm):

	class Meta:
		model = PEQ_INT_convocatoria_documentos
		fields = ('tipo_documento','detalle_documento','indispensable')
		widgets = {
			'tipo_documento' : forms.Select(attrs={'class': 'normal__select','required':'required'}),
			'detalle_documento' : forms.Select(attrs={'class': 'normal__select','required':'required'}),
		}

class RequisitoConvocatoriaForm(forms.ModelForm):

	descripcion = forms.CharField(label='Descripción', widget=forms.Textarea(attrs={'class' : 'form-control', 'rows':'5'}))

	class Meta:
		model = PEQ_MAE_requisitos
		fields = ('descripcion',)