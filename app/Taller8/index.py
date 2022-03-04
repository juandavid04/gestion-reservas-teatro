from flask import Flask, render_template, request, redirect, url_for, flash
from flask import request
from flask import render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_DATABASE_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2172000'
app.config['MYSQL_DB'] = 'taller8web'
mysql = MySQL(app)
mysql.init_app(app)

app.secret_key = "mysecretkey"

@app.route('/')
def Index():
    return render_template('Formulario.html')

@app.route('/add_user', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['nombre']
        apellido = request.form['apellido']
        documento = request.form['documento']
        fechaNacimiento = request.form['fechaNacimiento']
        email = request.form['email']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        password = request.form['password']
        tipoId = request.form['tipoId']
        departamento = request.form['departamento']
        municipio = request.form['municipio']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO persona (nombres, apellidos, tipoDocumento, documento, departamento, municipio, fechaNacimiento, email, telefono, usuario, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (name, apellido, tipoId, documento, departamento, municipio, fechaNacimiento, email, telefono, usuario, password))
        mysql.connection.commit()
        return redirect(url_for('view_contacts'))

@app.route('/view_contacts')
def view_contacts():
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, nombres, apellidos, tipoDocumento, documento, departamento, municipio, email, telefono, usuario FROM persona')
        data = cur.fetchall()
        cur.close()
        print(data)
        return render_template('Tabla.html', contacts = data)

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM persona WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Eliminado Correctamente')
    return redirect(url_for('view_contacts'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombres, apellidos, email, telefono, usuario FROM persona WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-user.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        name = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        cur = mysql.connection.cursor()
        print(name)
        print(apellido)
        cur.execute("UPDATE persona SET nombres = %s, apellidos = %s, email = %s, telefono = %s, usuario = %s WHERE id = %s", 
        (name, apellido, email, telefono, usuario, id))
        flash('Contacto Actualizado Correctamente')
        mysql.connection.commit()
        return redirect(url_for('view_contacts'))

if __name__ == '__main__': 
    app.run(port = 3000, debug=True)