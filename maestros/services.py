# -*- coding: utf-8 -*-
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail, BadHeaderError
from django.db.models import Sum, Count
from django.contrib.auth.models import Group 
from usuarios.models import Persona
from convocatorias.models import PEQ_INT_estado_postulacion, PEQ_INT_estado_convocatoria
# OTHERS
from datetime import datetime

def enviar_email(recipient, subject, message):
	if subject and message and recipient:
		try:
			send_mail(
				subject, strip_tags(message),
				settings.EMAIL_HOST_USER, [recipient],
				html_message=message)
		except BadHeaderError:
			return {'error': 'invalid header found.'}
		return {'status': 'message sent.', 'recipient': recipient}
	else:
		return {'status': 'Make sure all fields are entered and valid.'}

def enviar_mass_email(subject, data):
	list_messages = [(subject, strip_tags(item['message']), settings.EMAIL_HOST_USER, [item['recipient']]) for item in data]
	if list_messages:
		try:
			send_mass_mail(list_messages)
		except BadHeaderError:
			return {'error': 'invalid header found.'}
		return {'status': 'Correos enviados'}
	else:
		return {'status': 'Lista vacía.'}

def get_lugar(persona):
	lugar = 0
	if persona.departamento_nacimiento:
		if persona.departamento_nacimiento.descripcion.lower() == 'piura':
			lugar = 1
	if persona.provincia_nacimiento:
		if persona.provincia_nacimiento.descripcion.lower() == 'talara':
			lugar = 2
	if persona.provincia_residencia:
		if (persona.provincia_residencia.descripcion.lower() == 'talara') and ((persona.tipo_tiempo_residencia == Persona.MESES and persona.tiempo_residencia >= 12) or (persona.tipo_tiempo_residencia == Persona.ANNIOS and persona.tiempo_residencia >= 1)):
			lugar = 2
	return lugar

def Duplicate(model, query):
	return model.objects.filter(**query).count() > 1

def convocatoria_is_authorized(convocatoria):
	estados = PEQ_INT_estado_convocatoria.objects.filter(convocatoria=convocatoria).aggregate(total=Sum('estado__orden'))
	return (estados['total'] > 1) if estados['total'] else False

def convocatoria_is_vigente(convocatoria):
	estado_convocatoria = PEQ_INT_estado_convocatoria.objects.filter(convocatoria=convocatoria, estado__descripcion='en proceso')
	if estado_convocatoria:
		nowstr = datetime.now().strftime('%Y-%m-%d')
		vigente = estado_convocatoria.filter(fecha_inicio__lte=nowstr, fecha_fin__gte=nowstr).first()
		return True if vigente else False
	return False

def puesto_convocatoria_has_persons(convocatoria_puesto):
	# Postulantes excluidos
	estados_postulacion = PEQ_INT_estado_postulacion.objects.filter(postulacion__convocatoria_puesto=convocatoria_puesto).exclude(estado__descripcion='postulando')
	return estados_postulacion.count() > 0

def user_is_owner(user, convocatoria):
	# Si es analista tambien es propietario
	group =  Group.objects.get(name='analistas') 
	return True if user.is_superuser or convocatoria.user == user or group in user.groups.all() else False
