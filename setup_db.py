import sqlite3

def crear_base_de_datos():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            fecha_nacimiento TEXT,
            ingresos INTEGER,
            datacredito TEXT
        )
    ''')
    
    # Inserta algunos datos de ejemplo
    usuarios = [
        ("Mauricio Reyes Basto", "31/05/1975", 8000000, "no"),
        ("Laura Alexandra Reyes Mendoza", "28/09/2000", 2500000, "no"),
        ("Leydy Johanna Mendoza Hermoso", "25/02/1982", 9500000, "si"),
        ("Sergio Castro", "01/12/2010", 0, "no"),
        ("Amanda Avila Tinjacá", "10/04/1980", 5000000, "si")
    ]
    
    cursor.executemany('''
        INSERT INTO usuarios (nombre, fecha_nacimiento, ingresos, datacredito)
        VALUES (?, ?, ?, ?)
    ''', usuarios)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_base_de_datos()