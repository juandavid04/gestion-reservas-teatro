from wtforms import Form
from wtforms import StringField, TextField, PasswordField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from main import correos,verificarcontraseña

def existe_correo(form,field):
	if correos(field):
		raise validators.ValidationError('El correo que ingreso ya esta registrado.')

def no_existe_correo(form,field):
	if not correos(field):
		validators.StopValidation()
		raise validators.ValidationError('El correo que ingreso no existe.')

def verificar_contra(form,field):
	if not verificarcontraseña(form,field):
		raise validators.ValidationError('Contraseña Incorrecta.')

class formulario(Form):
	teatro = StringField('Nombre del Teatro',
		[
			validators.Required(message = "Es requerido  este campo.")
		])
	gerente = StringField('Gerente')
	direccion = StringField("Dirección",
		[
			validators.Required(message = "Es requerido  este campo.")
		])
	tel_teatro = StringField("Telefono",
		[
			validators.Required(message = "Es requerido  este campo."),
			validators.length(max=10, message="Tamaño maximo 10 caracteres.")
		])
	email = EmailField('Email',
		[
			validators.Required(message = "Es requerido  este campo."),
			validators.Email(message = "Ingrese un correo valido."),
			existe_correo
		])
	contraseña = PasswordField('Contraseña',
		[
			validators.Required(message = "Es requerido  este campo.")
		])
	otros_detalles = TextField('Otros detalles')

class login(Form):
	emailogin = EmailField('Email',
		[
			validators.Required(message = "Es requerido  este campo."),
			validators.Email(message = "Ingrese un correo valido."),
			no_existe_correo 
		])
	contraseña = PasswordField('Contraseña',
		[
			validators.Required(message = "Es requerido  este campo."),
			verificar_contra
		])
	
		