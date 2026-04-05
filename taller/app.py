from flask import Flask, render_template, request, jsonify, Response
import mysql.connector
import csv
from io import StringIO

app = Flask(__name__)

config = {
    'host': 'localhost',
    'user': 'root123',
    'password': 'rot123',
    'database': 'taller_motos'
}

def get_db_connection():
    return mysql.connector.connect(**config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/registros')
def get_registros():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, chasis, sede, asesor, modelo, fecha_registro, tecnico, cupon, cantidad_gasolina, tick, fecha_alistamiento, hora_alistamiento, descripcion, insumos FROM datosivan_taller ORDER BY id DESC")
        datos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convertir fechas a string
        for row in datos:
            if row.get('fecha_registro'):
                row['fecha_registro'] = str(row['fecha_registro'])
            if row.get('fecha_alistamiento'):
                row['fecha_alistamiento'] = str(row['fecha_alistamiento'])
            if row.get('hora_registro'):
                row['hora_registro'] = str(row['hora_registro'])
            if row.get('hora_alistamiento'):
                row['hora_alistamiento'] = str(row['hora_alistamiento'])
        
        print(f"📋 Registros encontrados: {len(datos)}")
        return jsonify(datos)
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agregar', methods=['POST'])
def agregar():
    try:
        data = request.json
        print(f"📝 Recibido: {data}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO datosivan_taller 
            (fecha_registro, hora_registro, chasis, sede, asesor, modelo) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            data.get('fecha_registro'),
            data.get('hora_registro'),
            data.get('chasis'),
            data.get('sede'),
            data.get('asesor'),
            data.get('modelo')
        ))
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        print(f"✅ Insertado ID: {nuevo_id}")
        return jsonify({'success': True, 'id': nuevo_id, 'mensaje': '✅ Guardado'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/eliminar/<int:id>', methods=['DELETE'])
def eliminar(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM datosivan_taller WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'mensaje': '✅ Eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buscar')
def buscar():
    termino = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    like = f'%{termino}%'
    cursor.execute("""
        SELECT id, chasis, sede, asesor, modelo, fecha_registro, tecnico, cupon, cantidad_gasolina, tick, fecha_alistamiento, hora_alistamiento, descripcion, insumos 
        FROM datosivan_taller 
        WHERE chasis LIKE %s OR sede LIKE %s OR asesor LIKE %s OR modelo LIKE %s OR tecnico LIKE %s
        ORDER BY id DESC
    """, (like, like, like, like, like))
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    for row in datos:
        if row.get('fecha_registro'):
            row['fecha_registro'] = str(row['fecha_registro'])
        if row.get('fecha_alistamiento'):
            row['fecha_alistamiento'] = str(row['fecha_alistamiento'])
    
    return jsonify(datos)

@app.route('/api/estadisticas')
def estadisticas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as total FROM datosivan_taller")
    total = cursor.fetchone()
    
    cursor.execute("""
        SELECT sede, COUNT(*) as cantidad 
        FROM datosivan_taller 
        WHERE sede IS NOT NULL AND sede != ''
        GROUP BY sede
    """)
    sedes = cursor.fetchall()
    
    cursor.execute("""
        SELECT tecnico, COUNT(*) as cantidad 
        FROM datosivan_taller 
        WHERE tecnico IS NOT NULL AND tecnico != ''
        GROUP BY tecnico
    """)
    tecnicos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'total': total['total'] if total else 0,
        'sedes': sedes,
        'tecnicos': tecnicos
    })

@app.route('/api/exportar_csv')
def exportar_csv():
    """Exporta TODOS los datos a CSV (incluyendo técnico, cupón, insumos, etc.)"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, chasis, sede, asesor, modelo, fecha_registro, 
               hora_registro, tecnico, cupon, cantidad_gasolina, 
               tick, fecha_alistamiento, hora_alistamiento, descripcion, insumos 
        FROM datosivan_taller 
        ORDER BY id DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Encabezados completos
    writer.writerow([
        'ID', 'CHASIS', 'SEDE', 'ASESOR', 'MODELO', 'FECHA_REGISTRO', 
        'HORA_REGISTRO', 'TECNICO', 'CUPON', 'CANTIDAD_GASOLINA', 
        'TICK', 'FECHA_ALISTAMIENTO', 'HORA_ALISTAMIENTO', 'DESCRIPCION', 'INSUMOS'
    ])
    
    # Datos completos
    for row in datos:
        writer.writerow([
            row['id'], 
            row['chasis'] or '', 
            row['sede'] or '', 
            row['asesor'] or '', 
            row['modelo'] or '', 
            row['fecha_registro'] or '',
            row['hora_registro'] or '',
            row['tecnico'] or '',
            row['cupon'] or '',
            row['cantidad_gasolina'] or '',
            row['tick'] or '',
            row['fecha_alistamiento'] or '',
            row['hora_alistamiento'] or '',
            row['descripcion'] or '',
            row['insumos'] or ''
        ])
    
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=datos_taller_completo.csv'}
    )

@app.route('/api/registro/<int:id>')
def get_registro(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM datosivan_taller WHERE id = %s", (id,))
        registro = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if registro:
            # Convertir fechas a string
            if registro.get('fecha_registro'):
                registro['fecha_registro'] = str(registro['fecha_registro'])
            if registro.get('fecha_alistamiento'):
                registro['fecha_alistamiento'] = str(registro['fecha_alistamiento'])
            if registro.get('hora_registro'):
                registro['hora_registro'] = str(registro['hora_registro'])
            if registro.get('hora_alistamiento'):
                registro['hora_alistamiento'] = str(registro['hora_alistamiento'])
            return jsonify(registro)
        else:
            return jsonify({"error": "Registro no encontrado"}), 404
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/actualizar/<int:id>', methods=['PUT'])
def actualizar_registro(id):
    try:
        data = request.json
        print(f"📝 Actualizando ID {id}: {data}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            UPDATE datosivan_taller SET 
            tecnico = %s,
            cupon = %s,
            cantidad_gasolina = %s,
            tick = %s,
            fecha_alistamiento = %s,
            hora_alistamiento = %s,
            descripcion = %s,
            insumos = %s
            WHERE id = %s
        """
        valores = (
            data.get('tecnico'),
            data.get('cupon'),
            data.get('cantidad_gasolina'),
            data.get('tick'),
            data.get('fecha_alistamiento'),
            data.get('hora_alistamiento'),
            data.get('descripcion'),
            data.get('insumos'),
            id
        )
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'mensaje': '✅ Datos actualizados'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 SERVICIO WEB INICIADO")
    print("="*50)
    print("📌 Abre tu navegador en: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)