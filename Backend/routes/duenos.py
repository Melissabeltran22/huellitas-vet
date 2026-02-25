"""
Rutas de la API para gestión de Dueños.
Endpoints:
    GET    /api/duenos          - Listar todos los dueños
    GET    /api/duenos/<id>     - Obtener un dueño por ID
    POST   /api/duenos          - Registrar nuevo dueño
    PUT    /api/duenos/<id>     - Actualizar dueño existente
    DELETE /api/duenos/<id>     - Eliminar dueño
    GET    /api/duenos/buscar   - Buscar dueño por documento
"""
from flask import Blueprint, request, jsonify
from models import db
from models.dueno import Dueno

# Blueprint agrupa las rutas bajo el prefijo /api/duenos
duenosBlueprint = Blueprint("duenos", __name__, url_prefix="/api/duenos")


@duenosBlueprint.route("", methods=["GET"])
def listarDuenos():
    """Obtiene la lista completa de dueños registrados."""
    duenos = Dueno.query.order_by(Dueno.nombre).all()
    return jsonify([dueno.toDict() for dueno in duenos]), 200


@duenosBlueprint.route("/<int:id>", methods=["GET"])
def obtenerDueno(id):
    """Obtiene un dueño específico por su ID."""
    dueno = Dueno.query.get(id)
    if not dueno:
        return jsonify({"error": "Dueño no encontrado"}), 404
    return jsonify(dueno.toDict()), 200


@duenosBlueprint.route("", methods=["POST"])
def crearDueno():
    """
    Registra un nuevo dueño.
    Validaciones:
        - Campos obligatorios: nombre, apellido, documento, telefono
        - Documento único (no duplicado)
    """
    datos = request.get_json()

    # Validar campos obligatorios (no permitir registros vacíos)
    camposRequeridos = ["nombre", "apellido", "documento", "telefono"]
    for campo in camposRequeridos:
        if not datos.get(campo, "").strip():
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    # Validar que el documento no esté duplicado
    duenoExistente = Dueno.query.filter_by(documento=datos["documento"].strip()).first()
    if duenoExistente:
        return jsonify({"error": "Ya existe un dueño con ese documento"}), 409

    # Crear el nuevo registro
    nuevoDueno = Dueno(
        nombre=datos["nombre"].strip(),
        apellido=datos["apellido"].strip(),
        documento=datos["documento"].strip(),
        telefono=datos["telefono"].strip(),
        correo=datos.get("correo", "").strip() or None,
        direccion=datos.get("direccion", "").strip() or None
    )

    db.session.add(nuevoDueno)
    db.session.commit()

    return jsonify({
        "mensaje": "Dueño registrado exitosamente",
        "dueno": nuevoDueno.toDict()
    }), 201


@duenosBlueprint.route("/<int:id>", methods=["PUT"])
def actualizarDueno(id):
    """
    Actualiza la información de un dueño existente.
    Solo modifica los campos enviados en el body.
    """
    dueno = Dueno.query.get(id)
    if not dueno:
        return jsonify({"error": "Dueño no encontrado"}), 404

    datos = request.get_json()

    # Validar que los campos obligatorios no queden vacíos
    if "nombre" in datos and not datos["nombre"].strip():
        return jsonify({"error": "El nombre no puede estar vacío"}), 400
    if "apellido" in datos and not datos["apellido"].strip():
        return jsonify({"error": "El apellido no puede estar vacío"}), 400

    # Validar documento único si se está cambiando
    if "documento" in datos and datos["documento"] != dueno.documento:
        existente = Dueno.query.filter_by(documento=datos["documento"].strip()).first()
        if existente:
            return jsonify({"error": "Ya existe un dueño con ese documento"}), 409

    # Actualizar campos presentes en la solicitud
    if "nombre" in datos:
        dueno.nombre = datos["nombre"].strip()
    if "apellido" in datos:
        dueno.apellido = datos["apellido"].strip()
    if "documento" in datos:
        dueno.documento = datos["documento"].strip()
    if "telefono" in datos:
        dueno.telefono = datos["telefono"].strip()
    if "correo" in datos:
        dueno.correo = datos["correo"].strip() or None
    if "direccion" in datos:
        dueno.direccion = datos["direccion"].strip() or None

    db.session.commit()

    return jsonify({
        "mensaje": "Dueño actualizado exitosamente",
        "dueno": dueno.toDict()
    }), 200


@duenosBlueprint.route("/<int:id>", methods=["DELETE"])
def eliminarDueno(id):
    """
    Elimina un dueño y todas sus mascotas/citas asociadas (CASCADE).
    Ejemplo de integridad referencial en la defensa.
    """
    dueno = Dueno.query.get(id)
    if not dueno:
        return jsonify({"error": "Dueño no encontrado"}), 404

    nombreCompleto = f"{dueno.nombre} {dueno.apellido}"
    db.session.delete(dueno)
    db.session.commit()

    return jsonify({
        "mensaje": f"Dueño '{nombreCompleto}' eliminado junto con sus mascotas y citas"
    }), 200


@duenosBlueprint.route("/buscar", methods=["GET"])
def buscarDueno():
    """
    Busca dueños por nombre, apellido o documento.
    Parámetro de consulta: ?q=texto_busqueda
    """
    termino = request.args.get("q", "").strip()
    if not termino:
        return jsonify({"error": "Debe proporcionar un término de búsqueda"}), 400

    # Buscar coincidencias parciales en nombre, apellido o documento
    resultados = Dueno.query.filter(
        db.or_(
            Dueno.nombre.ilike(f"%{termino}%"),
            Dueno.apellido.ilike(f"%{termino}%"),
            Dueno.documento.ilike(f"%{termino}%")
        )
    ).all()

    return jsonify([dueno.toDict() for dueno in resultados]), 200
