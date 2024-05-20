from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
import sqlite3

app = Flask(__name__)
api = Api(app)

def calcular_edad(fecha_nacimiento):
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
    hoy = datetime.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def verificar_ingresos(ingresos):
    if ingresos < 2000000:
        return "rechazar"
    elif 2000001 <= ingresos <= 4000000:
        return 2000000
    elif 4000001 <= 6000000:
        return 4000000
    elif 6000001 <= 8000000:
        return 6000000
    elif 8000001 <= 12000000:
        return 8000000
    else:
        return 10000000

def obtener_usuario(cc):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (cc,))
    usuario = cursor.fetchone()
    
    conn.close()
    return usuario

class VerificarTarjeta(Resource):
    def get(self, cc):
        usuario = obtener_usuario(cc)
        
        if usuario is None:
            return {"error": "No se encontraron datos para este número de identificación (cc)"}, 404

        nombre, fecha_nacimiento, ingresos, datacredito = usuario[1], usuario[2], usuario[3], usuario[4]
        edad = calcular_edad(fecha_nacimiento)

        if datacredito == "si":
            return {
                "mensaje": f"Lo siento, su solicitud de tarjeta de crédito ha sido rechazada debido a su historial en Datacredito.",
                "nombre": nombre,
                "edad": edad
            }, 200

        cupo = verificar_ingresos(ingresos)
        if cupo == "rechazar":
            return {
                "mensaje": "Lo siento, sus ingresos son demasiado bajos para ser aprobados para una tarjeta de crédito.",
                "nombre": nombre,
                "edad": edad
            }, 200

        return {
            "mensaje": f"¡Felicidades, {nombre}! Su solicitud de tarjeta de crédito ha sido aprobada con un cupo de {cupo} COP.",
            "nombre": nombre,
            "edad": edad
        }, 200

api.add_resource(VerificarTarjeta, '/api/verificar_tarjeta/<string:cc>')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verificar', methods=['POST'])
def verificar():
    cc = request.form['cc']
    response = obtener_usuario(cc)
    
    if response is None:
        return render_template('index.html', error="No se encontraron datos para este número de identificación (cc)")

    nombre, fecha_nacimiento, ingresos, datacredito = response[1], response[2], response[3], response[4]
    edad = calcular_edad(fecha_nacimiento)

    if datacredito == "si":
        return render_template('index.html', 
                                mensaje=f"Lo siento, su solicitud de tarjeta de crédito ha sido rechazada debido a su historial en Datacredito.",
                                nombre=nombre,
                                edad=edad)

    cupo = verificar_ingresos(ingresos)
    if cupo == "rechazar":
        return render_template('index.html', 
                                mensaje="Lo siento, sus ingresos son demasiado bajos para ser aprobados para una tarjeta de crédito.",
                                nombre=nombre,
                                edad=edad)

    return render_template('index.html', 
                            mensaje=f"¡Felicidades, {nombre}! Su solicitud de tarjeta de crédito ha sido aprobada con un cupo de {cupo} COP.",
                            nombre=nombre,
                            edad=edad)

if __name__ == '__main__':
    app.run(debug=True)
