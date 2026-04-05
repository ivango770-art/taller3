import mysql.connector

print("Probando conexión a MySQL...")

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root123',
        password='rot123',
        database='taller_motos'
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM seguimiento_taller")
    count = cursor.fetchone()
    print(f"✅ Conexión exitosa!")
    print(f"📊 Total de registros: {count[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")