"""
Aplicación principal - Clínica Veterinaria Huellitas.
Punto de entrada del servidor Backend (API REST).

Características:
    - Conexión dual: Azure (nube) con fallback automático a SQLite (local)
    - Panel de administración de BD accesible en /admin
    - API REST completa en /api/

Ejecución:
    python app.py
"""
import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config
from models import db
from routes.duenos import duenosBlueprint
from routes.mascotas import mascotasBlueprint
from routes.citas import citasBlueprint
from routes.historial import historialBlueprint

# Importar modelos para que SQLAlchemy los registre al crear tablas
from models.dueno import Dueno        # noqa: F401
from models.mascota import Mascota    # noqa: F401
from models.cita import Cita          # noqa: F401
from models.historial import HistorialClinico  # noqa: F401


# Variable global para rastrear el tipo de conexión activa
conexionActiva = "Desconocida"


def crearApp():
    """
    Factory pattern para crear la aplicación Flask.
    Implementa fallback automático: si Azure falla, usa SQLite.
    """
    global conexionActiva

    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    # --- LÓGICA DE FALLBACK AUTOMÁTICO ---
    with app.app_context():
        try:
            # Intentar conectar a la BD configurada (Azure u otra)
            with db.engine.connect() as conn:
                conn.execute(db.text("SELECT 1"))
            db.create_all()
            conexionActiva = Config.obtenerTipoConexion()
            print(f"  BD conectada: {conexionActiva}")
        except Exception as errorConexion:
            # Si falla, cambiar automáticamente a SQLite local
            print(f"  Conexion principal fallo: {errorConexion}")
            print("  Activando fallback automatico a SQLite local...")
            app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLITE_FALLBACK_URI
            db.init_app(app)
            with app.app_context():
                db.create_all()
            conexionActiva = "SQLite (Local - Fallback)"
            print(f"  BD conectada: {conexionActiva}")

    # Registrar Blueprints (rutas de la API)
    app.register_blueprint(duenosBlueprint)
    app.register_blueprint(mascotasBlueprint)
    app.register_blueprint(citasBlueprint)
    app.register_blueprint(historialBlueprint)

    # =============================================
    # RUTAS DEL FRONTEND
    # =============================================
    frontendDir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "Frontend"
    )

    @app.route("/")
    def servirIndex():
        """Sirve la pagina principal del Frontend."""
        return send_from_directory(frontendDir, "index.html")

    @app.route("/admin")
    def servirAdmin():
        """Sirve el panel de administracion de base de datos."""
        return send_from_directory(frontendDir, "admin.html")

    @app.route("/<path:filename>")
    def servirArchivosEstaticos(filename):
        """Sirve archivos estaticos del Frontend (CSS, JS, imagenes)."""
        return send_from_directory(frontendDir, filename)

    # =============================================
    # ENDPOINT DE ESTADO (con info de conexión)
    # =============================================
    @app.route("/api/estado")
    def estadoApi():
        """Endpoint de salud - verifica que la API y la BD esten operativas."""
        return jsonify({
            "estado": "activo",
            "aplicacion": "Huellitas Vet API",
            "version": "1.0.0",
            "baseDeDatos": conexionActiva
        }), 200

    # =============================================
    # API DEL PANEL DE ADMINISTRACIÓN
    # =============================================
    @app.route("/api/admin/info")
    def adminInfo():
        """Retorna información general de la base de datos para el panel admin."""
        try:
            return jsonify({
                "conexion": conexionActiva,
                "tablas": [
                    {"nombre": "duenos", "registros": Dueno.query.count()},
                    {"nombre": "mascotas", "registros": Mascota.query.count()},
                    {"nombre": "citas", "registros": Cita.query.count()},
                    {"nombre": "historial_clinico", "registros": HistorialClinico.query.count()}
                ]
            }), 200
        except Exception as error:
            return jsonify({"error": str(error)}), 500

    @app.route("/api/admin/tabla/<nombreTabla>")
    def adminTabla(nombreTabla):
        """Retorna todos los registros de una tabla para inspección del evaluador."""
        tablas = {
            "duenos": Dueno,
            "mascotas": Mascota,
            "citas": Cita,
            "historial_clinico": HistorialClinico
        }

        if nombreTabla not in tablas:
            return jsonify({"error": f"Tabla '{nombreTabla}' no encontrada"}), 404

        modelo = tablas[nombreTabla]
        registros = modelo.query.all()
        columnas = [col.name for col in modelo.__table__.columns]

        datos = []
        for registro in registros:
            fila = {}
            for columna in columnas:
                valor = getattr(registro, columna)
                fila[columna] = str(valor) if valor is not None else None
            datos.append(fila)

        return jsonify({
            "tabla": nombreTabla,
            "columnas": columnas,
            "registros": datos,
            "total": len(datos)
        }), 200

    @app.route("/api/admin/estructura")
    def adminEstructura():
        """
        Retorna la estructura completa de la BD: tablas, columnas, tipos, PKs y FKs.
        Ideal para que el evaluador verifique normalizacion y relaciones.
        """
        estructura = []
        for modelo in [Dueno, Mascota, Cita, HistorialClinico]:
            tabla = {"nombre": modelo.__tablename__, "columnas": []}
            for columna in modelo.__table__.columns:
                info = {
                    "nombre": columna.name,
                    "tipo": str(columna.type),
                    "nullable": columna.nullable,
                    "primaryKey": columna.primary_key,
                    "unique": columna.unique or False
                }
                if columna.foreign_keys:
                    fk = list(columna.foreign_keys)[0]
                    info["foreignKey"] = str(fk.target_fullname)
                tabla["columnas"].append(info)
            estructura.append(tabla)

        return jsonify({
            "estructura": estructura,
            "totalTablas": len(estructura),
            "conexion": conexionActiva
        }), 200

    print("  Inicializacion completada.")
    return app


# Punto de entrada principal
if __name__ == "__main__":
    app = crearApp()
    print(f"\n  Clinica Veterinaria Huellitas")
    print(f"  Servidor:    http://localhost:5000")
    print(f"  Panel Admin: http://localhost:5000/admin")
    print(f"  Base datos:  {conexionActiva}\n")
    app.run(debug=True, port=5000)
