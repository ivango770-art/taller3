import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root123',
    'password': 'rot123',
    'database': 'taller_motos'
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Ver cuántos registros hay
cursor.execute("SELECT COUNT(*) FROM datosivan_taller")
total = cursor.fetchone()[0]
print(f"Registros actuales: {total}")

if total == 0:
    print("Insertando datos de prueba...")
    cursor.execute("""
        INSERT INTO datosivan_taller (chasis, sede, asesor, modelo, fecha_registro) VALUES
        ('444455', 'pasto', 'ivan', 'GOMEZ', '2026-04-01'),
        ('2223', 'bogota', 'edixon', 'YAMAHA', '2026-04-02'),
        ('124', 'buesaco', 'ivan', 'HONDA', '2026-04-03')
    """)
    conn.commit()
    print("✅ Datos insertados")
else:
    print("✅ Ya hay datos")

cursor.execute("SELECT id, chasis, sede, asesor, modelo FROM datosivan_taller")
print("\n📋 REGISTROS EN MYSQL:")
for row in cursor.fetchall():
    print(f"   ID: {row[0]}, Chasis: {row[1]}, Sede: {row[2]}, Modelo: {row[4]}")

cursor.close()
conn.close()