import sqlite3
from datetime import datetime

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
    elif 4000001 <= ingresos <= 6000000:
        return 4000000
    elif 6000001 <= ingresos <= 8000000:
        return 6000000
    elif 8000001 <= ingresos <= 12000000:
        return 8000000
    else:
        return 10000000

def verificar_tarjeta_credito(cc):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (cc,))
    usuario = cursor.fetchone()
    
    if usuario is None:
        print("Lo siento, no se encontraron datos para este número de identificación (cc).")
        return
    
    nombre, fecha_nacimiento, ingresos, datacredito = usuario[1], usuario[2], usuario[3], usuario[4]
    edad = calcular_edad(fecha_nacimiento)
    print(f"Bienvenido, {nombre}! Su edad es: {edad} años")

    if datacredito == "si":
        print("Lo siento, su solicitud de tarjeta de crédito ha sido rechazada debido a su historial en Datacredito.")
        return
    
    cupo = verificar_ingresos(ingresos)
    if cupo == "rechazar":
        print("Lo siento, sus ingresos son demasiado bajos para ser aprobados para una tarjeta de crédito.")
        return

    print(f"¡Felicidades, {nombre}! Su solicitud de tarjeta de crédito ha sido aprobada con un cupo de {cupo} COP.")
    conn.close()

if __name__ == "__main__":
    cc = input("Por favor, ingrese su número de identificación (cc): ")
    verificar_tarjeta_credito(cc)
