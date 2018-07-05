# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
# models
from .models import *
from datetime import datetime
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
# AUTOCOMPLETE
from dal import autocomplete

from datetime import datetime

class PaseIngresoPersonaForm(forms.ModelForm):

	nombres = forms.CharField(label='(*) Nombres', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	apellidos = forms.CharField(label='(*) Apellidos', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	genero = forms.CharField(label=u'(*) Género', widget=forms.RadioSelect(choices=Persona.CHOICES_GENEROS))
	mano_obra = forms.CharField(label=u'(*) Mano de Obra', widget=forms.RadioSelect(choices=Persona.CHOICES_MANO_OBRA))
	numero_documento = forms.CharField(label=u'(*) Número de documento', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	nacionalidad = forms.CharField(required=False,label='Nacionalidad', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	email = forms.EmailField(required=False,help_text='Ingresar una dirección válida.', widget=forms.EmailInput(attrs={'class' : 'form-control'}))
	fecha_nacimiento = forms.DateField(label='(*) Fecha de nacimiento',widget=forms.SelectDateWidget(years=range((datetime.now().year - 18),(datetime.now().year - 70), -1), attrs={'class' : 'select__year'}))

	class Meta:
		model = Persona
		fields = ('nombres','apellidos','genero','numero_documento','email','departamento_nacimiento','provincia_nacimiento','distrito_nacimiento','fecha_nacimiento','nacionalidad')
		widgets = {
			'departamento_nacimiento': forms.Select(attrs={'class': 'normal__select'}),
			'provincia_nacimiento': forms.Select(attrs={'class': 'normal__select'}),
			'distrito_nacimiento': forms.Select(attrs={'class': 'normal__select'}),
		}

class PersonaForm(forms.ModelForm):

	nombres = forms.CharField(label='(*) Nombres', widget=forms.TextInput(attrs={'class' : 'form-control text-capitalize'}))
	apellidos = forms.CharField(label='(*) Apellidos', widget=forms.TextInput(attrs={'class' : 'form-control text-capitalize'}))
	genero = forms.CharField(label=u'(*) Género', widget=forms.RadioSelect(choices=Persona.CHOICES_GENEROS))
	numero_documento = forms.CharField(label=u'(*) Número de documento', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	email = forms.EmailField(required=False,help_text='Ingresar una dirección válida.', widget=forms.EmailInput(attrs={'class' : 'form-control'}))
	direccion = forms.CharField(label=u'(*) Dirección',widget=forms.TextInput(attrs={'class' : 'form-control text-capitalize','min':0}))
	tiempo_residencia = forms.IntegerField(required=False,label=u'Tiempo residencia', widget=forms.NumberInput(attrs={'class' : 'form-control'}))
	estado_civil = forms.CharField(required=True,label=u'(*) Estado Civil', widget=forms.RadioSelect(choices=Persona.CHOICES_ESTADOS_CIVIL))
	numero_licencia_conducir = forms.CharField(required=False,label='Nro. Licencia Conducir',widget=forms.TextInput(attrs={'class' : 'form-control'}))
	telefono_fijo = forms.CharField(required=False,label=u'Teléfono Fijo',widget=forms.TextInput(attrs={'class' : 'form-control'}))
	celular = forms.CharField(label='(*) Celular Principal',widget=forms.TextInput(attrs={'class' : 'form-control'}))
	celular_dos = forms.CharField(required=False, label='Celular Opcional',widget=forms.TextInput(attrs={'class' : 'form-control'}))
	discapacitado = forms.CharField(label=u'(*) Discapacitado', widget=forms.RadioSelect(choices=((True,'Si'),(False,'No'))))
	imagen = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={'placeholder':'Subir foto','class':'form-control'}))
	nacionalidad = forms.CharField(required=False,label='Nacionalidad', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	verificado = forms.BooleanField(required=False, label='Verificado')
	fecha_nacimiento = forms.DateField(label='(*) Fecha de nacimiento',widget=forms.SelectDateWidget(years=range((datetime.now().year - 18),(datetime.now().year - 70), -1), attrs={'class' : 'select__year'}))
	declaro = forms.BooleanField(required=True, label=' (*) “El Postulante declaró que la información ingresada tal como datos personales, datos académicos, experiencia laboral y dirección de residencia actual es verdadera; en caso de comprobarse alguna falsedad se somete a las sanciones contempladas en el Art. 427° del Código Penal y en concordancia con la Ley de Procedimientos Administrativos Nro.27444.”')

	class Meta:
		model = Persona
		fields = ('nombres','apellidos','genero','tipo_documento','numero_documento','email','departamento_nacimiento','provincia_nacimiento','distrito_nacimiento','departamento_residencia','provincia_residencia','distrito_residencia','direccion','tiempo_residencia','tipo_tiempo_residencia','estado_civil','numero_licencia_conducir','fecha_nacimiento','telefono_fijo','celular','celular_dos','discapacitado','tipo_discapacidad','imagen','nacionalidad','verificado','declaro','ingles')
		widgets = {
			'tipo_documento': forms.Select(attrs={'class': 'normal__select'}),
			'tipo_tiempo_residencia': forms.Select(attrs={'class': 'normal__select'}),
			'tipo_discapacidad': forms.Select(attrs={'class': 'normal__select'}),
			'ingles': forms.Select(attrs={'class': 'normal__select'}),
			'departamento_nacimiento': autocomplete.ModelSelect2(url='departamentos-autocomplete', attrs={'data-placeholder': 'Departamento'}),
			'provincia_nacimiento': autocomplete.ModelSelect2(url='provincias-autocomplete', attrs={'data-placeholder': 'Provincia'} , forward=['departamento_nacimiento']),
			'distrito_nacimiento': autocomplete.ModelSelect2(url='distritos-autocomplete', attrs={'data-placeholder': 'Distrito'} , forward=['provincia_nacimiento']),
			'departamento_residencia': autocomplete.ModelSelect2(url='departamentos-autocomplete', attrs={'data-placeholder': 'Departamento'}),
			'provincia_residencia': autocomplete.ModelSelect2(url='provincias-autocomplete', attrs={'data-placeholder': 'Provincia'} , forward=['departamento_residencia']),
			'distrito_residencia': autocomplete.ModelSelect2(url='distritos-autocomplete', attrs={'data-placeholder': 'Distrito'} , forward=['provincia_residencia'])
		}

	def clean(self):
		cleaned_data = super(PersonaForm, self).clean()

		self.add_error('departamento_nacimiento', "Campo obligatorio.") if not cleaned_data.get("departamento_nacimiento") else ''
		self.add_error('provincia_nacimiento', "Campo obligatorio.") if not cleaned_data.get("provincia_nacimiento") else ''
		self.add_error('distrito_nacimiento', "Campo obligatorio.") if not cleaned_data.get("distrito_nacimiento") else ''

		if cleaned_data.get('distrito_nacimiento'):
			if not cleaned_data.get('provincia_nacimiento').descripcion.lower() == 'talara':
				self.add_error('departamento_residencia', "Campo obligatorio.") if not cleaned_data.get("departamento_residencia") else ''
				self.add_error('provincia_residencia', "Campo obligatorio.") if not cleaned_data.get("provincia_residencia") else ''
				self.add_error('distrito_residencia', "Campo obligatorio.") if not cleaned_data.get("distrito_residencia") else ''
				if cleaned_data.get("distrito_residencia"):
					self.add_error('tiempo_residencia', "Campo obligatorio.") if not cleaned_data.get("tiempo_residencia") and cleaned_data.get('provincia_residencia').descripcion.lower() == 'talara' else ''

class RegisterPublicForm(PersonaForm):
	captcha = ReCaptchaField(widget=ReCaptchaWidget())

class BloqueadoForm(forms.ModelForm):

	numero_documento = forms.CharField(label=u'Número de documento', widget=forms.TextInput(attrs={'class' : 'form-control'}))

	class Meta:
		model = Bloqueados
		fields = ('numero_documento', )

class PersonaInformacionEducativaForm(forms.ModelForm):

	nombre = forms.CharField(required=False, label='Nombres', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	fecha_inicio = forms.DateField(label='Inicio', widget=forms.SelectDateWidget(years=range(datetime.now().year,(datetime.now().year - 70), -1), attrs={'class' : 'select__year'}))
	fecha_fin = forms.DateField(required=False, label='Fin', widget=forms.SelectDateWidget(years=range(datetime.now().year,(datetime.now().year - 70), -1), attrs={'class' : 'select__year'}))
	hasta_actualidad = forms.BooleanField(required=False, label='Hasta hoy')
	
	class Meta:
		model = InformacionEducativa
		fields = ('centro_estudio','nombre','grado','estado_grado','familia_carrera','carrera','fecha_inicio','fecha_fin','hasta_actualidad',)
		widgets = {
			'centro_estudio': autocomplete.ModelSelect2(url='centro-estudio-autocomplete'),
			'grado': forms.Select(attrs={'class':'normal__select'}),
			'estado_grado': forms.Select(attrs={'class':'normal__select'}),
			'familia_carrera': forms.Select(attrs={'class':'normal__select'}),
			'carrera': autocomplete.ModelSelect2(url='carreras-autocomplete', forward=['familia_carrera'])
		}

	def clean(self):
		cleaned_data = super(PersonaInformacionEducativaForm, self).clean()
		now = datetime.now()
		fecha_inicio = datetime.strptime(str(cleaned_data.get("fecha_inicio")),'%Y-%m-%d') if cleaned_data.get("fecha_inicio") else ''
		fecha_fin = datetime.strptime(str(cleaned_data.get("fecha_fin")),'%Y-%m-%d') if cleaned_data.get("fecha_fin") else ''
		hasta_actualidad = cleaned_data.get("hasta_actualidad")

		if hasta_actualidad:
			cleaned_data['fecha_fin'] = None
		else:
			if fecha_fin:
				self.add_error('fecha_fin', "Fecha debe ser menor que la fecha actual.") if fecha_fin >= now else ''
				self.add_error('fecha_fin', "Fecha fiin debe ser mayor.") if fecha_fin <= fecha_inicio else ''
			else:
				self.add_error('fecha_fin', "Fecha fin es obligatoria.")
		if fecha_inicio:
			self.add_error('fecha_inicio', "Fecha debe ser menor que la fecha actual.") if fecha_inicio >= now else ''
				

class PersonaInformacionLaboralForm(forms.ModelForm):

	nombre = forms.CharField(required=False, label='Nombres', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	fecha_inicio = forms.DateField(label='Inicio', widget=forms.SelectDateWidget(years=range(datetime.now().year,(datetime.now().year - 70), -1), attrs={'class' : 'select__year'}))
	fecha_fin = forms.DateField(required=False, label='Fin', widget=forms.SelectDateWidget(years=range(datetime.now().year,(datetime.now().year - 70), -1), attrs={'class' : 'select__year'}))
	hasta_actualidad = forms.BooleanField(required=False, label='Hasta hoy')

	class Meta:
		model = InformacionLaboral
		fields = ('empresa','nombre','fecha_inicio','fecha_fin','familia_puesto','especialidad','sub_especialidad','rango','hasta_actualidad',)
		widgets = {
			'empresa': autocomplete.ModelSelect2(url='empresas-autocomplete'),
			'familia_puesto': forms.Select(attrs={'class':'normal__select'}),
			'especialidad': autocomplete.ModelSelect2(url='especialidades-autocomplete', forward=['familia_puesto']),
			'sub_especialidad': autocomplete.ModelSelect2(url='sub-especialidades-autocomplete', forward=['especialidad']),
			'rango': forms.Select(attrs={'class':'normal__select'}),
		}

	def clean(self):
		cleaned_data = super(PersonaInformacionLaboralForm, self).clean()
		now = datetime.now()
		fecha_inicio = datetime.strptime(str(cleaned_data.get("fecha_inicio")),'%Y-%m-%d') if cleaned_data.get("fecha_inicio") else ''
		fecha_fin = datetime.strptime(str(cleaned_data.get("fecha_fin")),'%Y-%m-%d') if cleaned_data.get("fecha_fin") else ''
		hasta_actualidad = cleaned_data.get("hasta_actualidad")

		if hasta_actualidad:
			cleaned_data['fecha_fin'] = None
		else:
			if fecha_fin:
				self.add_error('fecha_fin', "Fecha debe ser menor que la fecha actual.") if fecha_fin >= now else ''
				self.add_error('fecha_fin', "Fecha fiin debe ser mayor.") if fecha_fin <= fecha_inicio else ''
			else:
				self.add_error('fecha_fin', "Fecha fin es obligatoria.")
		if fecha_inicio:
			self.add_error('fecha_inicio', "Fecha debe ser menor que la fecha actual.") if fecha_inicio >= now else ''

class DocumentosPersonalForm(forms.ModelForm):

	# nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	documento = forms.FileField(required=True,widget=forms.ClearableFileInput(attrs={'placeholder':'Subir documento','class':'form-control'}))

	class Meta:
		model = DocumentosPersonal
		fields = ('tipo','documento')
		widgets = {
			'tipo': forms.Select(attrs={'class':'normal__select'})
		}
		error_messages = {
				NON_FIELD_ERRORS: {
					'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
				}
			}

class CursosPersonaForm(forms.ModelForm):

	fecha_inicio = forms.DateField(label='Inicio', widget=forms.SelectDateWidget(years=range(datetime.now().year,(datetime.now().year - 70), -1), attrs={'class' : 'select__year'}))
	fecha_fin = forms.DateField(required=False, label='Fin', widget=forms.SelectDateWidget(years=range(datetime.now().year,(datetime.now().year - 70), -1), attrs={'class' : 'select__year'}))
	hasta_actualidad = forms.BooleanField(required=False, label='Hasta hoy')
	descripcion = forms.CharField(label=u'Descripción', required=True,widget=forms.Textarea(attrs={'class' : 'form-control', 'rows':'3'}))

	class Meta:
		model = CursosPostulantes
		fields = ('tipo','nombre','descripcion','fecha_inicio','fecha_fin','hasta_actualidad')
		widgets = {
			'tipo': forms.Select(attrs={'class':'normal__select'}),
			'nombre': forms.Select(attrs={'class':'normal__select'})
		}

	def clean(self):
		cleaned_data = super(CursosPersonaForm, self).clean()
		now = datetime.now()
		fecha_inicio = datetime.strptime(str(cleaned_data.get("fecha_inicio")),'%Y-%m-%d') if cleaned_data.get("fecha_inicio") else ''
		fecha_fin = datetime.strptime(str(cleaned_data.get("fecha_fin")),'%Y-%m-%d') if cleaned_data.get("fecha_fin") else ''
		hasta_actualidad = cleaned_data.get("hasta_actualidad")

		if hasta_actualidad:
			cleaned_data['fecha_fin'] = None
		else:
			if fecha_fin:
				self.add_error('fecha_fin', "Fecha debe ser menor que la fecha actual.") if fecha_fin >= now else ''
				self.add_error('fecha_fin', "Fecha fiin debe ser mayor.") if fecha_fin <= fecha_inicio else ''
			else:
				self.add_error('fecha_fin', "Fecha fin es obligatoria.")
		if fecha_inicio:
			self.add_error('fecha_inicio', "Fecha debe ser menor que la fecha actual.") if fecha_inicio >= now else ''