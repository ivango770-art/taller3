-- =====================================================
-- BASE DE DATOS PARA TALLER DE MOTOS
-- =====================================================

-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS taller_motos;
USE taller_motos;

-- 2. Eliminar tabla si existe
DROP TABLE IF EXISTS datosivan_taller;

-- 3. Crear la tabla principal
CREATE TABLE datosivan_taller (
    id INT PRIMARY KEY AUTO_INCREMENT,
    chasis VARCHAR(100),
    sede VARCHAR(200),
    asesor VARCHAR(150),
    tecnico VARCHAR(150),
    modelo VARCHAR(100),
    fecha_registro DATE,
    hora_registro TIME,
    cupon VARCHAR(50),
    cantidad_gasolina DECIMAL(10,2),
    tick INT,
    fecha_alistamiento DATE,
    hora_alistamiento TIME,
    descripcion TEXT,
    insumos TEXT
);

-- 4. Insertar datos de ejemplo
INSERT INTO datosivan_taller (chasis, sede, asesor, modelo, fecha_registro, hora_registro) VALUES
('9FSNE43NV7C100305', 'AKT CHPAÑATH', 'FELIPE', 'AKT 125', '2026-01-22', '08:10:00'),
('4444', 'pasto', 'ivan', 'HONDA CB190', '2026-04-01', '15:01:00'),
('2223', 'bogota', 'edixon', 'YAMAHA', '2026-04-02', '10:30:00');

-- 5. Verificar
SELECT * FROM datosivan_taller;
