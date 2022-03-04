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
from flask import abort
import form

abc = 'abcdefghijklmnopqrstuvwxyz'
generos = [['Tragedia'], ['Comedia'], ['Drama'], ['Musical'], ['Opera'], ['Tragicomedia']]


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

def DELETE(cod):
	cursor = mysql.get_db().cursor()
	cursor.execute(cod)
	mysql.get_db().commit()

def correos(field):
	cod = f"SELECT correo FROM Teatro WHERE correo = '{field.data}'"
	return SELECT(cod)

def DELETEASIENTOS(idfila):
	cursor = mysql.get_db().cursor()
	cursor.execute(f"DELETE FROM sillas_por_actuacion WHERE id_fila = {idfila};")
	mysql.get_db().commit()

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
		email = registro.email.data
		contraseña = genph(registro.contraseña.data)
		detalles = registro.otros_detalles.data

		cod = f"""INSERT INTO teatro(nombre,gerente,direccion,telefono,correo,contraseña,capacidad_sillas,otros_detalles)  
			VALUES('{teatro}','{gerente}','{direccion}','{tel_teatro}','{email}','{contraseña}',{0},'{detalles}');"""

		INSERTAR(cod)
		cod = "SELECT max(id_teatro) FROM TEATRO"
		id = SELECT(cod)      #Consulta por el último id agregado
		session["id"] = id[0][0]
		session["nombre"] = teatro
		session['esquema'] = []
		return redirect(f'/sesion/id={id[0][0]}')

	return render_template('registro.html',regist = registro )

@app.route('/login', methods=['GET','POST'])
def login():
	log = form.login(request.form)
	email = log.emailogin.data
	contraseña = log.contraseña.data
	if request.method == 'POST' and log.validate():
		cod  = f"SELECT id_teatro, nombre FROM teatro WHERE correo = '{email}'"
		datos = SELECT(cod)
		session["id"] = datos[0][0]
		session["nombre"] = datos[0][1]
		session['esquema'] = []
		return redirect(f'/sesion/id={datos[0][0]}')

	return render_template('login.html',log = log)

@app.route('/sesion/id=<id>')
def sesion(id):
	if session["id"] == int(id):
		cod = f"""SELECT gerente,direccion,telefono,correo,capacidad_sillas,otros_detalles 
			FROM teatro WHERE id_teatro = {id}"""
		datos = SELECT(cod)
		return render_template('inicio_sesion.html', nombre = session["nombre"], id = session["id"],datos = datos)
	else:
		abort(404)

@app.route('/sesion/id=<id>/esquema',  methods = ['GET','POST'])
def esquema(id):
	if session["id"] == int(id):
		if request.method == 'POST':
			Nbloques = int(request.form['Nbloques'])
			add_esquema(Nbloques,id)
			#Nbloques = 0
			return render_template('esquema.html', bloques = session['esquema'], nombre = session["nombre"], id = session["id"])
		else:
			cod = f"SELECT descripcion_bloque, id_bloque FROM bloque_de_sillas b WHERE b.id_teatro = {id} "
			datos = SELECT(cod)
			bloques = []
			bloques.append([])
			for i in datos:
				fila = len(bloques)
				if fila == int(i[0][0]):
					bloques[fila-1].append(i)
				elif fila+1 == int(i[0][0]):
					bloques.append([])
					bloques[fila].append(i)
			session['esquema'] = bloques
			return render_template('esquema.html', bloques = session['esquema'], nombre = session["nombre"], id = session["id"])
	else:
		abort(404)

def add_esquema(num,id):
	fila = len(session['esquema'])
	bloques = session['esquema']
	bloques.append([str(fila+1)+'a'])
	cod = f"INSERT INTO bloque_de_sillas(descripcion_bloque,id_teatro) VALUES('{str(fila+1)+'a'}',{id})"
	INSERTAR(cod)
	for i in range(1,num):
		etiq = str(fila+1)+abc[i]
		cod = f"INSERT INTO bloque_de_sillas(descripcion_bloque,id_teatro) VALUES('{etiq}',{id})"
		INSERTAR(cod)
		bloques[fila].append(etiq)
	session['esquema'] = bloques

def add_asientos(num,idbloq):
	fila = len(session['asientos_bloque'])
	bloque = session['asientos_bloque']
	cod = f"INSERT INTO fila_de_sillas(numero_fila,id_bloque,contador_sillas_por_fila) VALUES({fila+1},{idbloq},{num})"
	INSERTAR(cod)
	cod = f"SELECT max(id_fila) FROM fila_de_sillas WHERE id_bloque = {idbloq}"
	ultimo_id_fila_bloque = SELECT(cod)[0][0]

	bloque.append([(fila+1)*100+1])
	cod = f"INSERT INTO sillas_por_actuacion(id_fila,numero_silla) VALUES({ultimo_id_fila_bloque},{(fila+1)*100+1})"
	INSERTAR(cod)
	cod = f"""INSERT INTO sillas_por_actuacion(id_actuacion,id_estado,numero_silla,id_fila)
				SELECT DISTINCT id_actuacion,1,{(fila+1)*100+1},{ultimo_id_fila_bloque} FROM actuacion;"""
	INSERTAR(cod)
	for i in range(1,num):
		numero_silla = (fila+1)*100+(i+1)
		cod = f"INSERT INTO sillas_por_actuacion(id_fila,numero_silla) VALUES({ultimo_id_fila_bloque},{numero_silla})"
		INSERTAR(cod)
		cod = f"""INSERT INTO sillas_por_actuacion(id_actuacion,id_estado,numero_silla,id_fila)
				SELECT DISTINCT id_actuacion,1,{numero_silla},{ultimo_id_fila_bloque} FROM actuacion;"""
		INSERTAR(cod)
		bloque[fila].append(numero_silla)
	session['esquema'] = bloque

@app.route('/sesion/id=<id>/esquema/idbloque=<bl>/deletefila',  methods = ['GET','POST'])
def eliminar_fila_asientos(id,bl):
	cod = f"SELECT max(id_fila) FROM fila_de_sillas WHERE id_bloque = {bl}"
	ultimafila = SELECT(cod)[0][0]
	DELETEASIENTOS(ultimafila)
	cod = f"DELETE FROM fila_de_sillas WHERE id_fila = {ultimafila}"
	DELETE(cod)
	return redirect(f"/sesion/id={id}/esquema/idbloque={bl}")

@app.route('/sesion/id=<id>/esquema/deletebloque',  methods = ['GET','POST'])
def eliminar_bloque(id,bl=0):
	if request.method == 'POST':
		blnom = request.form['Eli_bloques']
		bl = SELECT(f"SELECT id_bloque FROM bloque_de_sillas WHERE descripcion_bloque = '{blnom}'")[0][0]
	cod = f"SELECT id_fila FROM fila_de_sillas WHERE id_bloque = {bl}"
	idsfilas = SELECT(cod)
	for i in idsfilas:
		DELETEASIENTOS(i[0])	
		cod = f"DELETE FROM fila_de_sillas WHERE id_fila = {i[0]}"
		DELETE(cod)
	cod = f"DELETE FROM bloque_de_sillas WHERE id_bloque = {bl}"
	DELETE(cod)
	return redirect(f"/sesion/id={id}/esquema")

@app.route('/sesion/id=<id>/eliminarcuenta',  methods = ['GET','POST'])
def eliminar_cuenta(id):
	idsbloques = SELECT(f"SELECT id_bloque FROM bloque_de_sillas WHERE id_teatro = {id}")
	for i in idsbloques:
		eliminar_bloque(id,i[0])
	idsbloques = SELECT(f"SELECT id_produccion FROM produccion WHERE id_teatro = {id}")
	for i in idsbloques:
		delete_produccion(i[0])	
	cod = f"DELETE FROM teatro WHERE id_teatro = {id}"
	DELETE(cod)
	return redirect('/logout')

@app.route('/sesion/id=<id>/esquema/idbloque=<bl>',  methods = ['GET','POST'])
def esquema_asientos(id,bl):
	if session["id"] == int(id):
		cod  = f"SELECT descripcion_bloque FROM bloque_de_sillas WHERE id_bloque = {bl}"
		datos = SELECT(cod)
		if request.method == 'POST':
			num = request.form['Nasientos']
			add_asientos(int(num),bl)
			return render_template('esquema_asientos.html', nombre = session["nombre"], id = session["id"], bloque=datos[0][0], idbloque = bl, asientos=session["asientos_bloque"])
		else:
			asientos_por_bloque = []
			cod = f"SELECT id_fila FROM fila_de_sillas WHERE id_bloque = {bl}"
			filas = SELECT(cod)
			for i in filas:
				cod = f"SELECT numero_silla FROM sillas_por_actuacion WHERE id_fila = {i[0]} and id_actuacion is null"
				asientos = SELECT(cod)
				asientos = [j[0] for j in asientos]
				asientos_por_bloque.append(asientos)
			session["asientos_bloque"] = asientos_por_bloque
			return render_template('esquema_asientos.html', nombre = session["nombre"], id = session["id"], bloque=datos[0][0], idbloque = bl, asientos=session["asientos_bloque"])
	else:
		abort(404)

def delete_produccion(idprod):
	cod = f"DELETE FROM actuacion WHERE id_produccion = {idprod}"
	DELETE(cod)
	cod = f"DELETE FROM produccion WHERE id_produccion = {idprod}"
	DELETE(cod)

@app.route('/sesion/id=<id>/producciones/<action>',  methods = ['GET','POST'])
def producciones(id,action):
	if session["id"] == int(id):

		cod = "SELECT descripcion_genero FROM genero"
		datosg = SELECT(cod)
		if len(datosg)==0:
			for i in generos:
				cod = f"INSERT INTO genero(descripcion_genero) VALUES('{i[0]}')"
				INSERTAR(cod)
			datosg = generos

		codtabla = f"""SELECT p.nombre,g.descripcion_genero, p.descripcion, p.otros_detalles, p.id_produccion FROM produccion p 
		INNER JOIN genero g ON g.id_genero = p.id_genero WHERE id_teatro = '{id}'"""
		

		if request.method == 'POST' and action == 'add':
			nombre = request.form['nomprod']
			descripcion = request.form['desc']
			detalles = request.form['detalles']
			genero = request.form['generos']

			cod = f"SELECT id_genero, descripcion_genero FROM genero WHERE descripcion_genero = '{genero}'"
			datos = SELECT(cod)
			if len(datos) == 0:
				cod = f"INSERT INTO genero(descripcion_genero) VALUES('{genero}')"
				INSERTAR(cod)
				cod = f"SELECT id_genero, descripcion_genero FROM genero WHERE descripcion_genero = '{genero}'"
				datos = SELECT(cod)
			cod = f"""INSERT INTO produccion(id_genero,id_teatro,nombre,descripcion,otros_detalles) 
			VALUES({datos[0][0]},{id},'{nombre}','{descripcion}','{detalles}')"""
			INSERTAR(cod)
			datostabla = SELECT(codtabla)
			return render_template('producciones.html', nombre = session["nombre"], id = session["id"], generos = datosg, tabla = datostabla)

		elif request.method == 'POST' and action == 'delete':
			idprod = request.form['eliminar']
			delete_produccion(idprod)
			datostabla = SELECT(codtabla)
			return render_template('producciones.html', nombre = session["nombre"], id = session["id"], generos = datosg, tabla = datostabla)
		else:
			datostabla = SELECT(codtabla)
			return render_template('producciones.html', nombre = session["nombre"], id = session["id"], generos = datosg, tabla = datostabla)
	else:
		abort(404)

@app.route('/sesion/id=<id>/producciones/idprod=<idprod>/<action>',  methods = ['GET','POST'])
def actuaciones(id,idprod,action):
	if session["id"] == int(id):

		codprod = f"""SELECT p.nombre,g.descripcion_genero, p.descripcion, p.otros_detalles, p.id_produccion FROM produccion p 
		INNER JOIN genero g ON g.id_genero = p.id_genero WHERE p.id_produccion = {idprod}"""

		codtabla = f""" SELECT fecha_actuacion,hora_inicio,hora_fin,id_actuacion FROM actuacion WHERE id_produccion = {idprod} """

		if request.method == 'POST' and action == 'add':

			fecha = request.form["fecha"]
			inicio = request.form["h_inicio"]
			fin = request.form["h_fin"]
			cod = f"""INSERT INTO actuacion(id_produccion,fecha_actuacion,hora_inicio, hora_fin) 
			VALUES({idprod},'{fecha}','{inicio}','{fin}');"""
			INSERTAR(cod)
			cod = f"SELECT max(id_actuacion) FROM actuacion"
			ultimo_id_act = SELECT(cod)[0][0]

			cod = f"""SELECT f.id_fila, s.numero_silla FROM bloque_de_sillas b
				INNER JOIN fila_de_sillas f ON f.id_bloque = b.id_bloque
				INNER JOIN sillas_por_actuacion s ON s.id_fila = f.id_fila
				WHERE b.id_teatro = {id}
				AND s.id_actuacion IS NULL;"""
			asientos = SELECT(cod)
			print(asientos)
			for i in asientos:
				cod = f"""INSERT INTO sillas_por_actuacion(id_fila,id_actuacion,id_estado,numero_silla)
				VALUES({i[0]},{ultimo_id_act},{1},{i[1]})"""
				INSERTAR(cod)

			datos = SELECT(codprod)
			tabla = SELECT(codtabla)
			return render_template('actuaciones.html', nombre = session["nombre"], id = session["id"], datos=datos, tabla=tabla)
		elif request.method == 'POST' and action == 'delete':
			id_act = request.form['eliminar_act']
			cod = f"DELETE FROM sillas_por_actuacion WHERE id_actuacion = {id_act}"
			DELETE(cod)
			cod = f"DELETE FROM actuacion WHERE id_actuacion = {id_act}"
			DELETE(cod)
			tabla = SELECT(codtabla)
			datos = SELECT(codprod)
			return render_template('actuaciones.html', nombre = session["nombre"], id = session["id"], datos=datos, tabla=tabla)
		else:
			tabla = SELECT(codtabla)
			datos = SELECT(codprod)
			return render_template('actuaciones.html', nombre = session["nombre"], id = session["id"], datos=datos, tabla=tabla)
	else:
		abort(404)

@app.route('/logout')
def logout():
	session.pop('id', None)
	session.pop('nombre', None)
	session.pop('asientos_bloque',None)
	return redirect('/')

@app.route('/id_tea=<id>')
def produccion(id):
	codtabla = f"""SELECT p.nombre,g.descripcion_genero, p.descripcion, p.otros_detalles, p.id_produccion FROM produccion p 
		INNER JOIN genero g ON g.id_genero = p.id_genero WHERE id_teatro = '{id}'"""
	tabla = SELECT(codtabla)
	cod = f"SELECT nombre FROM teatro WHERE id_teatro = {id}"
	nombre = SELECT(cod)[0][0]
	return render_template('produccion.html', tabla = tabla, id=id, nombre = nombre)

@app.route('/id_tea=<id>/idprod=<idprod>')
def actuacion(id,idprod):
	codtabla = f""" SELECT fecha_actuacion,hora_inicio,hora_fin,id_actuacion FROM actuacion WHERE id_produccion = {idprod} """
	tabla = SELECT(codtabla)
	cod = f"SELECT t.nombre, p.nombre FROM teatro t, produccion p WHERE t.id_teatro = {id} AND id_produccion = {idprod}"
	datos = SELECT(cod)
	nombre = datos[0][0]
	produccion = datos[0][1]
	return render_template('actuacion.html', tabla = tabla, id=id, idprod=idprod, nombre = nombre, produccion = produccion)

@app.route('/id_tea=<id>/idprod=<idprod>/idact=<idact>/<esq>',  methods = ['GET','POST'])
def reservar(id,idprod,idact,esq):
	cod = f"SELECT t.nombre, p.nombre FROM teatro t, produccion p WHERE t.id_teatro = {id} AND id_produccion = {idprod}"
	datos = SELECT(cod)
	nombre = datos[0][0]
	produccion = datos[0][1]
	if esq == 'bloques':
		cod = f"SELECT descripcion_bloque, id_bloque FROM bloque_de_sillas b WHERE b.id_teatro = {id} "
		datos = SELECT(cod)
		bloques = []
		bloques.append([])
		print(datos)
		for i in datos:
			fila = len(bloques)
			if fila == int(i[0][0]):
				bloques[fila-1].append(i)
			elif fila+1 == int(i[0][0]):
				bloques.append([])
				bloques[fila].append(i)
		return render_template('bloques.html', bloques = bloques, id=id, idprod=idprod, idact=idact, nombre = nombre, produccion = produccion, idbloque = esq)
	elif esq.isnumeric():
		if request.method == 'POST':
			asientos = request.form
			reservados = []
			ids = []
			for i in asientos:
				if asientos[i].isnumeric() and int(asientos[i]) == 2:
					num = SELECT(f"SELECT numero_silla FROM sillas_por_actuacion WHERE id_silla = {i}")[0][0]
					reservados.append([i,num])
					ids.append(i)
			session["ids_reservados"] = [ids,idact]
			return render_template('datos_reserva.html', id=id, idprod=idprod, idact=idact, nombre = nombre, produccion = produccion, asientos_reservados = reservados, idbloque = esq)

		cod  = f"SELECT descripcion_bloque FROM bloque_de_sillas WHERE id_bloque = {esq}"
		datos = SELECT(cod)
		asientos_por_bloque = []
		cod = f"SELECT id_fila FROM fila_de_sillas WHERE id_bloque = {esq}"
		filas = SELECT(cod)
		for i in filas:
			cod = f"SELECT numero_silla,id_estado,id_silla FROM sillas_por_actuacion WHERE id_fila = {i[0]} AND id_actuacion = {idact}"
			asientos = SELECT(cod)
			#asientos = [i[0] for i in asientos]
			asientos_por_bloque.append(asientos)
			print(asientos_por_bloque)
		return render_template('asientos.html', nombre = nombre, id = id, idact=idact, bloque=datos[0][0], idbloque = esq, asientos=asientos_por_bloque, idprod=idprod, produccion = produccion)
		
@app.route('/resumen_reserva',  methods = ['GET','POST'])
def resumen():
	if request.method == 'POST':
		nombre1 =  request.form['prnom']
		nombre2 =  request.form['senom']
		celular =  request.form['celular']
		tarjeta =  request.form['tarcred']
		correo =  request.form['correo']
		detalles =  request.form['detalles']
		cod = f"""INSERT INTO cliente(nombre1,nombre2,celular,informacion_tarjeta,correo,otros_detalles) 
		VALUES('{nombre1}','{nombre2}',{celular},'{tarjeta}','{correo}','{detalles}')"""
		INSERTAR(cod)
		id_cliente = SELECT("SELECT max(id_cliente) FROM cliente")[0][0]
		fecha_reserva = SELECT(f"SELECT fecha_actuacion FROM actuacion WHERE id_actuacion = {session['ids_reservados'][1]}")[0][0]
		fecha_en_que_se_hizo = SELECT("SELECT NOW();")[0][0]

		cod = f"INSERT INTO reserva(id_cliente,fecha_reserva,fecha_en_que_se_hizo) VALUES({id_cliente},'{fecha_reserva}','{fecha_en_que_se_hizo}')"
		INSERTAR(cod)
		id_reser = SELECT("SELECT max(id_reserva) FROM reserva;")[0][0]
		print(id_reser)
		
		for i in session['ids_reservados'][0]:
			cursor = mysql.get_db().cursor()
			cursor.execute(f"UPDATE sillas_por_actuacion SET id_reserva = {id_reser} WHERE id_silla = {i}")
			mysql.get_db().commit()
			cursor = mysql.get_db().cursor()
			cursor.execute(f"UPDATE sillas_por_actuacion SET id_estado = '2' WHERE id_silla = {i}")
			mysql.get_db().commit()

		nombreprod = SELECT(f"SELECT p.nombre FROM actuacion c INNER JOIN produccion p ON p.id_produccion = c.id_produccion WHERE c.id_actuacion = {session['ids_reservados'][1]}")

		return render_template('resumen_reserva.html',nombrep = nombreprod, fecha_reserva=fecha_reserva,fecha_realizada=fecha_en_que_se_hizo, nombre = nombre1 +" "+ nombre2, celular=celular, tarjeta=tarjeta, correo=correo,detalles=detalles)


@app.route('/')
def inicio():
	cod = "SELECT count(*) FROM estado_silla"
	dato = SELECT(cod)[0][0]
	if dato == 0:
		cod = f"INSERT INTO estado_silla VALUES(1,'Disponible')"
		INSERTAR(cod)
		cod = f"INSERT INTO estado_silla VALUES(2,'Reservado')"
		INSERTAR(cod)
	cod = f"SELECT nombre,direccion,telefono,otros_detalles,id_teatro FROM teatro"
	datos = SELECT(cod)
	print(datos)
	return render_template('index.html', datos= datos )
    
if __name__=='__main__':
    app.run(debug=True)
#style="background: url({{ url_for('static',filename='c4ddd6ba9875c69080ba538e1f4a9804.jpg') }});"

#cursor = mysql.get_db().cursor()
#    cursor.execute("SELECT * FROM dimension1")
#    datos = cursor.fetchall()
#    print(datos)