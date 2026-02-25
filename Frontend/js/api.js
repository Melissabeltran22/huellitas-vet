/**
 * Módulo API - Centraliza todas las peticiones HTTP al Backend.
 * Utiliza la Fetch API nativa de JavaScript para consumir la API REST.
 * 
 * Flujo de datos: Frontend (Fetch) --> API REST (Flask) --> Base de Datos (SQLite)
 */

// URL base de la API (relativa, funciona porque Flask sirve todo)
const API_BASE = "/api";

/**
 * Función genérica para realizar peticiones HTTP.
 * Encapsula la lógica de fetch, manejo de errores y parseo de JSON.
 * 
 * @param {string} endpoint - Ruta del endpoint (ej: "/duenos")
 * @param {string} metodo - Método HTTP (GET, POST, PUT, DELETE)
 * @param {object|null} datos - Body de la petición (se envía como JSON)
 * @returns {Promise<object>} - Respuesta parseada del servidor
 */
async function peticionApi(endpoint, metodo = "GET", datos = null) {
    // Configurar opciones de la petición
    const opciones = {
        method: metodo,
        headers: {
            "Content-Type": "application/json"
        }
    };

    // Solo incluir body en métodos que lo requieran
    if (datos && (metodo === "POST" || metodo === "PUT")) {
        opciones.body = JSON.stringify(datos);
    }

    try {
        // Realizar la petición con Fetch API
        const respuesta = await fetch(`${API_BASE}${endpoint}`, opciones);
        const json = await respuesta.json();

        // Si la respuesta no es exitosa, lanzar error con mensaje del servidor
        if (!respuesta.ok) {
            throw new Error(json.error || "Error en la petición");
        }

        return json;
    } catch (error) {
        // Relanzar el error para que lo maneje el componente que llamó
        console.error(`Error en ${metodo} ${endpoint}:`, error.message);
        throw error;
    }
}

// =============================================
// ENDPOINTS DE DUEÑOS
// =============================================

/** Obtiene la lista completa de dueños. */
function obtenerDuenos() {
    return peticionApi("/duenos");
}

/** Obtiene un dueño por su ID. */
function obtenerDuenoPorId(id) {
    return peticionApi(`/duenos/${id}`);
}

/** Registra un nuevo dueño. */
function crearDueno(datos) {
    return peticionApi("/duenos", "POST", datos);
}

/** Actualiza un dueño existente. */
function actualizarDueno(id, datos) {
    return peticionApi(`/duenos/${id}`, "PUT", datos);
}

/** Elimina un dueño (y sus mascotas/citas por CASCADE). */
function eliminarDueno(id) {
    return peticionApi(`/duenos/${id}`, "DELETE");
}

/** Busca dueños por nombre o documento. */
function buscarDuenos(termino) {
    return peticionApi(`/duenos/buscar?q=${encodeURIComponent(termino)}`);
}

// =============================================
// ENDPOINTS DE MASCOTAS
// =============================================

/** Obtiene la lista completa de mascotas. */
function obtenerMascotas() {
    return peticionApi("/mascotas");
}

/** Obtiene una mascota por su ID. */
function obtenerMascotaPorId(id) {
    return peticionApi(`/mascotas/${id}`);
}

/** Registra una nueva mascota. */
function crearMascota(datos) {
    return peticionApi("/mascotas", "POST", datos);
}

/** Actualiza una mascota existente. */
function actualizarMascota(id, datos) {
    return peticionApi(`/mascotas/${id}`, "PUT", datos);
}

/** Elimina una mascota (y sus citas por CASCADE). */
function eliminarMascota(id) {
    return peticionApi(`/mascotas/${id}`, "DELETE");
}

/** Busca mascotas por nombre o documento del dueño. */
function buscarMascotas(termino) {
    return peticionApi(`/mascotas/buscar?q=${encodeURIComponent(termino)}`);
}

// =============================================
// ENDPOINTS DE CITAS
// =============================================

/** Obtiene la lista completa de citas. */
function obtenerCitas() {
    return peticionApi("/citas");
}

/** Obtiene una cita por su ID. */
function obtenerCitaPorId(id) {
    return peticionApi(`/citas/${id}`);
}

/** Agenda una nueva cita. */
function crearCita(datos) {
    return peticionApi("/citas", "POST", datos);
}

/** Actualiza una cita existente. */
function actualizarCitaApi(id, datos) {
    return peticionApi(`/citas/${id}`, "PUT", datos);
}

/** Elimina una cita. */
function eliminarCita(id) {
    return peticionApi(`/citas/${id}`, "DELETE");
}

// =============================================
// ENDPOINTS DE HISTORIAL CLÍNICO
// =============================================

/** Obtiene todos los registros clínicos. */
function obtenerHistorial() {
    return peticionApi("/historial");
}

/** Obtiene un registro clínico por su ID. */
function obtenerRegistroPorId(id) {
    return peticionApi(`/historial/${id}`);
}

/** Obtiene el historial completo de una mascota específica. */
function obtenerHistorialPorMascota(mascotaId) {
    return peticionApi(`/historial/mascota/${mascotaId}`);
}

/** Crea un nuevo registro clínico. */
function crearRegistroClinico(datos) {
    return peticionApi("/historial", "POST", datos);
}

/** Actualiza un registro clínico existente. */
function actualizarRegistroClinico(id, datos) {
    return peticionApi(`/historial/${id}`, "PUT", datos);
}

/** Elimina un registro clínico. */
function eliminarRegistroClinico(id) {
    return peticionApi(`/historial/${id}`, "DELETE");
}
