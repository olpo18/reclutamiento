from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index_convocatoria, name='index-convocatoria'),
	url(r'^add/$', views.add_convocatoria, name='add-convocatoria'),
	url(r'^(?P<uuid>[^/]+)/editar/$', views.edit_convocatoria, name='edit-convocatoria'),
	url(r'^(?P<uuid>[^/]+)/eliminar/$', views.delete_convocatoria, name='delete-convocatoria'),
	url(r'^(?P<uuid>[^/]+)/puestos/$', views.add_convocatoria_puestos, name='add-convocatoria-puestos'),
	url(r'^(?P<uuid>[^/]+)/codigo/$', views.get_codigo_convocatoria, name='get-codigo-convocatoria'),
	url(r'^puestos/(?P<uuid>[^/]+)/editar/$', views.edit_convocatoria_puesto, name='edit-convocatoria-puesto'),
	url(r'^puestos/(?P<uuid>[^/]+)/delete/$', views.delete_convocatoria_puesto, name='delete-convocatoria-puesto'),
	url(r'^puestos/(?P<uuid>[^/]+)/postulantes/$', views.detail_convocatoria, name='detail-convocatoria'),
	url(r'^puestos/(?P<uuid>[^/]+)/postular/(?P<uuid_persona>[^/]+)/$', views.postulacion_convocatoria, name='postulacion-convocatoria'),
	url(r'^puestos/(?P<uuid>[^/]+)/pases_ingreso/$', views.pase_de_ingreso, name='pase-de-ingreso'),
	url(r'^puestos/(?P<uuid>[^/]+)/pases_ingreso/(?P<uuid_criterio>[^/]+)/$', views.pase_de_ingreso_add_persona, name='pase-de-ingreso-add-persona'),
	url(r'^pases_ingreso/(?P<uuid>[^/]+)/$', views.pase_de_ingreso_add_files, name='pase-de-ingreso-add-files'),
	# url(r'^puestos/(?P<uuid>[^/]+)/pases_ingreso/(?P<uuid_persona>[^/]+)/$', views.postulacion_convocatoria, name='postulacion-convocatoria'),
	url(r'^puesto/(?P<uuid>[^/]+)/personas/$', views.convocatoria_puesto_personas, name='convocatoria-puesto-personas'),
	url(r'^puesto/postular/$', views.postular_convocatoria_puesto, name='postular-convocatoria-puesto'),
	url(r'^puestos/(?P<uuid>[^/]+)/preseleccion/$', views.pre_seleccion, name='pre-seleccion'),
	url(r'^puestos/(?P<uuid>[^/]+)/add_preseleccion/$', views.add_pre_seleccion, name='add-pre-seleccion'),
	url(r'^puestos/(?P<uuid>[^/]+)/verificacion/$', views.verificacion, name='verificacion'),
	url(r'^puestos/(?P<uuid>[^/]+)/contactabilidad/$', views.contactabilidad, name='contactabilidad'),
	url(r'^puestos/(?P<uuid>[^/]+)/sesion_preseleccion/$', views.sesion_preseleccion, name='sesion_preseleccion'),
	url(r'^puestos/(?P<uuid>[^/]+)/aprobados/$', views.aprobados, name='aprobados'),
	url(r'^puestos/(?P<uuid>[^/]+)/tramite_documentario/$', views.tramite_documentario),
	url(r'^puestos/(?P<uuid>[^/]+)/criterios_busqueda/$', views.CriteriosBusqueda, name='criterios-busqueda'),
	url(r'^puestos/(?P<uuid>[^/]+)/criterios_busqueda_avanzada/$', views.criterios_avanzados),
	url(r'^puestos/(?P<uuid>[^/]+)/add_porcentaje_cumplimiento/$', views.add_porcentaje_cumplimiento),
	url(r'^puestos/(?P<uuid>[^/]+)/add_porcentaje_cumplimiento_criterio/$', views.add_porcentaje_cumplimiento_criterio),
	
	url(r'^estado_postulacion/(?P<pk>[^/]+)/visitado/$', views.postulante_visitado, name='postulante-llamado'),
	url(r'^estado_postulacion/(?P<pk>[^/]+)/verificado/$', views.postulante_verificado, name='confirmar-postulante'),
	url(r'^estado_postulacion/(?P<pk>[^/]+)/llamado/$', views.postulante_llamado, name='postulante-llamado'),
	url(r'^estado_postulacion/(?P<pk>[^/]+)/confirmado/$', views.confirmar_postulante, name='confirmar-postulante'),
	url(r'^estado_postulacion/(?P<pk>[^/]+)/entrevista/$', views.aprobado_entrevista, name='aprobado-entrevista'),
	url(r'^estado_postulacion/(?P<pk>[^/]+)/apto/$', views.aprobado_apto, name='aprobado_apto'),
	url(r'^estado_postulacion/(?P<pk>[^/]+)/observaciones/$', views.add_observaciones_postulacion, name='add-observaciones-postulacion'),
	url(r'^estado_postulacion/(?P<pk>[^/]+)/documentos/$', views.add_documentos_postulacion),

	url(r'^puestos/(?P<uuid>[^/]+)/preseleccionados/(?P<tipo_ingreso>[^/]+)/(?P<orden>[^/]+)/$', views.list_preseleccionados, name='list_preseleccionados'),
	url(r'^puestos/(?P<uuid>[^/]+)/aprobar_preseleccion/$', views.aprobar_pre_seleccion, name='aprobar-pre-seleccion'),
	url(r'^puestos/(?P<uuid>[^/]+)/contratar_aprobados/$', views.contratar_aprobados),
	# CRITERIOS AVANZADOS
	url(r'^add_plantilla_criterio_avanzado/$', views.add_plantilla_criterio_avanzado),
	url(r'^plantilla/(?P<uuid>[^/]+)/add_criterio/$', views.add_criterio_to_plantilla),
	url(r'^puestos/(?P<uuid>[^/]+)/add_extras_criterio_avanzado/$', views.add_extras_criterio_avanzado),

	url(r'^(?P<uuid>[^/]+)/autorizar/$', views.autorizar_convocatoria, name='autorizar-convocatoria'),
	url(r'^(?P<uuid>[^/]+)/iniciar/$', views.iniciar_convocatoria, name='iniciar-convocatoria'),
	url(r'^puestos/(?P<uuid>[^/]+)/preseleccion_manual/$', views.pre_seleccion_manual, name='pre-seleccion-manual'),
	url(r'^preseleccion/add_tags/$', views.add_pre_seleccion_tags, name='add-pre-seleccion-tags'),

	url(r'^search/$', views.search_name_puesto),	
	# PDFS
	url(r'^(?P<uuid>[^/]+)/pdf/$', views.PdfConvocatorias),	
	url(r'^puestos/(?P<uuid>[^/]+)/pdf/preseleccionados/$', views.PdfPreseleccionados),	
	url(r'^puestos/(?P<uuid>[^/]+)/pdf/seleccionados/$', views.PdfSeleccionados),	
	url(r'^puesto/(?P<uuid>[^/]+)/pdf/verificacion_domiciliaria/$', views.PdfVerificacionDomiciliaria),	
	url(r'^puesto/(?P<uuid>[^/]+)/pdf/pases_de_ingreso/$', views.PdfPasesDeIngreso),	
	# DOCUMENTOS
	url(r'^puesto/(?P<uuid>[^/]+)/documentos/add/$', views.add_documentos_convocatoria_puesto, name='add-documento-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/documentos/delete/(?P<pk_documento>[^/]+)/$', views.delete_documentos_convocatoria_puesto, name='delete-documento-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/documentos/edit/(?P<pk_documento>[^/]+)/$', views.edit_documentos_convocatoria_puesto, name='edit-documento-convocatoria-puesto'),
	# REQUISITOS
	url(r'^puesto/(?P<uuid>[^/]+)/requisito/add/$', views.add_requisitos_convocatoria_puesto, name='add-requisito-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/requisito/delete/(?P<uuid_requisito>[^/]+)/$', views.delete_requisitos_convocatoria_puesto, name='delete-requisito-convocatoria-puesto'),
	url(r'^puesto/(?P<uuid>[^/]+)/requisito/edit/(?P<uuid_requisito>[^/]+)/$', views.edit_requisitos_convocatoria_puesto, name='edit-requisito-convocatoria-puesto'),
]