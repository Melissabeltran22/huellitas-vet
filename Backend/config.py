"""
Configuración de la aplicación Huellitas Vet.

Estrategia de conexión DUAL:
    1. Si existe DATABASE_URL en variables de entorno → usa Azure (o cualquier BD en nube)
    2. Si no existe o la conexión falla → usa SQLite local como respaldo
    
Esto garantiza que el proyecto SIEMPRE funcione, incluso sin internet.
Las credenciales se cargan desde un archivo .env (nunca hardcodeadas en el código).
"""
import os
from dotenv import load_dotenv

# Cargar variables desde archivo .env (si existe)
load_dotenv()

# Directorio base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración principal de la aplicación."""

    # Clave secreta para sesiones y protección CSRF
    SECRET_KEY = os.environ.get("SECRET_KEY", "huellitas-dev-key-2025")

    # --- ESTRATEGIA DE CONEXIÓN DUAL ---
    # Prioridad 1: Variable de entorno DATABASE_URL (Azure, MySQL, PostgreSQL)
    # Prioridad 2: SQLite local (archivo huellitas.db, cero configuración)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'huellitas.db')}"
    )

    # Ruta de respaldo SQLite (se usa si la conexión principal falla)
    SQLITE_FALLBACK_URI = f"sqlite:///{os.path.join(BASE_DIR, 'huellitas.db')}"

    # Desactivar seguimiento de modificaciones (mejora rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de CORS para permitir peticiones del Frontend
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    @staticmethod
    def obtenerTipoConexion():
        """Retorna una descripción legible del tipo de conexión activa."""
        dbUrl = os.environ.get("DATABASE_URL", "")
        if "mysql" in dbUrl:
            return "MySQL (Azure/Nube)"
        elif "postgresql" in dbUrl:
            return "PostgreSQL (Azure/Nube)"
        elif "mssql" in dbUrl:
            return "SQL Server (Azure/Nube)"
        else:
            return "SQLite (Local)"

