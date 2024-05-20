from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

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

@app.route('/verificar_tarjeta_credito', methods=['GET'])
def verificar_tarjeta_credito():
    cc = request.args.get('cc')
    if not cc:
        return jsonify({"error": "Número de identificación (cc) es requerido"}), 400

    usuario = obtener_usuario(cc)
    
    if usuario is None:
        return jsonify({"error": "No se encontraron datos para este número de identificación (cc)"}), 404

    nombre, fecha_nacimiento, ingresos, datacredito = usuario[1], usuario[2], usuario[3], usuario[4]
    edad = calcular_edad(fecha_nacimiento)

    if datacredito == "si":
        return jsonify({
            "mensaje": f"Lo siento, su solicitud de tarjeta de crédito ha sido rechazada debido a su historial en Datacredito.",
            "nombre": nombre,
            "edad": edad
        }), 200

    cupo = verificar_ingresos(ingresos)
    if cupo == "rechazar":
        return jsonify({
            "mensaje": "Lo siento, sus ingresos son demasiado bajos para ser aprobados para una tarjeta de crédito.",
            "nombre": nombre,
            "edad": edad
        }), 200

    return jsonify({
        "mensaje": f"¡Felicidades, {nombre}! Su solicitud de tarjeta de crédito ha sido aprobada con un cupo de {cupo} COP.",
        "nombre": nombre,
        "edad": edad
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

