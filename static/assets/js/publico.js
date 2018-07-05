$(function(){
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
	// FORM POST
	$('#form-add-persona-publico').on('submit', function(){
		var btn_submit = $(this).find('button[type="submit"]');
		load_btn(btn_submit);
	})
	// FUNCTION LOAD BTN
	function load_btn(btn){
		btn.attr('disabled', true);
		btn.text('Cargando...');
		btn.prepend('<span><i class="zmdi zmdi-refresh zmdi-hc-spin"></i></span>');
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
	// POSTULAR CONVOCATORIA
	$('body').on('click', '.publico_postular_puesto', function(){
		var $this_btn = $(this);
		$this_btn.attr('disabled', true);
		$this_btn.text('Postulando...');
		
		$.ajax({
			method: 'GET',
			url: '/publico/postular/puesto/'+$this_btn.attr('data-puesto')+'/'
		}).done(function( response ) {
			console.log('Respuesta de autorizacion.');
			// $this_btn.parent().html('<button class="btn btn-danger text-uppercase" data-puesto="'+$this_btn.attr('data-puesto')+'" >abandonar</button>');
			$this_btn.parent().html('<span class="text-success" >Postulado</span>')
			$('#message_postulacion').addClass('alert-success');
			$('#message_postulacion').html('<span>Postulación realizada con éxito </span>');
		}).fail(function( jqXHR, response ) {
			$('#message_postulacion').addClass('alert-danger');
			$('#message_postulacion').html('<span>'+jqXHR.responseJSON.message+'</span>');
		});
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