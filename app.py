#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
#from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Usuarios:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database, port=3307):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
			port=port
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            imagen_url VARCHAR(255)
        )''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    # creamos una función para insertar registros

    def agregar_usuario(self, nombre, apellido, email, imagen):
        sql = "INSERT INTO usuarios (nombre, apellido, email, imagen_url) VALUES (%s, %s, %s, %s)"
        valores = (nombre, apellido, email, imagen)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid

    #----------------------------------------------------------------
    def consultar_usuario(self, id):
        # Consultamos un usuario a partir de su id
        self.cursor.execute(f"SELECT * FROM usuarios WHERE id = {id}")
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_usuario(self, id, nuevo_nombre, nueva_imagen):
        sql = "UPDATE usuarios SET nombre = %s, imagen_url = %s WHERE id = %s"
        valores = (nuevo_nombre, nueva_imagen, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        usuarios = self.cursor.fetchall()
        return usuarios

    #----------------------------------------------------------------
    def eliminar_usuario(self, id):
        # Eliminamos un usuario de la tabla a partir de su id
        self.cursor.execute(f"DELETE FROM usuarios WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def mostrar_usuario(self, id):
        # Mostramos los datos de un usuario a partir de su id
        usuario = self.consultar_usuario(id)
        if usuario:
            print("-" * 5)
            print(f"ID.....:            {usuario['id']}")
            print(f"Nombre:             {usuario['nombre']}")
            print(f"apellido...:        {usuario['apellido']}")
            print(f"Contraseña.....:    {usuario['email']}")
            print(f"Imagen.....:        {usuario['imagen_url']}")
            print("-" * 5)
        else:
            print("Usuario no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Usuarios
usuarios = Usuarios(host='localhost', user='root', password='', database='miapp3', port=3307)


# Carpeta para guardar las imagenes.
RUTA_DESTINO = './Static/img'

#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
#RUTA_DESTINO = '/home/USUARIO/mysite/static/imagenes'


#--------------------------------------------------------------------
# Listar todos los usuarios
#--------------------------------------------------------------------
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios_list = usuarios.listar_usuarios()
    return jsonify(usuarios_list)


#--------------------------------------------------------------------
# Mostrar un solo usuario según su id
#--------------------------------------------------------------------
@app.route("/usuarios/<int:id>", methods=["GET"])
def mostrar_usuario(id):
    usuario = usuarios.consultar_usuario(id)
    if usuario:
        return jsonify(usuario), 201
    else:
        return "Usuario no encontrado", 404


#--------------------------------------------------------------------
# Agregar un usuario
#--------------------------------------------------------------------
@app.route("/usuarios", methods=["POST"])
def agregar_usuario():
    #Recojo los datos del form
    nombre =    request.form['nombre']
    apellido =  request.form['apellido']
    email =     request.form['email']
    imagen =    request.files['imagen']
    nombre_imagen=""

    
    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

    nuevo_id = usuarios.agregar_usuario(nombre, apellido, email, nombre_imagen)
    if nuevo_id:    
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        #Si el usuario se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Usuario agregado correctamente.", "id": nuevo_id, "imagen": nombre_imagen}), 201
    else:
        #Si el usuario no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el usuario."}), 500
    

#--------------------------------------------------------------------
# Modificar un usuario según su id
#--------------------------------------------------------------------
@app.route("/usuarios/<int:id>", methods=["PUT"])
def modificar_usuario(id):
    #Se recuperan los nuevos datos del formulario
    nuevo_nombre = request.form.get("nombre")
    nuevo_apellido = request.form.get("apellido")
    nueva_email = request.form.get("email")
    
    
    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        
        # Busco el usuario guardado
        usuario = usuarios.consultar_usuario(id)
        if usuario: # Si existe el usuario...
            imagen_vieja = usuario["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    
    else:
        # Si no se proporciona una nueva imagen, simplemente usa la imagen existente del usuario
        usuario = usuarios.consultar_usuario(id)
        if usuario:
            nombre_imagen = usuario["imagen_url"]


    # Se llama al método modificar_usuario pasando el id del usuario y los nuevos datos.
    if usuarios.modificar_usuario(id, nuevo_nombre, nombre_imagen):
        
        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Usuario modificado"}), 200
    else:
        #Si el usuario no se encuentra (por ejemplo, si no hay ningún usuario con el id dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Usuario no encontrado"}), 403



#--------------------------------------------------------------------
# Eliminar un usuario según su id
#--------------------------------------------------------------------
@app.route("/usuarios/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    # Busco el usuario en la base de datos
    usuario = usuarios.consultar_usuario(id)
    if usuario: # Si el usuario existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = usuario["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el usuario del catálogo
        if usuarios.eliminar_usuario(id):
            #Si el usuario se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Usuario eliminado"}), 200
        else:
            #Si ocurre un error durante la eliminación (por ejemplo, si el usuario no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar el usuario"}), 500
    else:
        #Si el usuario no se encuentra (por ejemplo, si no existe un usuario con el id proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

#--------------------------------------------------------------------

# Ruta raíz para mensaje de bienvenida o redirección
@app.route("/")
def index():
    return "¡Bienvenido a la aplicación de gestión de usuarios!"


if __name__ == "__main__":
    app.run(debug=True)
