$(function(){
	$('#id_tipo').change(function(){
		if ($('#id_tipo :selected').text().toLowerCase() == 'postulación a capacitaciones') {
			$('#block_capacitacion').css('display','block');
			$('#id_capacitacion').attr('required','required');
		} else {
			$('#block_capacitacion').css('display','none');
			$('#id_capacitacion').removeAttr('required','required');
		}
	})
})