# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import ValidationError
# MODELS
from usuarios.models import Persona, InformacionEducativa
from convocatorias.models import Convocatoria, ConvocatoriaPuesto, PEQ_INT_convocatoria_academico
# FORMS
from usuarios.forms import PersonaInformacionEducativaForm
from convocatorias.forms import ConvocatoriaAcademicoForm
# SERVICES
from maestros.services import *

# PERSONA
@login_required()
@permission_required('usuarios.add_informacioneducativa', raise_exception=True)
def add_educativo_persona(request, uuid):
	persona = get_object_or_404(Persona, uuid=uuid)
	form = PersonaInformacionEducativaForm()
	if request.method == 'POST':
		form = PersonaInformacionEducativaForm(request.POST)
		if form.is_valid():
			educativo = form.save(commit=False)
			educativo.persona = persona
			educativo.save()
			messages.success(request, 'Registro agregado con éxito.')
			form = PersonaInformacionEducativaForm()
	return render(request, 'persona/add.html', {
		'title': 'Información Educativa',
		'persona': persona,
		'form': form
	})

@login_required()
@permission_required('usuarios.change_informacioneducativa', raise_exception=True)
def edit_educativo_persona(request, uuid, pk_educativo):
	persona = get_object_or_404(Persona, uuid=uuid)
	informacioneducativa = get_object_or_404(InformacionEducativa, pk=pk_educativo)
	form = PersonaInformacionEducativaForm(instance=informacioneducativa)
	if request.method == "POST":
		form = PersonaInformacionEducativaForm(request.POST, instance=informacioneducativa)
		if form.is_valid():
			form.save(commit=True)
			messages.success(request, 'Registro modificado con éxito.')
			return redirect('add-educativo-persona', uuid=persona.uuid)
	return render(request, 'persona/add.html', {
		'title': 'Información Educativa',
		'persona': persona,
		'form': form
	})

@login_required()
@permission_required('usuarios.delete_informacioneducativa', raise_exception=True)
def delete_educativo_persona(request, uuid, pk_educativo):
	persona = get_object_or_404(Persona, uuid=uuid)
	informacioneducativa = get_object_or_404(InformacionEducativa, pk=pk_educativo)
	if request.method == 'POST':
		informacioneducativa.delete()
		messages.success(request, 'Registro eliminado con éxito.')
		return redirect('add-educativo-persona', uuid=persona.uuid)
	return render(request, 'persona/delete.html', {
		'title': 'Eliminar registro de Información Educativa',
		'persona': persona,
		'informacioneducativa': informacioneducativa
	})

# CONVOCATORIA
@login_required()
@permission_required('convocatorias.add_peq_int_convocatoria_academico', raise_exception=True)
def add_educativo_convocatoria_puesto(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	form = None
	if puesto_convocatoria_has_persons(convocatoria_puesto):
		messages.error(request, 'No se puede agregar porque existe personal involucrado.')
	else:
		form = ConvocatoriaAcademicoForm()
		if request.method == 'POST':
			form = ConvocatoriaAcademicoForm(request.POST)
			if form.is_valid():
				educativo = form.save(commit=False)
				educativo.convocatoria_puesto = convocatoria_puesto
				if Duplicate(PEQ_INT_convocatoria_academico, {'convocatoria_puesto':convocatoria_puesto, 'familia_carrera': form.cleaned_data['familia_carrera'], 'carrera': form.cleaned_data['carrera'], 'grado': form.cleaned_data['grado'], 'estado_grado': form.cleaned_data['estado_grado']}):
					messages.error(request, 'Registro duplicado.')
				else:
					educativo.save()
					messages.success(request, 'Registro modificado con éxito.')
					form = ConvocatoriaAcademicoForm()
	return render(request, 'educativo_convocatoria/add.html', {
		'title': 'Información Educativa',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('convocatorias.change_peq_int_convocatoria_academico', raise_exception=True)
def edit_educativo_convocatoria_puesto(request, uuid, pk_educativo):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	informacioneducativa = get_object_or_404(PEQ_INT_convocatoria_academico, pk=pk_educativo)
	form = None
	if puesto_convocatoria_has_persons(convocatoria_puesto):
		messages.error(request, 'No se puede editar porque existe personal involucrado.')
	else:
		form = ConvocatoriaAcademicoForm(instance=informacioneducativa)
		if request.method == "POST":
			form = ConvocatoriaAcademicoForm(request.POST, instance=informacioneducativa)
			if form.is_valid():
				if Duplicate(PEQ_INT_convocatoria_academico, {'convocatoria_puesto':convocatoria_puesto, 'familia_carrera': form.cleaned_data['familia_carrera'], 'carrera': form.cleaned_data['carrera'], 'grado': form.cleaned_data['grado'], 'estado_grado': form.cleaned_data['estado_grado']}):
					messages.error(request, 'Registro duplicado.')
				else:
					form.save()
					messages.success(request, 'Registro modificado con éxito.')
					return redirect('add-educativo-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
	return render(request, 'educativo_convocatoria/add.html', {
		'title': 'Información Educativa',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('convocatorias.delete_peq_int_convocatoria_academico', raise_exception=True)
def delete_educativo_convocatoria_puesto(request, uuid, pk_educativo):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	informacioneducativa = get_object_or_404(PEQ_INT_convocatoria_academico, pk=pk_educativo)
	if puesto_convocatoria_has_persons(convocatoria_puesto):
		messages.error(request, 'No se puede eliminar porque existe personal involucrado.')
	else:
		if request.method == 'POST':
			informacioneducativa.delete()
			messages.success(request, 'Registro eliminado con éxito.')
			return redirect('add-educativo-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
	return render(request, 'educativo_convocatoria/delete.html', {
		'title': 'Eliminar registro de Información Educativa',
		'convocatoria_puesto': convocatoria_puesto,
		'informacioneducativa': informacioneducativa
	})