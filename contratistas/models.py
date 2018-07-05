# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
class Proyecto(models.Model):
	
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	nombre = models.CharField(max_length=255, null=False, blank=False)
	alias = models.CharField(max_length=255, null=False, blank=False)

	class Meta:
		verbose_name = "Proyecto"
		verbose_name_plural = "Proyectos"

	def __unicode__(self):
		return '%s' % self.nombre

class ContratistaPrincipal(models.Model):
	
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	razon_social = models.CharField(max_length=255, null=False, blank=False)
	nombre = models.CharField(max_length=255, null=False, blank=False)
	alias = models.CharField(max_length=255, null=False, blank=False)
	persona_contacto = models.CharField(max_length=255, null=False, blank=False)
	numero_celular = models.CharField(max_length=255, null=False, blank=False)

	class Meta:
		verbose_name = "Contratista Principal"
		verbose_name_plural = "Contratistas Principales"

	def __unicode__(self):
		return '%s' % self.nombre

class Contratista(models.Model):
	
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	razon_social = models.CharField(max_length=255, null=False, blank=False)
	nombre = models.CharField(max_length=255, null=False, blank=False)
	alias = models.CharField(max_length=255, null=False, blank=False)
	persona_contacto = models.CharField(max_length=255, null=False, blank=False)
	numero_celular = models.CharField(max_length=255, null=False, blank=False)

	class Meta:
		verbose_name = "Contratista"
		verbose_name_plural = "Contratistas"

	def __unicode__(self):
		return '%s' % self.nombre

class SubContratista(models.Model):
	
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	contratista = models.ForeignKey(Contratista)
	razon_social = models.CharField(max_length=255, null=False, blank=False)
	nombre = models.CharField(max_length=255, null=False, blank=False)
	alias = models.CharField(max_length=255, null=False, blank=False)
	persona_contacto = models.CharField(max_length=255, null=False, blank=False)
	numero_celular = models.CharField(max_length=255, null=False, blank=False)

	class Meta:
		verbose_name = "SubContratista"
		verbose_name_plural = "SubContratistas"

	def __unicode__(self):
		return '%s' % self.nombre

class ProyectoContratistas(models.Model):

	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	proyecto = models.ForeignKey(Proyecto)
	contratista_principal = models.ForeignKey(ContratistaPrincipal)
	contratistas = models.ManyToManyField(Contratista)

	class Meta:
		verbose_name = "Proyecto Contratistas"
		verbose_name_plural = "Proyecto Contratistas"
		unique_together = ('proyecto','contratista_principal')

	def __unicode__(self):
		return '%s' % self.proyecto.nombre	