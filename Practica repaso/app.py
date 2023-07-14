from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates', static_folder='public')

# Configurar la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'DB_Fruteria'
app.secret_key = 'Mysecretkey'

# Crear una instancia de la clase MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('menu.html')

@app.route('/iragregar')
def iragregar():
    return render_template('agregar.html')

@app.route('/agregarf', methods= ['POST'])
def agregar():
   if request.method == 'POST':
        vfruta = request.form['fruta']
        vtemporada = request.form['temporada']
        vprecio = request.form['precio']
        vstock = request.form['stock']
        
        curins = mysql.connection.cursor()
        curins.execute("Insert into tbfrutas (fruta, temporada, precio, stock) values (%s,%s,%s,%s)", (vfruta, vtemporada, vprecio, vstock))
        mysql.connection.commit()

        return redirect(url_for('irconsultageneral'))
    
@app.route('/irconsultageneral')
def irconsultageneral():
    curconsgen = mysql.connection.cursor()
    curconsgen.execute("select * from tbfrutas")
    consultageneral = curconsgen.fetchall()
    
    return render_template('consultaGeneral.html', datos = consultageneral )

@app.route('/eliminargen/<id>')
def eliminargen(id):
    
    cureliminar = mysql.connection.cursor()
    cureliminar.execute("delete from tbfrutas where id = %s", (id,))
    mysql.connection.commit()
    
    flash("Se elimino la fruta")
    return render_template("consultaGeneral.html")

@app.route('/editargen/<id>')
def editargen(id):
    cureditargen = mysql.connection.cursor()
    cureditargen.execute("select * from tbfrutas where id = %s", (id,))
    fruta = cureditargen.fetchone()
    
    return render_template("editargen.html", datosfruta = fruta)

@app.route('/updategen', methods=['POST'])
def updategen():
    if request.method == 'POST':
        vid = request.form['id']
        vfruta = request.form['fruta']
        vtemporada = request.form['temporada']
        vprecio = request.form['precio']
        vstock = request.form['stock']
        
        curupgen = mysql.connection.cursor()
        curupgen.execute('UPDATE tbfrutas SET fruta = %s, temporada = %s, precio = %s, stock = %s WHERE id = %s', (vfruta, vtemporada, vprecio, vstock, vid))
        mysql.connection.commit()
        
        flash("Se actualizó correctamente")
        return redirect(url_for('irconsultageneral'))

    
@app.route('/irconsultaespecifica')
def irconsultaespecifica():
        
    return render_template('consultaEspecifica.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/consultaespecifica', methods=['POST', 'GET'])
def consultaespecifica():
    if request.method == 'POST':
        vfruta = request.form['fruta']
        
        curconesp = mysql.connect.cursor()
        curconesp.execute('select * from tbfrutas where fruta like(%s)', (vfruta,))
        datosfruta = curconesp.fetchone()
        
        if datosfruta:
            return render_template('consultaEspecifica.html', fruta = datosfruta)
        else:
            flash('No se encontro la fruta')
            return render_template('consultaEspecifica.html')
    return render_template('consultaEspecifica.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    

    