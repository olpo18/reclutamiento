# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Atenciones

@admin.register(Atenciones)
class AtencionAdmin(admin.ModelAdmin):
	list_display = ('uuid','tipo','persona','fecha','hora_inicio','hora_fin')
	search_fields = ['persona','fecha']
	list_filter = ('tipo',)