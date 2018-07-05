# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
# MODELS
from .models import *
# Register your models here.
from django.contrib import messages

from django.contrib.auth.models import Permission

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
	list_display = ('id','content_type','codename','name')
	search_fields = ['name','codename']
	list_filter = ('content_type',)

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
	list_display = ('uuid','nombres','apellidos','numero_documento','genero','estado_civil','celular','fecha_nacimiento','direccion')
	search_fields = ['numero_documento', 'nombres', 'apellidos']

@admin.register(InformacionEducativa)
class InformacionEducativaAdmin(admin.ModelAdmin):
	search_fields = ['persona__numero_documento','persona__nombres','persona__apellidos']
	list_display = ('persona','centro_estudio','nombre','grado','fecha_inicio','fecha_fin','hasta_actualidad')

@admin.register(InformacionLaboral)
class InformacionLaboralAdmin(admin.ModelAdmin):
	search_fields = ['persona__numero_documento','persona__nombres','persona__apellidos']
	list_display = ('persona','empresa','nombre','rango','fecha_inicio','fecha_fin','hasta_actualidad')

@admin.register(Bloqueados)
class BloqueadosAdmin(admin.ModelAdmin):
	list_display = ('numero_documento','nombres','apellidos')
	search_fields = ['numero_documento',]

@admin.register(DocumentosPersonal)
class DocumentosPersonalAdmin(admin.ModelAdmin):
	list_display = ('persona','tipo')

@admin.register(UserAsociacion)
class UserAsociacionAdmin(admin.ModelAdmin):
	list_display = ('user','proyecto','contratista','contratista_principal','sub_contratista')	
	raw_id_fields = ('user',)

# CUSTOM USER ADMIN ADD ROLE
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class RoleInline(admin.StackedInline):
	model = Role
	can_delete = False
	verbose_name_plural = 'Rol'
	fk_name = 'user'

class CustomUserAdmin(UserAdmin):
	inlines = (RoleInline, )
	list_display = ('username', 'get_role', 'email', 'first_name', 'last_name', 'is_staff')
	list_select_related = ('role', )

	def get_role(self, instance):
		return instance.role.get_rol_display()
	get_role.short_description = 'Rol'

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)