from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index_public, name='index-publico'),
	url(r'^login/$', views.login_public),
	url(r'^registrarse/$', views.register_public),
	url(r'^perfil/$', views.profile_public),
	url(r'^editar/perfil/$', views.edit_profile_public),
	url(r'^postulaciones/$', views.postulaciones_public),
	url(r'^convocatorias/$', views.convocatorias_public),
	url(r'^preseleccionados/$', views.preseleccionados_public),
	url(r'^seleccionados/$', views.seleccionados_public),
	url(r'^convocatoria/puesto/(?P<uuid>[^/]+)/$', views.convocatoria_detail),
	url(r'^convocatoria/puesto/(?P<uuid>[^/]+)/(?P<fecha>[^/]+)/preseleccionados/$', views.convocatoria_puesto_preseleccionados_detail),
	url(r'^convocatoria/puesto/(?P<uuid>[^/]+)/(?P<fecha>[^/]+)/seleccionados/$', views.convocatoria_puesto_seleccionados_detail),
	url(r'^postular/puesto/(?P<uuid>[^/]+)/$', views.publico_postular_convocatoria),
]