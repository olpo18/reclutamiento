from django.conf.urls import url

from . import views

urlpatterns = [
	# PERSONA
	url(r'^persona/(?P<uuid>[^/]+)/add/$', views.add_curso_persona, name='add-curso-persona'),
	url(r'^persona/(?P<uuid>[^/]+)/delete/(?P<pk_curso>[^/]+)/$', views.delete_curso_persona, name='delete-curso-persona'),
	url(r'^persona/(?P<uuid>[^/]+)/edit/(?P<pk_curso>[^/]+)/$', views.edit_curso_persona, name='edit-curso-persona'),
	# CONVOCATORIA
	url(r'^puesto/(?P<uuid>[^/]+)/add/$', views.add_curso_convocatoria_puesto, name='add-curso-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/delete/(?P<pk_curso>[^/]+)/$', views.delete_curso_convocatoria_puesto, name='delete-curso-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/edit/(?P<pk_curso>[^/]+)/$', views.edit_curso_convocatoria_puesto, name='edit-curso-convocatoria-puesto')
]