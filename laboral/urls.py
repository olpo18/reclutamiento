from django.conf.urls import url

from . import views

urlpatterns = [
	# PERSONA
	url(r'^persona/(?P<uuid>[^/]+)/add/$', views.add_laboral_persona, name='add-laboral-persona'),
	url(r'^persona/(?P<uuid>[^/]+)/delete/(?P<pk_laboral>[^/]+)/$', views.delete_laboral_persona, name='delete-laboral-persona'),
	url(r'^persona/(?P<uuid>[^/]+)/edit/(?P<pk_laboral>[^/]+)/$', views.edit_laboral_persona, name='edit-laboral-persona'),
	# CONVOCATORIA
	url(r'^puesto/(?P<uuid>[^/]+)/add/$', views.add_experiencia_convocatoria_puesto, name='add-laboral-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/delete/(?P<pk_experiencia>[^/]+)/$', views.delete_experiencia_convocatoria_puesto, name='delete-laboral-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/edit/(?P<pk_experiencia>[^/]+)/$', views.edit_experiencia_convocatoria_puesto, name='edit-laboral-convocatoria-puesto')
]