# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
# MODELS
from usuarios.models import Persona, InformacionLaboral
from convocatorias.models import ConvocatoriaPuesto, PEQ_INT_convocatoria_experiencia, NORMAL, CRITERIO
from maestros.models import PEQ_MAE_tiempo_experiencia, PEQ_MAE_familia, PEQ_MAE_sub_especialidad
# FORMS
from usuarios.forms import PersonaInformacionLaboralForm
from convocatorias.forms import ConvocatoriaExperienciaForm
# SERVICES
from maestros.services import *

# PERSONA
@login_required()
@permission_required('usuarios.add_informacionlaboral', raise_exception=True)
def add_laboral_persona(request, uuid):
	persona = get_object_or_404(Persona, uuid=uuid)
	form = PersonaInformacionLaboralForm()
	if request.method == 'POST':
		form = PersonaInformacionLaboralForm(request.POST)
		if form.is_valid():
			laboral = form.save(commit=False)
			laboral.persona = persona
			laboral.save()
			messages.success(request, 'Registro agregado con éxito.')
			form = PersonaInformacionLaboralForm()
	return render(request, 'personalaboral/add.html', {
		'title': 'Información Laboral',
		'persona': persona,
		'form': form
	})

@login_required()
@permission_required('usuarios.change_informacionlaboral', raise_exception=True)
def edit_laboral_persona(request, uuid, pk_laboral):
	persona = get_object_or_404(Persona, uuid=uuid)
	informacionlaboral = get_object_or_404(InformacionLaboral, pk=pk_laboral)
	form = PersonaInformacionLaboralForm(instance=informacionlaboral)
	if request.method == "POST":
		form = PersonaInformacionLaboralForm(request.POST, instance=informacionlaboral)
		if form.is_valid():
			form.save(commit=True)
			messages.success(request, 'Registro modificado con éxito.')
			return redirect('add-laboral-persona', uuid=persona.uuid)
	return render(request, 'personalaboral/add.html', {
		'title': 'Información Laboral',
		'persona': persona,
		'form': form
	})

@login_required()
@permission_required('usuarios.delete_informacionlaboral', raise_exception=True)
def delete_laboral_persona(request, uuid, pk_laboral):
	persona = get_object_or_404(Persona, uuid=uuid)
	informacionlaboral = get_object_or_404(InformacionLaboral, pk=pk_laboral)
	if request.method == 'POST':
		informacionlaboral.delete()
		messages.success(request, 'Registro eliminado con éxito.')
		return redirect('add-laboral-persona', uuid=persona.uuid)
	return render(request, 'personalaboral/delete.html', {
		'title': 'Eliminar registro de Información Laboral',
		'persona': persona,
		'informacionlaboral': informacionlaboral
	})

# CONVOCATORIA
@login_required()
@permission_required('convocatorias.add_peq_int_convocatoria_experiencia', raise_exception=True)
def add_experiencia_convocatoria_puesto(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	form = None
	if puesto_convocatoria_has_persons(convocatoria_puesto):
		messages.error(request, 'No se puede agregar porque existe personal involucrado.')
	else:
		form = ConvocatoriaExperienciaForm()
		if request.method == 'POST':
			form = ConvocatoriaExperienciaForm(request.POST)
			if form.is_valid():
				laboral = form.save(commit=False)
				laboral.convocatoria_puesto = convocatoria_puesto
				if Duplicate(PEQ_INT_convocatoria_experiencia, {'convocatoria_puesto':convocatoria_puesto, 'especialidad': form.cleaned_data['especialidad'], 'familia_puesto': form.cleaned_data['familia_puesto'], 'sub_especialidad': form.cleaned_data['sub_especialidad'], 'rango': form.cleaned_data['rango'], 'tipo_registro': NORMAL}):
					messages.error(request, 'Registro duplicado.')
				else:
					laboral.save()
					messages.success(request, 'Registro agregado con éxito.')
					form = ConvocatoriaExperienciaForm()
		choices_tiempos = [('','seleccionar')]
		[choices_tiempos.append((registro.uuid, str(registro.tiempo)+' '+registro.get_tipo_display() )) for registro in PEQ_MAE_tiempo_experiencia.objects.all().order_by('-tipo','tiempo')]
		form.fields['experiencia'].choices = choices_tiempos 
		# INITIAL
		form.fields['rango'].initial = convocatoria_puesto.rango.uuid if convocatoria_puesto.rango else ''
		form.fields['familia_puesto'].initial = convocatoria_puesto.familia_puesto.uuid if convocatoria_puesto.familia_puesto else ''
		form.fields['especialidad'].initial = convocatoria_puesto.especialidad.uuid if convocatoria_puesto.especialidad else ''
		form.fields['sub_especialidad'].initial = convocatoria_puesto.sub_especialidad.uuid if convocatoria_puesto.sub_especialidad else ''
	return render(request, 'laboral_convocatoria/add.html', {
		'title': 'Información Laboral',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('convocatorias.change_peq_int_convocatoria_experiencia', raise_exception=True)
def edit_experiencia_convocatoria_puesto(request, uuid, pk_experiencia):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	informacionlaboral = get_object_or_404(PEQ_INT_convocatoria_experiencia, pk=pk_experiencia)
	form = None
	if puesto_convocatoria_has_persons(convocatoria_puesto):
		messages.error(request, 'No se puede editar porque existe personal involucrado.')
	else:
		form = ConvocatoriaExperienciaForm(instance=informacionlaboral)
		if request.method == "POST":
			form = ConvocatoriaExperienciaForm(request.POST, instance=informacionlaboral)
			if form.is_valid():
				if Duplicate(PEQ_INT_convocatoria_experiencia, {'convocatoria_puesto':convocatoria_puesto, 'especialidad': form.cleaned_data['especialidad'], 'familia_puesto': form.cleaned_data['familia_puesto'], 'sub_especialidad': form.cleaned_data['sub_especialidad'], 'rango': form.cleaned_data['rango'], 'tipo_registro': NORMAL}):
					messages.error(request, 'Registro duplicado.')
				else:
					form.save()
					messages.success(request, 'Registro modificado con éxito.')
					return redirect('add-laboral-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
		choices_tiempos = [('','seleccionar')]
		[choices_tiempos.append((registro.uuid, str(registro.tiempo)+' '+registro.get_tipo_display() )) for registro in PEQ_MAE_tiempo_experiencia.objects.all().order_by('-tipo','tiempo')]
		form.fields['experiencia'].choices = choices_tiempos
	return render(request, 'laboral_convocatoria/add.html', {
		'title': 'Información Laboral',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('convocatorias.delete_peq_int_convocatoria_experiencia', raise_exception=True)
def delete_experiencia_convocatoria_puesto(request, uuid, pk_experiencia):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	informacionlaboral = get_object_or_404(PEQ_INT_convocatoria_experiencia, pk=pk_experiencia)
	if puesto_convocatoria_has_persons(convocatoria_puesto):
		messages.error(request, 'No se puede eliminar porque existe personal involucrado.')
	else:
		if request.method == 'POST':
			informacionlaboral.delete()
			messages.success(request, 'Registro eliminado con éxito.')
			return redirect('add-laboral-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
	return render(request, 'laboral_convocatoria/delete.html', {
		'title': 'Eliminar registro de Información Laboral',
		'convocatoria_puesto': convocatoria_puesto,
		'informacionlaboral': informacionlaboral
	})