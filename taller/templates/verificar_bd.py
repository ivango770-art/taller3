import mysql.connector

print("=== VERIFICANDO BASE DE DATOS ===\n")

config = {
    'host': 'localhost',
    'user': 'root123',
    'password': 'rot123',
    'database': 'taller_motos'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    # Ver todas las tablas
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    
    print("📋 TABLAS EN LA BASE DE DATOS:")
    for tabla in tablas:
        print(f"   - {tabla[0]}")
    
    print("\n" + "="*40)
    
    # Ver datos de datosivan_taller si existe
    cursor.execute("SELECT * FROM datosivan_taller")
    datos = cursor.fetchall()
    
    print(f"\n📊 REGISTROS EN datosivan_taller: {len(datos)}")
    
    if len(datos) > 0:
        print("\n📝 PRIMEROS 5 REGISTROS:")
        for i, row in enumerate(datos[:5]):
            print(f"   {i+1}. ID: {row[0]}, Chasis: {row[1]}, Sede: {row[2]}")
    else:
        print("\n⚠️ La tabla está VACÍA. Debes importar datos.")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")