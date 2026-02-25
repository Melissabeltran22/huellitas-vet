"""
Script de datos semilla (seed) para la base de datos.
Inserta registros de prueba para demostración y testing.

Ejecución:
    python seed.py
"""
from datetime import date, time, timedelta
from app import crearApp
from models import db
from models.dueno import Dueno
from models.mascota import Mascota
from models.cita import Cita
from models.historial import HistorialClinico


def poblarBaseDeDatos():
    """Inserta datos de prueba en la base de datos."""
    app = crearApp()

    with app.app_context():
        # Limpiar datos existentes para evitar duplicados
        HistorialClinico.query.delete()
        Cita.query.delete()
        Mascota.query.delete()
        Dueno.query.delete()
        db.session.commit()

        # =============================================
        # DUEÑOS
        # =============================================
        dueno1 = Dueno(
            nombre="Carlos",
            apellido="Ramírez",
            documento="1001234567",
            telefono="3001234567",
            correo="carlos.ramirez@email.com",
            direccion="Cra 45 # 30-12, Medellín"
        )
        dueno2 = Dueno(
            nombre="María",
            apellido="González",
            documento="1009876543",
            telefono="3109876543",
            correo="maria.gonzalez@email.com",
            direccion="Calle 10 # 25-30, Medellín"
        )
        dueno3 = Dueno(
            nombre="Andrés",
            apellido="López",
            documento="1005551234",
            telefono="3205551234",
            correo="andres.lopez@email.com",
            direccion="Av 80 # 15-45, Medellín"
        )
        dueno4 = Dueno(
            nombre="Laura",
            apellido="Martínez",
            documento="1007778899",
            telefono="3157778899",
            correo="laura.martinez@email.com",
            direccion="Cra 70 # 48-20, Envigado"
        )

        db.session.add_all([dueno1, dueno2, dueno3, dueno4])
        db.session.flush()  # Asigna IDs sin hacer commit completo

        # =============================================
        # MASCOTAS
        # =============================================
        mascota1 = Mascota(
            nombre="Firulais",
            especie="Perro",
            raza="Labrador Retriever",
            fechaNacimiento=date(2021, 3, 15),
            peso=28.5,
            observaciones="Alergia a pollo. Vacunas al día.",
            duenoId=dueno1.id
        )
        mascota2 = Mascota(
            nombre="Michi",
            especie="Gato",
            raza="Siamés",
            fechaNacimiento=date(2022, 7, 20),
            peso=4.2,
            observaciones="Esterilizada. Dieta especial.",
            duenoId=dueno2.id
        )
        mascota3 = Mascota(
            nombre="Rocky",
            especie="Perro",
            raza="Bulldog Francés",
            fechaNacimiento=date(2020, 11, 5),
            peso=12.8,
            observaciones="Problemas respiratorios leves.",
            duenoId=dueno2.id
        )
        mascota4 = Mascota(
            nombre="Luna",
            especie="Gato",
            raza="Persa",
            fechaNacimiento=date(2023, 1, 10),
            peso=3.5,
            observaciones=None,
            duenoId=dueno3.id
        )
        mascota5 = Mascota(
            nombre="Max",
            especie="Perro",
            raza="Golden Retriever",
            fechaNacimiento=date(2019, 6, 22),
            peso=32.0,
            observaciones="Senior. Control cada 6 meses.",
            duenoId=dueno4.id
        )
        mascota6 = Mascota(
            nombre="Coco",
            especie="Ave",
            raza="Cocatiel",
            fechaNacimiento=date(2023, 9, 1),
            peso=0.09,
            observaciones="Recorte de alas periódico.",
            duenoId=dueno1.id
        )

        db.session.add_all([mascota1, mascota2, mascota3, mascota4, mascota5, mascota6])
        db.session.flush()

        # =============================================
        # CITAS (futuras para que pasen la validación)
        # =============================================
        hoy = date.today()

        cita1 = Cita(
            fecha=hoy + timedelta(days=2),
            hora=time(9, 0),
            motivo="Vacunación anual - refuerzo antirrábica",
            estado="Programada",
            mascotaId=mascota1.id
        )
        cita2 = Cita(
            fecha=hoy + timedelta(days=3),
            hora=time(10, 30),
            motivo="Control de peso y dieta",
            estado="Programada",
            mascotaId=mascota2.id
        )
        cita3 = Cita(
            fecha=hoy + timedelta(days=5),
            hora=time(14, 0),
            motivo="Revisión respiratoria trimestral",
            estado="Programada",
            mascotaId=mascota3.id
        )
        cita4 = Cita(
            fecha=hoy + timedelta(days=7),
            hora=time(11, 0),
            motivo="Desparasitación",
            estado="Programada",
            mascotaId=mascota4.id
        )
        cita5 = Cita(
            fecha=hoy + timedelta(days=10),
            hora=time(15, 30),
            motivo="Chequeo geriátrico completo",
            estado="Programada",
            mascotaId=mascota5.id
        )

        db.session.add_all([cita1, cita2, cita3, cita4, cita5])
        db.session.flush()

        # =============================================
        # HISTORIAL CLÍNICO (registros médicos pasados)
        # =============================================
        historial1 = HistorialClinico(
            fecha=date(2024, 8, 10),
            diagnostico="Dermatitis alérgica por contacto",
            tratamiento="Baño medicado cada 3 días por 2 semanas. Dieta hipoalergénica.",
            medicamentos="Prednisolona 5mg, Shampoo clorhexidina 2%",
            veterinario="Dra. Valentina Restrepo",
            observaciones="Reacción a nuevo alimento con pollo. Retirar de la dieta.",
            pesoEnConsulta=27.8,
            mascotaId=mascota1.id
        )
        historial2 = HistorialClinico(
            fecha=date(2024, 11, 22),
            diagnostico="Control de vacunación - Refuerzo parvovirus",
            tratamiento="Aplicación de vacuna séxtuple. Siguiente refuerzo en 12 meses.",
            medicamentos="Vacuna séxtuple canina",
            veterinario="Dr. Esteban Cárdenas",
            observaciones="Paciente en buen estado general. Sin reacciones adversas.",
            pesoEnConsulta=28.5,
            mascotaId=mascota1.id
        )
        historial3 = HistorialClinico(
            fecha=date(2024, 9, 15),
            diagnostico="Sobrepeso leve - Índice corporal 6/9",
            tratamiento="Plan nutricional: reducir porción diaria 15%. Actividad física 20 min/día.",
            medicamentos=None,
            veterinario="Dra. Valentina Restrepo",
            observaciones="Control en 2 meses para evaluar progreso.",
            pesoEnConsulta=4.5,
            mascotaId=mascota2.id
        )
        historial4 = HistorialClinico(
            fecha=date(2024, 10, 5),
            diagnostico="Estenosis de narinas - grado II",
            tratamiento="Monitoreo. Evitar ejercicio intenso y exposición al calor.",
            medicamentos="Sin medicamentos por ahora",
            veterinario="Dr. Esteban Cárdenas",
            observaciones="Si empeora, evaluar corrección quirúrgica de narinas.",
            pesoEnConsulta=12.6,
            mascotaId=mascota3.id
        )
        historial5 = HistorialClinico(
            fecha=date(2025, 1, 12),
            diagnostico="Chequeo geriátrico - Hemograma completo",
            tratamiento="Suplemento articular. Dieta senior. Control renal cada 6 meses.",
            medicamentos="Glucosamina 500mg, Omega 3",
            veterinario="Dra. Valentina Restrepo",
            observaciones="Valores renales ligeramente elevados. Vigilar hidratación.",
            pesoEnConsulta=31.5,
            mascotaId=mascota5.id
        )

        db.session.add_all([historial1, historial2, historial3, historial4, historial5])
        db.session.commit()

        print("\n  Datos semilla insertados exitosamente:")
        print(f"    Dueños:     {Dueno.query.count()}")
        print(f"    Mascotas:   {Mascota.query.count()}")
        print(f"    Citas:      {Cita.query.count()}")
        print(f"    Historial:  {HistorialClinico.query.count()}\n")


if __name__ == "__main__":
    poblarBaseDeDatos()
