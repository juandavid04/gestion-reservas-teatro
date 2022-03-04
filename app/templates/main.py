from flask import Flask
from flaskext.mysql import MySQL
from flask import render_template
from flask import request
from flask import redirect
from flask_wtf import CsrfProtect
from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph
from flask import make_response
from flask import session
import form


app = Flask(__name__)
app.secret_key = 'my_secret_key'
csrf = CsrfProtect(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3307
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2172000'
app.config['MYSQL_DATABASE_DB'] = 'reservas_teatro' 


#    datos = cursor.fetchall()
#    print(datos)

mysql = MySQL()
mysql.init_app(app)

def SELECT(cod):
	cursor = mysql.get_db().cursor()
	cursor.execute(cod)
	return cursor.fetchall()

def INSERTAR(cod):
	cursor = mysql.get_db().cursor()
	cursor.execute(cod)
	mysql.get_db().commit()

def correos(field):
	cod = f"SELECT correo FROM Teatro WHERE correo = '{field.data}'"
	return SELECT(cod)

def verificarcontraseña(form,field):
	cod = f"SELECT contraseña FROM Teatro WHERE correo = '{form.emailogin.data}'"
	contr_encr = SELECT(cod)
	if contr_encr:
		return checkph(contr_encr[0][0], field.data)
	else:
		return True


@app.route('/registro_teatro', methods = ['GET','POST'])
def registrar_teatro():
	
	registro = form.formulario(request.form)
	if request.method == 'POST' and registro.validate():
		teatro = registro.teatro.data
		gerente = registro.gerente.data
		direccion = registro.direccion.data
		tel_teatro = registro.tel_teatro.data
		capacidad = registro.capacidad_asientos.data
		email = registro.email.data
		contraseña = genph(registro.contraseña.data)
		detalles = registro.otros_detalles.data

		cursor = mysql.get_db().cursor()
		cursor.execute(f"""INSERT INTO teatro(nombre,gerente,direccion,telefono,correo,contraseña,capacidad_sillas,otros_detalles)  
			VALUES('{teatro}','{gerente}','{direccion}','{tel_teatro}','{email}','{contraseña}',{int(capacidad)},'{detalles}');""")

		mysql.get_db().commit()

		cursor.execute("SELECT max(id_teatro) FROM TEATRO")      #Consulta por el último id agregado
		id = cursor.fetchall()
		session['id'] = id[0][0]
		return redirect(f'/sesion/id={id[0][0]}')
	return render_template('registro.html',regist = registro )

@app.route('/login', methods=['GET','POST'])
def login():
	log = form.login(request.form)
	email = log.emailogin.data
	contraseña = log.contraseña.data
	if request.method == 'POST' and log.validate():
		cursor = mysql.get_db().cursor()
		cursor.execute(f"SELECT id_teatro FROM teatro WHERE correo = '{email}'")
		datos = cursor.fetchall()
		session[str(datos[0][0])] = email
		return redirect(f'/sesion/id={datos[0][0]}')

	return render_template('login.html',log = log)

@app.route('/sesion/id=<id>')
def sesion(id):
	if id in session:
		cursor = mysql.get_db().cursor()
		cursor.execute(f"""SELECT nombre,gerente,direccion,telefono,correo,capacidad_sillas,otros_detalles 
			FROM teatro WHERE id_teatro = {id}""")
		datos = cursor.fetchall()
		return render_template('inicio_sesion.html',datos = datos)


@app.route('/')
def inicio():
	return render_template('index.html' )
    
if __name__=='__main__':
    app.run(debug=True)


#cursor = mysql.get_db().cursor()
#    cursor.execute("SELECT * FROM dimension1")
#    datos = cursor.fetchall()
#    print(datos)