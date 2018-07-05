# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib import messages
# services
from maestros.services import *
# models
from .models import *
from convocatorias.models import Convocatoria, PostulacionConvocatoria, ConvocatoriaPuesto
from maestros.models import PEQ_MAE_departamentos, PEQ_MAE_provincias, PEQ_MAE_distritos, PEQ_MAE_rango_seleccion, PEQ_MAE_carreras
# forms
from .forms import *
import json
# RESTFRAMEWORK
from rest_framework import generics
# SERIALIZERS
from .serializers import *
from maestros.serializers import CentroEstudioSerializer
from rest_framework.response import Response
# PDF
from io import BytesIO
from maestros.pdfs import PDFCurriculum
# REST FRAMEWORK
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from convocatorias.views import get_rango_seleccion
from datetime import datetime
import xlrd

# AUTOCOMPLETE
from dal import autocomplete

class PersonaAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated():
			return Persona.objects.none()

		qs = Persona.objects.all()

		if self.q:
			qs = qs.filter(Q(nombres__icontains=self.q) | Q(apellidos__icontains=self.q) | Q(numero_documento__icontains=self.q))

		return qs[:20]

	def get_result_label(self, item):
		return item.numero_documento +' '+ item.nombres.upper() +' '+ item.apellidos.upper()

	def get_selected_result_label(self, item):
		return item.numero_documento

class CentroEstudioAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated():
			return PEQ_MAE_centros_estudio.objects.none()

		qs = PEQ_MAE_centros_estudio.objects.all().order_by('descripcion')

		if self.q:
			qs = qs.filter(descripcion__icontains=self.q)

		return qs

class NombreCursoAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated():
			return PEQ_MAE_cursos.objects.none()

		qs = PEQ_MAE_cursos.objects.all().order_by('descripcion')

		if self.q:
			qs = qs.filter(descripcion__icontains=self.q)

		return qs

class EmpresasAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated():
			return PEQ_MAE_empresas.objects.none()

		qs = PEQ_MAE_empresas.objects.all().order_by('descripcion')

		if self.q:
			qs = qs.filter(descripcion__icontains=self.q)

		return qs

class CarrerasAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated():
			return PEQ_MAE_carreras.objects.none()

		qs = PEQ_MAE_carreras.objects.all().order_by('descripcion')

		familia_carrera = self.forwarded.get('familia_carrera', None)

		if familia_carrera:
			qs = qs.filter(familia_carrera=familia_carrera)

		if self.q:
			qs = qs.filter(descripcion__icontains=self.q)

		return qs

class EspecialidadesAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated():
			return PEQ_MAE_familia.objects.none()

		qs = PEQ_MAE_familia.objects.all().order_by('descripcion')

		familia_puesto = self.forwarded.get('familia_puesto', None)

		if familia_puesto:
			qs = qs.filter(familia_puesto=familia_puesto)

		if self.q:
			qs = qs.filter(descripcion__icontains=self.q)

		return qs

class SubEspecialidadesAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated():
			return PEQ_MAE_sub_especialidad.objects.none()

		qs = PEQ_MAE_sub_especialidad.objects.all().order_by('descripcion')

		especialidad = self.forwarded.get('especialidad', None)

		if especialidad:
			qs = qs.filter(especialidad=especialidad)

		if self.q:
			qs = qs.filter(name__icontains=self.q)

		return qs

class PersonaInformacionLaboralList(generics.ListCreateAPIView):
	serializer_class = InformacionLaboralSerializer

	def list(self, request, uuid):
		# Note the use of `get_queryset()` instead of `self.queryset`
		persona = get_object_or_404(Persona, uuid=uuid)
		laboral = InformacionLaboral.objects.filter(persona=persona)
		educativo = InformacionEducativa.objects.filter(persona=persona)
		serializer = InformacionLaboralSerializer(laboral, many=True)
		serializer_educativo = InformacionEducativaSerializer(educativo, many=True)
		return Response({ 'persona': PersonaSerializer(persona).data ,'laboral':serializer.data, 'educativo': serializer_educativo.data})
# PDF
def PdfCurriculum(request, uuid):
	persona = get_object_or_404(Persona, uuid=uuid)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="'+persona.numero_documento+'.pdf"'
	buffer = BytesIO()
	report = PDFCurriculum(buffer, 'A4', uuid)
	pdf = report.print_curriculum()
	response.write(pdf)
	return response

def logout_view(request):
	rol = request.user.role.rol if hasattr(request.user,'role') else ''
	logout(request)
	return redirect('/login/') if not rol == Role.POSTULANTE else redirect('index-publico')

def login_view(request):
	message = {'message':''}
	if request.user.is_authenticated:
		return redirect('/convocatorias/')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if request.GET.get('next'):
				return redirect(request.GET.get('next'))
			return redirect('/convocatorias/')
		else:
			message['message'] = "Usuario y/o contraseña no validos."
			message['class'] = "danger"
	return render(request, 'registration/login.html', {'message':message})

def find_persona(request):
	if request.GET.get('numero_documento'):
		numero_documento = request.GET.get('numero_documento')
		postulantes_uuid = [ postulacion.persona.uuid for postulacion in  PostulacionConvocatoria.objects.filter(convocatoria_puesto__uuid=request.GET.get('convocatoria_puesto'))]
		personas = Persona.objects.filter(numero_documento__icontains=numero_documento).exclude(uuid__in=postulantes_uuid)[:5]
		data = []
		convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=request.GET.get('convocatoria_puesto'))
		for persona in personas:
			totales = get_rango_seleccion(convocatoria_puesto, persona)
			total = totales['academico']+totales['laboral']+totales['cursos']
			rango = PEQ_MAE_rango_seleccion.objects.filter(minimo__lte=total, maximo__gte=total).first()
			data.append({'uuid':persona.uuid, 'rango':{'uuid':rango.uuid, 'descripcion':rango.descripcion},'porcentaje':total,'nombres_apellidos':persona.nombres+' '+persona.apellidos, 'lugar_nacimiento': persona.distrito_nacimiento.descripcion.lower() if persona.distrito_nacimiento else '', 'celular': persona.celular, 'numero_documento': persona.numero_documento, 'direccion': persona.direccion, 'genero': persona.get_genero_display()})
		return JsonResponse({'data':data}, status=200)

@login_required()
@permission_required('usuarios.read_persona', raise_exception=True)
def index_personas(request):
	personas = Persona.objects.all()
	if request.GET.get('search'):
		search = request.GET.get('search')
		personas = Persona.objects.filter(Q(numero_documento__icontains=search) | Q(nombres__icontains=search) | Q(apellidos__icontains=search))
	return render(request, 'personas/index_personas.html', {
		'personas': personas[:20]
	})

@login_required()
@permission_required('usuarios.read_postulaciones', raise_exception=True)
def persona_postulaciones(request, uuid):
	persona = get_object_or_404(Persona, uuid=uuid)
	postulaciones = PostulacionConvocatoria.objects.filter(persona=persona)
	return render(request, 'personas/persona_postulaciones.html', {
		'title': 'Postulaciones',
		'postulaciones': postulaciones,
		'persona': persona
	})

@login_required()
@permission_required('usuarios.add_bloqueados', raise_exception=True)
def add_bloquear_persona(request):
	form = BloqueadoForm()
	messages = {'message_form_one': '', 'class_message_form_one': '' }
	bloqueados = []
	if request.method == "POST":
		if request.POST.get('tipo') == 'add_numero_documento':
			form = BloqueadoForm(request.POST)
			if form.is_valid():
				bloqueado = form.save(commit=False)
				# bloqueado.user = request.user
				bloqueado.save()
				messages['message_form_one'] = 'Agregado con éxito.'
				messages['class_message_form_one'] = 'text-success'
				form = BloqueadoForm()
		elif request.POST.get('tipo') == 'add_file_documentos':
			book = xlrd.open_workbook(filename=None, file_contents=request.FILES.get('file_excel').file.read())
			worksheet = book.sheet_by_name(book.sheet_names()[0])
			documentos_bloqueados = [obj.numero_documento for obj in Bloqueados.objects.all()]
			for row in xrange(1, worksheet.nrows):
				documento = str(worksheet.cell_value(row, 5)).split('.')[0]
				if documento not in documentos_bloqueados:
					bloqueados.append(Bloqueados(nombres=worksheet.cell_value(row, 4), apellidos=worksheet.cell_value(row, 3), numero_documento=documento))
			Bloqueados.objects.bulk_create(bloqueados) if bloqueados else ''

	return render(request, 'personas/add_bloquear.html',{
		'form': form,
		'bloqueados':bloqueados,
		'messages': messages
	})

@login_required()
@permission_required('usuarios.add_persona', raise_exception=True)
def add_persona(request):
	form = PersonaForm()
	params_get = ''
	convocatoria_puesto = ''
	if request.GET.get('convocatoria_puesto'):
		convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=request.GET.get('convocatoria_puesto')) 
		params_get = '?convocatoria_puesto='+str(convocatoria_puesto.uuid)
		if not convocatoria_is_authorized(convocatoria_puesto.convocatoria):
			messages.error(request, 'La convocatoria no esta autorizada.')
	if request.method == "POST":
		form = PersonaForm(request.POST, request.FILES)
		if form.is_valid():
			password = User.objects.make_random_password()
			user, created = User.objects.update_or_create(username=form.cleaned_data['numero_documento'], email=form.cleaned_data['email'])
			user.set_password(password)
			user.save()
			persona = form.save(commit=False)
			persona.user = user
			persona.save()
			Role.objects.create(rol=Role.POSTULANTE, user=user)
			# ENVIAR CORREO
			message_html = u'<h1><strong>Usuario</strong></h1><hr>\n'\
							u'<h3><strong>Username: </strong>{username}</h3>\n'\
							u'<h3><strong>Contraseña: </strong>{password}</h3>\n'\
							u'<p><a href="{url_login}" target="_blank">Clic aquí para ingresar {url_login}</a></p>'.format(username=user.username, password=password, url_login=settings.URL_SITE+'/login/postulantes')
			enviar_email(persona.email,'Creacion de usuario',message_html) if persona.email else ''
			if request.POST.get('checkbox_postular_convocatoria_puesto'):
				if convocatoria_is_authorized(convocatoria_puesto.convocatoria):
					postulacion_convocatoria_puesto = PostulacionConvocatoria()
					postulacion_convocatoria_puesto.convocatoria_puesto = convocatoria_puesto
					postulacion_convocatoria_puesto.persona = persona
					postulacion_convocatoria_puesto.tipo_ingreso = 'directo'
					postulacion_convocatoria_puesto.save()
			return redirect('add-educativo-persona', persona.uuid)
	return render(request, 'personas/add_persona.html', { 
		'title': 'Agregar persona', 
		'form': form,
		'departamentos': PEQ_MAE_departamentos.objects.all().order_by('descripcion'),
		'convocatoria_puesto' : convocatoria_puesto 
	})

@login_required()
@permission_required('usuarios.change_persona', raise_exception=True)
def edit_persona(request, uuid):
	persona = get_object_or_404(Persona, uuid=uuid)
	form = PersonaForm(instance=persona)
	if request.method == "POST":
		form = PersonaForm(request.POST, request.FILES, instance=persona)
		if form.is_valid():
			persona = form.save(commit=False)
			persona.save()
			return redirect('add-educativo-persona', uuid=persona.uuid)
	return render(request, 'personas/add_persona.html', { 
		'title': 'Editar persona', 
		'departamentos': PEQ_MAE_departamentos.objects.all().order_by('descripcion'),
		'form': form
	})

# DOCUMENTOS
@login_required()
@permission_required('usuarios.add_documentospersonal', raise_exception=True)
def add_documentos_persona(request, uuid): 
	persona = get_object_or_404(Persona, uuid=uuid)
	form = DocumentosPersonalForm()
	if request.method == 'POST':
		form = DocumentosPersonalForm(request.POST, request.FILES)
		if form.is_valid():
			documento = form.save(commit=False)
			documento.persona = persona
			if Duplicate(DocumentosPersonal, {'persona':persona, 'tipo': form.cleaned_data['tipo']}):
				messages.error(request, 'Registro duplicado.')
			else:
				documento.save()
				messages.success(request, 'Registro agregado con éxito.')
				form = DocumentosPersonalForm()
	return render(request, 'personas/documentos/add.html', {
		'title': 'Documentos',
		'persona': persona,
		'form': form
	})

@login_required()
@permission_required('usuarios.change_documentospersonal', raise_exception=True)
def edit_documentos_persona(request, uuid, pk_documento):
	persona = get_object_or_404(Persona, uuid=uuid)
	documento_persona = get_object_or_404(DocumentosPersonal, pk=pk_documento)
	form = DocumentosPersonalForm(instance=documento_persona)
	if request.method == "POST":
		form = DocumentosPersonalForm(request.POST, request.FILES, instance=documento_persona)
		if form.is_valid():
			if Duplicate(DocumentosPersonal, {'persona':persona, 'tipo': form.cleaned_data['tipo']}):
				messages.error(request, 'Registro duplicado.')
			else:
				form.save(commit=True)
				messages.success(request, 'Registro modificado con éxito.')
				return redirect('add-documento-persona', uuid=persona.uuid)
	return render(request, 'personas/documentos/add.html', {
		'title': 'Documentos',
		'persona': persona,
		'form': form
	})

@login_required()
@permission_required('usuarios.delete_documentospersonal', raise_exception=True)
def delete_documentos_persona(request, uuid, pk_documento):
	persona = get_object_or_404(Persona, uuid=uuid)
	documento_persona = get_object_or_404(DocumentosPersonal, pk=pk_documento)
	if request.method == 'POST':
		documento_persona.delete()
		messages.success(request, 'Registro eliminado con éxito.')
		return redirect('add-documento-persona', uuid=persona.uuid)
	return render(request, 'personas/documentos/delete.html', {
		'title': 'Eliminar registro de documento',
		'persona': persona,
		'documento_persona': documento_persona
	})

# EXCEL
import xlwt
def ExcelInformacionPersonas(request):
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Informacion personas.xls"'
	book = xlwt.Workbook(encoding='utf8')
	sheet_educativo = book.add_sheet('EDUCATIVO')

	for index, item in enumerate(['nombres','apellidos','numero documento','centro educativo', 'grado', 'estado grado', 'familia carrera', 'carrera']):
		sheet_educativo.write(0,index, item.upper())	

	educativo = InformacionEducativa.objects.all().order_by('persona__nombres','persona__apellidos')

	for index, item in enumerate(educativo):
		sheet_educativo.write((index+1),0, item.persona.nombres)
		sheet_educativo.write((index+1),1, item.persona.apellidos)
		sheet_educativo.write((index+1),2, item.persona.numero_documento)
		sheet_educativo.write((index+1),3, item.centro_estudio.descripcion if item.centro_estudio else '')
		sheet_educativo.write((index+1),4, item.grado.descripcion if item.grado else '')
		sheet_educativo.write((index+1),5, item.estado_grado.descripcion if item.estado_grado else '')
		sheet_educativo.write((index+1),6, item.familia_carrera.descripcion if item.familia_carrera else '')
		sheet_educativo.write((index+1),7, item.carrera.descripcion if item.carrera else '')

	sheet_laboral = book.add_sheet('LABORAL')

	for index, item in enumerate(['nombres','apellidos','numero documento','empresa', 'rango', 'famlia puesto', 'especialidad', 'subespecialidad']):
		sheet_laboral.write(0,index, item.upper())	

	laboral = InformacionLaboral.objects.all().order_by('persona__nombres','persona__apellidos')

	for index, item in enumerate(laboral):
		sheet_laboral.write((index+1),0, item.persona.nombres)
		sheet_laboral.write((index+1),1, item.persona.apellidos)
		sheet_laboral.write((index+1),2, item.persona.numero_documento)
		sheet_laboral.write((index+1),3, item.empresa.descripcion if item.empresa else '')
		sheet_laboral.write((index+1),4, item.rango.descripcion if item.rango else '')
		sheet_laboral.write((index+1),5, item.familia_puesto.descripcion if item.familia_puesto else '')
		sheet_laboral.write((index+1),6, item.especialidad.descripcion if item.especialidad else '')
		sheet_laboral.write((index+1),7, item.sub_especialidad.descripcion if item.sub_especialidad else '')

	book.save(response)
	return response
