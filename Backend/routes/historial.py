"""
Rutas de la API para gestión del Historial Clínico.
Valor agregado: permite registrar diagnósticos, tratamientos y seguimiento
médico por cada mascota, complementando la gestión de citas.

Endpoints:
    GET    /api/historial                    - Listar todos los registros
    GET    /api/historial/<id>               - Obtener un registro por ID
    GET    /api/historial/mascota/<mascotaId> - Historial de una mascota específica
    POST   /api/historial                    - Crear nuevo registro clínico
    PUT    /api/historial/<id>               - Actualizar registro
    DELETE /api/historial/<id>               - Eliminar registro
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db
from models.historial import HistorialClinico
from models.mascota import Mascota

historialBlueprint = Blueprint("historial", __name__, url_prefix="/api/historial")


@historialBlueprint.route("", methods=["GET"])
def listarHistorial():
    """Obtiene todos los registros clínicos ordenados por fecha (más recientes primero)."""
    registros = HistorialClinico.query.order_by(HistorialClinico.fecha.desc()).all()
    return jsonify([registro.toDict() for registro in registros]), 200


@historialBlueprint.route("/<int:id>", methods=["GET"])
def obtenerRegistro(id):
    """Obtiene un registro clínico específico por su ID."""
    registro = HistorialClinico.query.get(id)
    if not registro:
        return jsonify({"error": "Registro clínico no encontrado"}), 404
    return jsonify(registro.toDict()), 200


@historialBlueprint.route("/mascota/<int:mascotaId>", methods=["GET"])
def historialPorMascota(mascotaId):
    """
    Obtiene el historial clínico completo de una mascota específica.
    Ordenado por fecha descendente (más reciente primero).
    Este endpoint es clave para la consulta veterinaria en tiempo real.
    """
    mascota = Mascota.query.get(mascotaId)
    if not mascota:
        return jsonify({"error": "Mascota no encontrada"}), 404

    registros = HistorialClinico.query.filter_by(
        mascotaId=mascotaId
    ).order_by(
        HistorialClinico.fecha.desc()
    ).all()

    return jsonify({
        "mascota": mascota.toDict(),
        "historial": [registro.toDict() for registro in registros],
        "totalRegistros": len(registros)
    }), 200


@historialBlueprint.route("", methods=["POST"])
def crearRegistro():
    """
    Crea un nuevo registro en el historial clínico de una mascota.
    Validaciones:
        - Campos obligatorios: diagnostico, tratamiento, veterinario, mascotaId
        - La mascota debe existir
        - La fecha no puede ser futura (es un evento que ya ocurrió)
    """
    datos = request.get_json()

    # Validar campos obligatorios
    camposRequeridos = ["diagnostico", "tratamiento", "veterinario", "mascotaId"]
    for campo in camposRequeridos:
        if not datos.get(campo):
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    # Validar textos no vacíos
    if not datos["diagnostico"].strip():
        return jsonify({"error": "El diagnóstico no puede estar vacío"}), 400
    if not datos["tratamiento"].strip():
        return jsonify({"error": "El tratamiento no puede estar vacío"}), 400

    # Validar que la mascota exista (integridad referencial)
    mascota = Mascota.query.get(datos["mascotaId"])
    if not mascota:
        return jsonify({"error": "La mascota especificada no existe"}), 404

    # Parsear fecha (por defecto es hoy)
    fecha = None
    if datos.get("fecha"):
        try:
            fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
    else:
        fecha = datetime.now().date()

    nuevoRegistro = HistorialClinico(
        fecha=fecha,
        diagnostico=datos["diagnostico"].strip(),
        tratamiento=datos["tratamiento"].strip(),
        medicamentos=datos.get("medicamentos", "").strip() or None,
        veterinario=datos["veterinario"].strip(),
        observaciones=datos.get("observaciones", "").strip() or None,
        pesoEnConsulta=datos.get("pesoEnConsulta"),
        mascotaId=datos["mascotaId"]
    )

    db.session.add(nuevoRegistro)
    db.session.commit()

    return jsonify({
        "mensaje": "Registro clínico creado exitosamente",
        "registro": nuevoRegistro.toDict()
    }), 201


@historialBlueprint.route("/<int:id>", methods=["PUT"])
def actualizarRegistro(id):
    """Actualiza un registro clínico existente."""
    registro = HistorialClinico.query.get(id)
    if not registro:
        return jsonify({"error": "Registro clínico no encontrado"}), 404

    datos = request.get_json()

    # Validar campos de texto no vacíos si se envían
    if "diagnostico" in datos and not datos["diagnostico"].strip():
        return jsonify({"error": "El diagnóstico no puede estar vacío"}), 400
    if "tratamiento" in datos and not datos["tratamiento"].strip():
        return jsonify({"error": "El tratamiento no puede estar vacío"}), 400

    # Actualizar campos presentes
    if "fecha" in datos:
        try:
            registro.fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido"}), 400
    if "diagnostico" in datos:
        registro.diagnostico = datos["diagnostico"].strip()
    if "tratamiento" in datos:
        registro.tratamiento = datos["tratamiento"].strip()
    if "medicamentos" in datos:
        registro.medicamentos = datos["medicamentos"].strip() or None
    if "veterinario" in datos:
        registro.veterinario = datos["veterinario"].strip()
    if "observaciones" in datos:
        registro.observaciones = datos["observaciones"].strip() or None
    if "pesoEnConsulta" in datos:
        registro.pesoEnConsulta = datos["pesoEnConsulta"]

    db.session.commit()

    return jsonify({
        "mensaje": "Registro clínico actualizado exitosamente",
        "registro": registro.toDict()
    }), 200


@historialBlueprint.route("/<int:id>", methods=["DELETE"])
def eliminarRegistro(id):
    """Elimina un registro del historial clínico."""
    registro = HistorialClinico.query.get(id)
    if not registro:
        return jsonify({"error": "Registro clínico no encontrado"}), 404

    db.session.delete(registro)
    db.session.commit()

    return jsonify({"mensaje": "Registro clínico eliminado exitosamente"}), 200
