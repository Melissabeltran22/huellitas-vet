"""
Modelo de Mascota (Pet).
Representa a un paciente de la clínica veterinaria.
Relación: Cada mascota pertenece a un dueño (N:1) y puede tener muchas citas (1:N).
"""
from datetime import date, datetime
from models import db


class Mascota(db.Model):
    """Tabla 'mascotas' - Información del paciente animal."""

    __tablename__ = "mascotas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)  # Perro, Gato, Ave, etc.
    raza = db.Column(db.String(100), nullable=False)
    fechaNacimiento = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Float, nullable=True)  # Peso en kg
    observaciones = db.Column(db.Text, nullable=True)

    # Llave foránea: referencia al dueño
    duenoId = db.Column(
        db.Integer,
        db.ForeignKey("duenos.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relación con citas: cascade elimina citas si se borra la mascota
    citas = db.relationship(
        "Cita",
        backref="mascota",
        cascade="all, delete-orphan",
        lazy=True
    )

    # Relación con historial clínico: cascade elimina registros si se borra la mascota
    historiales = db.relationship(
        "HistorialClinico",
        backref="mascota",
        cascade="all, delete-orphan",
        lazy=True
    )

    @property
    def edad(self):
        """
        Calcula la edad automáticamente a partir de la fecha de nacimiento.
        Retorna un string descriptivo (años y meses).
        """
        hoy = date.today()
        anios = hoy.year - self.fechaNacimiento.year
        meses = hoy.month - self.fechaNacimiento.month

        # Ajuste si aún no ha pasado el mes/día de cumpleaños
        if hoy.day < self.fechaNacimiento.day:
            meses -= 1
        if meses < 0:
            anios -= 1
            meses += 12

        if anios > 0:
            return f"{anios} año{'s' if anios != 1 else ''} y {meses} mes{'es' if meses != 1 else ''}"
        else:
            return f"{meses} mes{'es' if meses != 1 else ''}"

    @property
    def edadAnios(self):
        """Retorna la edad en años decimales para cálculos."""
        hoy = date.today()
        diferencia = hoy - self.fechaNacimiento
        return round(diferencia.days / 365.25, 1)

    def toDict(self):
        """Serializa el modelo a diccionario para respuesta JSON."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "raza": self.raza,
            "fechaNacimiento": self.fechaNacimiento.isoformat(),
            "edad": self.edad,
            "edadAnios": self.edadAnios,
            "peso": self.peso,
            "observaciones": self.observaciones,
            "duenoId": self.duenoId,
            "duenoNombre": f"{self.dueno.nombre} {self.dueno.apellido}" if self.dueno else None,
            "cantidadCitas": len(self.citas),
            "cantidadHistoriales": len(self.historiales)
        }
