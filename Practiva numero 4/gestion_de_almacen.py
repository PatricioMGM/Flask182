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

# Declarar la variable global para tabla_registros
tabla_registros = None

def mostrar_registros():
    global tabla_registros

    # Eliminar los registros existentes en la tabla si ya existe
    if tabla_registros:
        tabla_registros.destroy()

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

    # Configurar las columnas de la tabla
    tabla_registros.heading("ID", text="ID")
    tabla_registros.heading("Nombre", text="Nombre")
    tabla_registros.heading("Precio", text="Precio")
    tabla_registros.heading("Clasificación", text="Clasificación")
    tabla_registros.heading("Marca", text="Marca")

    # Mostrar los datos obtenidos en la tabla
    for bebida in bebidas:
        tabla_registros.insert("", tk.END, values=(bebida[0], bebida[1], bebida[2], bebida[3], bebida[4]))

    # Ajustar el tamaño de la tabla al cambiar el tamaño de la ventana
    tabla_registros.pack(fill="both", expand=True)
    tabla_registros.bind("<Configure>", lambda e: tabla_registros.pack_configure(expand=True))

    # Centrar los registros en la tabla
    for column in ("ID", "Nombre", "Precio", "Clasificación", "Marca"):
        tabla_registros.column(column, anchor="center")

    # Establecer el ancho de las columnas de la tabla
    tabla_registros.column("ID", width=50)
    tabla_registros.column("Nombre", width=100)
    tabla_registros.column("Precio", width=80)
    tabla_registros.column("Clasificación", width=100)
    tabla_registros.column("Marca", width=100)


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

    # Obtener las clasificaciones de la base de datos
    cursor.execute("SELECT id, clasificacion FROM Clasificaciones")
    clasificaciones = cursor.fetchall()
    clasificaciones_ids = [clasificacion[0] for clasificacion in clasificaciones]
    clasificaciones_nombres = [clasificacion[1] for clasificacion in clasificaciones]

    # Obtener las marcas de la base de datos
    cursor.execute("SELECT id, Marca FROM Marca")
    marcas = cursor.fetchall()
    marcas_ids = [marca[0] for marca in marcas]
    marcas_nombres = [marca[1] for marca in marcas]

    etiqueta_clasificacion = tk.Label(pestaña_agregar, text="Clasificación:")
    etiqueta_clasificacion.pack()
    campo_clasificacion = ttk.Combobox(pestaña_agregar, values=clasificaciones_nombres)
    campo_clasificacion.pack()

    etiqueta_marca = tk.Label(pestaña_agregar, text="Marca:")
    etiqueta_marca.pack()
    campo_marca = ttk.Combobox(pestaña_agregar, values=marcas_nombres)
    campo_marca.pack()

    def agregar():
        nombre = campo_nombre.get()
        precio = campo_precio.get()
        id_clasificacion = clasificaciones_ids[clasificaciones_nombres.index(campo_clasificacion.get())]
        id_marca = marcas_ids[marcas_nombres.index(campo_marca.get())]

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

    etiqueta_clasificacion = tk.Label(pestaña_actualizar, text="Nueva clasificación:")
    etiqueta_clasificacion.pack()
    combobox_clasificacion = ttk.Combobox(pestaña_actualizar)
    combobox_clasificacion.pack()

    etiqueta_marca = tk.Label(pestaña_actualizar, text="Nueva marca:")
    etiqueta_marca.pack()
    combobox_marca = ttk.Combobox(pestaña_actualizar)
    combobox_marca.pack()

    def actualizar():
        id_registro = campo_id.get()
        nombre = campo_nombre.get()
        precio = campo_precio.get()
        id_clasificacion = clasificaciones_ids[combobox_clasificacion.current()]
        id_marca = marcas_ids[combobox_marca.current()]

        # Actualizar el registro con los nuevos valores en la tabla Bebidas
        consulta = "UPDATE Bebidas SET Nombre = %s, Precio = %s, id_clasificacion = %s, id_marca = %s WHERE id = %s"
        valores = (nombre, precio, id_clasificacion, id_marca, id_registro)
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

    # Obtener las clasificaciones de la base de datos
    cursor.execute("SELECT id, clasificacion FROM Clasificaciones")
    clasificaciones = cursor.fetchall()
    clasificaciones_ids = [clasificacion[0] for clasificacion in clasificaciones]
    clasificaciones_nombres = [clasificacion[1] for clasificacion in clasificaciones]

    # Obtener las marcas de la base de datos
    cursor.execute("SELECT id, Marca FROM Marca")
    marcas = cursor.fetchall()
    marcas_ids = [marca[0] for marca in marcas]
    marcas_nombres = [marca[1] for marca in marcas]

    # Establecer las opciones de clasificación y marca en los comboboxes
    combobox_clasificacion['values'] = clasificaciones_nombres
    combobox_marca['values'] = marcas_nombres



def calcular_precio_promedio():
    # Limpiar la pestaña antes de calcular el precio promedio
    for widget in pestaña_calcular.winfo_children():
        if widget != boton_calcular:  # Evitar eliminar el botón
            widget.destroy()
    
    # Calcular el precio promedio de las bebidas
    consulta_promedio = "SELECT AVG(Precio) FROM Bebidas"
    cursor.execute(consulta_promedio)
    precio_promedio = cursor.fetchone()[0]

    # Mostrar el resultado del precio promedio en una etiqueta
    etiqueta_promedio = tk.Label(pestaña_calcular)
    etiqueta_promedio.config(text=f"Precio promedio de las bebidas: {round(precio_promedio, 2)}")
    etiqueta_promedio.pack()

    # Consultar la cantidad de bebidas por marca
    consulta_marca = """
    SELECT m.Marca, COUNT(*) AS Cantidad
    FROM Bebidas b
    JOIN Marca m ON b.id_marca = m.id
    GROUP BY m.Marca
    """
    cursor.execute(consulta_marca)
    marcas = cursor.fetchall()

    # Mostrar la cantidad de bebidas por marca en una etiqueta
    etiqueta_marcas = tk.Label(pestaña_calcular)
    etiqueta_marcas.config(text="Cantidad de bebidas por marca:")
    etiqueta_marcas.pack()

    for marca in marcas:
        etiqueta_marca = tk.Label(pestaña_calcular)
        etiqueta_marca.config(text=f"{marca[0]}: {marca[1]} bebidas")
        etiqueta_marca.pack()

    # Consultar la cantidad de bebidas por clasificación
    consulta_clasificacion = """
    SELECT c.clasificacion, COUNT(*) AS Cantidad
    FROM Bebidas b
    JOIN Clasificaciones c ON b.id_clasificacion = c.id
    GROUP BY c.clasificacion
    """
    cursor.execute(consulta_clasificacion)
    clasificaciones = cursor.fetchall()

    # Mostrar la cantidad de bebidas por clasificación en una etiqueta
    etiqueta_clasificaciones = tk.Label(pestaña_calcular)
    etiqueta_clasificaciones.config(text="Cantidad de bebidas por clasificación:")
    etiqueta_clasificaciones.pack()

    for clasificacion in clasificaciones:
        etiqueta_clasificacion = tk.Label(pestaña_calcular)
        etiqueta_clasificacion.config(text=f"{clasificacion[0]}: {clasificacion[1]} bebidas")
        etiqueta_clasificacion.pack()


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
pestañas.add(pestaña_calcular, text="Calculos")

# Mostrar el control de pestañas
pestañas.pack(expand=True, fill="both")

# Llamar a las funciones correspondientes para mostrar el contenido en las pestañas

agregar_registro()
eliminar_registro()
actualizar_registro()

# Crear una etiqueta para mostrar el resultado del cálculo del precio promedio
etiqueta_resultado = tk.Label(pestaña_calcular)
etiqueta_resultado.pack()

# Crear botones para cada funcionalidad
boton_mostrar = tk.Button(pestaña_mostrar, text="Mostrar Registros", command=mostrar_registros)
boton_mostrar.pack()

boton_calcular = tk.Button(pestaña_calcular, text="Calcular Precio Promedio", command=calcular_precio_promedio)
boton_calcular.pack()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()

# Cerrar la conexión y liberar los recursos
cursor.close()
conexion.close()
