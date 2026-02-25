"""
Modelo de Historial Clínico.
Representa un registro médico asociado a una mascota.
Relación: Cada registro pertenece a una mascota (N:1).
Diferencia con Cita: la cita es una reserva futura, el historial es
un evento médico que YA ocurrió (diagnóstico, tratamiento, resultado).
"""
from datetime import date
from models import db


class HistorialClinico(db.Model):
    """Tabla 'historial_clinico' - Registros médicos de las mascotas."""

    __tablename__ = "historial_clinico"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    diagnostico = db.Column(db.String(300), nullable=False)
    tratamiento = db.Column(db.Text, nullable=False)
    medicamentos = db.Column(db.String(300), nullable=True)
    veterinario = db.Column(db.String(150), nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    pesoEnConsulta = db.Column(db.Float, nullable=True)  # Peso al momento de la consulta

    # Llave foránea: referencia a la mascota
    mascotaId = db.Column(
        db.Integer,
        db.ForeignKey("mascotas.id", ondelete="CASCADE"),
        nullable=False
    )

    def toDict(self):
        """Serializa el modelo a diccionario para respuesta JSON."""
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "diagnostico": self.diagnostico,
            "tratamiento": self.tratamiento,
            "medicamentos": self.medicamentos,
            "veterinario": self.veterinario,
            "observaciones": self.observaciones,
            "pesoEnConsulta": self.pesoEnConsulta,
            "mascotaId": self.mascotaId,
            "mascotaNombre": self.mascota.nombre if self.mascota else None,
            "duenoNombre": (
                f"{self.mascota.dueno.nombre} {self.mascota.dueno.apellido}"
                if self.mascota and self.mascota.dueno else None
            )
        }
