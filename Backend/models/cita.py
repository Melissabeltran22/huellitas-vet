"""
Modelo de Cita (Appointment).
Representa una cita veterinaria agendada para una mascota.
Relación: Cada cita pertenece a una mascota (N:1).
"""
from datetime import datetime
from models import db


class Cita(db.Model):
    """Tabla 'citas' - Registro de citas veterinarias."""

    __tablename__ = "citas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    motivo = db.Column(db.String(300), nullable=False)
    estado = db.Column(
        db.String(20),
        nullable=False,
        default="Programada"
    )  # Programada, Completada, Cancelada

    # Llave foránea: referencia a la mascota
    mascotaId = db.Column(
        db.Integer,
        db.ForeignKey("mascotas.id", ondelete="CASCADE"),
        nullable=False
    )

    @staticmethod
    def validarFechaFutura(fecha, hora):
        """
        Valida que la fecha y hora de la cita sea en el futuro.
        Regla de negocio: no se permiten citas en fechas pasadas.
        Retorna True si la fecha es válida (futura), False si no.
        """
        fechaHoraCita = datetime.combine(fecha, hora)
        return fechaHoraCita > datetime.now()

    def toDict(self):
        """Serializa el modelo a diccionario para respuesta JSON."""
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "hora": self.hora.strftime("%H:%M"),
            "motivo": self.motivo,
            "estado": self.estado,
            "mascotaId": self.mascotaId,
            "mascotaNombre": self.mascota.nombre if self.mascota else None,
            "duenoNombre": (
                f"{self.mascota.dueno.nombre} {self.mascota.dueno.apellido}"
                if self.mascota and self.mascota.dueno else None
            )
        }
