
import mysql.connector
from flask import Flask, render_template, request


#inicializion del servidor flask
app = Flask(__name__)

# Configurar la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbflask'

#Declaracion de rutas
# ruta Index http://localhost:5000
# ruta se compone del nombre y la funcion
@app.route('/')
def index():
    
    # Devolver la vista como respuesta
    return render_template('index.html')


@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        titulo = request.form['txtTitulo']
        artista = request.form['txtArtista']
        anio = request.form['txtAnio']
        print(titulo, artista, anio)
    
    return "La info del Album llegó a su ruta, amigo ;)"


@app.route('/eliminar')
def eliminar():
    return "Se Elimino el album en la BD"

# Ejecucion
if __name__== '__main__':
    app.run(port= 5000, debug=True)