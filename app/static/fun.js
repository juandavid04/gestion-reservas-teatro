document.querySelector('#generos').addEventListener('change', otro);
document.querySelector('#atras').addEventListener('click', genero);

var codigo = "";

function otro(){
	var opt = document.getElementById("generos");
	if(opt.options[opt.selectedIndex].text == 'Otro Genero'){
		document.getElementById("ge").innerHTML = "<h4>Otro Genero</h4>"
		codigo = opt.parentElement.innerHTML
		opt.parentElement.innerHTML = "<input class='row form-control' type='text' id='generos' name='generos'> \n <button id='atras' name='atras' class='btn btn-outline-primary my-2 my-sm-0' type='button'onclick='genero()'>Atras</button>";
	}
}

function genero(){
	var opt = document.getElementById('generos');
	document.getElementById("ge").innerHTML = "<h4>Generos</h4>"
	opt.parentElement.innerHTML = codigo;
}


function seleccionado(button){
	if(button.className == 'btn btn-info'){
		button.className = 'btn btn-outline-info';
		document.getElementById(button.value).value = 1;
	}
	else{
		button.className = 'btn btn-info';
		document.getElementById(button.value).value = 2;
	}
}


/*
document.addEventListener("DOMContentLoaded", function() {
	document.getElementById("formulario").addEventListener('submit', validarFormulario); 
  });
  
  function validarFormulario(evento) {
	evento.preventDefault();
	var usuario = document.getElementById('usuario').value;
	if(usuario.length == 0) {
	  alert('No has escrito nada en el usuario');
	  return;
	}
	var clave = document.getElementById('clave').value;
	if (clave.length < 6) {
	  alert('La clave no es válida');
	  return;
	}
	this.submit();
  }*/