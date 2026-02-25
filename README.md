# 🐾 Huellitas - Clínica Veterinaria

Sistema de gestión clínica veterinaria con arquitectura desacoplada (Backend API REST + Frontend Web).

## Tecnologías

- **Backend:** Python 3 + Flask + SQLAlchemy
- **Frontend:** HTML5 + CSS3 + JavaScript (Fetch API)
- **Base de datos:** SQLite (archivo local, cero configuración)
- **Arquitectura:** Cliente-Servidor (API REST + SPA)

## Instalación Rápida (3 pasos)

### Prerequisitos
- Python 3.8 o superior (verificar con `python --version`)

### Paso 1: Instalar dependencias
```bash
cd Backend
pip install -r requirements.txt
```

### Paso 2: Cargar datos de prueba
```bash
python seed.py
```

### Paso 3: Iniciar el servidor
```bash
python app.py
```

### ¡Listo!
Abrir el navegador en: **http://localhost:5000**

## Estructura del Proyecto

```
huellitas-vet/
├── Backend/              # API REST (Flask)
│   ├── app.py            # Punto de entrada del servidor
│   ├── config.py         # Configuración de la aplicación
│   ├── seed.py           # Datos semilla para pruebas
│   ├── requirements.txt  # Dependencias de Python
│   ├── models/           # Modelos de datos (SQLAlchemy)
│   │   ├── dueno.py      # Modelo de Dueño
│   │   ├── mascota.py    # Modelo de Mascota
│   │   └── cita.py       # Modelo de Cita
│   └── routes/           # Endpoints de la API
│       ├── duenos.py     # CRUD de Dueños
│       ├── mascotas.py   # CRUD de Mascotas
│       └── citas.py      # CRUD de Citas
├── Frontend/             # Cliente Web
│   ├── index.html        # Página principal (SPA)
│   ├── css/styles.css    # Estilos responsive
│   └── js/               # Lógica del cliente
│       ├── api.js        # Módulo de comunicación con la API
│       ├── duenos.js     # Gestión de Dueños
│       ├── mascotas.js   # Gestión de Mascotas
│       ├── citas.js      # Gestión de Citas
│       └── app.js        # Navegación y utilidades
├── BdD/                  # Base de datos
│   ├── schema.sql        # Script de creación de tablas
│   ├── seed.sql          # Datos semilla (INSERT)
│   └── diagrama_er.png   # Diagrama Entidad-Relación
└── DT/                   # Documentación técnica
    ├── huellitas_vet_api.postman_collection.json
    ├── link_video.txt
    └── (manual_despliegue.pdf)
```

## API REST - Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/estado | Estado de la API |
| GET | /api/duenos | Listar dueños |
| POST | /api/duenos | Crear dueño |
| PUT | /api/duenos/:id | Actualizar dueño |
| DELETE | /api/duenos/:id | Eliminar dueño |
| GET | /api/duenos/buscar?q= | Buscar dueño |
| GET | /api/mascotas | Listar mascotas |
| POST | /api/mascotas | Crear mascota |
| PUT | /api/mascotas/:id | Actualizar mascota |
| DELETE | /api/mascotas/:id | Eliminar mascota |
| GET | /api/mascotas/buscar?q= | Buscar mascotas |
| GET | /api/citas | Listar citas |
| POST | /api/citas | Crear cita |
| PUT | /api/citas/:id | Actualizar cita |
| DELETE | /api/citas/:id | Eliminar cita |

## Autor

Desarrollado como proyecto de Certificación Alemana: Técnico en Asistencia para el Desarrollo de Software

