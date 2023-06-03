import tkinter as tk
from tkinter import ttk
import mysql.connector

# Establecer la conexión con la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="almacenbeb",
    database="bebidas"
)

# Crear el cursor para ejecutar las consultas
cursor = conexion.cursor()

def mostrar_registros():
    # Consultar los datos de la tabla Bebidas con los nombres de clasificación y marca asociados
    consulta = """
    SELECT b.id, b.Nombre, b.Precio, c.clasificacion, m.Marca
    FROM Bebidas b
    JOIN Clasificaciones c ON b.id_clasificacion = c.id
    JOIN Marca m ON b.id_marca = m.id
    """
    cursor.execute(consulta)
    bebidas = cursor.fetchall()

    # Crear un widget Treeview para mostrar los registros en una tabla
    tabla_registros = ttk.Treeview(pestaña_mostrar, columns=("ID", "Nombre", "Precio", "Clasificación", "Marca"), show="headings")

    # Eliminar los widgets existentes en la pestaña

        
    # Configurar las columnas de la tabla
    tabla_registros.heading("ID", text="ID")
    tabla_registros.heading("Nombre", text="Nombre")
    tabla_registros.heading("Precio", text="Precio")
    tabla_registros.heading("Clasificación", text="Clasificación")
    tabla_registros.heading("Marca", text="Marca")

    # Mostrar los datos obtenidos en la tabla
    for bebida in bebidas:
        tabla_registros.insert("", tk.END, values=(bebida[0], bebida[1], bebida[2], bebida[3], bebida[4]))

    tabla_registros.pack(fill="both", expand=True)

def agregar_registro():
    # Crear etiquetas y campos de entrada para los datos del nuevo registro
    etiqueta_nombre = tk.Label(pestaña_agregar, text="Nombre:")
    etiqueta_nombre.pack()
    campo_nombre = tk.Entry(pestaña_agregar)
    campo_nombre.pack()

    etiqueta_precio = tk.Label(pestaña_agregar, text="Precio:")
    etiqueta_precio.pack()
    campo_precio = tk.Entry(pestaña_agregar)
    campo_precio.pack()

    etiqueta_id_clasificacion = tk.Label(pestaña_agregar, text="ID Clasificación:")
    etiqueta_id_clasificacion.pack()
    campo_id_clasificacion = tk.Entry(pestaña_agregar)
    campo_id_clasificacion.pack()

    etiqueta_id_marca = tk.Label(pestaña_agregar, text="ID Marca:")
    etiqueta_id_marca.pack()
    campo_id_marca = tk.Entry(pestaña_agregar)
    campo_id_marca.pack()
    
    def agregar():
        nombre = campo_nombre.get()
        precio = campo_precio.get()
        id_clasificacion = campo_id_clasificacion.get()
        id_marca = campo_id_marca.get()

        # Insertar el nuevo registro en la tabla Bebidas
        consulta = """
        INSERT INTO Bebidas (Nombre, Precio, id_clasificacion, id_marca)
        VALUES (%s, %s, %s, %s)
        """
        valores = (nombre, precio, id_clasificacion, id_marca)
        cursor.execute(consulta, valores)
        conexion.commit()

        # Mostrar mensaje de confirmación
        etiqueta_confirmacion.config(text="Registro agregado correctamente")

    # Crear un botón para agregar el registro
    boton_agregar = tk.Button(pestaña_agregar, text="Agregar", command=agregar)
    boton_agregar.pack()

    # Crear una etiqueta para mostrar mensajes de confirmación
    etiqueta_confirmacion = tk.Label(pestaña_agregar)
    etiqueta_confirmacion.pack()

def eliminar_registro():
    # Crear una etiqueta y un campo de entrada para el ID del registro a eliminar
    etiqueta_id = tk.Label(pestaña_eliminar, text="ID del registro a eliminar:")
    etiqueta_id.pack()
    campo_id = tk.Entry(pestaña_eliminar)
    campo_id.pack()

    def eliminar():
        id_registro = campo_id.get()

        # Eliminar el registro con el ID especificado de la tabla Bebidas
        consulta = "DELETE FROM Bebidas WHERE id = %s"
        valores = (id_registro,)
        cursor.execute(consulta, valores)
        conexion.commit()

        # Mostrar mensaje de confirmación
        etiqueta_confirmacion.config(text="Registro eliminado correctamente")

    # Crear un botón para eliminar el registro
    boton_eliminar = tk.Button(pestaña_eliminar, text="Eliminar", command=eliminar)
    boton_eliminar.pack()

    # Crear una etiqueta para mostrar mensajes de confirmación
    etiqueta_confirmacion = tk.Label(pestaña_eliminar)
    etiqueta_confirmacion.pack()

def actualizar_registro():
    # Crear etiquetas y campos de entrada para los datos del registro a actualizar
    etiqueta_id = tk.Label(pestaña_actualizar, text="ID del registro a actualizar:")
    etiqueta_id.pack()
    campo_id = tk.Entry(pestaña_actualizar)
    campo_id.pack()

    etiqueta_nombre = tk.Label(pestaña_actualizar, text="Nuevo nombre:")
    etiqueta_nombre.pack()
    campo_nombre = tk.Entry(pestaña_actualizar)
    campo_nombre.pack()

    etiqueta_precio = tk.Label(pestaña_actualizar, text="Nuevo precio:")
    etiqueta_precio.pack()
    campo_precio = tk.Entry(pestaña_actualizar)
    campo_precio.pack()

    def actualizar():
        id_registro = campo_id.get()
        nombre = campo_nombre.get()
        precio = campo_precio.get()

        # Actualizar el registro con los nuevos valores en la tabla Bebidas
        consulta = "UPDATE Bebidas SET Nombre = %s, Precio = %s WHERE id = %s"
        valores = (nombre, precio, id_registro)
        cursor.execute(consulta, valores)
        conexion.commit()

        # Mostrar mensaje de confirmación
        etiqueta_confirmacion.config(text="Registro actualizado correctamente")

    # Crear un botón para actualizar el registro
    boton_actualizar = tk.Button(pestaña_actualizar, text="Actualizar", command=actualizar)
    boton_actualizar.pack()

    # Crear una etiqueta para mostrar mensajes de confirmación
    etiqueta_confirmacion = tk.Label(pestaña_actualizar)
    etiqueta_confirmacion.pack()

def calcular_precio_promedio():
    # Calcular el precio promedio de las bebidas
    consulta = "SELECT AVG(Precio) FROM Bebidas"
    cursor.execute(consulta)
    resultado = cursor.fetchone()[0]

    # Mostrar el resultado en una etiqueta
    etiqueta_resultado = tk.Label(pestaña_calcular)
    etiqueta_resultado.config(text=f"Precio promedio de las bebidas: {resultado}")
    etiqueta_resultado.pack()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Bebidas")
ventana.geometry("600x400")

# Crear un control de pestañas para navegar entre las diferentes funcionalidades
pestañas = ttk.Notebook(ventana)

# Crear las pestañas para mostrar, agregar, eliminar, actualizar y calcular
pestaña_mostrar = ttk.Frame(pestañas)
pestaña_agregar = ttk.Frame(pestañas)
pestaña_eliminar = ttk.Frame(pestañas)
pestaña_actualizar = ttk.Frame(pestañas)
pestaña_calcular = ttk.Frame(pestañas)

# Agregar las pestañas al control de pestañas
pestañas.add(pestaña_mostrar, text="Mostrar Registros")
pestañas.add(pestaña_agregar, text="Agregar Registro")
pestañas.add(pestaña_eliminar, text="Eliminar Registro")
pestañas.add(pestaña_actualizar, text="Actualizar Registro")
pestañas.add(pestaña_calcular, text="Calcular Precio Promedio")

# Mostrar el control de pestañas
pestañas.pack(expand=True, fill="both")

# Crear una etiqueta para mostrar el resultado del cálculo del precio promedio
etiqueta_resultado = tk.Label(pestaña_calcular)
etiqueta_resultado.pack()

# Crear botones para cada funcionalidad
boton_mostrar = tk.Button(pestaña_mostrar, text="Mostrar Registros", command=mostrar_registros)
boton_mostrar.pack()

boton_agregar = tk.Button(pestaña_agregar, text="Agregar Registro", command=agregar_registro)
boton_agregar.pack()

boton_eliminar = tk.Button(pestaña_eliminar, text="Eliminar Registro", command=eliminar_registro)
boton_eliminar.pack()

boton_actualizar = tk.Button(pestaña_actualizar, text="Actualizar Registro", command=actualizar_registro)
boton_actualizar.pack()

boton_calcular = tk.Button(pestaña_calcular, text="Calcular Precio Promedio", command=calcular_precio_promedio)
boton_calcular.pack()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()

# Cerrar la conexión y liberar los recursos
cursor.close()
conexion.close()
