-- =============================================
-- Clínica Veterinaria Huellitas
-- Script de creación de base de datos
-- Normalización: Tercera Forma Normal (3FN)
-- =============================================

-- Eliminar tablas si existen (orden inverso por dependencias)
DROP TABLE IF EXISTS historial_clinico;
DROP TABLE IF EXISTS citas;
DROP TABLE IF EXISTS mascotas;
DROP TABLE IF EXISTS duenos;

-- =============================================
-- TABLA: duenos
-- Descripción: Almacena información de los propietarios de mascotas.
-- Esta es la tabla padre en la jerarquía relacional.
-- =============================================
CREATE TABLE duenos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(20) NOT NULL UNIQUE,  -- Documento de identidad (único)
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(150),
    direccion VARCHAR(200)
);

-- =============================================
-- TABLA: mascotas
-- Descripción: Almacena información de los pacientes (mascotas).
-- Relación: N:1 con duenos (cada mascota pertenece a un dueño).
-- La FK con ON DELETE CASCADE asegura integridad referencial:
-- si se elimina un dueño, se eliminan sus mascotas automáticamente.
-- =============================================
CREATE TABLE mascotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,        -- Perro, Gato, Ave, Reptil, Otro
    raza VARCHAR(100) NOT NULL,
    "fechaNacimiento" DATE NOT NULL,     -- Se usa para calcular la edad automáticamente
    peso FLOAT,                          -- Peso en kilogramos
    observaciones TEXT,
    "duenoId" INTEGER NOT NULL,
    FOREIGN KEY ("duenoId") REFERENCES duenos(id) ON DELETE CASCADE
);

-- =============================================
-- TABLA: citas
-- Descripción: Registro de citas veterinarias.
-- Relación: N:1 con mascotas (cada cita pertenece a una mascota).
-- La FK con ON DELETE CASCADE mantiene la integridad:
-- si se elimina una mascota, se eliminan sus citas.
-- =============================================
CREATE TABLE citas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo VARCHAR(300) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Programada',  -- Programada, Completada, Cancelada
    "mascotaId" INTEGER NOT NULL,
    FOREIGN KEY ("mascotaId") REFERENCES mascotas(id) ON DELETE CASCADE
);

-- =============================================
-- TABLA: historial_clinico (VALOR AGREGADO)
-- Descripción: Registros médicos de consultas realizadas.
-- Diferencia con 'citas': una cita es una reserva futura,
-- el historial es un evento médico que ya ocurrió.
-- Relación: N:1 con mascotas (cada registro pertenece a una mascota).
-- Esto demuestra un modelo relacional más complejo: la tabla 'mascotas'
-- tiene DOS relaciones 1:N (hacia citas Y hacia historial_clinico).
-- =============================================
CREATE TABLE historial_clinico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE NOT NULL,
    diagnostico VARCHAR(300) NOT NULL,
    tratamiento TEXT NOT NULL,
    medicamentos VARCHAR(300),
    veterinario VARCHAR(150) NOT NULL,
    observaciones TEXT,
    "pesoEnConsulta" FLOAT,              -- Peso al momento de la consulta
    "mascotaId" INTEGER NOT NULL,
    FOREIGN KEY ("mascotaId") REFERENCES mascotas(id) ON DELETE CASCADE
);

-- =============================================
-- JUSTIFICACIÓN DE NORMALIZACIÓN (3FN):
--
-- 1FN: Todos los campos son atómicos (no hay campos multivaluados).
-- 2FN: No hay dependencias parciales (todas las tablas usan ID simple).
-- 3FN: No hay dependencias transitivas:
--       - Los datos del dueño están solo en 'duenos'
--       - Los datos de la mascota están solo en 'mascotas'
--       - Los datos de la cita están solo en 'citas'
--       - Los datos clínicos están solo en 'historial_clinico'
--       - Las relaciones se manejan mediante Foreign Keys
--       - La tabla 'mascotas' tiene DOS relaciones 1:N independientes
-- =============================================
