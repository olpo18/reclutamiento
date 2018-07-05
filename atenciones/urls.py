from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index_atenciones, name='index-atenciones'),
	url(r'^add/$', views.add_atencion, name='add-atencion'),
	url(r'^(?P<uuid>[^/]+)/finalizar/$', views.finalizar_atencion, name='finalizar-atencion'),
	url(r'^(?P<uuid>[^/]+)/edit/$', views.edit_atencion, name='edit-atencion'),
	url(r'^(?P<uuid>[^/]+)/delete/$', views.delete_atencion, name='delete-atencion'),
]