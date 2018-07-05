# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
# MODELS
from usuarios.models import Role
from convocatorias.models import Convocatoria, PostulacionConvocatoria, PEQ_INT_estado_postulacion, ConvocatoriaPuesto,PEQ_INT_estado_convocatoria
from maestros.models import PEQ_MAE_estados_postulacion, PEQ_MAE_departamentos
# FORMS
from usuarios.forms import PersonaForm, RegisterPublicForm
# services
from maestros.services import enviar_email
# from convocatorias.tasks import enviar_email

from datetime import datetime

def index_public(request):
	now_str = datetime.now().strftime('%Y-%m-%d')
	convocatorias_iniciadas = PEQ_INT_estado_convocatoria.objects.filter(estado__descripcion='en proceso', fecha_inicio__lte=now_str, fecha_fin__gte=now_str)
	# preseleccionados
	preseleccionados = PEQ_INT_estado_postulacion.objects.values('fecha','postulacion__convocatoria_puesto').filter(estado__descripcion='preseleccion').annotate(total=Count('pk'))
	convocatoria_puesto_uuid_preseleccionados = [obj['postulacion__convocatoria_puesto'] for obj in preseleccionados]
	convocatoria_puestos_preseleccionados = ConvocatoriaPuesto.objects.filter(uuid__in=convocatoria_puesto_uuid_preseleccionados)
	# seleccionados
	seleccionados = PEQ_INT_estado_postulacion.objects.values('fecha','postulacion__convocatoria_puesto').filter(estado__descripcion='aprobado').annotate(total=Count('pk'))
	convocatoria_puesto_uuid_seleccionados = [obj['postulacion__convocatoria_puesto'] for obj in seleccionados]
	convocatoria_puestos_seleccionados = ConvocatoriaPuesto.objects.filter(uuid__in=convocatoria_puesto_uuid_seleccionados)
	return render(request, 'index_publico.html', {
		'title': 'Inicio',
		'convocatorias': convocatorias_iniciadas,
		'convocatoria_puestos_preseleccionados': convocatoria_puestos_preseleccionados,
		'preseleccionados': preseleccionados,
		'convocatoria_puestos_seleccionados': convocatoria_puestos_seleccionados,
		'seleccionados': seleccionados
	})

def convocatorias_public(request):
	now_str = datetime.now().strftime('%Y-%m-%d')
	convocatorias = PEQ_INT_estado_convocatoria.objects.filter(estado__descripcion='en proceso', fecha_inicio__lte=now_str, fecha_fin__gte=now_str)
	return render(request, 'convocatorias.html', {
		'title': 'Convocatorias',
		'convocatorias': convocatorias
	})

def preseleccionados_public(request):
	preseleccionados = PEQ_INT_estado_postulacion.objects.values('fecha','postulacion__convocatoria_puesto').filter(estado__descripcion='preseleccion').annotate(total=Count('pk'))
	convocatoria_puesto_uuid_preseleccionados = [obj['postulacion__convocatoria_puesto'] for obj in preseleccionados]
	convocatoria_puestos_preseleccionados = ConvocatoriaPuesto.objects.filter(uuid__in=convocatoria_puesto_uuid_preseleccionados)
	return render(request, 'preseleccionados.html', {
		'title': 'preseleccionados',
		'convocatoria_puestos_preseleccionados': convocatoria_puestos_preseleccionados,
		'preseleccionados': preseleccionados,
	})

def seleccionados_public(request):
	seleccionados = PEQ_INT_estado_postulacion.objects.values('fecha','postulacion__convocatoria_puesto').filter(estado__descripcion='aprobado').annotate(total=Count('pk'))
	convocatoria_puesto_uuid_seleccionados = [obj['postulacion__convocatoria_puesto'] for obj in seleccionados]
	convocatoria_puestos_seleccionados = ConvocatoriaPuesto.objects.filter(uuid__in=convocatoria_puesto_uuid_seleccionados)
	return render(request, 'seleccionados.html', {
		'title': 'seleccionados',
		'convocatoria_puestos_seleccionados': convocatoria_puestos_seleccionados,
		'seleccionados': seleccionados,
	})

def convocatoria_detail(request, uuid):
	puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	estado = PEQ_INT_estado_convocatoria.objects.filter(convocatoria=puesto.convocatoria,estado__descripcion='en proceso').first()
	title = '('+str(puesto.cantidad_vacantes)+') '+puesto.rango.descripcion+' '+puesto.especialidad.descripcion
	postulacion = PostulacionConvocatoria.objects.filter(convocatoria_puesto=puesto, persona=request.user.persona).first() if hasattr(request.user, 'persona' ) else ''
	return render(request, 'convocatoria_puesto_detail.html', {
		'title': title,
		'estado': estado,
		'postulacion': postulacion,
		'puesto': puesto
	})

def convocatoria_puesto_preseleccionados_detail(request, uuid, fecha):
	puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	preseleccionados = PEQ_INT_estado_postulacion.objects.filter(estado__descripcion='preseleccion', fecha=fecha, postulacion__convocatoria_puesto=puesto)
	title = '('+str(puesto.cantidad_vacantes)+') '+puesto.rango.descripcion+' '+puesto.especialidad.descripcion + ' - preselección'
	return render(request, 'convocatoria_puesto_preseleccionado_detail.html', {
		'title': title,
		'puesto': puesto,
		'fecha': datetime.strptime(fecha, '%Y-%m-%d'),
		'preseleccionados': preseleccionados
	})

def convocatoria_puesto_seleccionados_detail(request, uuid, fecha):
	puesto = get_object_or_404(ConvocatoriaPuesto, uuid=uuid)
	seleccionados = PEQ_INT_estado_postulacion.objects.filter(estado__descripcion='aprobado', fecha=fecha, postulacion__convocatoria_puesto=puesto)
	title = '('+str(puesto.cantidad_vacantes)+') '+puesto.rango.descripcion+' '+puesto.especialidad.descripcion + ' - selección'
	return render(request, 'convocatoria_puesto_seleccionado_detail.html', {
		'title': title,
		'puesto': puesto,
		'fecha': datetime.strptime(fecha, '%Y-%m-%d'),
		'seleccionados': seleccionados
	})

def publico_postular_convocatoria(request, uuid):
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
		postulacion_convocatoria.persona = request.user.persona
		postulacion_convocatoria.tipo_ingreso = 'postulante'
		postulacion_convocatoria.save()
		estado_postulacion = PEQ_INT_estado_postulacion()
		estado_postulacion.postulacion = postulacion_convocatoria
		estado_postulacion.estado = PEQ_MAE_estados_postulacion.objects.get(descripcion='postulando')
		estado_postulacion.fecha = datetime.now()
		estado_postulacion.save()
		# ENVIAR CORREO
		puesto = postulacion_convocatoria.convocatoria_puesto
		name_puesto = puesto.rango.descripcion +' '+ (puesto.sub_especialidad.descripcion if puesto.sub_especialidad else '') +' '+ puesto.especialidad.descripcion
		message_html = u'<h1><strong>Su postulación ha sido agregada correctamente, revisaremos si cumple con el perfil de la convocatoria.</strong></h1>'
		enviar_email(request.user.persona.email,'Postulacion a '+name_puesto.lower(),message_html) if request.user.persona.email else ''
		return JsonResponse({'message':'Registro agregado correctamente.', 'class':'text-green'}, status=200)
	except Exception, e:
		return JsonResponse({'message': str(e),'class':'text-red'}, status=400)

def login_public(request):
	message = {}
	if request.user.is_authenticated:
		return redirect('index-publico')
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if request.GET.get('next'):
				return redirect(request.GET.get('next'))
			return redirect('index-publico')
		else:
			message['value'] = "Usuario y/o contraseña no validos."
			message['class'] = "danger"
	return render(request, 'login_publico.html', {'message':message})

def register_public(request):
	if request.user.is_authenticated:
		return redirect('/publico/perfil/')
	form = RegisterPublicForm()
	if request.method == "POST":
		form = RegisterPublicForm(request.POST, request.FILES)
		if form.is_valid():
			password = User.objects.make_random_password()
			user, created = User.objects.update_or_create(username=form.cleaned_data['numero_documento'], email=form.cleaned_data['email'])
			user.set_password(password)
			user.save()
			persona = form.save(commit=False)
			persona.user = user
			persona.verificado = False
			persona.save()
			Role.objects.create(rol=Role.POSTULANTE, user=user)
			# ENVIAR CORREO
			message_html = u'<h1><strong>Usuario</strong></h1><hr>\n'\
							u'<h3><strong>Username: </strong>{username}</h3>\n'\
							u'<h3><strong>Contraseña: </strong>{password}</h3>\n'\
							u'<p><a href="{url_login}" target="_blank">Clic aquí para ingresar {url_login}</a></p>'.format(username=user.username, password=password, url_login=settings.URL_SITE+'/publico/login')
			enviar_email(persona.email,'Creacion de usuario',message_html) if persona.email else ''
			if user is not None:
				login(request, user)
				if request.GET.get('next'):
					return redirect(request.GET.get('next'))
			return redirect('/publico/perfil/')
	return render(request, 'registrar_publico.html', {
		'title': 'Registrarse',
		'form': form,
		'departamentos': PEQ_MAE_departamentos.objects.all().order_by('descripcion')
	})

def profile_public(request):
	return render(request, 'profile_publico.html', {
		'title': 'Perfil'
	})

@login_required(login_url='/publico/login/')
def postulaciones_public(request):
	postulaciones = ''
	message = ''
	if hasattr(request.user, 'persona'):
		postulaciones = PostulacionConvocatoria.objects.filter(persona=request.user.persona)	
	else:
		message = {'value':'el usuario no tiene una persona asociada', 'class':'danger'}
	return render(request, 'mis_postulaciones.html', {
		'title': 'mis postulaciones',
		'message': message,
		'postulaciones': postulaciones
	})

@login_required(login_url='/publico/login/')
def edit_profile_public(request):
	persona = request.user.persona
	form = PersonaForm(instance=persona)
	if request.method == "POST":
		form = PersonaForm(request.POST, request.FILES, instance=persona)
		if form.is_valid():
			persona = form.save(commit=True)
			return redirect('/publico/perfil/')
		print form.errors
	return render(request, 'registrar_publico.html', { 
		'title': 'Editar perfil', 
		'departamentos': PEQ_MAE_departamentos.objects.all().order_by('descripcion'),
		'form': form
	})
