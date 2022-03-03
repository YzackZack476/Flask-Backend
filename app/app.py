from logging import exception
from pprint import pprint
from flask import Flask,render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL
from src.config import config

# Crear la aplicacion en la var app > instancia
app = Flask(__name__)

conexion = MySQL(app)




# Decoradores
@app.before_request
def before_request():
    print(config)
    print("Antes de la petición.")

@app.after_request
def after_request(response):
    print("Despues de la petición.")
    return response 




# Crear metodo que hara si estamos en la ruta raiz 
@app.route('/')
def index(): # Esto es una vista (expresada como funcion)

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


# Api que trae los datos json de la Base de datos
@app.route("/api/get-data", methods=["GET"])
def base_de_datos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM master LIMIT 10";
        cursor.execute(sql)
        datos = cursor.fetchall()   # Devuelve los datos pero registro por registro
        
        data = [{
            'MENSAJE': "OK"
        }]   
        for fila in datos: # Acomoda los datos
            dato = {
                "PP_CODE" : fila[0],
                "MCH_CODE" : fila[1],
                "BLC_MACHINE_SIDE" : fila[2],
                "BLC_START" : fila[3],
                "WM_NAME" : fila[8],
                "WM_SURNAME" : fila[9]
            }
            data.append(dato)

    except Exception as ex:
        data.append({
            'Mensaje':'Error'
            }) 

    return jsonify(data) 





# Crear vista para el error 404
def pagina_no_encontrada(error):
    # return render_template('404.html'), 404 # Para enviar un mensaje de error
    return redirect(url_for('index')) # Re-direccion a otra plantilla





# Validacion: Si el nombre de la app se encuentra en la ruta principal 
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.add_url_rule('/query_string', view_func = query_string) # Regla que levanta la vista query_string
    app.register_error_handler(404, pagina_no_encontrada) # Manejador de error
    app.run() # Si es así ejecutar la app

