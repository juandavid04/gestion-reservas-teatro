function otro(opt){
	alert(opt.value);
	if(opt.value == 'Otro Genero'){
		div = opt.parentElement;
		div.innerHTML = "<h4 class='row'>Otro Genero</h4> \n <input class='row' type='text'> \n <button onclick='generos(this)'>Atras</button>";
	}
}

