# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(ContratistaPrincipal)
class ContratistaPrincipalAdmin(admin.ModelAdmin):
	list_display = ('uuid','nombre','alias','razon_social','persona_contacto','numero_celular')

@admin.register(Contratista)
class ContratistaAdmin(admin.ModelAdmin):
	list_display = ('uuid','nombre','alias','razon_social','persona_contacto','numero_celular')

@admin.register(SubContratista)
class SubContratistaAdmin(admin.ModelAdmin):
	list_display = ('uuid','contratista','nombre','razon_social','persona_contacto','numero_celular')

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
	list_display = ('uuid','nombre','alias')

@admin.register(ProyectoContratistas)
class ProyectoContratistasAdmin(admin.ModelAdmin):
	list_display = ('uuid','proyecto','contratista_principal','display_contratistas')

	def display_contratistas(self, instance):
		return ', '.join([ contratista.nombre for contratista in instance.contratistas.all() ])
	display_contratistas.short_description = 'Contratistas'