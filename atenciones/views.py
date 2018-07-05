# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required

from .forms import AtencionForm, FinalizarAtencionForm
# models
from .models import Atenciones
from maestros.models import PEQ_MAE_tipo_atencion

from io import BytesIO
from .pdfs import PDFAtenciones

from datetime import datetime

def index_atenciones(request):
	atenciones = Atenciones.objects.all()
	tipo_selected = get_object_or_404(PEQ_MAE_tipo_atencion, uuid=request.GET.get('tipo')) if request.GET.get('tipo') else ''
	dni = request.GET.get('dni')
	fecha_inicio = request.GET.get('fecha_inicio')
	fecha_fin = request.GET.get('fecha_fin')
	atenciones = atenciones.filter(dni__icontains=dni) if dni else atenciones
	atenciones = atenciones.filter(tipo=tipo_selected) if tipo_selected else atenciones
	if fecha_inicio and fecha_fin:
		atenciones = atenciones.filter(fecha__range=(fecha_inicio, fecha_fin))
	elif fecha_inicio:
		atenciones = atenciones.filter(fecha=fecha_inicio)
	tipo_atenciones = PEQ_MAE_tipo_atencion.objects.all()
	if request.method == 'POST':
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="Atenciones '+fecha_inicio+(' hasta '+fecha_fin if fecha_fin else '')+' '+(tipo_selected.descripcion if tipo_selected else '')+'.pdf"'
		buffer = BytesIO()
		report = PDFAtenciones(buffer, 'A4', atenciones)
		pdf = report.print_atenciones()
		response.write(pdf)
		return response
	return render(request, 'atenciones/index_atenciones.html', {
		'atenciones': atenciones.order_by('-fecha_creacion')[:20],
		'tipo_atenciones': tipo_atenciones,
		'tipo_selected': tipo_selected,
		'dni': dni,
		'inicio': fecha_inicio,
		'fin': fecha_fin
	})

@login_required()
@permission_required('atenciones.add_atenciones', raise_exception=True)
def add_atencion(request):
	form = AtencionForm()
	if request.method == "POST":
		form = AtencionForm(request.POST)
		if form.is_valid():
			atencion = form.save(commit=False)
			atencion.user = request.user
			atencion.save()
			form = AtencionForm()
			messages.success(request, 'Registro agregado correctamente.')
	form.fields['fecha'].initial = datetime.now().strftime('%Y-%m-%d')
	form.fields['hora_inicio'].initial = datetime.now().strftime('%H:%M')
	return render(request, 'atenciones/add_atencion.html', { 
		'title': 'Agregar atención',
		'form': form
	})

@login_required()
@permission_required('atenciones.change_atenciones', raise_exception=True)
def edit_atencion(request, uuid):
	atencion = get_object_or_404(Atenciones, uuid=uuid)
	form = AtencionForm(instance=atencion)
	form2 = FinalizarAtencionForm(instance=atencion) if atencion.finalizada else None
	if request.method == "POST":
		form = AtencionForm(request.POST, instance=atencion)
		form2 = FinalizarAtencionForm(request.POST, instance=atencion) if atencion.finalizada else None
		if form.is_valid():
			form.save()
			messages.success(request, 'Atención modificada correctamente.')
		if form2:
			if form2.is_valid():
				form2.save()
				return redirect('index-atenciones')
		elif form.is_valid():
			return redirect('index-atenciones')

	return render(request, 'atenciones/edit_atencion.html', { 
		'title': 'Editar atención',
		'form': form,
		'form2': form2
	})

@login_required()
@permission_required('atenciones.delete_atenciones', raise_exception=True)
def delete_atencion(request, uuid):
	atencion = get_object_or_404(Atenciones, uuid=uuid)
	if request.method == 'POST':
		atencion.delete()
		messages.success(request, 'Registro eliminado con éxito.')
		return redirect('index-atenciones')
	return render(request, 'atenciones/delete_atencion.html', {
		'title': 'Eliminar Atención',
		'atencion': atencion
	})

@login_required()
@permission_required('atenciones.add_atenciones', raise_exception=True)
def finalizar_atencion(request, uuid):
	atencion = get_object_or_404(Atenciones, uuid=uuid)
	form = FinalizarAtencionForm()
	if request.method == "POST":
		form = FinalizarAtencionForm(request.POST, instance=atencion)
		if form.is_valid():
			atencion.finalizada = True
			atencion.save()
			messages.success(request, 'Atención finalizada correctamente.')
			return redirect('index-atenciones')
	form.fields['hora_fin'].initial = datetime.now().strftime('%H:%M')
	form.fields['fecha_finalizacion'].initial = datetime.now().strftime('%Y-%m-%d')
	return render(request, 'atenciones/finalizar_atencion.html', { 
		'title': 'Finalizar Atención',
		'atencion': atencion,
		'form': form
	})
	