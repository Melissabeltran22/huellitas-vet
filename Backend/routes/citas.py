"""
Rutas de la API para gestión de Citas.
Endpoints:
    GET    /api/citas          - Listar todas las citas
    GET    /api/citas/<id>     - Obtener una cita por ID
    POST   /api/citas          - Agendar nueva cita
    PUT    /api/citas/<id>     - Actualizar cita existente
    DELETE /api/citas/<id>     - Cancelar/eliminar cita
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db
from models.cita import Cita
from models.mascota import Mascota

citasBlueprint = Blueprint("citas", __name__, url_prefix="/api/citas")


@citasBlueprint.route("", methods=["GET"])
def listarCitas():
    """Obtiene la lista de citas ordenadas por fecha (más próximas primero)."""
    citas = Cita.query.order_by(Cita.fecha.asc(), Cita.hora.asc()).all()
    return jsonify([cita.toDict() for cita in citas]), 200


@citasBlueprint.route("/<int:id>", methods=["GET"])
def obtenerCita(id):
    """Obtiene una cita específica por su ID."""
    cita = Cita.query.get(id)
    if not cita:
        return jsonify({"error": "Cita no encontrada"}), 404
    return jsonify(cita.toDict()), 200


@citasBlueprint.route("", methods=["POST"])
def crearCita():
    """
    Agenda una nueva cita para una mascota.
    Validaciones:
        - Campos obligatorios: fecha, hora, motivo, mascotaId
        - La mascota debe existir
        - La fecha/hora debe ser futura (regla de negocio)
    """
    datos = request.get_json()

    # Validar campos obligatorios
    camposRequeridos = ["fecha", "hora", "motivo", "mascotaId"]
    for campo in camposRequeridos:
        if not datos.get(campo):
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    # Validar que el motivo no esté vacío
    if not datos["motivo"].strip():
        return jsonify({"error": "El motivo de la cita no puede estar vacío"}), 400

    # Validar que la mascota exista (integridad referencial)
    mascota = Mascota.query.get(datos["mascotaId"])
    if not mascota:
        return jsonify({"error": "La mascota especificada no existe"}), 404

    # Parsear fecha y hora
    try:
        fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
        hora = datetime.strptime(datos["hora"], "%H:%M").time()
    except ValueError:
        return jsonify({
            "error": "Formato inválido. Fecha: YYYY-MM-DD, Hora: HH:MM"
        }), 400

    # Validar que la cita sea en el futuro (regla de negocio clave)
    if not Cita.validarFechaFutura(fecha, hora):
        return jsonify({
            "error": "No se permite agendar citas en fechas u horas pasadas"
        }), 400

    nuevaCita = Cita(
        fecha=fecha,
        hora=hora,
        motivo=datos["motivo"].strip(),
        estado=datos.get("estado", "Programada"),
        mascotaId=datos["mascotaId"]
    )

    db.session.add(nuevaCita)
    db.session.commit()

    return jsonify({
        "mensaje": "Cita agendada exitosamente",
        "cita": nuevaCita.toDict()
    }), 201


@citasBlueprint.route("/<int:id>", methods=["PUT"])
def actualizarCita(id):
    """Actualiza una cita existente (reagendar o cambiar estado)."""
    cita = Cita.query.get(id)
    if not cita:
        return jsonify({"error": "Cita no encontrada"}), 404

    datos = request.get_json()

    # Si se cambia la fecha/hora, validar que sea futura
    if "fecha" in datos or "hora" in datos:
        try:
            nuevaFecha = (
                datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
                if "fecha" in datos else cita.fecha
            )
            nuevaHora = (
                datetime.strptime(datos["hora"], "%H:%M").time()
                if "hora" in datos else cita.hora
            )
        except ValueError:
            return jsonify({
                "error": "Formato inválido. Fecha: YYYY-MM-DD, Hora: HH:MM"
            }), 400

        if not Cita.validarFechaFutura(nuevaFecha, nuevaHora):
            return jsonify({
                "error": "No se permite reagendar citas a fechas u horas pasadas"
            }), 400

        cita.fecha = nuevaFecha
        cita.hora = nuevaHora

    # Validar mascota si se cambia
    if "mascotaId" in datos:
        mascota = Mascota.query.get(datos["mascotaId"])
        if not mascota:
            return jsonify({"error": "La mascota especificada no existe"}), 404
        cita.mascotaId = datos["mascotaId"]

    # Actualizar otros campos
    if "motivo" in datos:
        if not datos["motivo"].strip():
            return jsonify({"error": "El motivo no puede estar vacío"}), 400
        cita.motivo = datos["motivo"].strip()
    if "estado" in datos:
        estadosValidos = ["Programada", "Completada", "Cancelada"]
        if datos["estado"] not in estadosValidos:
            return jsonify({
                "error": f"Estado inválido. Opciones: {', '.join(estadosValidos)}"
            }), 400
        cita.estado = datos["estado"]

    db.session.commit()

    return jsonify({
        "mensaje": "Cita actualizada exitosamente",
        "cita": cita.toDict()
    }), 200


@citasBlueprint.route("/<int:id>", methods=["DELETE"])
def eliminarCita(id):
    """Elimina una cita del sistema."""
    cita = Cita.query.get(id)
    if not cita:
        return jsonify({"error": "Cita no encontrada"}), 404

    db.session.delete(cita)
    db.session.commit()

    return jsonify({"mensaje": "Cita eliminada exitosamente"}), 200
