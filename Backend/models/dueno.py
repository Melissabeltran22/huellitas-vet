"""
Modelo de Dueño (Owner).
Representa al propietario de una o varias mascotas.
Relación: Un dueño puede tener muchas mascotas (1:N).
"""
from models import db


class Dueno(db.Model):
    """Tabla 'duenos' - Información del propietario."""

    __tablename__ = "duenos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(150), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)

    # Relación con mascotas: cascade elimina mascotas si se borra el dueño
    mascotas = db.relationship(
        "Mascota",
        backref="dueno",
        cascade="all, delete-orphan",
        lazy=True
    )

    def toDict(self):
        """Serializa el modelo a diccionario para respuesta JSON."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "documento": self.documento,
            "telefono": self.telefono,
            "correo": self.correo,
            "direccion": self.direccion,
            "cantidadMascotas": len(self.mascotas)
        }
