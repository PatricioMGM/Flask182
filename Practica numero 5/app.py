from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurar la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbflask'
app.secret_key = 'Mysecretkey'

# Crear una instancia de la clase MySQL
mysql = MySQL(app)


@app.route('/')
def index():
    curSelect = mysql.connection.cursor()
    curSelect.execute('SELECT * FROM albums')
    consulta = curSelect.fetchall()
    print(consulta)

    return render_template('index.html', listAlbums = consulta )


@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        titulo = request.form['txtTitulo']
        artista = request.form['txtArtista']
        anio = request.form['txtAnio']
        
        curInsert = mysql.connection.cursor()
        curInsert.execute("INSERT INTO albums (titulo, artista, año) VALUES (%s, %s, %s)", (titulo, artista, anio))
        mysql.connection.commit()
        curInsert.close()
    flash("Se ha guardado el nuebo album")
    return redirect("/")

@app.route('/editar/<id>')
def editar(id):
    cursoreditar = mysql.connection.cursor()
    cursoreditar.execute('select * from albums where id = %s', (id,))
    consulta = cursoreditar.fetchone()
    
    return render_template('editarAlbum.html', consulta = consulta)

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        Vtitulo = request.form['txtTitulo']
        Vartista = request.form['txtArtista']
        Vanio = request.form['txtAnio']
        
        curActu = mysql.connection.cursor()
        curActu.execute('update albums set titulo = %s, artista = %s, año = %s where id = %s', (Vtitulo, Vartista, Vanio, id))
        mysql.connection.commit()
        
        flash("Album actualizado correctamente")
        return redirect(url_for("index"))

@app.route('/eliminaraviso/<id>')
def eliminaraviso(id):
    cursoreliminarav = mysql.connection.cursor()
    cursoreliminarav.execute('select * from albums where id = %s', (id,))
    consulta = cursoreliminarav.fetchone()

    return render_template('eliminar.html', consulta = consulta)

@app.route('/eliminar/<id>')
def eliminar(id):
    cursoreliminar = mysql.connection.cursor()
    cursoreliminar.execute('delete from albums where id = %s', (id,))
    mysql.connection.commit()
    
    flash("Album eliminado correctamente")
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
