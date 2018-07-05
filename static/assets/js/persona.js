$(function(){
	// GRADO
	$('#id_grado').change(function(){
		console.log('change grado');
		if($('#id_grado :selected').text().toLowerCase() == 'primaria' || $('#id_grado :selected').text().toLowerCase() == 'secundaria'){
			$('#familia_carrera').css('display','none');
			$('#id_familia_carrera').removeAttr('required','required');
			$('#carrera').css('display','none');
			$('#id_carrera').removeAttr('required','required');
		} else {
			$('#familia_carrera').css('display','block');
			$('#id_familia_carrera').attr('required','required');
			$('#carrera').css('display','block');
			$('#id_carrera').attr('required','required');
		}
	})
	// discapacidad
	$(":radio[name='discapacitado']").change(function() {
		if(this.value == 'True'){
			$('#tipo_discapacidad').css('display','block');
			$('#id_tipo_discapacidad').attr('required','required');
		} else {
			$('#tipo_discapacidad').css('display','none');
			$('#id_tipo_discapacidad').removeAttr('required','required');
		}
	});
	// empresa
	// $('#id_empresa').change(function(){
	// 	if($('#id_empresa').find("option:selected").text()=="otros"){
	// 		$('#nombre-empresa-otros').css('display','block');
	// 		$('#id_nombre').attr('required','required');
	// 	} else {
	// 		$('#nombre-empresa-otros').css('display','none');
	// 		$('#id_nombre').removeAttr('required','required');
	// 	}
	// })
	// centro de estudios
	// $('#id_centro_estudio').change(function(){
	// 	if($('#id_centro_estudio').find("option:selected").text()=="otros"){
	// 		$('#nombre-centro-otros').css('display','block');
	// 		$('#id_nombre').attr('required','required');
	// 	} else {
	// 		$('#nombre-centro-otros').css('display','none');
	// 		$('#id_nombre').removeAttr('required','required');
	// 	}
	// })
	// SUBMIT FORM DOCUMENTOS
	var $form__documentos_persona = $('#form-documentos-persona');
	$form__documentos_persona.on('submit', function(evt){
		load_btn($('#form-documentos-persona').find(':submit'));
	});
	var $form__add_bloqueado = $('#form-add-bloqueado-file');
	$form__add_bloqueado.on('submit', function(evt){
		load_btn($('#form-add-bloqueado-file').find(':submit'));
	});

	// FORM POST
	$('#form-add-persona').on('submit', function(){
		var btn_submit = $(this).find('button[type="submit"]');
		load_btn(btn_submit);
	})
	// FUNCTION LOAD BTN
	function load_btn(btn){
		btn.attr('disabled', true);
		btn.text('Cargando...');
		btn.prepend('<span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i></span>');
	}
	function enable_btn(btn, text){
		btn.attr('disabled', false);
		btn.text(text);
		btn.prepend('');
	}
	// GET DATA API
	function load_combo(url, combo){
		var uuid = combo.val();
		combo.html('<option value="" >Cargando...</option>');
		return $.ajax({ 
			method: "GET", 
			url: url, 
			beforeSend: function(xhr) { 
						xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))}
			}).done(function( data ) {
				var options = '<option value="" >---------</option>';
				for (var i=0; i< data.length; i++){
					options += '<option value="'+data[i].uuid+'" >'+data[i].descripcion+'</option>';
				}
				combo.html(options);
				if (uuid != ''){
					combo.val(uuid);
					combo.change();
				}
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			}); 
	}
	// COMBOS DEPARTAMENTOS, PROVINCIAS
	$('#id_departamento_nacimiento').on('change', function(){
		$('#id_provincia_nacimiento').val('');
		$('#id_provincia_nacimiento').change();
	})
	$('#id_provincia_nacimiento').on('change', function(){
		$('#id_distrito_nacimiento').val('');
		$('#id_distrito_nacimiento').change();
	})
	$('#id_departamento_residencia').on('change', function(){
		$('#id_provincia_residencia').val('');
		$('#id_provincia_residencia').change();
	})
	$('#id_provincia_residencia').on('change', function(){
		$('#id_distrito_residencia').val('');
		$('#id_distrito_residencia').change();
	})
	// FUNCTION SAVE OBJ
	function insert_ajax(url, formSerialize){
		return $.ajax({ method: "POST", url: url, data: formSerialize })
	}
	// POSTULAR CONVOCATORIA
	$('.postular_convocatoria').on('click', function(){
		var $this_btn = $(this);
		$this_btn.attr('disabled', true);
		$this_btn.text('Postulando...');
		$this_btn.prepend('<span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i></span>');
		
		$.ajax({
			method: 'GET',
			url: '/convocatorias/puestos/'+$this_btn.attr('data-convocatoria')+'/postular/'+$this_btn.attr('data-postulante')
		}).done(function( response ) {
			console.log('Respuesta de autorizacion.');
			$this_btn.parent().prepend('<button class="btn btn-danger btn-round excluir_convocatoria" data-postulante="'+$this_btn.attr('data-postulante')+'" data-convocatoria="'+$this_btn.attr('data-convocatoria')+'" >excluir convocatoria</button>');
			$this_btn.remove();

		}).fail(function( jqXHR, response ) {
			$this_btn.parent().prepend('<span class="'+jqXHR.responseJSON.class+'" >'+jqXHR.responseJSON.message+'</span>');
			enable_btn($this_btn,'postular');
		});

		// ajax_api('POST' ,'/convocatorias/puesto/postular/', {'convocatoria_puesto':$this_btn.attr('data-convocatoria'), 'persona': $this_btn.attr('data-postulante')})
		// .done(function(response){
		// 	console.log('DONE ===> ', response);
		// })
		// .fail(function(response){
		// 	console.log('FAIL ====> ', response);
		// })

	})
	// FIND PERSONAS
	$('#button__find__persona').on('click', function(){
		var uuid_convocatoria_puesto = $(this).attr('data-puesto');
		$('#registros').html('<span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i> Cargando...</span>');
		$.ajax({ 
			method: "GET", 
			url: '/personas/find_persona/', 
			data: {
				'convocatoria_puesto': uuid_convocatoria_puesto,
				'numero_documento': $('#numero_documento').val()
			} 
		})
		.done(function( response ) {
			length = response.data.length;
			registros = '';
			for (var i=0; i < length; i++){
				lugar = response.data[i].lugar == 'talara' ? '<i class="zmdi zmdi-star text-yellow"></i><p>TALAREÑO</p>' : '';
				var nueva_direccion = response.data[i].direccion != null ? response.data[i].direccion.toString().replace(/"/g , "'") : '';
				response.data[i].direccion = nueva_direccion;
				registros += "<div class='registro border-bottom col-sm-12'>\
					<div class='col-sm-1'>\
						<img src='https://s3.amazonaws.com/limagas/dashboard/user.jpg' alt=' class='img-thumbnail' />\
					</div>\
					<div class='col-sm-1'>"+lugar+"</div>\
					<div class='col-sm-1'>"+response.data[i].rango.descripcion+"("+response.data[i].porcentaje+")</div>\
					<div class='col-sm-2'>"+response.data[i].nombres_apellidos+"</div>\
					<div class='col-sm-1'>"+response.data[i].numero_documento+"</div>\
					<div class='col-sm-2'>"+response.data[i].direccion+"</div>\
					<div class='col-sm-2'><button class='btn btn-round btn-success add_persona' data-convocatoria='"+uuid_convocatoria_puesto+"' data-persona='"+JSON.stringify(response.data[i])+"' >agregar</button></div>\
					<div class='col-sm-1'><button type='button' class='btn btn-info btn-sm btn-round btn-view-detail' data-persona='"+response.data[i].uuid+"' data-toggle='modal' data-target='#modal__view_detail' >\
							<span data-toggle='tooltip' data-placement='top' title='ver detalle' ><i class='zmdi zmdi-eye'></i></span>\
						</button></div>\
				</div>";
			}
			$('#registros').html(registros)

		}).fail(function( jqXHR, response ) {
			console.log(response);
		});
	})
	// POSTULANTE VISITADO
	$('.postulante_verificado').on('change', function(){
		$this_check = $(this);
		ajax_api('POST','/convocatorias/estado_postulacion/'+$this_check.attr('data-id')+'/verificado/', {'verificado':String($this_check.is(':checked'))})
	})
	// POSTULANTE VISITADO
	$('.postulante_visitado').on('change', function(){
		$this_check = $(this);
		ajax_api('POST','/convocatorias/estado_postulacion/'+$this_check.attr('data-id')+'/visitado/', {'visitado':String($this_check.is(':checked'))});
	})
	// POSTULANTES LLAMADO
	$('.postulante_llamado').on('change', function(){
		$this_check = $(this);
		ajax_api('POST','/convocatorias/estado_postulacion/'+$this_check.attr('data-id')+'/llamado/', {'llamado':String($this_check.is(':checked'))})
	})
	// QUIERO PARTICIPAR
	$('.quiero_participar').on('change', function(){
		$this_check = $(this);
		ajax_api('POST','/convocatorias/estado_postulacion/'+$this_check.attr('data-id')+'/confirmado/', {'confirmado':String($this_check.is(':checked'))})
	})
	// APROBADO ENTREVISTA
	$('.aprobado_entrevista').on('change', function(){
		$this_check = $(this);
		ajax_api('POST','/convocatorias/estado_postulacion/'+$this_check.attr('data-id')+'/entrevista/', {'entrevista':String($this_check.is(':checked'))})
	})
	// APROBADO APTO
	$('.aprobado_apto').on('change', function(){
		$this_check = $(this);
		ajax_api('POST','/convocatorias/estado_postulacion/'+$this_check.attr('data-id')+'/apto/', {'apto':String($this_check.is(':checked'))})
	})
	function ajax_api(method ,url, data){
		return $.ajax({ 
			method: method, 
			url: url, 
			data: JSON.stringify(data), 
			datType: 'json', contentType:"application/json", 
			beforeSend: function(xhr) {
				xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
		}})
	}
	// TABle
	var $table_seleccion_manual = $('#table-pre-seleccion-manual').DataTable();
	$('body').on('click', '.add_persona', function(){
		var data_persona = JSON.parse($(this).attr('data-persona'));
		var lugar = data_persona.lugar == 'talara' ? '<i class="zmdi zmdi-star text-yellow"></i><p>TALAREÑO</p>' : '';
		$(this).remove();
		$table_seleccion_manual.row.add( [
            '<div class="check" ><input type="checkbox" data-persona="'+data_persona.uuid+'" data-rango="'+data_persona.rango.uuid+'" checked></div>',
            '<img src="https://s3.amazonaws.com/limagas/dashboard/user.jpg" alt="" class="img-thumbnail" />',
            lugar,
            data_persona.nombres_apellidos,
            data_persona.rango.descripcion,
            data_persona.celular,
            data_persona.numero_documento,
            data_persona.direccion
        ] ).node().id = data_persona.uuid;
        $table_seleccion_manual.draw( false );
	})
	// Ejecutar pre seleccion manual
	$('#button__ejecutar__manual').on('click', function(){
		var data = [];
		$this_btn = $(this);
		$this_btn.attr('disabled', true);
		$this_btn.text('Postulando...');
		$this_btn.prepend('<span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i></span>');
		$table_seleccion_manual.$(".check input[type=checkbox]:checked").each(function(index,elem){
			data.push({'rango':$(elem).attr('data-rango'), 'persona':$(elem).attr('data-persona'), 'tipo':'manual'});
		});
		$.ajax({ 
			method: "POST", 
			url: '/convocatorias/puestos/'+$(this).attr('data-puesto')+'/add_preseleccion/', 
			data: JSON.stringify(data), 
			datType: 'json', contentType:"application/json", 
			beforeSend: function(xhr) {
				xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
			}})
			.done(function( response ) {
				$('#message__ejecutar').text(response.message);
				var total = response.vacantes-response.preseleccionados;
				$('#message__ejecutar').html('<span class="text-green" >'+response.message+' Quedan: '+total+' vacantes</span>');
				$this_btn.attr('disabled', false);
				$this_btn.html('');
				$this_btn.text('EJECUTAR');
				for (var i = 0; i < data.length; i++) {
					$table_seleccion_manual.row('#'+data[i].persona).remove().draw( false );
				}
			})
			.fail(function( jqXHR, response ) {
				console.log(response);
				$('#message__ejecutar').html('<span class="text-red" >ocurrió un error en el servidor.</span>');
				$this_btn.attr('disabled', false);
				$this_btn.html('');
				$this_btn.text('EJECUTAR');	
			}); 
	})
	// ADD OBSERVACION POSTULACION
	$('.add_observacion_postulacion').on('click', function(){
		$('#form-add-observacion').attr('data-id',$(this).attr('data-id'));
		$('#list_observaciones').html('<span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i> Cargando...</span>');
		ajax_api('GET','/convocatorias/estado_postulacion/'+$(this).attr('data-id')+'/observaciones/', undefined )
			.done(function( response ) {
				var template = '';
				for (var i=0; i<response.length; i++){
					template += '<div class="row m-t-10"><div class="col-sm-1 text-right"><i class="zmdi zmdi-check"></i></div><div class="col-sm-11"><span>'+response[i]['descripcion']+'</span><p>'+response[i]['fecha_creacion']+'</p></div></div>';
				}
				console.log(response);
				$('#list_observaciones').html(template);
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			});
	})

	$('#form-add-observacion').on('submit', function(evt){
		evt.preventDefault();
		pk_postulacion = $(this).attr('data-id');
		ajax_api('POST','/convocatorias/estado_postulacion/'+pk_postulacion+'/observaciones/', {'descripcion': $('#descripcion_observacion').val() })
			.done(function( response ) {
				$('#list_observaciones').prepend('<div class="row m-t-10"><div class="col-sm-1 text-right"><i class="zmdi zmdi-check"></i></div><div class="col-sm-11"><p>'+$('#descripcion_observacion').val()+'</p></div></div>');
				$('#descripcion_observacion').val('');
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			});

	})
	// CONTRATAR
	$('#contratar').on('click', function(){
		var postulaciones = [];
		var uuid_convocatoria = $(this).attr('data-convocatoria');
		$(".checkbox-aprobados input[type=checkbox]:checked").each(function(index,elem){
			postulaciones.push($(elem).attr('data-id'));
		});
		ajax_api('POST','/convocatorias/puestos/'+uuid_convocatoria+'/contratar_aprobados/', {'postulaciones': postulaciones })
			.done(function( response ) {
				var total = response.vacantes-response.contratados;
				$('#result_contrato').html('<span class="text-green" >'+response.message+' Quedan: '+total+' vacantes</span>');
				for (var i=0; i<postulaciones.length; i++){
					$('#'+postulaciones[i]).hide(500);
				}
			})
			.fail(function( jqXHR, response ) {
				console.log(response);	
			});
	})

	// COCKIES
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