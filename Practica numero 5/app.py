
import mysql.connector
from flask import Flask


#inicializion del servidor flask
app = Flask(__name__)


#Declaracion de rutas

# Configurar la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbflask'

# Crear una instancia de conexión
db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

# ruta Index http://localhost:5000
# ruta se compone del nombre y la funcion
@app.route('/')
def index():
    # Realizar la consulta a la tabla
    cursor = db.cursor()
    cursor.execute("SELECT id, nombre FROM nombres")
    results = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    db.close()

    # Construir una cadena de texto con los resultados de la consulta
    response = "ID\tNombre\n"
    for result in results:
        response += f"{result[0]}\t{result[1]}\n"

    # Devolver la cadena de texto como respuesta
    return response


@app.route('/guardar')
def guardar():
    return "Se gurado el album en la BD"

@app.route('/eliminar')
def eliminar():
    return "Se Elimino el album en la BD"



# Ejecucion
if __name__== '__main__':
    app.run(port= 5000, debug=True)