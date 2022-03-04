/* $(document).ready(function(){
    $('.datepicker').datepicker();
  });
 */   
var url = "https://www.datos.gov.co/resource/xdk5-pm3f.json";
var peticion = new XMLHttpRequest();
peticion.open('GET' , url);
peticion.responseType = 'json';
peticion.send();

peticion.onreadystatechange = function(){
	$("#departamentos").change( function(event){
		$("#municipios").html('<option>Municipios</option>');
		var respuesta = peticion.response;
		for (var i=0; i<respuesta.length;i++) {
			//alert(respuesta[10]['municipio']);
			if($("#departamentos").val() == respuesta[i]['departamento']){
				$("#municipios").append('<option>'+respuesta[i]['municipio']+'</option>');
			}
		}

	})
}
