from logging import exception
from pprint import pprint
from flask import Flask,render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL

# Crear la aplicacion en la var app > instancia
app = Flask(__name__)

# Parametros para la base de datos
app.config['MYSQL_HOST'] = '192.168.1.11'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Issac#corona'
app.config['MYSQL_DB'] = 'test'

conexion = MySQL(app)




# Decoradores
@app.before_request
def before_request():
    print("Antes de la petición.")

@app.after_request
def after_request(response):
    print("Antes de la petición.")
    return response 




# Crear metodo que hara si estamos en la ruta raiz 
@app.route('/')
def index(): # Esto es una vista (expresada como funcion)
    # return 'Texto plano'
    integrantes_ls = ["Jesus Bautista", "Daniel Galvan", "Alejandro Estrada",
                   "Brandon Vargas", "Alejandra Hernandez", "Issac Corona"]
    mydata = {
        'Titulo': "Pagina de ejemplo SMO",
        "Saludo": "Bienvenido a el ejemplo más basico",
        "Integrantes": integrantes_ls,
        "Numero_Integrantes": len(integrantes_ls)

    }
    return render_template('index.html', data = mydata)



# Se espera un parametro dentro de la url
# los <> Indican que se le puede escribir un parametro y manipularlo.
# Construccion de url dinamica atraves de cambio de parametros.
@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre,edad):
    mydata = {
        "Titulo": 'Contacto',
        "Nombre": nombre,
        "Edad": edad
    } 
    return render_template('contacto.html', data = mydata)

# request es una solicitud, lo que el cliente pide al servidor
# No tiene un route, pero se agregará una regla en main
def query_string():
    print(request)
    print(request.args)
    print(request.args.get('Parametro1'))
    print(request.args.get('Parametro2'))
    
    return "Ok"


# Vista para la base de datos.
@app.route("/datos")
def base_de_datos():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM master";
        cursor.execute(sql)

        datos_in = cursor.fetchall()
        # print(datos_in)
        data['Mensaje'] = 'Exito!'
        data['master'] = datos_in
    except Exception as ex:
        data['Mensaje'] = 'Error'

    return jsonify(data)


# Crear vista para el error 404
def pagina_no_encontrada(error):
    # return render_template('404.html'), 404 # Para enviar un mensaje de error
    return redirect(url_for('index')) # Re-direccion a otra plantilla









# Validacion: Si el nombre de la app se encuentra en la ruta principal 
if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func = query_string) # Regla que levanta la vista query_string
    app.register_error_handler(404, pagina_no_encontrada) # Manejador de error
    app.run(debug=True, port=80) # Si es así ejecutar la app

