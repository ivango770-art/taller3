import mysql.connector

print("=== ARREGLANDO TABLA DATOSIVAN_TALLER ===\n")

config = {
    'host': 'localhost',
    'user': 'root123',
    'password': 'rot123',
    'database': 'taller_motos'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    # Ver qué columnas existen
    cursor.execute("DESCRIBE datosivan_taller")
    columnas = cursor.fetchall()
    
    print("📋 Columnas actuales:")
    columnas_existentes = []
    for col in columnas:
        columnas_existentes.append(col[0])
        print(f"   - {col[0]}")
    
    # Agregar columna tecnico
    if 'tecnico' not in columnas_existentes:
        cursor.execute("ALTER TABLE datosivan_taller ADD COLUMN tecnico VARCHAR(150)")
        print("\n✅ Columna 'tecnico' agregada")
    
    # Agregar columna modelo
    if 'modelo' not in columnas_existentes:
        cursor.execute("ALTER TABLE datosivan_taller ADD COLUMN modelo VARCHAR(100)")
        print("✅ Columna 'modelo' agregada")
    
    # Agregar columna fecha_registro
    if 'fecha_registro' not in columnas_existentes:
        cursor.execute("ALTER TABLE datosivan_taller ADD COLUMN fecha_registro DATE")
        print("✅ Columna 'fecha_registro' agregada")
    
    conn.commit()
    
    # Verificar resultado
    cursor.execute("DESCRIBE datosivan_taller")
    columnas_final = cursor.fetchall()
    
    print("\n📋 Columnas FINALES:")
    for col in columnas_final:
        print(f"   - {col[0]}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ TABLA ACTUALIZADA")
    
except Exception as e:
    print(f"❌ Error: {e}")