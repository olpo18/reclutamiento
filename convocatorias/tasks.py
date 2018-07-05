# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail,BadHeaderError

@shared_task
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

@shared_task
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