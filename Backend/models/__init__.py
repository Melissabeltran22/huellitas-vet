"""
Inicialización de la base de datos con SQLAlchemy.
Este módulo centraliza la instancia de la BD para evitar importaciones circulares.
"""
from flask_sqlalchemy import SQLAlchemy

# Instancia global de SQLAlchemy, se inicializa en app.py
db = SQLAlchemy()
