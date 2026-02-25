-- =============================================
-- Clínica Veterinaria Huellitas
-- Datos semilla para pruebas
-- Ejecutar después de schema.sql
-- =============================================

-- DUEÑOS
INSERT INTO duenos (nombre, apellido, documento, telefono, correo, direccion)
VALUES ('Carlos', 'Ramírez', '1001234567', '3001234567', 'carlos.ramirez@email.com', 'Cra 45 # 30-12, Medellín');

INSERT INTO duenos (nombre, apellido, documento, telefono, correo, direccion)
VALUES ('María', 'González', '1009876543', '3109876543', 'maria.gonzalez@email.com', 'Calle 10 # 25-30, Medellín');

INSERT INTO duenos (nombre, apellido, documento, telefono, correo, direccion)
VALUES ('Andrés', 'López', '1005551234', '3205551234', 'andres.lopez@email.com', 'Av 80 # 15-45, Medellín');

INSERT INTO duenos (nombre, apellido, documento, telefono, correo, direccion)
VALUES ('Laura', 'Martínez', '1007778899', '3157778899', 'laura.martinez@email.com', 'Cra 70 # 48-20, Envigado');

-- MASCOTAS
INSERT INTO mascotas (nombre, especie, raza, "fechaNacimiento", peso, observaciones, "duenoId")
VALUES ('Firulais', 'Perro', 'Labrador Retriever', '2021-03-15', 28.5, 'Alergia a pollo. Vacunas al día.', 1);

INSERT INTO mascotas (nombre, especie, raza, "fechaNacimiento", peso, observaciones, "duenoId")
VALUES ('Michi', 'Gato', 'Siamés', '2022-07-20', 4.2, 'Esterilizada. Dieta especial.', 2);

INSERT INTO mascotas (nombre, especie, raza, "fechaNacimiento", peso, observaciones, "duenoId")
VALUES ('Rocky', 'Perro', 'Bulldog Francés', '2020-11-05', 12.8, 'Problemas respiratorios leves.', 2);

INSERT INTO mascotas (nombre, especie, raza, "fechaNacimiento", peso, observaciones, "duenoId")
VALUES ('Luna', 'Gato', 'Persa', '2023-01-10', 3.5, NULL, 3);

INSERT INTO mascotas (nombre, especie, raza, "fechaNacimiento", peso, observaciones, "duenoId")
VALUES ('Max', 'Perro', 'Golden Retriever', '2019-06-22', 32.0, 'Senior. Control cada 6 meses.', 4);

INSERT INTO mascotas (nombre, especie, raza, "fechaNacimiento", peso, observaciones, "duenoId")
VALUES ('Coco', 'Ave', 'Cocatiel', '2023-09-01', 0.09, 'Recorte de alas periódico.', 1);

-- CITAS (fechas relativas, ajustar según la fecha actual)
INSERT INTO citas (fecha, hora, motivo, estado, "mascotaId")
VALUES ('2025-03-01', '09:00', 'Vacunación anual - refuerzo antirrábica', 'Programada', 1);

INSERT INTO citas (fecha, hora, motivo, estado, "mascotaId")
VALUES ('2025-03-03', '10:30', 'Control de peso y dieta', 'Programada', 2);

INSERT INTO citas (fecha, hora, motivo, estado, "mascotaId")
VALUES ('2025-03-05', '14:00', 'Revisión respiratoria trimestral', 'Programada', 3);

INSERT INTO citas (fecha, hora, motivo, estado, "mascotaId")
VALUES ('2025-03-08', '11:00', 'Desparasitación', 'Programada', 4);

INSERT INTO citas (fecha, hora, motivo, estado, "mascotaId")
VALUES ('2025-03-12', '15:30', 'Chequeo geriátrico completo', 'Programada', 5);

-- HISTORIAL CLÍNICO (Valor Agregado)
INSERT INTO historial_clinico (fecha, diagnostico, tratamiento, medicamentos, veterinario, observaciones, "pesoEnConsulta", "mascotaId")
VALUES ('2024-08-10', 'Dermatitis alérgica por contacto', 'Baño medicado cada 3 días por 2 semanas. Dieta hipoalergénica.', 'Prednisolona 5mg, Shampoo clorhexidina 2%', 'Dra. Valentina Restrepo', 'Reacción a nuevo alimento con pollo. Retirar de la dieta.', 27.8, 1);

INSERT INTO historial_clinico (fecha, diagnostico, tratamiento, medicamentos, veterinario, observaciones, "pesoEnConsulta", "mascotaId")
VALUES ('2024-11-22', 'Control de vacunación - Refuerzo parvovirus', 'Aplicación de vacuna séxtuple. Siguiente refuerzo en 12 meses.', 'Vacuna séxtuple canina', 'Dr. Esteban Cárdenas', 'Paciente en buen estado general. Sin reacciones adversas.', 28.5, 1);

INSERT INTO historial_clinico (fecha, diagnostico, tratamiento, medicamentos, veterinario, observaciones, "pesoEnConsulta", "mascotaId")
VALUES ('2024-09-15', 'Sobrepeso leve - Índice corporal 6/9', 'Plan nutricional: reducir porción diaria 15%. Actividad física 20 min/día.', NULL, 'Dra. Valentina Restrepo', 'Control en 2 meses para evaluar progreso.', 4.5, 2);

INSERT INTO historial_clinico (fecha, diagnostico, tratamiento, medicamentos, veterinario, observaciones, "pesoEnConsulta", "mascotaId")
VALUES ('2024-10-05', 'Estenosis de narinas - grado II', 'Monitoreo. Evitar ejercicio intenso y exposición al calor.', 'Sin medicamentos por ahora', 'Dr. Esteban Cárdenas', 'Si empeora, evaluar corrección quirúrgica de narinas.', 12.6, 3);

INSERT INTO historial_clinico (fecha, diagnostico, tratamiento, medicamentos, veterinario, observaciones, "pesoEnConsulta", "mascotaId")
VALUES ('2025-01-12', 'Chequeo geriátrico - Hemograma completo', 'Suplemento articular. Dieta senior. Control renal cada 6 meses.', 'Glucosamina 500mg, Omega 3', 'Dra. Valentina Restrepo', 'Valores renales ligeramente elevados. Vigilar hidratación.', 31.5, 5);
