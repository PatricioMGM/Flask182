from flask import Flask, render_template, request, flash, redirect
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

@app.route('/eliminar')
def eliminar():
    return "Se eliminó el álbum en la BD"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
