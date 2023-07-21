from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates', static_folder='public')

# Configurar la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'DB_Floreria'
app.secret_key = 'Mysecretkey'

# Crear una instancia de la clase MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    cgen = mysql.connection.cursor()
    cgen.execute('select * from tbFlores')
    flores = cgen.fetchall()
    
    return render_template('general.html', dflores = flores)

@app.route('/iragregar')
def agregar():
    return render_template('ingresar.html')

@app.route('/irgeneral')
def irgeneral():
    cgen = mysql.connection.cursor()
    cgen.execute('select * from tbFlores')
    flores = cgen.fetchall()
    
    return render_template('general.html', dflores = flores)

@app.route('/insertar', methods= ['POST'])
def insertar():
    if request.method == 'POST':
        vflor = request.form['flor']
        vcantidad = request.form['cantidad']
        vprecio = request.form['precio']
        
        cagr = mysql.connection.cursor()
        cagr.execute("Insert into tbFlores (Nombre, cantidad, precio) values (%s,%s,%s)", (vflor, vcantidad, vprecio))
        mysql.connection.commit()

    cgen = mysql.connection.cursor()
    cgen.execute('select * from tbFlores')
    flores = cgen.fetchall()
    
    return render_template('general.html', dflores = flores)

@app.route('/irconsultaespecifica')
def irconsultaespecifica():
    return render_template('consultaespecifica.html')

@app.route('/consultaespecifica', methods=['POST', 'GET'])
def consultaespecifica():
    if request.method == 'POST':
        vflor = request.form['flor']
        
        curconesp = mysql.connect.cursor()
        curconesp.execute('select * from tbFlores where nombre like(%s)', (vflor,))
        datosflor = curconesp.fetchone()
        
        if datosflor:
            return render_template('consultaEspecifica.html', flor = datosflor)
        else:
            flash('No se encontro la fruta')
            return render_template('consultaEspecifica.html')
    return render_template('consultaEspecifica.html')
    
@app.route('/ireditar/<id>')
def ireditar(id):
    
    curconesp = mysql.connect.cursor()
    curconesp.execute('select * from tbFlores where id = %s', (id,))
    datosflor = curconesp.fetchone()
    
    return render_template('editarflor.html', flor = datosflor)

@app.route('/editar', methods=['POST'])
def editar():
    if request.method == 'POST':
        vid = request.form['id']
        vflor = request.form['flor']
        vcantidad = request.form['cantidad']
        vprecio = request.form['precio']

        
        curupgen = mysql.connection.cursor()
        curupgen.execute('UPDATE tbFlores SET nombre = %s, cantidad = %s, precio = %s WHERE id = %s', (vflor, vcantidad, vprecio, vid))
        mysql.connection.commit()
        
        flash("Se actualizó correctamente")
        return redirect(url_for('irgeneral'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)