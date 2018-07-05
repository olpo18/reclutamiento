# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from maestros.models import PEQ_MAE_tipo_atencion, PEQ_MAE_capacitaciones
from usuarios.models import Persona
from django.contrib.auth.models import User

import uuid

class Atenciones(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, null=True, blank=True)
	persona = models.ForeignKey(Persona, null=True, blank=True)
	tipo = models.ForeignKey(PEQ_MAE_tipo_atencion, null=False, blank=False)
	capacitacion = models.ForeignKey(PEQ_MAE_capacitaciones, null=True, blank=True)
	observaciones = models.CharField(max_length=1000, null=True, blank=True)
	fecha = models.DateField(null=False, blank=False)
	hora_inicio = models.TimeField(null=False, blank=False)
	hora_fin = models.TimeField(null=True, blank=True)
	fecha_finalizacion = models.DateField(null=True, blank=True)
	finalizada = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Atención"
		verbose_name_plural = "Atenciones"

	def __unicode__(self):
		return '{0} {1}'.format(self.persona.dni, self.fecha)