# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Max, Sum
from django.contrib import messages
# MODELS
from .models import *
from maestros.models import PEQ_MAE_tipo_cursos, PEQ_MAE_estados_convocatoria, PEQ_MAE_estados_postulacion, PEQ_MAE_tags, PEQ_MAE_requisitos, PEQ_MAE_rango_seleccion, PEQ_MAE_detalle_documentacion, PEQ_MAE_rangos, PEQ_MAE_sub_especialidad, PEQ_MAE_criterios_aprobacion, PEQ_MAE_distritos, PEQ_MAE_tiempo_experiencia
from usuarios.models import Persona, InformacionLaboral, InformacionEducativa, Role, Bloqueados, UserAsociacion
from contratistas.models import Contratista
# FORM
from .forms import ConvocatoriaForm, ConvocatoriaPuestoForm,ConvocatoriaAcademicoForm, ConvocatoriaExperienciaForm, ConvocatoriaCursosForm, ConvocatoriaDocumentosForm, RequisitoConvocatoriaForm
from usuarios.forms import PaseIngresoPersonaForm
# SERIALIZERS
from .serializers import ObservacionesSerializer
from maestros.serializers import RangoSerializer, SearchSubEspecialidadSerializer, EspecialidadSerializer
# others
from datetime import datetime
import json
import re
from django.conf import settings
# services
from maestros.services import *
# REST FRAMEWORK
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# tasks
# from .tasks import enviar_email
from io import BytesIO
from maestros.pdfs import PDFConvocatorias, PDFPostulantes
# CRITERISO DE BUSQUEDA
def CriteriosBusqueda(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	# enviar el total
	
	return render(request, 'convocatorias/criterios_de_busqueda.html',{
		'title':'Agregar porcentaje de cumplimiento a los requisitos',
		'convocatoria_puesto': convocatoria_puesto
	})

@api_view(['POST'])
@permission_classes([AllowAny])
def add_porcentaje_cumplimiento(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	# --- Validar max 100%
	if request.method == 'POST':
		data = request.data
		modelo = None
		if data['tipo'] == 'academico':
			modelo = get_object_or_404(PEQ_INT_convocatoria_academico, pk=data['pk'])
		elif data['tipo'] == 'experiencia':
			modelo = get_object_or_404(PEQ_INT_convocatoria_experiencia, pk=data['pk'])
		elif data['tipo'] == 'curso':
			modelo = get_object_or_404(PEQ_INT_convocatoria_cursos, pk=data['pk'])
		if modelo:
			modelo.porcentaje_cumplimiento = data['porcentaje']
			modelo.save()
			return JsonResponse({'message':'Registro agregado correctamente.','class':'success'}, status=200)
	return JsonResponse({'message':'Ocurrió un error inesperado','class':'danger'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_porcentaje_cumplimiento_criterio(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	# --- Validar max en cada modelo
	if request.method == 'POST':
		data = request.data
		modelo = None
		if data['tipo'] == 'academico':
			modelo = get_object_or_404(PEQ_INT_convocatoria_academico, pk=data['pk'])
		elif data['tipo'] == 'experiencia':
			modelo = get_object_or_404(PEQ_INT_convocatoria_experiencia, pk=data['pk'])
		elif data['tipo'] == 'curso':
			modelo = get_object_or_404(PEQ_INT_convocatoria_cursos, pk=data['pk'])
		if modelo:
			modelo.porcentaje_cumplimiento = data['porcentaje']
			modelo.save()
			return JsonResponse({'message':'Registro agregado correctamente.','class':'success'}, status=200)
	return JsonResponse({'message':'Ocurrió un error inesperado','class':'danger'}, status=400)

def exist_criterio_plantilla(plantilla, criterio, tipo):
	total = 0
	if tipo == 'academico':
		total = plantilla.academico.all().filter(carrera=criterio.carrera, grado=criterio.grado, estado_grado=criterio.estado_grado).count()
	elif tipo == 'experiencia':
		total = plantilla.experiencia.all().filter(especialidad=criterio.especialidad, rango=criterio.rango, familia_puesto=criterio.familia_puesto).count()
	elif tipo == 'curso':
		total = plantilla.experiencia.all().filter(tipo=criterio.tipo, descripcion=criterio.descripcion).count()
	return total > 0

def insert_criterio_to_plantilla(plantilla, data):
	if data['tipo'] == 'academico':
		modelo = get_object_or_404(PEQ_INT_convocatoria_academico, pk=data['pk'])
		plantilla.academico.add(modelo) if not exist_criterio_plantilla(plantilla, modelo, 'academico') else ''
	elif data['tipo'] == 'experiencia':
		modelo = get_object_or_404(PEQ_INT_convocatoria_experiencia, pk=data['pk'])
		plantilla.experiencia.add(modelo) if not exist_criterio_plantilla(plantilla, modelo, 'experiencia') else ''
	elif data['tipo'] == 'curso':
		modelo = get_object_or_404(PEQ_INT_convocatoria_cursos, pk=data['pk'])
		plantilla.cursos.add(modelo) if not exist_criterio_plantilla(plantilla, modelo, 'cursos') else ''

@api_view(['POST'])
@permission_classes([AllowAny])
def add_criterio_to_plantilla(request, uuid):
	plantilla = get_object_or_404(PlantillaCriteriosAvanzados, uuid=uuid)
	if request.method == 'POST':
		insert_criterio_to_plantilla(plantilla,request.data)
		return JsonResponse({'message':'Registro agregado correctamente.','class':'success'}, status=200)
	return JsonResponse({'message':'Ocurrió un error inesperado','class':'danger'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_plantilla_criterio_avanzado(request):
	if request.method == "POST":
		data = request.data
		plantilla = PlantillaCriteriosAvanzados()
		plantilla.descripcion = data['descripcion']
		try:
			plantilla.validate_unique()
		except ValidationError as err:
			return JsonResponse({'message':'Ya existe una plantilla con la misma descripcion.','class':'red'}, status=400)
		plantilla.save()
		for item in data['criterios']:
			insert_criterio_to_plantilla(plantilla,item)
		return JsonResponse({'message':'registro agregado correctamente.','class':'success','uuid':str(plantilla.uuid)}, status=200)

def create_criterio_by_exist(criterios, convocatoria_puesto):
	for criterio in criterios:
		criterio.uuid = None
		criterio.convocatoria_puesto = convocatoria_puesto
		criterio.save()

@login_required
@permission_required(('convocatorias.add_criterio_academico','convocatorias.add_criterio_laboral','convocatorias.add_criterio_curso'), raise_exception=True)
def criterios_avanzados(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	total_criterios = convocatoria_puesto.peq_int_convocatoria_academico_set.all().filter(tipo_registro=CRITERIO).count() + convocatoria_puesto.peq_int_convocatoria_experiencia_set.all().filter(tipo_registro=CRITERIO).count() + convocatoria_puesto.peq_int_convocatoria_cursos_set.all().filter(tipo_registro=CRITERIO).count()
	form_academico = ConvocatoriaAcademicoForm()
	form_experiencia = ConvocatoriaExperienciaForm()
	form_curso = ConvocatoriaCursosForm()
	form_documento = ConvocatoriaDocumentosForm()
	plantilla = None
	plantillas = PlantillaCriteriosAvanzados.objects.all()
	message = {}
	if request.method == 'POST':
		tipo_formulario = request.POST.get('tipo_formulario')
		if tipo_formulario == 'select_plantilla':
			plantilla = get_object_or_404(PlantillaCriteriosAvanzados, uuid=request.POST.get('plantilla'))
		elif tipo_formulario == 'usar_plantilla':
			if total_criterios == 0:
				criterios_plantilla = get_object_or_404(PlantillaCriteriosAvanzados, uuid=request.POST.get('plantilla'))
				create_criterio_by_exist(criterios_plantilla.academico.all(), convocatoria_puesto)
				create_criterio_by_exist(criterios_plantilla.experiencia.all(), convocatoria_puesto)
				create_criterio_by_exist(criterios_plantilla.cursos.all(), convocatoria_puesto)
				total_criterios = convocatoria_puesto.peq_int_convocatoria_academico_set.all().filter(tipo_registro=CRITERIO).count() + convocatoria_puesto.peq_int_convocatoria_experiencia_set.all().filter(tipo_registro=CRITERIO).count() + convocatoria_puesto.peq_int_convocatoria_cursos_set.all().filter(tipo_registro=CRITERIO).count()
			else:
				message = {'value':'No se puede usar la plantilla porque ya existen criterios.', 'class':'warning'}
	return render(request, 'convocatorias/criterios_de_busqueda_avanzados.html', {
		'title':'Agregar criterios de busqueda',
		'total_criterios': total_criterios,
		'message': message,
		'plantilla': plantilla,
		'plantillas': plantillas,
		'convocatoria_puesto': convocatoria_puesto,
		'form_academico':form_academico, 
		'form_experiencia':form_experiencia,
		'form_curso':form_curso,
		'form_documento':form_documento
	})

def add_extras_criterio_avanzado(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	if request.method == "POST":
		form = None
		if request.POST.get('tipo_modelo') == 'academico':
			form = ConvocatoriaAcademicoForm(request.POST)
		elif request.POST.get('tipo_modelo') == 'experiencia':
			form = ConvocatoriaExperienciaForm(request.POST)
		elif request.POST.get('tipo_modelo') == 'cursos':
			form = ConvocatoriaCursosForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.porcentaje_cumplimiento = request.POST.get('porcentaje_cumplimiento_criterio')
			obj.convocatoria_puesto = convocatoria_puesto
			obj.tipo_registro = CRITERIO
			try:
				obj.validate_unique()
			except ValidationError as err:
				return JsonResponse({'message':'Registro duplicado.','class':'red'}, status=400)
			obj.save()
			title = ''
			if request.POST.get('tipo_modelo') == 'academico':
				title = (obj.grado.descripcion if obj.grado else '' )+' '+(obj.estado_grado.descripcion if obj.estado_grado else '')+' '+(obj.carrera.descripcion if obj.carrera else '')
			elif request.POST.get('tipo_modelo') == 'experiencia':
				title = (obj.rango.descripcion if obj.rango else '' )+' '+(obj.especialidad.descripcion if obj.especialidad else '')+' '+(obj.familia_puesto.descripcion if obj.familia_puesto else '')
			elif request.POST.get('tipo_modelo') == 'cursos':
				title = (obj.tipo.descripcion if obj.tipo else '' )+' '+obj.descripcion
			return JsonResponse({'message':'Registro agregado correctamente.', 'data': {'title':title,'porcentaje':obj.porcentaje_cumplimiento,'puesto':str(convocatoria_puesto.uuid), 'pk': obj.pk}}, status=200)

def get_title_convocatoria_puesto(convocatoria_puesto):
	return (convocatoria_puesto.rango.descripcion.upper() if convocatoria_puesto.rango else '') +' '+(convocatoria_puesto.sub_especialidad.descripcion.upper() if convocatoria_puesto.sub_especialidad else '') +' '+ (convocatoria_puesto.especialidad.descripcion.upper() if convocatoria_puesto.especialidad else '') +' '+(convocatoria_puesto.familia_puesto.descripcion.upper() if convocatoria_puesto.familia_puesto else '')

# PDFS
def PdfConvocatorias(request, uuid):
	convocatoria = get_object_or_404(Convocatoria, uuid=uuid)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="'+convocatoria.nombre.upper()+' '+convocatoria.codigo.upper()+'.pdf"'
	buffer = BytesIO()
	report = PDFConvocatorias(buffer, 'A4', uuid)
	pdf = report.print_convocatoria()         
	response.write(pdf)
	return response

def PdfPreseleccionados(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	response = HttpResponse(content_type='application/pdf')
	title_pdf = get_title_convocatoria_puesto(convocatoria_puesto) 
	preseleccionados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='preseleccion')
	title = '('+str(preseleccionados.count())+') PRESELECCIONADOS '+title_pdf
	response['Content-Disposition'] = 'attachment; filename="'+title+'.pdf"'
	buffer = BytesIO()
	report = PDFPostulantes(buffer, 'A4', preseleccionados, title)
	pdf = report.print_informacion_general()         
	response.write(pdf)
	return response

def PdfSeleccionados(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	response = HttpResponse(content_type='application/pdf')
	title_pdf = get_title_convocatoria_puesto(convocatoria_puesto) 
	seleccionados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='aprobado')
	title = '('+str(seleccionados.count())+') SELECCIONADOS '+title_pdf
	response['Content-Disposition'] = 'attachment; filename="'+title+'.pdf"'
	buffer = BytesIO()
	report = PDFPostulantes(buffer, 'A4', seleccionados, title)
	pdf = report.print_informacion_general()         
	response.write(pdf)
	return response

def PdfPasesDeIngreso(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	response = HttpResponse(content_type='application/pdf')
	title_pdf = get_title_convocatoria_puesto(convocatoria_puesto)
	pases_de_ingreso = PasesIngreso.objects.filter(convocatoria_puesto=convocatoria_puesto)
	title = '('+str(pases_de_ingreso.count())+') PASES DE INGRESO '+title_pdf
	response['Content-Disposition'] = 'attachment; filename="'+title+'.pdf"'
	buffer = BytesIO()
	report = PDFPostulantes(buffer, 'A4', pases_de_ingreso, title)
	pdf = report.print_pase_de_ingreso()         
	response.write(pdf)
	return response

def PdfVerificacionDomiciliaria(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	response = HttpResponse(content_type='application/pdf')
	title_pdf = (convocatoria_puesto.rango.descripcion.upper() if convocatoria_puesto.rango else '') +' '+(convocatoria_puesto.sub_especialidad.descripcion.upper() if convocatoria_puesto.sub_especialidad else '') +' '+ (convocatoria_puesto.especialidad.descripcion.upper() if convocatoria_puesto.especialidad else '') +' '+(convocatoria_puesto.familia_puesto.descripcion.upper() if convocatoria_puesto.familia_puesto else '') 
	preseleccionados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='preseleccion')
	if request.GET.get('distrito'):
		preseleccionados = preseleccionados.filter(Q(postulacion__persona__distrito_nacimiento__uuid=request.GET.get('distrito')) | Q(postulacion__persona__distrito_residencia__uuid=request.GET.get('distrito')))
	title = '('+str(preseleccionados.count())+') VERIFICACIÓN DOMICILIARIA '+title_pdf
	response['Content-Disposition'] = 'attachment; filename="'+title+'.pdf"'
	buffer = BytesIO()
	report = PDFPostulantes(buffer, 'A4', preseleccionados, title)
	pdf = report.print_informacion_general()         
	response.write(pdf)
	return response

#PASE DE INGRESO
@login_required()
@permission_required('usuarios.add_persona', raise_exception=True)
def pase_de_ingreso(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	criterios_aprobacion = PEQ_MAE_criterios_aprobacion.objects.all().order_by('orden')
	pases_convocatoria_puesto = PasesIngreso.objects.filter(convocatoria_puesto=convocatoria_puesto)
	registros = [{'criterio':criterio, 'total' : pases_convocatoria_puesto.filter(criterio_aprobacion=criterio).count()} for criterio in criterios_aprobacion]
	return render(request, 'personas/pase_de_ingreso.html', { 
		'title': 'Escoger criterio de aprobación', 
		'registros': registros,
		'convocatoria_puesto' : convocatoria_puesto 
	})

# ADD PERSONA TO PASE DE INGRESO
@login_required()
@permission_required('usuarios.add_persona', raise_exception=True)
def pase_de_ingreso_add_persona(request, uuid, uuid_criterio):
	form = PaseIngresoPersonaForm()
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid) 
	criterio_aprobacion = get_object_or_404(PEQ_MAE_criterios_aprobacion, uuid=uuid_criterio)
	message = {'error': False}
	bloqueado = {'value': False}
	add_persona = False
	pases = PasesIngreso.objects.filter(convocatoria_puesto=convocatoria_puesto)
	pases_personas_uuid = [ obj.persona.uuid for obj in pases]
	registros = [ {'pase':obj.uuid,'criterio':obj.criterio_aprobacion, 'persona': obj.persona} for obj in pases]
	if criterio_aprobacion.alias == 'A1':
		contratados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='contratado').count()
		vacantes_libres = convocatoria_puesto.cantidad_vacantes - contratados - pases.count()
		bloqueado = { 'value': True, 'message': 'Pase bloqueado, vacantes ocupadas.', 'class': 'danger'} if vacantes_libres < 1 else { 'value': False, 'message': 'Quedan {0} vacantes'.format(vacantes_libres), 'class':'warning'}
	numero_documento = request.GET.get('numero_documento')
	if numero_documento:
		registros = [{'persona': obj} for obj in Persona.objects.filter(numero_documento__icontains=numero_documento).exclude(uuid__in=pases_personas_uuid)]
	if request.method == "POST":
		pase_ingreso = PasesIngreso()
		pase_ingreso.convocatoria_puesto = convocatoria_puesto
		pase_ingreso.criterio_aprobacion = criterio_aprobacion
		if request.POST.get('tipo') == 'new_persona':
			form = PaseIngresoPersonaForm(request.POST)
			if form.is_valid():
				password = User.objects.make_random_password()
				user, created = User.objects.update_or_create(username=form.cleaned_data['numero_documento'], email=form.cleaned_data['email'], password= password)
				user.set_password(password)
				user.save()
				persona = form.save(commit=False)
				persona.user = user
				persona.verificado = True
				persona.save()
				Role.objects.create(rol=Role.POSTULANTE, user=user)
				# ENVIAR CORREO
				message_html = u'<h1><strong>Usuario</strong></h1><hr>\n'\
								u'<h3><strong>Username: </strong>{username}</h3>\n'\
								u'<h3><strong>Contraseña: </strong>{password}</h3>\n'\
								u'<p><a href="{url_login}" target="_blank">Clic aquí para ingresar {url_login}</a></p>'.format(username=user.username, password=password, url_login=settings.URL_SITE+'/login/postulantes')
				enviar_email(persona.email,'Creacion de usuario',message_html)
			else:
				message['error'] = True
				add_persona = True
		else:
			persona = get_object_or_404(Persona, uuid=request.POST.get('persona'))		
		if not message['error']:
			pase_ingreso.persona = persona
			pase_ingreso.save()
			return redirect('pase-de-ingreso-add-persona', uuid=convocatoria_puesto.uuid, uuid_criterio=criterio_aprobacion.uuid) if criterio_aprobacion.alias == 'A1' else redirect('pase-de-ingreso-add-files', uuid=pase_ingreso.uuid)

	return render(request, 'personas/pase_de_ingreso_add_persona.html', { 
		'title': 'Agregar persona', 
		'back_url': '/convocatorias/puestos/'+str(convocatoria_puesto.uuid)+'/pases_ingreso/',
		'form': form, 
		'add_persona': add_persona,
		'numero_documento': numero_documento,
		'registros': registros,
		'bloqueado': bloqueado,
		'criterio_aprobacion': criterio_aprobacion 
	})

@login_required()
@permission_required('usuarios.add_pasesingreso', raise_exception=True)
def pase_de_ingreso_add_files(request, uuid):
	pase_de_ingreso = get_object_or_404(PasesIngreso, uuid=uuid)
	message = {'error': False}
	if request.method == 'POST':
		if pase_de_ingreso.criterio_aprobacion.alias == 'A2':
			if ('boleta_pago' not in request.FILES and 'pdt' not in request.FILES and 'registro_laboral' not in request.FILES):
				message = {'value':'Ingresar Boleta de Pago, PDT ó Registro de Información Laboral.', 'class':'danger', 'error': True}
			else:
				pase_de_ingreso.boleta_pago = request.FILES.get('boleta_pago') or None
				pase_de_ingreso.pdt = request.FILES.get('pdt') or None
				pase_de_ingreso.registro_laboral = request.FILES.get('registro_laboral') or None
		elif pase_de_ingreso.criterio_aprobacion.alias == 'A3':
			if ('carnet_extranjeria' not in request.FILES and 'tramite_migratorio' not in request.FILES):
				message = {'value':'Ingresar copia simple del carnet de extranjería o del trámite de cambio de calidad migratoria.', 'class':'danger', 'error': True}
			else:
				pase_de_ingreso.carnet_extranjeria = request.FILES.get('carnet_extranjeria') or None
				pase_de_ingreso.tramite_calidad_migratoria = request.FILES.get('tramite_migratorio') or None
		elif pase_de_ingreso.criterio_aprobacion.alias == 'A4': 
			if 'orden_servicios' not in request.FILES:
				message = {'value':'Ingresar copia simple de la orden de servicios.', 'class':'danger', 'error': True}
			else:
				pase_de_ingreso.orden_servicio = request.FILES.get('orden_servicios') or None
		pase_de_ingreso.save()
		if not message['error']:
			message = {'value':'Documento(s) agregado con exito.', 'class':'success'}

	return render(request, 'personas/pase_de_ingreso_add_documentos.html', { 
		'title': 'Agregar documentos',
		'message': message,
		'pase_de_ingreso': pase_de_ingreso
	})

@login_required()
@permission_required('convocatorias.read_convocatoria', raise_exception=True)
def index_convocatoria(request):
	contratistas = ''
	if hasattr(request.user, 'role'):
		if request.user.role.rol == Role.SUB_CONTRATISTA or request.user.role.rol == Role.CONTRATISTA:
			asociaciones = UserAsociacion.objects.filter(user=request.user)
			messages.error(request, 'El usuario no esta asociado a ninguna Subcontratista ó Contratista.') if not asociaciones else ''
			contratistas__uuid = [obj.sub_contratista.contratista.uuid for obj in asociaciones]
			contratistas = Contratista.objects.filter(uuid__in=contratistas__uuid)
	else:
		messages.error(request, 'El usuario no tiene ningun rol asignado.') if not request.user.is_superuser else ''
	if request.user.is_superuser:
		contratistas = Contratista.objects.all()
	convocatorias = Convocatoria.objects.filter(contratista__in=contratistas, activo=True)
	if request.GET.get('name_codigo'):
		name_codigo = request.GET.get('name_codigo')
		convocatorias = convocatorias.filter(Q(nombre__icontains=name_codigo) | Q(codigo__icontains=name_codigo))
	data = []
	if hasattr(request.user, 'role'):
		if request.user.role.rol == Role.SUB_CONTRATISTA:
			convocatorias = convocatorias.filter(user=request.user)
	for convocatoria in convocatorias.order_by('-fecha_creacion')[:50]:
		estados = PEQ_INT_estado_convocatoria.objects.filter(convocatoria=convocatoria).order_by('estado__orden')
		estado_actual = estados.filter(activo=True).order_by('-fecha_creacion').first()
		data.append({'convocatoria':convocatoria,'estado_actual':estado_actual, 'estados': estados })
	return render(request, 'convocatorias/index_convocatoria.html', {'data': data})

@login_required()
@permission_required(('convocatorias.read_preseleccionados','convocatorias.read_seleccionados','convocatorias.read_aprobados'), raise_exception=True)
def convocatoria_puesto_personas(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	postulantes = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='postulando')
	preseleccionados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='preseleccion')
	aprobados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='aprobado')
	contratados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='contratado')
	return render(request, 'convocatorias/convocatoria_puesto_personas.html', { 
		'title': 'Personas en el puesto', 
		'postulantes': postulantes,
		'preseleccionados': preseleccionados,
		'aprobados': aprobados,
		'contratados': contratados,
		'convocatoria_puesto': convocatoria_puesto
	})

def autorizar_convocatoria(request, uuid):
	# Validar si tiene permiso
	try:
		convocatoria = get_object_or_404(Convocatoria, uuid=uuid)
		if convocatoria.user:
			# ENVIAR CORREO
			message_html = u'<h1><strong>La Convocatoria {0} ha sido autorizada.</strong></h1>'.format(convocatoria.nombre+' '+convocatoria.codigo)
			enviar_email(convocatoria.user.email,'Autorización de convocatoria',message_html) if convocatoria.user.email else ''
		estado_convocatoria = PEQ_INT_estado_convocatoria()
		estado_convocatoria.estado = PEQ_MAE_estados_convocatoria.objects.filter(descripcion='autorizada').first()
		estado_convocatoria.convocatoria = convocatoria
		estado_convocatoria.save()
		PEQ_INT_estado_convocatoria.objects.filter(convocatoria=convocatoria).exclude(uuid=estado_convocatoria.uuid).update(activo=False)
		return JsonResponse({'message':'Registro agregado correctamente.', 'class':'text-green'}, status=200)
	except Exception, e:
		return JsonResponse({'message': str(e),'class':'text-red'}, status=400)

@login_required()
@permission_required('convocatorias.iniciar_convocatoria', raise_exception=True)
def iniciar_convocatoria(request, uuid):
	# Validar si tiene permiso
	try:
		convocatoria = get_object_or_404(Convocatoria, uuid=uuid)
		estado_convocatoria = PEQ_INT_estado_convocatoria()
		estado_convocatoria.estado = PEQ_MAE_estados_convocatoria.objects.filter(descripcion='en proceso').first()
		estado_convocatoria.fecha_inicio = request.POST.get('fecha_inicio')
		estado_convocatoria.fecha_fin = request.POST.get('fecha_fin')
		estado_convocatoria.fecha_comite = request.POST.get('fecha_comite')
		estado_convocatoria.convocatoria = convocatoria
		estado_convocatoria.save()
		PEQ_INT_estado_convocatoria.objects.filter(convocatoria=convocatoria).exclude(uuid=estado_convocatoria.uuid).update(activo=False)
		return JsonResponse({'message':'Registro agregado correctamente.', 'class':'green'}, status=200)
	except Exception, e:
		return JsonResponse({'message': str(e),'class':'text-red'}, status=400)		

@api_view(['GET'])
@permission_classes([AllowAny])
def get_codigo_convocatoria(request, uuid):
	contratista = get_object_or_404(Contratista, uuid=uuid)
	mayor = Convocatoria.objects.filter(contratista=contratista).aggregate(Max('numero'))
	numero = mayor['numero__max'] + 1 if mayor['numero__max'] else 1
	numero_str = '0'+str(numero) if numero < 10 else str(numero)
	codigo = contratista.alias+' '+numero_str+' - '+str(datetime.now().year) if contratista else ''
	return Response({'codigo': codigo}, status=200)

@login_required()
@permission_required('convocatorias.add_convocatoria', raise_exception=True)
def add_convocatoria(request):
	contratistas = ''
	if hasattr(request.user, 'role'):
		if request.user.role.rol == Role.SUB_CONTRATISTA or request.user.role.rol == Role.CONTRATISTA:
			asociaciones = UserAsociacion.objects.filter(user=request.user)
			messages.error(request, 'El usuario no esta asociado a ninguna sub_contratista ó contratista.') if not asociaciones else ''
			contratistas__uuid = [ obj.sub_contratista.contratista.uuid for obj in asociaciones]
			contratistas = Contratista.objects.filter(uuid__in=contratistas__uuid)
	else:
		messages.error(request, 'El usuario no tiene ningun rol asignado.') if not request.user.is_superuser else ''
	if request.user.is_superuser:
		contratistas = Contratista.objects.all()
	form = ConvocatoriaForm()
	choices_contratistas = [('','seleccionar')]
	[choices_contratistas.append((contratista.uuid, contratista.nombre)) for contratista in contratistas]
	form.fields['contratista'].choices = choices_contratistas
	if request.method == "POST":
		form = ConvocatoriaForm(request.POST)
		if form.is_valid():
			mayor = Convocatoria.objects.filter(contratista__uuid=request.POST.get('contratista')).aggregate(Max('numero'))
			numero = mayor['numero__max'] + 1 if mayor['numero__max'] else 1
			new_convocatoria = form.save(commit=False)
			new_convocatoria.user = request.user
			new_convocatoria.numero = numero
			new_convocatoria.save()
			estado_convocatoria = PEQ_INT_estado_convocatoria()
			estado_convocatoria.estado = PEQ_MAE_estados_convocatoria.objects.filter(descripcion='registrado').first()
			estado_convocatoria.convocatoria = new_convocatoria
			estado_convocatoria.save()
			return redirect('add-convocatoria-puestos', uuid=new_convocatoria.uuid)
	return render(request, 'convocatorias/add_convocatoria.html', {
		'title': 'Agregar convocatoria',
		'form': form,
		'contratistas': contratistas
	})

@login_required()
@permission_required('convocatorias.change_convocatoria', raise_exception=True)
def edit_convocatoria(request, uuid):
	convocatoria = get_object_or_404(Convocatoria, uuid=uuid)
	contratistas = ''
	form = None
	if convocatoria_is_authorized(convocatoria):
		messages.error(request, 'No se puede editar porque ya está autorizada.')
	else:
		if hasattr(request.user, 'role'):
			if request.user.role.rol == Role.SUB_CONTRATISTA or request.user.role.rol == Role.CONTRATISTA:
				asociaciones = UserAsociacion.objects.filter(user=request.user)
				messages.error(request, 'El usuario no esta asociado a ninguna sub_contratista ó contratista.') if not asociaciones else ''
				contratistas__uuid = [ obj.sub_contratista.contratista.uuid for obj in asociaciones]
				contratistas = Contratista.objects.filter(uuid__in=contratistas__uuid)
		else:
			if not request.user.is_superuser:
				messages.error(request, 'El usuario no tiene ningun rol asignado.')
		if request.user.is_superuser:
			contratistas = Contratista.objects.all()
		form = ConvocatoriaForm(instance=convocatoria)
		choices_contratistas = [('','seleccionar')]
		[choices_contratistas.append((contratista.uuid, contratista.nombre)) for contratista in contratistas]
		form.fields['contratista'].choices = choices_contratistas
		if request.method == "POST":
			form = ConvocatoriaForm(request.POST, instance=convocatoria)
			if form.is_valid():
				convocatoria = form.save(commit=True)
				return redirect('add-convocatoria-puestos', uuid=convocatoria.uuid)
	return render(request, 'convocatorias/add_convocatoria.html', { 
		'title': 'Editar convocatoria', 
		'convocatoria': convocatoria,
		'contratistas': contratistas,
		'form': form
	})

@login_required()
@permission_required('convocatorias.delete_convocatoria', raise_exception=True)
def delete_convocatoria(request, uuid):
	convocatoria = get_object_or_404(Convocatoria, uuid=uuid)
	if convocatoria_is_authorized(convocatoria):
		messages.error(request, 'No se puede eliminar porque ya esta autorizada.')
	else:
		if request.method == 'POST':
			convocatoria.activo = False
			convocatoria.save()
			messages.success(request, 'Convocatoria eliminada con exito.')
			return redirect('index-convocatoria')
	return render(request, 'convocatorias/delete_convocatoria.html', { 
		'title': 'Eliminar convocatoria', 
		'convocatoria': convocatoria
	})

@login_required()
@permission_required('convocatorias.add_convocatoriapuesto', raise_exception=True)
def add_convocatoria_puestos(request, uuid):
	convocatoria = get_object_or_404(Convocatoria, uuid=uuid)
	convocatoria_puestos = ConvocatoriaPuesto.objects.filter(convocatoria__uuid=uuid).order_by('-fecha_creacion')
	estado_actual = PEQ_INT_estado_convocatoria.objects.filter(convocatoria__uuid=uuid, activo=True).order_by('-fecha_creacion').first()
	form = ConvocatoriaPuestoForm()
	if request.method == 'POST':
		form = ConvocatoriaPuestoForm(request.POST)
		if form.is_valid():
			convocatoria_puesto = form.save(commit=False)
			convocatoria_puesto.convocatoria = convocatoria
			if Duplicate(ConvocatoriaPuesto, {'convocatoria':convocatoria, 'especialidad': form.cleaned_data['especialidad'], 'familia_puesto': form.cleaned_data['familia_puesto'], 'sub_especialidad': form.cleaned_data['sub_especialidad'], 'rango': form.cleaned_data['rango']}):
				messages.error(request, 'Registro duplicado.')
			else:
				convocatoria_puesto.save()
				form = ConvocatoriaPuestoForm()
				messages.success(request, 'Registro agregado con éxito.')
	return render(request, 'convocatorias/add_convocatoria_puestos.html', {
		'title': 'Puestos convocatoria', 
		'convocatoria_puestos': convocatoria_puestos,
		'convocatoria': convocatoria,
		'estado_actual': estado_actual,
		'form': form
	})

@login_required()
@permission_required('convocatorias.change_convocatoriapuesto', raise_exception=True)
def edit_convocatoria_puesto(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	convocatoria = convocatoria_puesto.convocatoria
	convocatoria_puestos = ConvocatoriaPuesto.objects.filter(convocatoria=convocatoria).order_by('-fecha_creacion')
	estados_postulacion = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto__convocatoria=convocatoria).exclude(estado__descripcion='postulando')
	form = None
	if puesto_convocatoria_has_persons(convocatoria_puesto):
		messages.error(request, 'No se puede editar porque existe personal involucrado.')
	else:
		form = ConvocatoriaPuestoForm(instance=convocatoria_puesto)
		if request.method == 'POST':
			form = ConvocatoriaPuestoForm(request.POST, instance=convocatoria_puesto)
			if form.is_valid():
				convocatoria_puesto = form.save(commit=False)
				if Duplicate(ConvocatoriaPuesto, {'convocatoria':convocatoria, 'especialidad': form.cleaned_data['especialidad'], 'familia_puesto': form.cleaned_data['familia_puesto'], 'sub_especialidad': form.cleaned_data['sub_especialidad'], 'rango': form.cleaned_data['rango']}):
					messages.error(request, 'Registro duplicado.')
				else:
					convocatoria_puesto.save()
					form = ConvocatoriaPuestoForm()
					messages.success(request, 'Registro modificado con éxito.')
					return redirect('add-convocatoria-puestos', uuid=convocatoria.uuid)
	return render(request, 'convocatorias/add_convocatoria_puestos.html', {
		'title': 'Puestos convocatoria', 
		'convocatoria_puestos': convocatoria_puestos,
		'convocatoria': convocatoria,
		'form': form
	})

@login_required()
@permission_required('convocatorias.delete_convocatoriapuesto', raise_exception=True)
def delete_convocatoria_puesto(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	if puesto_convocatoria_has_persons(convocatoria_puesto):
		messages.error(request, 'No se puede eliminar porque existe personal involucrado.')
	else:
		if request.method == 'POST':
			convocatoria_puesto.delete()
			return redirect('add-convocatoria-puestos', uuid=convocatoria_puesto.convocatoria.uuid)
	return render(request, 'convocatorias/delete_convocatoria_puesto.html', { 
		'title': 'Eliminar puesto convocatoria', 
		'convocatoria_puesto': convocatoria_puesto
	})

@api_view(['POST'])
@permission_classes([AllowAny])
def add_pre_seleccion_tags(request):
	data = request.data 
	tags = []
	for obj in data['tags']:
		tag = PEQ_MAE_tags()
		tag.descripcion = obj
		tag.save()
		tags.append(tag)

	for dato in data['data']:
		convocatoria_tags = ConvocatoriaTags()
		convocatoria_tags.convocatoria = get_object_or_404(Convocatoria, uuid=dato['convocatoria'])
		convocatoria_tags.persona = get_object_or_404(Persona, uuid=dato['persona'])
		convocatoria_tags.save()
		convocatoria_tags.tags.add(*tags)
	return Response({'message':'Tags agregados con exito.'}, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def postular_convocatoria_puesto(request):
	if request.user.has_perm('convocatorias.add_postulacionconvocatoria'):
		data = request.data
		convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=data['convocatoria_puesto'])
		if not convocatoria_is_authorized(convocatoria_puesto.convocatoria):
			return Response({'message':u'La convocatoria no está autorizada.'}, status=403)
		if not convocatoria_is_vigente(convocatoria_puesto.convocatoria):
			return Response({'message':u'La convocatoria no está vigente.'}, status=403)
		# make insert code
		return Response({'message': 'Postulación existosa.', 'data':request.data, 'user': unicode(request.user), 'auth': unicode(request.auth)})
	else:
		return Response({'message': 'No tiene permiso para agregar postulante.'}, status=403)

def postulacion_convocatoria(request, uuid, uuid_persona):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	estado_convocatoria = PEQ_INT_estado_convocatoria.objects.filter(convocatoria=convocatoria_puesto.convocatoria, estado__descripcion='en proceso')
	if estado_convocatoria:
		now_str = datetime.now().strftime('%Y-%m-%d')
		vigente = estado_convocatoria.filter(fecha_inicio__lte=now_str, fecha_fin__gte=now_str).first()
		if not vigente:
			return JsonResponse({'message':'El puesto no esta vigente', 'class':'text-red'}, status=400)
	else:
		return JsonResponse({'message':'La convocatoria no esta en proceso.', 'class':'text-red'}, status=400)
	try:
		postulacion_convocatoria = PostulacionConvocatoria()
		postulacion_convocatoria.convocatoria_puesto = convocatoria_puesto
		postulacion_convocatoria.persona = get_object_or_404(Persona, uuid=uuid_persona)
		postulacion_convocatoria.tipo_ingreso = 'postulante'
		postulacion_convocatoria.save()
		estado_postulacion = PEQ_INT_estado_postulacion()
		estado_postulacion.postulacion = postulacion_convocatoria
		estado_postulacion.estado = PEQ_MAE_estados_postulacion.objects.get(descripcion='postulando')
		estado_postulacion.fecha = datetime.now()
		estado_postulacion.save()
		return JsonResponse({'message':'Registro agregado correctamente.', 'class':'text-green'})
	except Exception, e:
		return JsonResponse({'message': str(e),'class':'text-red'})

@api_view(['GET'])
@permission_classes([AllowAny])
def search_name_puesto(request):
	text = re.sub(' +',' ',request.GET.get('text'))
	text_split = text.split(' ')
	rango = PEQ_MAE_rangos.objects.filter(descripcion__icontains=text_split[0]).first()
	especialidades = PEQ_MAE_familia.objects.filter(descripcion__icontains=text_split[1])
	sub_especialidades = PEQ_MAE_sub_especialidad.objects.filter(descripcion__icontains=text_split[1])
	return Response({ 
		'rango': RangoSerializer(rango).data,
		'especialidades': EspecialidadSerializer(especialidades, many=True).data,
		'sub_especialidades': SearchSubEspecialidadSerializer(sub_especialidades, many=True).data
	}, status=200)

@login_required()
@permission_required('convocatorias.add_postulacionconvocatoria', raise_exception=True)
def detail_convocatoria(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	if user_is_owner(request.user, convocatoria_puesto.convocatoria):
		postulantes = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='postulando')
		registrados = []
		if convocatoria_is_authorized(convocatoria_puesto.convocatoria):
			if request.GET.get('numero_documento'):
				numero_documento = request.GET.get('numero_documento')
				postulantes_convocatoria = [obj.postulacion.persona for obj in postulantes]
				personas = Persona.objects.filter(numero_documento__icontains=numero_documento)
				for persona in personas:
					postulado = True if persona in postulantes_convocatoria else False
					registrados.append({'persona':persona, 'postulado': postulado})
		else:
			messages.warning(request, 'La convocatoria no esta autorizada, no puedes agregar personas.')
		return render(request, 'convocatorias/postulacion_convocatoria.html', {
			'convocatoria_puesto': convocatoria_puesto,
			'postulantes': postulantes,
			'registrados': registrados
		})
	else:
		messages.error(request, 'No eres propietario.')
		return render(request, 'convocatorias/postulacion_convocatoria.html')

def get_rango_seleccion(puesto, persona):
	totales = {'academico':0, 'laboral': 0, 'cursos': 0}
	now = datetime.now().date()
	# ACADEMICO
	requisitos_academicos = puesto.peq_int_convocatoria_academico_set.all().filter(tipo_registro=NORMAL)
	persona_academico = persona.informacioneducativa_set.all()
	for requisito_academico in requisitos_academicos:
		for educativo in persona_academico:
			if educativo.carrera == requisito_academico.carrera and (educativo.estado_grado.orden if educativo.estado_grado else 0) >= (requisito_academico.estado_grado.orden if requisito_academico.estado_grado else 0) and (educativo.estado_grado.orden if educativo.estado_grado else 0) >= (requisito_academico.estado_grado.orden if requisito_academico.estado_grado else 0):
				totales['academico'] += requisito_academico.porcentaje_cumplimiento
	#LABORAL
	requisitos_laborales = puesto.peq_int_convocatoria_experiencia_set.all().filter(tipo_registro=NORMAL)
	persona_laboral = persona.informacionlaboral_set.all()	
	for requisito_laboral in requisitos_laborales:
		tiempo_requisito_meses = requisito_laboral.experiencia.tiempo * 12 if requisito_laboral.experiencia.tipo == PEQ_MAE_tiempo_experiencia.ANNIO else requisito_laboral.experiencia.tiempo
		orden_rango = (requisito_laboral.rango.orden if requisito_laboral.rango else 0)
		tiempo_experiencia_meses = 0
		for laboral in persona_laboral.filter(rango__orden__gte=(orden_rango if orden_rango else 0), especialidad=requisito_laboral.especialidad):
			if laboral.hasta_actualidad:
				tiempo_experiencia_meses += (now - laboral.fecha_inicio).days/30 if laboral.fecha_inicio else 0
			else:
				tiempo_experiencia_meses += (laboral.fecha_fin - laboral.fecha_inicio).days/30 if laboral.fecha_inicio and laboral.fecha_fin else 0

		if tiempo_experiencia_meses >= tiempo_requisito_meses:
			totales['laboral'] += requisito_laboral.porcentaje_cumplimiento
		elif tiempo_experiencia_meses > 0:
			totales['laboral'] += (((tiempo_experiencia_meses*100)/tiempo_requisito_meses) * requisito_laboral.porcentaje_cumplimiento)/100
	# -- CRITERIOS AVANZADOS
	if totales['academico'] == 0:
		requisitos_academicos = puesto.peq_int_convocatoria_academico_set.all().filter(tipo_registro=NORMAL)
		persona_academico = persona.informacioneducativa_set.all()
		for requisito_academico in requisitos_academicos:
			for educativo in persona_academico:
				if educativo.carrera == requisito_academico.carrera and (educativo.estado_grado.orden if educativo.estado_grado else 0) >= (requisito_academico.estado_grado.orden if requisito_academico.estado_grado else 0) and (educativo.estado_grado.orden if educativo.estado_grado else 0) >= (requisito_academico.estado_grado.orden if requisito_academico.estado_grado else 0):
					totales['academico'] = requisito_academico.porcentaje_cumplimiento if requisito_academico.porcentaje_cumplimiento > totales['academico'] else totales['academico']
	#LABORAL
	if totales['laboral'] == 0:
		requisitos_laborales = puesto.peq_int_convocatoria_experiencia_set.all().filter(tipo_registro=NORMAL)
		persona_laboral = persona.informacionlaboral_set.all()	
		for requisito_laboral in requisitos_laborales:
			tiempo_requisito_meses = requisito_laboral.experiencia.tiempo * 12 if requisito_laboral.experiencia.tipo == PEQ_MAE_tiempo_experiencia.ANNIO else requisito_laboral.experiencia.tiempo
			
			orden_rango = (requisito_laboral.rango.orden if requisito_laboral.rango else 0)
			orden_especialidad = (requisito_laboral.especialidad.orden if requisito_laboral.especialidad else 0)
			tiempo_experiencia_meses = 0
			for laboral in persona_laboral.filter(rango__orden__gte=(orden_rango if orden_rango else 0), especialidad__orden__gte=(orden_especialidad if orden_especialidad else 0)):
				if laboral.hasta_actualidad:
					tiempo_experiencia_meses += (now - laboral.fecha_inicio).days/30 if laboral.fecha_inicio else 0
				else:
					tiempo_experiencia_meses += (laboral.fecha_fin - laboral.fecha_inicio).days/30 if laboral.fecha_inicio and laboral.fecha_fin else 0
			if tiempo_experiencia_meses >= tiempo_requisito_meses:
				totales['laboral'] += requisito_laboral.porcentaje_cumplimiento if requisito_laboral.porcentaje_cumplimiento > totales['laboral'] else totales['laboral']
			elif tiempo_experiencia_meses > 0:
				totales['laboral'] += (((tiempo_experiencia_meses*100)/tiempo_requisito_meses) * requisito_laboral.porcentaje_cumplimiento)/100

	return totales

from operator import itemgetter

def months_str_description(tiempo_meses):
	annios = tiempo_meses / 12
	meses = tiempo_meses % 12
	return ( u'{0} AÑOS '.format(annios) if annios > 0 else '' ) + (str(meses)+' MESES' if meses > 0 else '')

def get_experiencia_persona_puesto(persona, convocatoria_puesto):
	now = datetime.now().date()
	requisitos_laborales = convocatoria_puesto.peq_int_convocatoria_experiencia_set.all()
	persona_laboral = persona.informacionlaboral_set.all()	
	list_experiencia = []
	for requisito_laboral in requisitos_laborales:
		tiempo_experiencia_meses = 0
		for laboral in persona_laboral.filter(especialidad=requisito_laboral.especialidad):
			if laboral.hasta_actualidad:
				tiempo_experiencia_meses += (now - laboral.fecha_inicio).days/30 if laboral.fecha_inicio else 0
			else:
				tiempo_experiencia_meses += (laboral.fecha_fin - laboral.fecha_inicio).days/30 if laboral.fecha_inicio and laboral.fecha_fin else 0
		list_experiencia.append({'convocatoria_laboral':requisito_laboral,'meses':months_str_description(tiempo_experiencia_meses)})
	return list_experiencia

@login_required()
@permission_required('convocatorias.add_preseleccionados', raise_exception=True)
def pre_seleccion(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	if convocatoria_is_authorized(convocatoria_puesto.convocatoria):
		documentos_bloqueados = [ obj.numero_documento for obj in Bloqueados.objects.all()]
		total_criterios = convocatoria_puesto.peq_int_convocatoria_academico_set.all().filter(tipo_registro=CRITERIO).count() + convocatoria_puesto.peq_int_convocatoria_experiencia_set.all().filter(tipo_registro=CRITERIO).count() + convocatoria_puesto.peq_int_convocatoria_cursos_set.all().filter(tipo_registro=CRITERIO).count()
		preseleccionados_uuid = [obj.postulacion.persona.uuid for obj in PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='preseleccion')]
		postulaciones = PostulacionConvocatoria.objects.filter(convocatoria_puesto=convocatoria_puesto).order_by('rango__orden').exclude(persona__uuid__in=preseleccionados_uuid).exclude(persona__numero_documento__in=documentos_bloqueados)
		# UUID's ARRAY
		postulados_uuid = [obj.persona.uuid for obj in postulaciones]
		especialidades_convocatoria = [ obj.especialidad for obj in PEQ_INT_convocatoria_experiencia.objects.filter(convocatoria_puesto=convocatoria_puesto)]
		especialidades_convocatoria.append(convocatoria_puesto.especialidad)
		personas_aptas_uuid =[obj['persona'] for obj in InformacionLaboral.objects.values('persona').annotate(count=Count('nombre')).filter(especialidad__in=especialidades_convocatoria, rango__orden__gte=convocatoria_puesto.rango.orden).exclude(persona__uuid__in=postulados_uuid).exclude(persona__uuid__in=preseleccionados_uuid)]
		
		# PERSONAS POSTULANTES
		personas_postulaciones = []
		for postulacion in postulaciones:
			lugar = get_lugar(postulacion.persona)
			totales = get_rango_seleccion(convocatoria_puesto, postulacion.persona)
			total = totales['academico']+totales['laboral']+totales['cursos']
			rango = PEQ_MAE_rango_seleccion.objects.filter(minimo__lte=total, maximo__gte=total).first()
			list_experiencia = get_experiencia_persona_puesto(postulacion.persona, convocatoria_puesto)
			experiencia = sorted(list_experiencia, key=itemgetter('meses'), reverse=True) if list_experiencia else []
			personas_postulaciones.append({'persona':postulacion.persona,'rango':rango,'porcentaje':total,'lugar':lugar,'experiencia': experiencia[0] if experiencia else ''})

		new_personas_postulaciones = sorted(personas_postulaciones, key=itemgetter('porcentaje','lugar'), reverse=True)
		# PERSONAS APTAS
		personas_aptas = []
		personas = Persona.objects.filter(uuid__in=personas_aptas_uuid).exclude(numero_documento__in=documentos_bloqueados)
		for persona in personas:
			lugar = get_lugar(persona)
			totales = get_rango_seleccion(convocatoria_puesto, persona)
			total = totales['academico']+totales['laboral']+totales['cursos']
			rango = PEQ_MAE_rango_seleccion.objects.filter(minimo__lte=total, maximo__gte=total).first()
			list_experiencia = get_experiencia_persona_puesto(persona, convocatoria_puesto)
			experiencia = sorted(list_experiencia, key=itemgetter('meses'), reverse=True) if list_experiencia else []
			personas_aptas.append({'persona':persona,'rango':rango,'porcentaje':total,'lugar': lugar,'experiencia':experiencia[0] if experiencia else ''})

		new_personas_aptas = sorted(personas_aptas, key=itemgetter('porcentaje','lugar'), reverse=True)

		return render(request, 'seleccion/pre_seleccion.html', {
			'convocatoria_puesto': convocatoria_puesto,
			'personas_postulaciones': new_personas_postulaciones,
			'personas_aptas': new_personas_aptas
		})
	else:
		messages.error(request, 'La convocatoria no esta autorizada.')
		return render(request, 'seleccion/pre_seleccion.html', {'convocatoria_puesto':convocatoria_puesto})

@login_required()
@permission_required('convocatorias.add_preseleccionados', raise_exception=True)
def pre_seleccion_manual(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	return render(request, 'seleccion/pre_seleccion_manual.html', { 'convocatoria_puesto': convocatoria_puesto })

@login_required()
@permission_required('convocatorias.read_verificaciondomiciliaria', raise_exception=True)
def verificacion(request, uuid):
	convocatoria_puesto = ConvocatoriaPuesto.objects.get(uuid=uuid)
	preseleccionados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='preseleccion')
	distritos_nacimiento__uid = [item['postulacion__persona__distrito_nacimiento__uuid'] for item in preseleccionados.values('postulacion__persona__distrito_nacimiento__uuid').annotate(Count('pk')).exclude(postulacion__persona__distrito_nacimiento__isnull=True)]
	distritos_residencia__uid = [item['postulacion__persona__distrito_residencia__uuid'] for item in preseleccionados.values('postulacion__persona__distrito_residencia__uuid').annotate(Count('pk')).exclude(postulacion__persona__distrito_residencia__isnull=True)]
	distritos__uid = list(set(distritos_nacimiento__uid) | set(distritos_residencia__uid))
	distritos = PEQ_MAE_distritos.objects.filter(uuid__in=distritos__uid)
	distrito_select = {}
	if request.GET.get('distrito'):
		distrito_select = get_object_or_404(PEQ_MAE_distritos, uuid=request.GET.get('distrito'))
		preseleccionados = preseleccionados.filter(postulacion__persona__distrito_nacimiento=distrito_select)
	personas = []
	for preseleccion in preseleccionados:
		personas.append({'persona':preseleccion.postulacion.persona,'pk':preseleccion.pk,'verificado': preseleccion.verificado,'visitado': preseleccion.visitado,'experiencia': InformacionLaboral.objects.filter(persona=preseleccion.postulacion.persona, especialidad=convocatoria_puesto.especialidad).order_by('-fecha_inicio').first()})
	return render(request, 'seleccion/verificacion.html', { 
		'convocatoria_puesto': convocatoria_puesto,
		'title': 'verificación domiciliaria',
		'distritos': distritos,
		'distrito_select': distrito_select,
		'personas': personas
	})

@login_required()
@permission_required('convocatorias.read_contactabilidad', raise_exception=True)
def contactabilidad(request, uuid):
	convocatoria_puesto = ConvocatoriaPuesto.objects.get(uuid=uuid)
	preseleccionados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='preseleccion')
	personas = []
	for preseleccion in preseleccionados:
		personas.append({'persona':preseleccion.postulacion.persona,'pk':preseleccion.pk,'confirmado': preseleccion.quiero_participar,'llamado': preseleccion.llamado,'experiencia': InformacionLaboral.objects.filter(persona=preseleccion.postulacion.persona, especialidad=convocatoria_puesto.especialidad).order_by('-fecha_inicio').first()})
	return render(request, 'seleccion/contactabilidad.html', { 
		'convocatoria_puesto': convocatoria_puesto,
		'personas': personas
	})

@login_required()
@permission_required('convocatorias.add_aprobados', raise_exception=True)
def aprobados(request, uuid):
	convocatoria_puesto = ConvocatoriaPuesto.objects.get(uuid=uuid)
	contratados_uuid = [obj.postulacion.persona.uuid for obj in PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='contratado')]
	aprobados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='aprobado').exclude(postulacion__persona__uuid__in=contratados_uuid)
	personas = []
	for aprobado in aprobados:
		personas.append({'persona':aprobado.postulacion.persona,'postulacion':aprobado.postulacion.pk,'pk':aprobado.pk,'apto': aprobado.apto,'entrevista': aprobado.entrevista,'rango':aprobado.postulacion.rango,'experiencia': InformacionLaboral.objects.filter(persona=aprobado.postulacion.persona, especialidad=convocatoria_puesto.especialidad).order_by('-fecha_inicio').first()})
	return render(request, 'convocatorias/aprobados.html', { 
		'title': 'Aprobados',
		'convocatoria_puesto': convocatoria_puesto,
		'personas': personas
	})
@login_required()
@permission_required('convocatorias.add_tramitedocumentario', raise_exception=True)
def tramite_documentario(request, uuid):
	convocatoria_puesto = ConvocatoriaPuesto.objects.get(uuid=uuid)
	contratados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='contratado')
	personas = []
	for contratado in contratados:
		personas.append({'persona':contratado.postulacion.persona,'pk':contratado.pk,'apto': contratado.apto,'entrevista': contratado.entrevista,'rango':contratado.postulacion.rango,'experiencia': InformacionLaboral.objects.filter(persona=contratado.postulacion.persona, especialidad=convocatoria_puesto.especialidad).order_by('-fecha_inicio').first()})
	return render(request, 'convocatorias/tramite_documentario.html', { 
		'title': 'Trámite Documentario',
		'convocatoria_puesto': convocatoria_puesto,
		'personas': personas
	})

@api_view(['POST'])
@permission_classes([AllowAny])
def add_documentos_postulacion(request, pk):
	estado_postulacion = get_object_or_404(PEQ_INT_estado_postulacion, pk=pk)
	if request.method == 'POST':
		detalle_documento = get_object_or_404(PEQ_MAE_detalle_documentacion, uuid=request.data['detalle_documento'])
		documento_postulacion = DocumentoPostulacion.objects.filter(detalle_documento=detalle_documento, estado_postulacion=estado_postulacion).first()
		if not documento_postulacion:
			documento_postulacion = DocumentoPostulacion()
			documento_postulacion.detalle_documento = detalle_documento
			documento_postulacion.estado_postulacion = estado_postulacion
		documento_postulacion.documento = request.data['documento']
		documento_postulacion.save()
		return Response({'message':'Archivo subido con exito'}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def postulante_visitado(request, pk):
	if request.method == 'POST':
		estado_postulacion = get_object_or_404(PEQ_INT_estado_postulacion, pk=pk)
		estado_postulacion.visitado = True if request.data['visitado'] == 'true' else False
		estado_postulacion.save()
		observacion = Observaciones.objects.create(descripcion='Postulante visitado')
		estado_postulacion.observaciones.add(observacion)
		return JsonResponse({'message':'Operacion con exito'})

@api_view(['POST'])
@permission_classes([AllowAny])
def postulante_verificado(request, pk):
	if request.method == 'POST':
		estado_postulacion = get_object_or_404(PEQ_INT_estado_postulacion, pk=pk)
		estado_postulacion.verificado = True if request.data['verificado'] == 'true' else False
		estado_postulacion.save()
		observacion = Observaciones.objects.create(descripcion='Postulante verificado')
		estado_postulacion.observaciones.add(observacion)
		return JsonResponse({'message':'Operacion con exito'})

@api_view(['POST'])
@permission_classes([AllowAny])
def postulante_llamado(request, pk):
	if request.method == 'POST':
		estado_postulacion = get_object_or_404(PEQ_INT_estado_postulacion, pk=pk)
		estado_postulacion.llamado = True if request.data['llamado'] == 'true' else False
		estado_postulacion.save()
		observacion = Observaciones.objects.create(descripcion='Postulante llamado')
		estado_postulacion.observaciones.add(observacion)
		return JsonResponse({'message':'Operacion con exito'})

@api_view(['POST'])
@permission_classes([AllowAny])
def confirmar_postulante(request, pk):
	if request.method == 'POST':
		estado_postulacion = get_object_or_404(PEQ_INT_estado_postulacion, pk=pk)
		estado_postulacion.quiero_participar = True if request.data['confirmado'] == 'true' else False
		estado_postulacion.save()
		observacion = Observaciones.objects.create(descripcion='Postulante confirmado')
		estado_postulacion.observaciones.add(observacion)
		return JsonResponse({'message':'Operacion con exito'})

@api_view(['POST'])
@permission_classes([AllowAny])
def aprobado_entrevista(request, pk):
	if request.method == 'POST':
		estado_postulacion = get_object_or_404(PEQ_INT_estado_postulacion, pk=pk)
		estado_postulacion.entrevista = True if request.data['entrevista'] == 'true' else False
		estado_postulacion.save()
		observacion = Observaciones.objects.create(descripcion='Postulante entrevista')
		estado_postulacion.observaciones.add(observacion)
		return JsonResponse({'message':'Operacion con exito'})

@api_view(['POST'])
@permission_classes([AllowAny])
def aprobado_apto(request, pk):
	if request.method == 'POST':
		estado_postulacion = get_object_or_404(PEQ_INT_estado_postulacion, pk=pk)
		estado_postulacion.apto = True if request.data['apto'] == 'true' else False
		estado_postulacion.save()
		observacion = Observaciones.objects.create(descripcion='Postulante apto')
		estado_postulacion.observaciones.add(observacion)
		return JsonResponse({'message':'Operacion con exito'})

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def add_observaciones_postulacion(request, pk):
	estado_postulacion = get_object_or_404(PEQ_INT_estado_postulacion, pk=pk)
	if request.method == 'POST':
		observacion = Observaciones()
		observacion.descripcion = request.data['descripcion']
		observacion.save()
		estado_postulacion.observaciones.add(observacion)
		return Response({'message':'Operacion con exito'})
	return Response(ObservacionesSerializer(estado_postulacion.observaciones, many=True).data, status=200)

@login_required()
@permission_required('convocatorias.add_seleccionarpreseleccionado', raise_exception=True)
def sesion_preseleccion(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	rangos = PEQ_MAE_rango_seleccion.objects.all().order_by('orden')
	aprobados__uuid = [ obj.postulacion.persona.uuid for obj in PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='aprobado')]
	preseleccionados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='preseleccion').exclude(postulacion__persona__uuid__in=aprobados__uuid)
	postulados = []
	base_datos = []
	comite = []
	for rango in rangos:
		for item in [{'tipo': 'postulante', 'array': postulados},{'tipo':'bd','array': base_datos},{'tipo':'manual','array': comite}]:

			preseleccionados_rango = preseleccionados.filter(postulacion__tipo_ingreso=item['tipo'], postulacion__rango=rango)
			if preseleccionados_rango:
				diccionario = {	
					'orden' : rango.orden,
					'descripcion': rango.descripcion,
					'data':{ 
						'total' : preseleccionados_rango.count(), 
						'confirmados': preseleccionados_rango.filter(quiero_participar=True).count(), 
						'no_confirmados': preseleccionados_rango.filter(quiero_participar=False).count() 
					}
				}
				item['array'].append(diccionario)

	return render(request, 'convocatorias/sesion_preseleccion.html', {
		'convocatoria_puesto': convocatoria_puesto,
		'postulados': postulados,
		'comite': comite,
		'base_datos': base_datos
	})

@login_required()
@permission_required('convocatorias.add_seleccionarpreseleccionado', raise_exception=True)
def list_preseleccionados(request, uuid, tipo_ingreso, orden):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	rango_seleccion = PEQ_MAE_rango_seleccion.objects.get(orden=orden)
	aprobados__uuid = [ obj.postulacion.persona.uuid for obj in PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='aprobado')]
	preseleccionados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, postulacion__tipo_ingreso=tipo_ingreso, postulacion__rango=rango_seleccion,estado__descripcion='preseleccion').exclude(postulacion__persona__uuid__in=aprobados__uuid)
	personas = []
	for preseleccion in preseleccionados:
		personas.append({'persona':preseleccion.postulacion.persona,'pk':preseleccion.postulacion.pk,'postulacion':preseleccion.pk,'confirmado': preseleccion.quiero_participar,'experiencia': InformacionLaboral.objects.filter(persona=preseleccion.postulacion.persona, especialidad=convocatoria_puesto.especialidad).order_by('-fecha_inicio').first()})
	return render(request, 'convocatorias/participantes_rango.html', {
		'title' : 'Cumplen al '+rango_seleccion.descripcion,
		'convocatoria_puesto': convocatoria_puesto,
		'personas' : personas
	})

def add_aprobado(postulacion_convocatoria):
	estado_postulacion = PEQ_INT_estado_postulacion()
	estado_postulacion.postulacion = postulacion_convocatoria
	estado_postulacion.estado = PEQ_MAE_estados_postulacion.objects.get(descripcion='aprobado')
	estado_postulacion.fecha = datetime.now().date()
	try:
		estado_postulacion.validate_unique()
	except ValidationError as err:
		pass
	else:
		estado_postulacion.save()

@api_view(['POST'])
@permission_classes([AllowAny])
def aprobar_pre_seleccion(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	data = request.data
	if data['tipo'] == 'individual':
		for dato in data['datos']:
			postulacion_convocatoria = get_object_or_404(PostulacionConvocatoria, pk=dato['postulacion'])
			add_aprobado(postulacion_convocatoria)
	elif data['tipo'] == 'rangos':
		for rango in data['rangos']:
			preseleccionados = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, postulacion__tipo_ingreso=data['tipo_ingreso'], postulacion__rango__orden=rango,estado__descripcion='preseleccion')
			for preseleccionado in preseleccionados:
				add_aprobado(preseleccionado.postulacion)
			
	registros = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='aprobado')
	return Response({'message':'Agregados con exito.','vacantes': convocatoria_puesto.cantidad_vacantes, 'aprobados':len(registros)}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def contratar_aprobados(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	data = request.data
	for postulacion in data['postulaciones']:
		estado_postulacion = PEQ_INT_estado_postulacion()
		estado_postulacion.postulacion = get_object_or_404(PostulacionConvocatoria, pk=postulacion)
		estado_postulacion.estado = PEQ_MAE_estados_postulacion.objects.get(descripcion='contratado')
		estado_postulacion.fecha = datetime.now()
		try:
			estado_postulacion.validate_unique()
		except ValidationError as err:
			pass
		else:
			estado_postulacion.save()

	registros = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='contratado')
	return Response({'message':'Agregados con exito.','vacantes': convocatoria_puesto.cantidad_vacantes, 'contratados':registros.count()}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_pre_seleccion(request, uuid):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	data = request.data
	list_email = []
	for dato in data:
		if dato['tipo'] != 'postulante':
			postulacion_convocatoria = PostulacionConvocatoria()
			postulacion_convocatoria.convocatoria_puesto = convocatoria_puesto
			postulacion_convocatoria.persona = get_object_or_404(Persona, uuid=dato['persona'])
			postulacion_convocatoria.tipo_ingreso = dato['tipo']
		else:
			postulacion_convocatoria = PostulacionConvocatoria.objects.get(convocatoria_puesto=convocatoria_puesto, persona__uuid=dato['persona'])
		postulacion_convocatoria.rango = get_object_or_404(PEQ_MAE_rango_seleccion, uuid=dato['rango'])

		try:
			postulacion_convocatoria.validate_unique()
		except ValidationError as err:
			pass
		else:
			postulacion_convocatoria.save()
			if dato['tipo'] != 'postulante':
				estado_postulacion = PEQ_INT_estado_postulacion()
				estado_postulacion.postulacion = postulacion_convocatoria
				estado_postulacion.estado = PEQ_MAE_estados_postulacion.objects.get(descripcion='postulando')
				estado_postulacion.fecha = datetime.now()
				try:
					estado_postulacion.validate_unique()
				except ValidationError as err:
					pass
				else:
					estado_postulacion.save()
		estado_postulacion = PEQ_INT_estado_postulacion()
		estado_postulacion.postulacion = postulacion_convocatoria
		estado_postulacion.estado = PEQ_MAE_estados_postulacion.objects.get(descripcion='preseleccion')
		estado_postulacion.fecha = datetime.now()
		try:
			estado_postulacion.validate_unique()
		except ValidationError as err:
			pass
		else:
			estado_postulacion.save()
		# EMAIL
		if postulacion_convocatoria.persona.email:
			message_html = u'<h1><strong>Postulante {nombres} {apellidos}</strong></h1><hr>\n'\
							u'<h3>Usted ha sido preseleccionado para este puesto, seguiremos con la selección.</h3>'.format(nombres=postulacion_convocatoria.persona.nombres, apellidos=postulacion_convocatoria.persona.apellidos)
			list_email.append({'message':message_html, 'recipient': postulacion_convocatoria.persona.email})

	enviar_mass_email(get_title_convocatoria_puesto(convocatoria_puesto), list_email) if list_email else 'no hay correos'

	registros = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto, estado__descripcion='preseleccion')
	return Response({'message':'Agregados con exito.','vacantes': convocatoria_puesto.cantidad_vacantes, 'preseleccionados':len(registros)}, status=200)
	
# DOCUMENTOS
@login_required()
@permission_required('usuarios.add_peq_int_convocatoria_documentos', raise_exception=True)
def add_documentos_convocatoria_puesto(request, uuid): 
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	form = ConvocatoriaDocumentosForm()
	if request.method == 'POST':
		form = ConvocatoriaDocumentosForm(request.POST)
		if form.is_valid():
			documento = form.save(commit=False)
			documento.convocatoria_puesto = convocatoria_puesto
			try:
				documento.validate_unique()
			except ValidationError as err:
				messages.error(request, 'Registro duplicado.')
			else:
				documento.save()
				messages.success(request, 'Registro agregado con éxito.')
				form = ConvocatoriaDocumentosForm()
	return render(request, 'convocatorias/documentos/add.html', {
		'title': 'Documentos',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('usuarios.change_peq_int_convocatoria_documentos', raise_exception=True)
def edit_documentos_convocatoria_puesto(request, uuid, pk_documento):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	documento_convocatoria = get_object_or_404(PEQ_INT_convocatoria_documentos, pk=pk_documento)
	form = ConvocatoriaDocumentosForm(instance=documento_convocatoria)
	if request.method == "POST":
		form = ConvocatoriaDocumentosForm(request.POST, instance=documento_convocatoria)
		if form.is_valid():
			try:
				form.validate_unique()
			except ValidationError as err:
				messages.error(request, 'Registro duplicado.')
			else:
				form.save(commit=True)
				messages.success(request, 'Registro modificado con éxito.')
				return redirect('add-documento-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
	return render(request, 'convocatorias/documentos/add.html', {
		'title': 'Documentos',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('usuarios.delete_peq_int_convocatoria_documentos', raise_exception=True)
def delete_documentos_convocatoria_puesto(request, uuid, pk_documento):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	documento_convocatoria = get_object_or_404(PEQ_INT_convocatoria_documentos, pk=pk_documento)
	if request.method == 'POST':
		documento_convocatoria.delete()
		messages.success(request, 'Registro eliminado con éxito.')
		return redirect('add-documento-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
	return render(request, 'convocatorias/documentos/delete.html', {
		'title': 'Eliminar registro de documento',
		'convocatoria_puesto': convocatoria_puesto,
		'documento_convocatoria': documento_convocatoria
	})

# EXPERIENCIA ESPECIFICA
@login_required()
@permission_required('usuarios.add_convocatoriapuesto', raise_exception=True)
def add_requisitos_convocatoria_puesto(request, uuid): 
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	form = RequisitoConvocatoriaForm()
	if request.method == 'POST':
		form = RequisitoConvocatoriaForm(request.POST)
		if form.is_valid():
			requisito = form.save()
			convocatoria_puesto.requisitos.add(requisito)
			form = RequisitoConvocatoriaForm()
	return render(request, 'convocatorias/requisitos/add.html', {
		'title': 'Experiencia Específica',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('usuarios.change_convocatoriapuesto', raise_exception=True)
def edit_requisitos_convocatoria_puesto(request, uuid, uuid_requisito):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	requisito = get_object_or_404(PEQ_MAE_requisitos, uuid=uuid_requisito)
	form = RequisitoConvocatoriaForm(instance=requisito)
	if request.method == "POST":
		form = RequisitoConvocatoriaForm(request.POST, instance=requisito)
		if form.is_valid():
			form.save(commit=True)
			messages.success(request, 'Registro modificado con éxito.')
			return redirect('add-requisito-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
	return render(request, 'convocatorias/requisitos/add.html', {
		'title': 'Experiencia Específica',
		'convocatoria_puesto': convocatoria_puesto,
		'form': form
	})

@login_required()
@permission_required('usuarios.delete_convocatoriapuesto', raise_exception=True)
def delete_requisitos_convocatoria_puesto(request, uuid, uuid_requisito):
	convocatoria_puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	requisito = get_object_or_404(PEQ_MAE_requisitos, uuid=uuid_requisito)
	if request.method == 'POST':
		requisito.delete()
		messages.success(request, 'Registro eliminado con éxito.')
		return redirect('add-requisito-convocatoria-puesto', uuid=convocatoria_puesto.uuid)
	return render(request, 'convocatorias/requisitos/delete.html', {
		'title': 'Eliminar registro de requisito',
		'convocatoria_puesto': convocatoria_puesto,
		'requisito': requisito
	})