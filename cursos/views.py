# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
# MODELS
from usuarios.models import Persona, CursosPostulantes
from convocatorias.models import ConvocatoriaPuesto, PEQ_INT_convocatoria_cursos, NORMAL
# FORMS
from usuarios.forms import CursosPersonaForm
from convocatorias.forms import ConvocatoriaCursosForm
# SERVICES
from maestros.services import Duplicate

# PERSONA
@login_required()
@permission_required('usuarios.add_cursospostulante', raise_exception=True)
def add_curso_persona(request, uuid): 
	persona = get_object_or_404(Persona, uuid=uuid)
	form = CursosPersonaForm()
	if request.method == 'POST':
		form = CursosPersonaForm(request.POST)
		if form.is_valid():
			curso = form.save(commit=False)
			curso.persona = persona
			curso.save()
			messages.success(request, 'Registro agregado con éxito.')
			form = CursosPersonaForm()
	return render(request, 'personacursos/add.html', {
		'title': 'Estudios Complementarios',
		'persona': persona,
		'form': form
	})

@login_required()
@permission_required('usuarios.change_cursospostulante', raise_exception=True)
def edit_curso_persona(request, uuid, pk_curso):
	persona = get_object_or_404(Persona, uuid=uuid)
	curso_persona = get_object_or_404(CursosPostulantes, pk=pk_curso)
	form = CursosPersonaForm(instance=curso_persona)
	if request.method == "POST":
		form = CursosPersonaForm(request.POST, instance=curso_persona)
		if form.is_valid():
			form.save(commit=True)
			messages.success(request, 'Registro modificado con éxito.')
			return redirect('add-curso-persona', uuid=persona.uuid)
	return render(request, 'personacursos/add.html', {
		'title': 'Estudios Complementarios',
		'persona': persona,
		'form': form
	})

@login_required()
@permission_required('usuarios.delete_cursospostulante', raise_exception=True)
def delete_curso_persona(request, uuid, pk_curso):
	persona = get_object_or_404(Persona, uuid=uuid)
	curso_persona = get_object_or_404(CursosPostulantes, pk=pk_curso)
	if request.method == 'POST':
		curso_persona.delete()
		messages.success(request, 'Registro eliminado con éxito.')
		return redirect('add-curso-persona', uuid=persona.uuid)
	return render(request, 'personacursos/delete.html', {
		'title': 'Eliminar registro de curso',
		'persona': persona,
		'curso_persona': curso_persona
	})

# CONVOCATORIA
@login_required()
@permission_required('usuarios.add_peq_int_convocatoria_cursos', raise_exception=True)
def add_curso_convocatoria_puesto(request, uuid): 
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	form = ConvocatoriaCursosForm()
	if request.method == 'POST':
		form = ConvocatoriaCursosForm(request.POST)
		if form.is_valid():
			curso = form.save(commit=False)
			curso.convocatoria_puesto = convocatoria_puesto
			if Duplicate(PEQ_INT_convocatoria_cursos, {'convocatoria_puesto': convocatoria_puesto, 'tipo': form.cleaned_data['tipo'], 'nombre': form.cleaned_data['nombre'], 'tipo_registro': NORMAL}):
				messages.error(request, 'Registro duplicado.')
			else:	
				curso.save()
				messages.success(request, 'Registro agregado con éxito.')
				form = ConvocatoriaCursosForm()
	return render(request, 'cursos_convocatoria/add.html', {
		'title': 'Estudios Complementarios',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('usuarios.change_peq_int_convocatoria_cursos', raise_exception=True)
def edit_curso_convocatoria_puesto(request, uuid, pk_curso):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	curso_persona = get_object_or_404(PEQ_INT_convocatoria_cursos, pk=pk_curso)
	form = ConvocatoriaCursosForm(instance=curso_persona)
	if request.method == "POST":
		form = ConvocatoriaCursosForm(request.POST, instance=curso_persona)
		if form.is_valid():
			if Duplicate(PEQ_INT_convocatoria_cursos, {'convocatoria_puesto': convocatoria_puesto, 'tipo': form.cleaned_data['tipo'], 'nombre': form.cleaned_data['nombre'], 'tipo_registro': NORMAL}):
				messages.error(request, 'Registro duplicado.')
			else:	
				form.save(commit=True)
				messages.success(request, 'Registro modificado con éxito.')
				return redirect('add-curso-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
	return render(request, 'cursos_convocatoria/add.html', {
		'title': 'Estudios Complementarios',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('usuarios.delete_peq_int_convocatoria_cursos', raise_exception=True)
def delete_curso_convocatoria_puesto(request, uuid, pk_curso):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	curso_convocatoria = get_object_or_404(PEQ_INT_convocatoria_cursos, pk=pk_curso)
	if request.method == 'POST':
		curso_convocatoria.delete()
		messages.success(request, 'Registro eliminado con éxito.')
		return redirect('add-curso-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
	return render(request, 'cursos_convocatoria/delete.html', {
		'title': 'Eliminar registro de curso',
		'convocatoria_puesto': convocatoria_puesto,
		'curso_convocatoria': curso_convocatoria
	})