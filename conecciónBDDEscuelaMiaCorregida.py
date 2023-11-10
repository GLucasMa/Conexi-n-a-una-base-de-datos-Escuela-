import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

#AGU CONNECTION STRING 
# conexion = mysql.connector.connect(host="localhost", user="root", password="123456789", database="ESCUELA")
#CONNECTION STRING LUCAS
conexion = mysql.connector.connect(host="127.0.0.1", user="root", password="root",port=3305 ,database="ESCUELA")
def cargar_datos():
    # (*) Desempaquetar datos y traerlos separados
    # (get_children) Funcion pre hecha 
    tree.delete(*tree.get_children())
    cursor = conexion.cursor()
    #cursor.execute("SELECT Alumnos.IdAlumno, Alumnos.Nombre, Alumnos.Apellido, Carreras.Nombre, Alumnos.DNI, EstadoAlumno.Nombre FROM Alumnos JOIN Carreras ON Alumnos.IdCarrera = Carreras.IdCarrera JOIN EstadoAlumno ON Alumnos.IdEstadoAlumno = EstadoAlumno.IdEstadoAlumno")
    #AGU NUEVA SENTENCIA PARA ORDEN POR EL IDALUMNO MAS ALTO EN LA PRIMER FILA, SI QUIERES AL REVES QUITAS ASC POR DESC
    cursor.execute("SELECT Alumnos.IdAlumno, Alumnos.Nombre, Alumnos.Apellido, Carreras.Nombre, Alumnos.DNI, EstadoAlumno.Nombre FROM Alumnos JOIN Carreras ON Alumnos.IdCarrera = Carreras.IdCarrera JOIN EstadoAlumno ON Alumnos.IdEstadoAlumno = EstadoAlumno.IdEstadoAlumno WHERE Alumnos.IdEstadoAlumno = 2 ORDER BY Alumnos.IdAlumno ASC")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row) #El primer argumento que le pasamos a insert() es un ítem o una cadena vacía ("") para indicar que el nuevo ítem no tiene predecesor.

def cargar_datos_sin_estado():
    # (*) Desempaquetar datos y traerlos separados
    # (get_children) Funcion pre hecha 
    tree.delete(*tree.get_children())
    cursor = conexion.cursor()
    #cursor.execute("SELECT Alumnos.IdAlumno, Alumnos.Nombre, Alumnos.Apellido, Carreras.Nombre, Alumnos.DNI, EstadoAlumno.Nombre FROM Alumnos JOIN Carreras ON Alumnos.IdCarrera = Carreras.IdCarrera JOIN EstadoAlumno ON Alumnos.IdEstadoAlumno = EstadoAlumno.IdEstadoAlumno")
    #AGU NUEVA SENTENCIA PARA ORDEN POR EL IDALUMNO MAS ALTO EN LA PRIMER FILA, SI QUIERES AL REVES QUITAS ASC POR DESC
    cursor.execute("SELECT Alumnos.IdAlumno, Alumnos.Nombre, Alumnos.Apellido, Carreras.Nombre, Alumnos.DNI, EstadoAlumno.Nombre FROM Alumnos JOIN Carreras ON Alumnos.IdCarrera = Carreras.IdCarrera JOIN EstadoAlumno ON Alumnos.IdEstadoAlumno = EstadoAlumno.IdEstadoAlumno ORDER BY Alumnos.IdAlumno ASC")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row) #El primer argumento que le pasamos a insert() es un ítem o una cadena vacía ("") para indicar que el nuevo ítem no tiene predecesor.


def cargar_carreras():
    cursor = conexion.cursor()
    cursor.execute("SELECT IdCarrera, Nombre FROM Carreras ORDER BY NOMBRE")
    carreras = cursor.fetchall()
    carrera_combobox['values'] = [row[1] for row in carreras]
    return carreras#                                                                         } Estos son
#                                                                                            }  para los            
def cargar_estadoAlumno():#                                                                  }  combobox  
    cursor = conexion.cursor()
    cursor.execute("SELECT idestadoalumno, nombre FROM estadoalumno")
    estadoAlumno = cursor.fetchall()
    estadoAlumno_combobox['values'] = [row[1] for row in estadoAlumno]
    return estadoAlumno 

def mostrar_alerta(mensaje): 
    messagebox.showwarning("Alerta", mensaje)

def guardar_alumno():
    nombre = nombre_entry.get().upper()
    apellido = apellido_entry.get().upper()
    dni = dni_entry.get().upper()
    carrera_nombre = carrera_combobox.get()
    estado_alumno = 2  

    if nombre and apellido and dni and carrera_nombre:
        if not dni.isdigit() or len(dni) != 8:
            mostrar_alerta("El dni debe contener exactamente 8 números")
            return
        carreras = cargar_carreras()
        carrera_id = None
        for carrera in carreras:
            if carrera[1] == carrera_nombre:
                carrera_id = carrera[0]
                break
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Alumnos (Nombre, Apellido, DNI, IdCarrera, IdEstadoAlumno) VALUES (%s,%s,%s,%s,%s)", (nombre,apellido,dni,carrera_id,estado_alumno))
        conexion.commit()
        cargar_datos()
        nombre_entry.delete(0, tk.END)
        apellido_entry.delete(0, tk.END)
        dni_entry.delete(0, tk.END)
        carrera_combobox.set("") 
    else:
        mostrar_alerta("Los campos son obligatorios. Debe completarlos.")

""" def seleccionar_registro(event):
    item = tree.selection()[0]  # Obtener el ítem seleccionado en el Treeview
    habilitar_modificar(event)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Alumnos JOIN Carreras ON Alumnos.IDCARRERA = Carreras.IDCARRERA WHERE Alumnos.NOMBRE = %s", (tree.item(item, "values")[0],))
    registro = cursor.fetchone()

    if registro:
        # Actualizar los campos del formulario con los datos del registro seleccionado
        nombre_entry.delete(0, tk.END)
        nombre_entry.insert(0, registro[1])
        apellido_entry.delete(0, tk.END)
        apellido_entry.insert(0, registro[2])
        dni_entry.delete(0, tk.END)
        dni_entry.insert(0, registro[3])
        carrera_combobox.set(registro[5])  # Suponiendo que el nombre de la carrera está en la sexta posición """

#AGU Función para habilitar el botón Modificar cuando se selecciona un registro en el Treeview
def habilitar_modificar(event):
    if tree.selection():
        modificar_button.config(state=tk.NORMAL)
        guardar_button.config(state=tk.DISABLED)
        
def seleccionar_registro(event):
    estadoAlumno_combobox.config(state=tk.NORMAL)
    item = tree.selection()[0]  # traes el ítem seleccionado en el Treeview(grilla)
    habilitar_modificar(event) #AGU llamamos a la funcion que deshabilita el "guardar"
    valores = tree.item(item, "values")  # obtenes los valores del ítem seleccionado
    # cargas los campos del formulario con los valores seleccionados
    nombre_entry.delete(0, tk.END)
    apellido_entry.delete(0, tk.END)
    dni_entry.delete(0, tk.END)
    carrera_combobox.set("")
    # AGU SE AÑADE COMBOBOX ESTADO ALUMNO 
    estadoAlumno_combobox.set("")
    
    nombre_entry.insert(0, valores[1])
    apellido_entry.insert(0, valores[2])
    dni_entry.insert(0, valores[4]) #AGU el nº q esta entre corchetes indica la columna en la q se encuentra el dato
    carrera_combobox.set(valores[3])
    estadoAlumno_combobox.set(valores[5])

def modificar_alumno():
    item = tree.selection()[0]  # Obtener el ítem seleccionado en el Treeview
    alumno_id = tree.item(item, "values")[0]  # Obtener el ID del alumno seleccionado
    nombre = nombre_entry.get().upper()
    apellido = apellido_entry.get().upper()
    dni = dni_entry.get()
    carrera_nombre = carrera_combobox.get()
    estado_alumno = estadoAlumno_combobox.get()

    if nombre and apellido and dni and carrera_nombre and estado_alumno:
        #Obtener el ID de la carrera seleccionada
        carreras = cargar_carreras()
        carrera_id = None
        for carrera in carreras:
            if carrera[1] == carrera_nombre:
                carrera_id = carrera[0]
                break

        #AGU se añade la carga del combo para estado alumno
        estados = cargar_estadoAlumno()
        estado_id = None
        for estado in estados:
            if estado[1] == estado_alumno:
                estado_id = estado[0]
                break

        cursor = conexion.cursor()
        #Actualizar el registro en la tabla Alumnos con los nuevos datos
        #se añade q levante el idestadoalumno seleccionado del formulario de edicion y lo updatee en la query de la bdd
        #cursor.execute("UPDATE Alumnos SET NOMBRE = %s, APELLIDO = %s, DNI = %s, IDCARRERA = %s, IDESTADOALUMNO = %s WHERE IDALUMNO = %s", (alumno_id, nombre, apellido, dni, carrera_id, estado_id ))
        cursor.execute("UPDATE Alumnos SET NOMBRE = %s, APELLIDO = %s, DNI = %s, IDCARRERA = %s, IDESTADOALUMNO = %s WHERE IDALUMNO = %s", (nombre, apellido, dni, carrera_id, estado_id, alumno_id))
        conexion.commit()
        guardar_button.config(state=tk.NORMAL)
        cargar_datos()  # Actualizar la vista
        #Limpiar los campos después de actualizar
        nombre_entry.delete(0, tk.END)
        apellido_entry.delete(0, tk.END)
        dni_entry.delete(0, tk.END)
        carrera_combobox.set("")  # Limpiar la selección del ComboBox
        #Deshabilitar el botón Modificar después de la modificación
        estadoAlumno_combobox.set("")

        # AGU ESTO LO COMENTO PORQUE ESTA MAL , TIENE QUE ESTAR HABILITADO ->modificar_button.config(state=tk.DISABLED)
        #Habilitar el botón Guardar
        # AGU MAL ->guardar_button.config(state=tk.NORMAL)
        
    else:
        mostrar_alerta("Los campos son obligatorios. Debe completarlos.")

def eliminar_alumno():
    item = tree.selection()[0]  # Obtener el ítem seleccionado en el Treeview
    alumno_id = tree.item(item, "values")[0]  # Obtener el ID del alumno seleccionado

    if alumno_id:
        respuesta = messagebox.askquestion("Confirmación", "¿Estás seguro de que deseas eliminar este alumno?")
        if respuesta == "yes":
            cursor = conexion.cursor()
            cursor.execute("UPDATE Alumnos SET IdEstadoAlumno = 4 WHERE IdAlumno = %s", (alumno_id,))
            conexion.commit()
            cargar_datos()  # Actualizar la vista
            mostrar_alerta("Alumno eliminado correctamente.")
    else:
        mostrar_alerta("Por favor, seleccione un alumno de la lista.")

# Crear ventana
root = tk.Tk()
root.title("Consulta de Alumnos")
root.configure(background='lightblue')
# img = tk.PhotoImage(file="ISAUILogo.png")
# lbl_img = tk.Label(root, image=img)
# lbl_img.pack(row=0, column=0, columnspan=2, pady=10)

# Crear un frame con un borde visible para el formulario de inscripción
formulario_frame = tk.Frame(root, bd=2, relief=tk.SOLID)
formulario_frame.pack(padx=10, pady=10)

# Título del formulario
titulo_label = tk.Label(formulario_frame, text="Formulario Inscripción", font=("Humanst521 Lt BT", 14))
titulo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Campos de entrada para nombre, apellido y DNI con el mismo ancho que el ComboBox
nombre_label = tk.Label(formulario_frame, text="Nombre:", font=("Humanst521 Lt BT", 12))
nombre_label.grid(row=1, column=0)
nombre_entry = tk.Entry(formulario_frame)
nombre_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

apellido_label = tk.Label(formulario_frame, text="Apellido:", font=("Humanst521 Lt BT", 12))
apellido_label.grid(row=2, column=0)
apellido_entry = tk.Entry(formulario_frame)
apellido_entry.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

# Combo box para la carrera
carrera_label = tk.Label(formulario_frame, text="Carrera:", font=("Humanst521 Lt BT", 12))
carrera_label.grid(row=3, column=0)
carrera_combobox = ttk.Combobox(formulario_frame,  state="readonly")# Configurar el ComboBox como de solo lectura
carrera_combobox.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

dni_label = tk.Label(formulario_frame, text="DNI:", font=("Humanst521 Lt BT", 12))
dni_label.grid(row=4, column=0)
dni_entry = tk.Entry(formulario_frame)
dni_entry.grid(row=4, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

# Combo box para el estado alumno
estadoAlumno_label = tk.Label(formulario_frame, text="Estado del alumno:", font=("Humanst521 Lt BT", 12))
estadoAlumno_label.grid(row=5, column=0)
estadoAlumno_combobox = ttk.Combobox(formulario_frame,  state="readonly", )# Configurar el ComboBox como de solo lectura
estadoAlumno_combobox.config(state=tk.DISABLED)
estadoAlumno_combobox.grid(row=5, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

# Cargar las carreras al inicio de la aplicación y obtener la lista de carreras con sus IDs
carreras = cargar_carreras()
estado_alumno = cargar_estadoAlumno()

# Botón para modificar registro de alumno
modificar_button = tk.Button(formulario_frame, text="Modificar", font=("Humanst521 Lt BT", 12, "bold"), command=modificar_alumno, background="CadetBlue")
modificar_button.grid(row=6, column=0, columnspan=1, padx=5, pady=10, ipadx=10,sticky="ew")

# Botón para guardar un nuevo registro de alumno
guardar_button = tk.Button(formulario_frame, text="Guardar", font=("Humanst521 Lt BT", 12, "bold"), command= guardar_alumno, background="green")
guardar_button.grid(row=6, column=1, columnspan=1, padx=25, pady=10, ipadx=15, sticky="ew")

# Botón para eliminar un registro de alumno
eliminar_button = tk.Button(formulario_frame, text="Eliminar", font=("Humanst521 Lt BT", 12, "bold"), command= eliminar_alumno, background="red")
eliminar_button.grid(row=6, column=2, columnspan=1, padx=5, pady=10, ipadx=25, sticky="ew")

# Crear Treeview para mostrar la información
tree = ttk.Treeview(root, columns=("Id","Nombre", "Apellido", "Carrera", "DNI","Estado"))
tree.heading("#1", text="Id")
tree.heading("#2", text="Nombre")
tree.heading("#3", text="Apellido")
tree.heading("#4", text="Carrera")
tree.heading("#5", text="DNI")
tree.heading("#6", text="Estado")

tree.column("#0", width=0, stretch=tk.NO)  # Ocultar la columna #0 que habitualmente muestra las primary key de los objetos

tree.pack(padx=10, pady=10)

# Asociar la función seleccionar_registro con el evento de selección en el Treeview
tree.bind("<ButtonRelease-1>", seleccionar_registro)

# Botón para cargar datos
cargar_button = tk.Button(root, text="Cargar Datos",font=("Humanst521 Lt BT", 12), command=cargar_datos)
cargar_button.pack(pady=5)

# Ejecutar la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos al cerrar la aplicación
conexion.close()
