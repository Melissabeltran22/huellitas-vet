"""
Rutas de la API para gestión de Mascotas (Pacientes).
Endpoints:
    GET    /api/mascotas          - Listar todas las mascotas
    GET    /api/mascotas/<id>     - Obtener una mascota por ID
    POST   /api/mascotas          - Registrar nueva mascota
    PUT    /api/mascotas/<id>     - Actualizar mascota existente
    DELETE /api/mascotas/<id>     - Eliminar mascota
    GET    /api/mascotas/buscar   - Buscar mascota por nombre o documento del dueño
"""
from datetime import date, datetime
from flask import Blueprint, request, jsonify
from models import db
from models.mascota import Mascota
from models.dueno import Dueno

mascotasBlueprint = Blueprint("mascotas", __name__, url_prefix="/api/mascotas")


@mascotasBlueprint.route("", methods=["GET"])
def listarMascotas():
    """Obtiene la lista completa de mascotas con datos del dueño."""
    mascotas = Mascota.query.order_by(Mascota.nombre).all()
    return jsonify([mascota.toDict() for mascota in mascotas]), 200


@mascotasBlueprint.route("/<int:id>", methods=["GET"])
def obtenerMascota(id):
    """Obtiene una mascota específica por su ID."""
    mascota = Mascota.query.get(id)
    if not mascota:
        return jsonify({"error": "Mascota no encontrada"}), 404
    return jsonify(mascota.toDict()), 200


@mascotasBlueprint.route("", methods=["POST"])
def crearMascota():
    """
    Registra una nueva mascota asociada a un dueño existente.
    Validaciones:
        - Campos obligatorios: nombre, especie, raza, fechaNacimiento, duenoId
        - El dueño debe existir en la base de datos
        - La fecha de nacimiento no puede ser futura
    """
    datos = request.get_json()

    # Validar campos obligatorios
    camposRequeridos = ["nombre", "especie", "raza", "fechaNacimiento", "duenoId"]
    for campo in camposRequeridos:
        if not datos.get(campo):
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    # Validar que el dueño exista (integridad referencial)
    dueno = Dueno.query.get(datos["duenoId"])
    if not dueno:
        return jsonify({"error": "El dueño especificado no existe"}), 404

    # Parsear y validar fecha de nacimiento
    try:
        fechaNacimiento = datetime.strptime(datos["fechaNacimiento"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    # La fecha de nacimiento no puede ser futura
    if fechaNacimiento > date.today():
        return jsonify({"error": "La fecha de nacimiento no puede ser una fecha futura"}), 400

    nuevaMascota = Mascota(
        nombre=datos["nombre"].strip(),
        especie=datos["especie"].strip(),
        raza=datos["raza"].strip(),
        fechaNacimiento=fechaNacimiento,
        peso=datos.get("peso"),
        observaciones=datos.get("observaciones", "").strip() or None,
        duenoId=datos["duenoId"]
    )

    db.session.add(nuevaMascota)
    db.session.commit()

    return jsonify({
        "mensaje": "Mascota registrada exitosamente",
        "mascota": nuevaMascota.toDict()
    }), 201


@mascotasBlueprint.route("/<int:id>", methods=["PUT"])
def actualizarMascota(id):
    """Actualiza la información de una mascota existente."""
    mascota = Mascota.query.get(id)
    if not mascota:
        return jsonify({"error": "Mascota no encontrada"}), 404

    datos = request.get_json()

    # Validar nombre no vacío
    if "nombre" in datos and not datos["nombre"].strip():
        return jsonify({"error": "El nombre no puede estar vacío"}), 400

    # Validar dueño si se cambia
    if "duenoId" in datos:
        dueno = Dueno.query.get(datos["duenoId"])
        if not dueno:
            return jsonify({"error": "El dueño especificado no existe"}), 404
        mascota.duenoId = datos["duenoId"]

    # Validar fecha de nacimiento si se cambia
    if "fechaNacimiento" in datos:
        try:
            fechaNacimiento = datetime.strptime(datos["fechaNacimiento"], "%Y-%m-%d").date()
            if fechaNacimiento > date.today():
                return jsonify({"error": "La fecha de nacimiento no puede ser futura"}), 400
            mascota.fechaNacimiento = fechaNacimiento
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    # Actualizar campos presentes
    if "nombre" in datos:
        mascota.nombre = datos["nombre"].strip()
    if "especie" in datos:
        mascota.especie = datos["especie"].strip()
    if "raza" in datos:
        mascota.raza = datos["raza"].strip()
    if "peso" in datos:
        mascota.peso = datos["peso"]
    if "observaciones" in datos:
        mascota.observaciones = datos["observaciones"].strip() or None

    db.session.commit()

    return jsonify({
        "mensaje": "Mascota actualizada exitosamente",
        "mascota": mascota.toDict()
    }), 200


@mascotasBlueprint.route("/<int:id>", methods=["DELETE"])
def eliminarMascota(id):
    """Elimina una mascota y todas sus citas asociadas (CASCADE)."""
    mascota = Mascota.query.get(id)
    if not mascota:
        return jsonify({"error": "Mascota no encontrada"}), 404

    nombreMascota = mascota.nombre
    db.session.delete(mascota)
    db.session.commit()

    return jsonify({
        "mensaje": f"Mascota '{nombreMascota}' eliminada junto con sus citas"
    }), 200


@mascotasBlueprint.route("/buscar", methods=["GET"])
def buscarMascotas():
    """
    Busca mascotas por nombre o por documento del dueño.
    Parámetro de consulta: ?q=texto_busqueda
    Este endpoint cumple con el requerimiento del buscador solicitado.
    """
    termino = request.args.get("q", "").strip()
    if not termino:
        return jsonify({"error": "Debe proporcionar un término de búsqueda"}), 400

    # Buscar por nombre de mascota O por documento/nombre del dueño
    resultados = Mascota.query.join(Dueno).filter(
        db.or_(
            Mascota.nombre.ilike(f"%{termino}%"),
            Dueno.documento.ilike(f"%{termino}%"),
            Dueno.nombre.ilike(f"%{termino}%"),
            Dueno.apellido.ilike(f"%{termino}%")
        )
    ).all()

    return jsonify([mascota.toDict() for mascota in resultados]), 200
