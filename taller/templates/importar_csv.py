import mysql.connector
import pandas as pd

print("=== IMPORTANDO CSV A MYSQL ===\n")

# Configuración
config = {
    'host': 'localhost',
    'user': 'root123',
    'password': 'rot123',
    'database': 'taller_motos'
}

# Ruta de tu archivo CSV (cambia el nombre)
archivo_csv = 'SEGUIMIENTO MENSUAL TALLER HORAS TECNICO FERXXO - CONTROL ALISTAMIENTO.csv'

try:
    # Leer CSV
    df = pd.read_csv(archivo_csv, encoding='latin1')
    print(f"📄 CSV leído: {len(df)} filas")
    
    # Conectar a MySQL
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datosivan_taller (
            id INT PRIMARY KEY AUTO_INCREMENT,
            chasis VARCHAR(100),
            sede VARCHAR(200),
            asesor VARCHAR(150),
            tecnico VARCHAR(150)
        )
    """)
    
    # Insertar datos
    insertados = 0
    for index, row in df.iterrows():
        try:
            sql = "INSERT INTO datosivan_taller (chasis, sede, asesor, tecnico) VALUES (%s, %s, %s, %s)"
            valores = (
                str(row.iloc[2])[:100] if len(row) > 2 else '',  # CHASIS
                str(row.iloc[3])[:200] if len(row) > 3 else '',  # SEDE
                str(row.iloc[6])[:150] if len(row) > 6 else '',  # ASESOR
                str(row.iloc[10])[:150] if len(row) > 10 else ''  # TECNICO
            )
            cursor.execute(sql, valores)
            insertados += 1
        except:
            pass
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Importados {insertados} registros")
    
except Exception as e:
    print(f"❌ Error: {e}")