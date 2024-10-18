import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random

# Función para crear la base de datos y las tablas
def crear_base_datos():
    try:
        # Conexión al servidor MySQL
        
        conexion = mysql.connector.connect(
            host='localhost',  # Cambia por la dirección de tu servidor MySQL
            user='root',       # Cambia por tu usuario
            password='psw@Sena2024',  # Cambia por tu contraseña
        )
        if conexion.is_connected():
            cursor = conexion.cursor()

            # Crear la base de datos
            cursor.execute("CREATE DATABASE IF NOT EXISTS hoy")
            cursor.execute("USE hoy")

            # Crear tabla de clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20),
                    nacio ENUM('Hombre', 'Mujer') DEFAULT 'Hombre'
                )
            """)

            print("Base de datos y tablas creadas exitosamente.")
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada.")

def llenartabla():
    db = mysql.connector.connect(
        host='localhost', user='root', password='psw@Sena2024', database="hoy" # Acá también se debe cambiar los dastos de la base de datos
    )

    cursor = db.cursor()
    fake = Faker()
    
    nombres_masculinos = [fake.name_male() for _ in range(25)]
    nombres_femeninos = [fake.name_female() for _ in range(25)]

    # Generar y agregar 50 registros
    for _ in range(50):
        
        nombre = random.choice(nombres_masculinos + nombres_femeninos)
        telefono = f"{random.randint(300, 324)}-{random.randint(1000000, 9999999)}"
        nacio = 'Hombre' if nombre in nombres_masculinos else 'Mujer'
        
        query = "INSERT INTO clientes (nombre, telefono, nacio) VALUES (%s, %s, %s)"
        values = (nombre, telefono, nacio)
        cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    print("50 registros agregados a la tabla cliente.")

'''
    Creo una clase para manejar solicitudes HTTP.
    Al heredar de esta clase, RequestHandler podrá gestionar solicitudes
    de manera sencilla y personalizada.
'''
class RequestHandler(BaseHTTPRequestHandler):
    db = mysql.connector.connect(
        host='localhost', user='root', password='psw@Sena2024', database="hoy" # Acá también se debe cambiar los dastos de la base de datos
    )
    '''
        Este bloque de codigo se encarga de configurar y enviar la respuesta HTTP a una solicitud del cliente.
    '''
    def _set_response(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    '''
        Este bloque de codigo se encarga de manejar las solicitudes HTTP GET que llegan al servidor.
    '''
    def do_GET(self):
        if self.path == '/clientes/mujeres':
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes WHERE nacio = 'Mujer'")
            mujeres = cursor.fetchall()
            '''
                Se llama al método _set_response para configurar la respuesta HTTP,
                estableciendo el código de estado (200) y el tipo de contenido (JSON) para la respuesta.
            '''
            self._set_response()

            #Esta línea convierte la lista de mujeres (una lista de diccionarios) a formato JSON usando json.dumps().
            self.wfile.write(json.dumps(mujeres, indent=4).encode('utf-8'))

        else:
            self.send_response(404)
            self.wfile.write(b"404 Not Found")


'''
    Este bloque de codigo define una función llamada run, que se encarga de iniciar un servidor HTTP
    utilizando la clase HTTPServer y el manejador de solicitudes definido por RequestHandler.
'''
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor iniciado en puerto {port}, abrir el navegador o herramienta de solicitudes para obtener el json con esta dirección: http://localhost:{port}/clientes/mujeres')
    httpd.serve_forever()


# Ejecutar la función
crear_base_datos()
llenartabla()

if __name__ == "__main__":
    run()