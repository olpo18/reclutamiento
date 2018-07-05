$(function(){
	startPicker = new Pikaday({
		field: document.getElementById('fecha_inicio')
	})
	var endPicker = new Pikaday({
		field: document.getElementById('fecha_fin')
	})
	startPicker2 = new Pikaday({
		field: document.getElementById('fecha_inicio_two')
	})
	var endPicker2 = new Pikaday({
		field: document.getElementById('fecha_fin_two')
	})
	// $form__academico = $('#form-academico');
	// $form__experiencia = $('#form-experiencia');
	// $form__cursos = $('#form-cursos');
	// $form__documentos = $('#form-documentos');
	$form__iniciar__convocatoria = $('#form-iniciar-convocatoria');
	// FECHAS
	$('#fecha_inicio').on('change', function(){
		endPicker.setMinDate(new Date($(this).val()+' 05:00:00'));
	})
	// SUBMIT FORM ACADEMICO
	// $form__academico.on('submit', function(evt){
	// 	evt.preventDefault();
	// 	insert_ajax($form__academico.attr('data-url'), $form__academico.serialize())
	// 		.done(function( response ) {
	// 			$('#message-form-academico').html('<span class="text-green" >'+ response.message +'</span>');
	// 			$('#list-academico').prepend(makeItem(response.data.estado_grado,response.data.carrera, response.data.grado));
	// 			$form__academico[0].reset();
	// 		})
	// 		.fail(function( jqXHR, response ) {
	// 			$('#message-form-academico').html('<span class="text-red" >'+ jqXHR.responseJSON.message +'</span>');
	// 		}); 
	// });
	// SUBMIT FORM EXPERIENCIA
	// $form__experiencia.on('submit', function(evt){
	// 	evt.preventDefault();
	// 	insert_ajax($form__experiencia.attr('data-url'), $form__experiencia.serialize())
	// 		.done(function( response ) {
	// 			$('#message-form-experiencia').html('<span class="text-green" >'+ response.message +'</span>');
	// 			$('#list-experiencia').prepend(makeItem(response.data.experiencia,response.data.familia_puesto, response.data.especialidad));
	// 			$form__experiencia[0].reset();
	// 		})
	// 		.fail(function( jqXHR, response ) {
	// 			$('#message-form-experiencia').html('<span class="text-red" >'+ jqXHR.responseJSON.message +'</span>');
	// 		}); 
	// });
	// SUBMIT FORM CURSOS
	// $form__cursos.on('submit', function(evt){
	// 	evt.preventDefault();
	// 	insert_ajax($form__cursos.attr('data-url'), $form__cursos.serialize())
	// 		.done(function( response ) {
	// 			$('#message-form-cursos').html('<span class="text-green" >'+ response.message +'</span>');
	// 			var indispensable = response.data.indispensable ? '<label> (indispensable)</label>' : '';
	// 			$('#list-cursos').prepend(makeItem(response.data.tipo+' '+response.data.nombre+indispensable,response.data.descripcion,''));
	// 			$form__cursos[0].reset();
	// 		})
	// 		.fail(function( jqXHR, response ) {
	// 			$('#message-form-cursos').html('<span class="text-red" >'+ jqXHR.responseJSON.message +'</span>');
	// 		}); 
	// });
	// SUBMIT FORM DOCUMENTOS
	// $form__documentos.on('submit', function(evt){
	// 	evt.preventDefault();
	// 	insert_ajax($form__documentos.attr('data-url'), $form__documentos.serialize())
	// 		.done(function( response ) {
	// 			$('#message-form-documentos').html('<span class="text-green" >'+ response.message +'</span>');
	// 			var indispensable = response.data.indispensable ? '<label>Indispensable: </label> SI ' : '<label>Indispensable: </label> NO ';
	// 			$('#list-documentos').prepend(makeItem(response.data.detalle_documento,indispensable, ''));
	// 			$form__documentos[0].reset();
	// 		})
	// 		.fail(function( jqXHR, response ) {
	// 			$('#message-form-documentos').html('<span class="text-red" >'+ jqXHR.responseJSON.message +'</span>');
	// 		}); 
	// });
	// SUBMIT FORM INICIAR CONVOCATORIA
	$form__iniciar__convocatoria.on('submit', function(evt){
		evt.preventDefault();
		var uuid_convocatoria_iniciar = $('#uuid-convocatoria-iniciar').val();
		insert_ajax('/convocatorias/'+uuid_convocatoria_iniciar+'/iniciar/', $form__iniciar__convocatoria.serialize())
			.done(function( response ) {
				$('#message-form-iniciar').html('<span class="text-green" >'+ response.message +'</span>');
				$form__iniciar__convocatoria[0].reset();
				$('#'+uuid_convocatoria_iniciar).parent().html('<label>Estado:</label><span class="text-green" >EN PROCESO</span>');
				$('#basic_modal').modal('hide');
			})
			.fail(function( jqXHR, response ) {
				$('#message-form-iniciar').html('<span class="text-red" >'+ jqXHR.responseJSON.message +'</span>');
			}); 
	});
	// FUNCTION SAVE OBJ
	function insert_ajax(url, data){
		return $.ajax({ method: "POST", url: url, data: data })
	}
	// FUNCITON MAKE ITEM
	function makeItem(paramOne, paramTwo, paramThree){
		return '<li class="list-group-item ">\
					<span class="pull-left"><span class="img-circle max-w-40 m-r-10 " ><i class="zmdi zmdi-assignment"></i></span></span>\
					<div class="list-group-item-body">\
						<div class="list-group-item-heading">'+paramOne+'</div>\
						<p>'+paramTwo+' '+paramThree+'</p>\
					</div>\
				</li>';
	}
	// PASES DE INGRESO
	$('.btn_pase_de_ingreso_add_persona').on('click', function(evt){
		evt.preventDefault();
		$('#criterios_aprobacion_step_find_persona').hide(1000);
		$('#criterios_aprobacion_step_add_persona').show();
	})
	$('.cancelar_pase_de_ingreso_add_persona').on('click', function(){
		$('#criterios_aprobacion_step_add_persona').hide(1000);
		$('#criterios_aprobacion_step_find_persona').show();
	})
	// CONVOCATORIAS
	// "AUTOCOMPLETE" puesto
	var ajaxReq = 'ToCancelPrevReq';
	$('#autocomplete_puesto').focus(function(){
		$('#result__autocomplete').show(500);
	})
	$('#autocomplete_puesto').keyup(function() {
		$this_input = $(this);
		var val_split = $this_input.val().split(" ");
		if (val_split.length > 1 && val_split[1] != ""){
			$('#result__autocomplete').html('<div class="col-sm-12"><span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i> Buscando ...</span></div>');
			ajaxReq = $.ajax({ 
				method: "GET", 
				url: '/convocatorias/search/?text='+$this_input.val(), 
				beforeSend: function(xhr) {
					xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
					if(ajaxReq != 'ToCancelPrevReq' && ajaxReq.readyState < 4) {
						ajaxReq.abort();
						$('#result__autocomplete').html('');
					}
				}})
				.done(function( response ) {
					$('#result__autocomplete').html('');
					if (response.sub_especialidades.length > 0){
						items = '';
						for (var i=0; i < response.sub_especialidades.length; i++){
							var diccionario = { 'rango':response.rango, 'subespecialidad': response.sub_especialidades[i], 'especialidad': response.sub_especialidades[i].especialidad , 'familia_puesto': response.sub_especialidades[i].especialidad.familia_puesto };
							items += "<div class='col-sm-12 border-bottom' ><a href='#' data-item='"+JSON.stringify(diccionario)+"' class='link__autocomplete btn-info btn-flat m-0 p-0 item__autocomplete' >"+response.rango.descripcion+" "+response.sub_especialidades[i].descripcion+" "+response.sub_especialidades[i].especialidad.descripcion+" "+response.sub_especialidades[i].especialidad.familia_puesto.descripcion+"</a></div>";
						}
						$('#result__autocomplete').append(items);
					} 
					if (response.especialidades.length > 0){
						items_especialidades = '';
						for (var i=0; i < response.especialidades.length; i++){
							var diccionario = { 'rango':response.rango, 'especialidad': response.especialidades[i] , 'familia_puesto': response.especialidades[i].familia_puesto };
							items_especialidades += "<div class='col-sm-12 border-bottom' ><a href='#' data-item='"+JSON.stringify(diccionario)+"' class='link__autocomplete btn-info btn-flat m-0 p-0 item__autocomplete' >"+response.rango.descripcion+" "+response.especialidades[i].descripcion+" "+response.especialidades[i].familia_puesto.descripcion+"</a></div>";
						}
						$('#result__autocomplete').append(items_especialidades);
					} 
					if (response.sub_especialidades.length < 0 && response.especialidades.length < 0) {
						$('#result__autocomplete').html('<div class="col-sm-12 text-warning"><span>No se encontraron resultados.</span></div>');
					}
				})
				.fail(function( jqXHR, response ) {
					console.log(response);	
				}); 
		} else {
			$('#result__autocomplete').html('');
		}
	});
	$('body').on('click', '.item__autocomplete', function(evt){
		evt.preventDefault();
		$('#result__autocomplete').hide(500);
		var item = JSON.parse($(this).attr('data-item'));
		$('#id_rango').val(item.rango.uuid);
		$('#id_familia_puesto').val(item.familia_puesto.uuid);
		item.especialidad ? $('#id_especialidad').append('<option selected="selected" value="'+item.especialidad.uuid+'">'+item.especialidad.descripcion+'</option>') : '';
		item.subespecialidad ? $('#id_sub_especialidad').append('<option selected="selected" value="'+item.subespecialidad.uuid+'">'+item.subespecialidad.descripcion+'</option>') : $('#id_sub_especialidad').append('<option selected="selected" value=""></option>');
		
	})
	// autorizar
	$('.autorizar_convocatoria').on('click', function(){
		var $this_btn = $(this);
		$this_btn.attr('disabled', true);
		$this_btn.text('Autorizando...');
		$this_btn.prepend('<span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i></span>');
		
		$.ajax({
			method: 'GET',
			url: '/convocatorias/'+$this_btn.attr('data-uuid')+'/autorizar/'
		}).done(function( response ) {
			console.log('Respuesta de autorizacion.');
			$this_btn.parent().append('<button class="btn btn-primary btn-round iniciar_convocatoria" data-toggle="modal" data-uuid="'+$this_btn.attr('data-uuid')+'" data-target="#basic_modal">Iniciar</button><span class="'+response.class+' m-l-10" >'+response.message+'</span>');
			$this_btn.parent().prev().find('.dropdown-menu .disabled').each(function(index, elem){
				$(elem).attr('class','');
			})
			$this_btn.remove();

		}).fail(function( response ) {
			$this_btn.parent().prepend('<span class="'+response.responseJSON.class+'" >'+response.responseJSON.message+'</span>');
			enable_btn($this_btn, 'autorizar');
		});
	})
	// enable button
	function enable_btn(btn, text){
		btn.attr('disabled', false);
		btn.text(text);
		btn.prepend('');
	}
	// iniciar convocatoria
	$('body').on('click', '.iniciar_convocatoria',function(){
		$('#uuid-convocatoria-iniciar').val($(this).attr('data-uuid'));
	})
	// get codigo contratista to convocatoria
	$('#id_contratista').change(function(){
		var uuid = $(this).val();
		$.ajax({
			method: 'GET',
			url: '/convocatorias/'+uuid+'/codigo/'
		}).done(function( response ) {
			$('#id_codigo').val(response.codigo);
		}).fail(function(response) {
			console.log(response);
		});
	})
	// TABLES
	var $table_personas;
	var $table_bd;
	$table_personas = $('#table-pre-seleccion-personas').DataTable();
	$table_bd = $('#table-pre-seleccion-bd').DataTable();
	// DATA ROWS CHECK
	function data_checkbox_checked(){
		var data = [];
		$table_personas.$(".checkbox input[type=checkbox]:checked").each(function(index,elem){
			data.push({'persona':$(elem).attr('data-persona'), 'rango':$(elem).attr('data-rango'),'tipo':'postulante'});
		});
		$table_bd.$(".checkbox input[type=checkbox]:checked").each(function(index,elem){
			data.push({'persona':$(elem).attr('data-persona'), 'rango':$(elem).attr('data-rango'),'tipo':'BD'});
		});
		return data;
	}
	// SELECT EJECUTAR
	$('#button__ejecutar').on('click', function(){
		var data = data_checkbox_checked();
		if (data.length > 0){
			$this_btn = $(this);
			var uuid_convocatoria_puesto = $this_btn.attr('data-convocatoria');
			$this_btn.attr('disabled', true);
			$this_btn.text('Preseleccionando...');
			$this_btn.prepend('<span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i></span>');
			if($('#select__ejecutar').val()=='preseleccionar'){
					$.ajax({ 
						method: "POST", 
						url: '/convocatorias/puestos/'+uuid_convocatoria_puesto+'/add_preseleccion/', 
						data: JSON.stringify(data), 
						datType: 'json', 
						contentType:"application/json",
						contentType:"application/json", 
						beforeSend: function(xhr) {
							xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
						}})
						.done(function( response ) {
							var total = response.vacantes-response.preseleccionados;
							$('#message__ejecutar').html('<span class="text-green" >'+response.message+' Quedan: '+total+' vacantes</span>');
							$this_btn.attr('disabled', false);
							$this_btn.html('');
							$this_btn.text('EJECUTAR');
							for (var i = 0; i < data.length; i++) {
								data[i].tipo == 'postulante' ? $table_personas.row('#'+data[i].persona).remove().draw( false ): $table_bd.row('#'+data[i].persona).remove().draw( false ) ;
							}
						})
						.fail(function( jqXHR, response ) {
							console.log(response);	
							$this_btn.attr('disabled', false);
							$this_btn.html('');
							$this_btn.text('EJECUTAR');
						});
			} else {
				$('#modal__add_tags').modal('show');
			}
		} else {
			$('#message__ejecutar').html('<span class="text-red" >No hay personas seleccionadas.</span>');
		}
	});
	// APROBAR SELECCION
	$('#aprobar_preseleccionados').on('click', function(){
		var data = [];
		var uuid_convocatoria_puesto = $(this).attr('data-convocatoria');
		$(".checkbox-aprobar input[type=checkbox]:checked").each(function(index,elem){
			data.push({'postulacion':$(elem).attr('data-id')});
		});
		aprobar_seleccionados({'tipo':'individual', 'datos': data}, uuid_convocatoria_puesto)
			.done(function( response ) {
				var total = response.vacantes-response.aprobados;
				$('#message__aprobar').html('<span class="text-green" >'+response.message+' Quedan: '+total+' vacantes</span>');
				for (var i=0; i<data.length; i++){
					$('#'+data[i].postulacion).hide(500);
				}
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			}); 
	});
	$('.aprobar_rango').on('click', function(){
		var uuid_convocatoria_puesto = $(this).attr('data-convocatoria');
		var tipo_ingreso = $(this).attr('data-tipo');
		var rangos = [];
		var $this_btn = $(this);
		$(this).parent().prev().find(".checkbox input[type=checkbox]:checked").each(function(index,elem){
			rangos.push($(elem).attr('data-rango'));
		});
		var diccionario = {'tipo':'rangos','tipo_ingreso':tipo_ingreso,'rangos':rangos}
		aprobar_seleccionados(diccionario, uuid_convocatoria_puesto)
			.done(function( response ) {
				var total = response.vacantes-response.aprobados;
				$('#message__aprobar_rangos').html('<span class="text-green" >'+response.message+' Quedan: '+total+' vacantes</span>');
				$this_btn.parent().siblings().hide(500);
				$this_btn.parent().hide(500);
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			}); 
	})
	function aprobar_seleccionados(data, uuid_convocatoria_puesto){
		return $.ajax({ 
			method: "POST", 
			url: '/convocatorias/puestos/'+uuid_convocatoria_puesto+'/aprobar_preseleccion/', 
			data: JSON.stringify(data), 
			datType: 'json', 
			contentType:"application/json",
			contentType:"application/json", 
			beforeSend: function(xhr) {
				xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
			}})
	}
	// VIEW DETAIL PERSON
	var uuid__persona = '';
	$('body').on('click', '.btn-view-detail', function(){
		var btn_uuid = $(this).attr('data-persona');
		if ($(this).attr('data-persona') != uuid__persona){
			$('#modal-body').html('<span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i> Cargando...</span>');
			$.ajax({ method: "GET", url: '/personas/api/'+btn_uuid+'/info_laboral/'})
			.done(function( data ) {
				var template_html = '<h2><strong>Datos Personales</strong></h2>\
						<div class="row">\
							<div class="col-sm-12"><label>Nombres: </label> '+data.persona.nombres+'</div>\
							<div class="col-sm-12"><label>Apellidos: </label> '+data.persona.apellidos+'</div>\
							<div class="col-sm-12"><label>Nº Documento: </label> '+data.persona.numero_documento+'</div>\
							<div class="col-sm-12"><label>Email: </label> '+data.persona.email+'</div>\
							<div class="col-sm-12"><label>Celular: </label> '+data.persona.celular+'</div>\
							<div class="col-sm-6"><label>Genero: </label> '+data.persona.genero+'</div>\
							<div class="col-sm-6"><label>Estado Civil: </label> '+data.persona.estado_civil+'</div>\
						</div>'
				var items = '';
				var data_laboral = data.laboral;
				for (var i = 0; i < data_laboral.length; i++){
					items += '<div class="list-group-item">\
								<div class="row-action-primary">\
									<i class="zmdi zmdi-folder circle mw-blue"></i>\
								</div>\
								<div class="row-content">\
									<p class="list-group-item-text"><label>Empresa: </label> '+data_laboral[i].empresa+'</p>\
									<p class="list-group-item-text"><label>Rango: </label> '+data_laboral[i].rango+'</p>\
									<p class="list-group-item-text"><label>Familia Puesto: </label> '+data_laboral[i].familia_puesto+'</p>\
									<p class="list-group-item-text"><label>Especialidad: </label> '+data_laboral[i].especialidad+'</p>\
									<p class="list-group-item-text"><label>Tiempo: </label> '+data_laboral[i].fecha_inicio+'</p>\
								</div>\
							</div>';
				}
				var template_body = '<h2><strong>Experiencia</strong></h2><div class="list-group m-t-40">'+items+'</div>';
				var items_educativo = '';
				var data_educativo = data.educativo;
				for (var i = 0; i < data_educativo.length; i++){
					items_educativo += '<div class="list-group-item">\
								<div class="row-action-primary">\
									<i class="zmdi zmdi-folder circle mw-blue"></i>\
								</div>\
								<div class="row-content">\
									<p class="list-group-item-text"><label>Centro de estudios: </label> '+data_educativo[i].centro_estudio+'</p>\
									<p class="list-group-item-text"><label>Familia Carrera: </label> '+data_educativo[i].familia_carrera+'</p>\
									<p class="list-group-item-text"><label>Carrera: </label> '+data_educativo[i].carrera+'</p>\
									<p class="list-group-item-text"><label>Tiempo: </label> '+data_educativo[i].fecha_inicio+'</p>\
								</div>\
							</div>';
				}
				var template_body_educativo = '<h2><strong>Educativo</strong></h2><div class="list-group m-t-40">'+items_educativo+'</div>';
				$('#modal-body').html(template_html+template_body+template_body_educativo);
				uuid__persona = btn_uuid;
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			}); 
		}
	})
	// ADD DATA
	function add_data(url, data){
		return $.ajax({ method: "POST", url: url, data: data, datType: 'json', contentType:"application/json", beforeSend: function(xhr) {xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))}})
	}
	// MODAL ADD TAGS
	$('#add_tags').on('click', function(){
		var tags = [];
		$('.chip').each(function(index, elem){
			tags.push($(elem).text());
			$(elem).remove()
		})
		var data = data_checkbox_checked($(this).attr('data-convocatoria'));
		console.log(data);
		add_data('/convocatorias/preseleccion/add_tags/', JSON.stringify({'tags':tags, 'data': data}))
			.done(function( response ) {
				$('#message__ejecutar').text(response.message);
				$('#modal__add_tags').modal('hide');
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			}); 
	})
	// MODAL ADD REQUISITOS
	$('#form-add-requisito').on('submit', function(evt){
		evt.preventDefault();
		var convocatoria_puesto = $(this).attr('data-convocatoria');
		add_data('/convocatorias/puestos/'+convocatoria_puesto+'/requisitos/', JSON.stringify({'descripcion':$('#descripcion_requisito').val(), 'convocatoria_puesto': convocatoria_puesto}))
			.done(function( response ) {
				console.log(response);
				$('#requisitos').prepend('<div class="row m-t-10"><div class="col-sm-1 text-right"><i class="zmdi zmdi-check"></i></div><div class="col-sm-11"><p>'+$('#descripcion_requisito').val()+'</p></div></div>');
				$('#descripcion_requisito').val('');
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			}); 
	})
	// CRITERIOS DE BUSQUEDA
	function total_percent(clase){
		var total = 0;
		$('.'+clase).each(function(index, elem){
			total += parseInt($(elem).val()) > 0 ? parseInt($(elem).val()) : 0;
		})
		$('#total_cumplimiento_normal').html('<strong>'+String(total)+'</strong>');
		return total;
	}
	function total_percent_valid(){
		var total = total_percent('porcentaje_cumplimiento');
		return !(total > 100);
	}
	$('body').on('change','.porcentaje_cumplimiento', function(){
		$this_box = $(this);
		if( total_percent_valid()){
			add_data('/convocatorias/puestos/'+$this_box.attr('data-puesto')+'/add_porcentaje_cumplimiento/', JSON.stringify({'tipo':$this_box.attr('data-tipo'), 'pk': $this_box.attr('data-id'), 'porcentaje': $this_box.val()}))
				.done(function( response ) {
					clean_messages('message_porcentaje_cumplimiento');
					$this_box.parent().parent().next().find('.message_porcentaje_cumplimiento').html('<span class="text-success" >agregado con éxito</span>');
				})
				.fail(function( jqXHR, response ) {
					clean_messages('message_porcentaje_cumplimiento');
					$this_box.parent().parent().next().find('.message_porcentaje_cumplimiento').html('<span class="text-danger" >'+jqXHR.responseJSON.message+'</span>');	
				}); 
		} else {
			clean_messages('message_porcentaje_cumplimiento');
			$this_box.parent().parent().next().find('.message_porcentaje_cumplimiento').html('<span class="text-danger" >Excediste el 100%</span>');
		}
		
	})
	// CUMPLIMIENTO CRITERIO
	function clean_messages(clase){
		$('.'+clase).each(function(index, elem){
			$(elem).html('');
		});
	}
	$('body').on('change','.porcentaje_cumplimiento_criterio', function(){
		$this_box = $(this);
		console.log('LoG ==> ', $this_box.attr('data-id'), parseInt($this_box.val()))
		if(parseInt($this_box.val()) <= 100){
		add_data('/convocatorias/puestos/'+$this_box.attr('data-puesto')+'/add_porcentaje_cumplimiento_criterio/', JSON.stringify({'tipo':$this_box.attr('data-tipo'), 'pk': $this_box.attr('data-id'), 'porcentaje': $this_box.val()}))
			.done(function( response ) {
				clean_messages('message_porcentaje_cumplimiento_criterio');
				$this_box.parent().parent().next().find('.message_porcentaje_cumplimiento_criterio').html('<span class="text-success" >agregado con éxito</span>');
			})
			.fail(function( jqXHR, response ) {
				clean_messages('message_porcentaje_cumplimiento_criterio');
				$this_box.parent().parent().next().find('.message_porcentaje_cumplimiento_criterio').html('<span class="text-danger" >'+jqXHR.responseJSON.message+'</span>');	
			}); 
		} else {
			clean_messages('message_porcentaje_cumplimiento_criterio');
			$this_box.parent().parent().next().find('.message_porcentaje_cumplimiento_criterio').html('<span class="text-danger" >Excediste el 100%</span>');
		}
		
	})
	$('#btn_siguiente_cumplimiento_normal').on('click', function(){
		var total = total_percent('porcentaje_cumplimiento');
		if (total < 100){
			$('#message_siguiente_cumplimiento_normal').html('<span class="text-red" >Aún no llegas al 100% obligatorio.</span>');
		} else {
			window.location.replace($(this).attr('data-url'))
		}
	})
	// HEADER CRITERIOS AVANZADOS
	// -- agregar criterio avanzado
	$('#btn_add_plantilla').on('click', function(){
		if($('#name_new_plantilla').val() != ''){
			criterios = [];
			$('.porcentaje_cumplimiento_criterio').each(function(index, elem){
				($(elem).attr('data-id') != '' && $(elem).attr('data-tipo') != '') ? criterios.push({'pk':$(elem).attr('data-id'), 'tipo':$(elem).attr('data-tipo')}) : '';
			})
			add_data('/convocatorias/add_plantilla_criterio_avanzado/', JSON.stringify({'criterios':criterios,'descripcion':$('#name_new_plantilla').val()}))
				.done(function( response ) {
					$('#name_new_plantilla').attr('data-uuid', response.uuid);
					$('#message_name_plantilla').html('<span class="text-'+response.class+'" >'+response.message+'</span>')
				})
				.fail(function( jqXHR, response ) {
					$('#message_name_plantilla').html('<span class="text-'+jqXHR.responseJSON.class+'" >'+jqXHR.responseJSON.message+'</span>')
				}); 
		} else {
			$('#message_name_plantilla').html('<span class="text-red" >Ingresa un nombre</span>')
		}
	})
	function makeItemCriterio(title, porcentaje, puesto, pk){
		return '<div class="row">\
						<div class="col-sm-8 border-bottom">\
							<h5 class="m-t-10" >'+title+'</h5>\
						</div>\
						<div class="col-sm-4">\
							<div class="col-sm-6">\
								<div class="form-group m-0 p-0">\
									<input type="number" value="'+porcentaje+'" min="0" max="100" class="form-control text-center porcentaje_cumplimiento_criterio" data-puesto="'+puesto+'" data-id="'+pk+'" data-tipo="academico" placeholder="% de cumplimiento">\
								</div>\
							</div>\
							<div class="col-sm-6 m-t-10">\
								<div class="message_porcentaje_cumplimiento_criterio"></div>\
							</div>\
						</div>\
					</div>'
	}
	// ADD CRITERIO TO PLANTILLA
	function add_criterio_to_plantilla(pk_criterio, tipo){
		var uuid = $('#name_new_plantilla').attr('data-uuid');
		if (uuid != '' && uuid != undefined){
			add_data('/convocatorias/plantilla/'+uuid+'/add_criterio/', JSON.stringify({'tipo':tipo,'pk':pk_criterio}))
				.done(function( response ) {
					console.log('done ==> ',response.message)
				})
				.fail(function( jqXHR, response ) {
					console.log('fail ==> ',jqXHR.responseJSON.message)
				}); 
		}
	}
	// SUBMIT FORM ACADEMICO
	$('#form_criterio_academico').on('submit', function(evt){
		evt.preventDefault();
		insert_ajax($('#form_criterio_academico').attr('data-url'), $('#form_criterio_academico').serialize())
			.done(function( response ) {
				$('#message-form-academico-criterio').html('<span class="text-green" >'+ response.message +'</span>');
				$('#list-academico-criterio').prepend(makeItemCriterio(response.data.title, response.data.porcentaje, response.data.puesto, response.data.pk));
				$('#form_criterio_academico')[0].reset();
				add_criterio_to_plantilla(response.data.pk, 'academico');
			})
			.fail(function( jqXHR, response ) {
				$('#message-form-academico-criterio').html('<span class="text-red" >'+ jqXHR.responseJSON.message +'</span>');
			}); 
	});
	// SUBMIT FORM EXPERIENCIA
	$('#form_criterio_experiencia').on('submit', function(evt){
		evt.preventDefault();
		insert_ajax($('#form_criterio_experiencia').attr('data-url'), $('#form_criterio_experiencia').serialize())
			.done(function( response ) {
				$('#message-form-experiencia-criterio').html('<span class="text-green" >'+ response.message +'</span>');
				$('#list-experiencia-criterio').prepend(makeItemCriterio(response.data.title, response.data.porcentaje, response.data.puesto, response.data.pk));
				$('#form_criterio_experiencia')[0].reset();
				add_criterio_to_plantilla(response.data.pk, 'experiencia');
			})
			.fail(function( jqXHR, response ) {
				$('#message-form-experiencia-criterio').html('<span class="text-red" >'+ jqXHR.responseJSON.message +'</span>');
			}); 
	});
	// SUBMIT FORM CURSOS
	$('#form_criterio_cursos').on('submit', function(evt){
		evt.preventDefault();
		insert_ajax($('#form_criterio_cursos').attr('data-url'), $('#form_criterio_cursos').serialize())
			.done(function( response ) {
				$('#message-form-cursos-criterio').html('<span class="text-green" >'+ response.message +'</span>');
				$('#list-cursos-criterio').prepend(makeItemCriterio(response.data.title, response.data.porcentaje, response.data.puesto, response.data.pk));
				$('#form_criterio_cursos')[0].reset();
				add_criterio_to_plantilla(response.data.pk, 'cursos');
			})
			.fail(function( jqXHR, response ) {
				$('#message-form-cursos-criterio').html('<span class="text-red" >'+ jqXHR.responseJSON.message +'</span>');
			}); 
	});

	// FIN CRITERIOS DE BUSQUEDA
	// ALERTIFY
	$('body').on('click', '.delete-convocatoria-puesto-academico', function(evt){
		evt.stopPropagation();
		var $this_btn = $(this);
		alertify.confirm('Estas seguro de eliminar el registro ?', function(){ 
			delete_object('/convocatorias/puestos/delete/academico/'+$this_btn.attr('data-id')+'/')
			.done(function( response ) {
				console.log(response);
				$this_btn.parent().parent().remove();
				alertify.success(response.message);
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			}); 
		}, function(){ 
			alertify.error('Cancel')
		});
	});
	// DELETE OBJECT
	function delete_object(url){
		return $.ajax({ 
			method: 'DELETE', 
			url: url, 
			beforeSend: function(xhr) {
				xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
			}
		})
	}
	// GET DATA API
	function get_data(url){
		return $.ajax({ method: "GET", url: url, beforeSend: function(xhr) { xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))}})
	}
	// GET ESPECIALIDADES Y BY FAMILIA
	$('#id_familia_puesto').on('change', function(){
		var uuid = $(this).val();
		get_data('/api/maestros/familias/especialidades/?familia='+uuid)
		.done(function( data ) {
			var options = '<option value="" >---------</option>';
			for (var i=0; i< data.length; i++){
				options += '<option value="'+data[i].uuid+'" >'+data[i].descripcion+'</option>';
			}
			$('#id_especialidad').html(options);
			$('#id_especialidad').change();
		})
		.fail(function( jqXHR, response ) {
			console.log(response);	
		}); 
	})
	// GET SUB ESPECIALIDADES BY ESPECIALIDAD
	$('#id_especialidad').on('change', function(){
		var uuid = $(this).val();
		if (uuid){
			get_data('/api/maestros/especialidades/sub_especialidades/?especialidad='+uuid)
			.done(function( data ) {
				var options = '<option value="" >---------</option>';
				for (var i=0; i< data.length; i++){
					options += '<option value="'+data[i].uuid+'" >'+data[i].descripcion+'</option>';
				}
				$('#id_sub_especialidad').html(options);
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			}); 
		}
	})
	// GET GRADOS Y BY FAMILIA
	$('#id_familia_carrera').on('change', function(){
		var uuid = $(this).val();
		get_data('/api/maestros/familias/carreras/?familia='+uuid)
		.done(function( data ) {
			var options = '<option value="" >---------</option>';
			for (var i=0; i< data.length; i++){
				options += '<option value="'+data[i].uuid+'" >'+data[i].descripcion+'</option>';
			}
			$('#id_carrera').html(options);
		})
		.fail(function( jqXHR, response ) {
			console.log(response);	
		}); 
	})
	// GET DOCUMENTOS Y DETALLE
	$('#id_tipo_documento').on('change', function(){
		var uuid = $(this).val();
		get_data('/api/maestros/documentos/detalle/?tipo='+uuid)
		.done(function( data ) {
			var options = '<option value="" >---------</option>';
			for (var i=0; i< data.length; i++){
				options += '<option value="'+data[i].uuid+'" >'+data[i].descripcion+'</option>';
			}
			$('#id_detalle_documento').html(options);
		})
		.fail(function( jqXHR, response ) {
			console.log(response);	
		}); 
	})
	// DOCUMENTOS FILE
	$('.documento').on('change', function(){
		var file = $(this)[0].files[0];
		if (file){
			$this_input = $(this);
			$this_input.siblings(".message_upload").html('<span class="text-warning" ><i class="zmdi zmdi-refresh zmdi-hc-spin"></i> Subiendo documento...</span>');
			var formData = new FormData();
			var estado = $(this).attr('data-estado');
			var tipo = $(this).attr('data-tipo');
			formData.append('documento', file, file.name);
			formData.append('detalle_documento', tipo);
			$.ajax({ 
				method: 'POST', 
				url: '/convocatorias/estado_postulacion/'+estado+'/documentos/', 
				data: formData,
				contentType: false,
				processData: false,
				beforeSend: function(xhr) {
					xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
				}
			})
			.done(function( response ) {
				$this_input.siblings(".message_upload").html('<span class="text-success" >'+response.message+'</span>');
			})
			.fail(function( jqXHR, response ) {
				console.log(response);
			}); 
		} else {
			console.log('No hay archivo.');
		}

	})
	// GET COOKIE
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

})