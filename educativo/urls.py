from django.conf.urls import url

from . import views

urlpatterns = [
	# PERSONA
	url(r'^persona/(?P<uuid>[^/]+)/add/$', views.add_educativo_persona, name='add-educativo-persona'),
	url(r'^persona/(?P<uuid>[^/]+)/delete/(?P<pk_educativo>[^/]+)/$', views.delete_educativo_persona, name='delete-educativo-persona'),
	url(r'^persona/(?P<uuid>[^/]+)/edit/(?P<pk_educativo>[^/]+)/$', views.edit_educativo_persona, name='edit-educativo-persona'),
	# PUESTO CONVOCATORIA
	url(r'^puesto/(?P<uuid>[^/]+)/add/$', views.add_educativo_convocatoria_puesto, name='add-educativo-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/delete/(?P<pk_educativo>[^/]+)/$', views.delete_educativo_convocatoria_puesto, name='delete-educativo-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/edit/(?P<pk_educativo>[^/]+)/$', views.edit_educativo_convocatoria_puesto, name='edit-educativo-convocatoria-puesto'),
]