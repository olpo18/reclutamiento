from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index_personas, name='index-personas'),
	url(r'^add/$', views.add_persona, name='add-persona'),
	url(r'^find_persona/$', views.find_persona, name='find-persona'),
	url(r'^(?P<uuid>[^/]+)/editar/$', views.edit_persona, name='edit-persona'),
	url(r'^(?P<uuid>[^/]+)/postulaciones/$', views.persona_postulaciones, name='postulaciones-persona'),
	# AUTOCOMPLETE
    url(r'^persona-autocomplete/$', views.PersonaAutocomplete.as_view(), name='persona-autocomplete'),
    url(r'^centro-estudio-autocomplete/$', views.CentroEstudioAutocomplete.as_view(), name='centro-estudio-autocomplete'),
    url(r'^nombre-curso-autocomplete/$', views.NombreCursoAutocomplete.as_view(), name='nombre-curso-autocomplete'),
    url(r'^carreras-autocomplete/$', views.CarrerasAutocomplete.as_view(), name='carreras-autocomplete'),
    url(r'^empresas-autocomplete/$', views.EmpresasAutocomplete.as_view(), name='empresas-autocomplete'),
    url(r'^especialidades-autocomplete/$', views.EspecialidadesAutocomplete.as_view(), name='especialidades-autocomplete'),
    url(r'^sub-especialidades-autocomplete/$', views.SubEspecialidadesAutocomplete.as_view(), name='sub-especialidades-autocomplete'),
	# DOCUMENTOS
	url(r'^(?P<uuid>[^/]+)/documentos/add/$', views.add_documentos_persona, name='add-documento-persona'),
	url(r'^(?P<uuid>[^/]+)/documentos/delete/(?P<pk_documento>[^/]+)/$', views.delete_documentos_persona, name='delete-documento-persona'),
	url(r'^(?P<uuid>[^/]+)/documentos/edit/(?P<pk_documento>[^/]+)/$', views.edit_documentos_persona, name='edit-documento-persona'),
	# PDF
	url(r'^(?P<uuid>[^/]+)/pdf/$', views.PdfCurriculum, name='pdf-persona'),
	url(r'^bloquear/add/$', views.add_bloquear_persona),
	# EXCEL
	# url(r'^excel/$', views.ExcelInformacionPersonas),
	# url(r'^(?P<uuid>[^/]+)/documentos/$', views.add_persona_documentos, name='add-persona-documentos'),
	# API
	url(r'^api/(?P<uuid>[^/]+)/info_laboral/$', views.PersonaInformacionLaboralList.as_view())
]