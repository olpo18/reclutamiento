from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^familias/especialidades/$', views.EspecialidadesByFamiliaList.as_view()),
	url(r'^familias/grados/$', views.GradosByFamiliaList.as_view()),
	url(r'^familias/carreras/$', views.CarrerasByFamiliaList.as_view()),
	url(r'^especialidades/sub_especialidades/$', views.SubEspecialidadesByFamiliaList.as_view()),
	url(r'^documentos/detalle/$', views.DetalleByTipoDocumentoList.as_view()),
	# AUTOCOMPLETE
    url(r'^departamentos-autocomplete/$', views.DepartamentosAutocomplete.as_view(), name='departamentos-autocomplete'),
    url(r'^provincias-autocomplete/$', views.ProvinciasAutocomplete.as_view(), name='provincias-autocomplete'),
    url(r'^distritos-autocomplete/$', views.DistritosAutocomplete.as_view(), name='distritos-autocomplete'),
]