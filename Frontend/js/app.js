/**
 * Módulo principal de la aplicación.
 * Controla: navegación entre secciones, notificaciones toast,
 * modal de confirmación, estadísticas del dashboard y buscador global.
 */

// =============================================
// NAVEGACIÓN ENTRE SECCIONES (SPA)
// =============================================

// Referencia a la función de callback del modal (se asigna dinámicamente)
let accionConfirmacion = null;

/**
 * Navega entre las secciones de la aplicación.
 * Implementa un patrón SPA (Single Page Application) básico:
 * oculta todas las secciones y muestra solo la seleccionada.
 * 
 * @param {string} seccion - Nombre de la sección destino
 */
function navegarA(seccion) {
    // Ocultar todas las secciones
    document.querySelectorAll(".section").forEach(sec => {
        sec.classList.add("hidden");
    });

    // Mostrar la sección seleccionada
    const seccionId = `section${seccion.charAt(0).toUpperCase() + seccion.slice(1)}`;
    document.getElementById(seccionId).classList.remove("hidden");

    // Actualizar estado activo en la barra de navegación
    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.remove("active");
        if (link.dataset.section === seccion) {
            link.classList.add("active");
        }
    });

    // Cargar datos de la sección al navegar
    switch (seccion) {
        case "dashboard":
            actualizarEstadisticas();
            cargarCitasDashboard();
            break;
        case "duenos":
            cargarDuenos();
            break;
        case "mascotas":
            cargarMascotas();
            break;
        case "citas":
            cargarCitas();
            break;
        case "historial":
            cargarHistorial();
            break;
    }

    // Cerrar menú móvil si está abierto
    document.getElementById("navbarMenu").classList.remove("open");
}

// =============================================
// NOTIFICACIONES TOAST
// =============================================

/**
 * Muestra una notificación temporal (toast) al usuario.
 * Se auto-elimina después de 3 segundos.
 * 
 * @param {string} mensaje - Texto de la notificación
 * @param {string} tipo - Tipo: "success", "error", "warning"
 */
function mostrarToast(mensaje, tipo = "success") {
    const contenedor = document.getElementById("toastContainer");
    const toast = document.createElement("div");
    toast.className = `toast toast-${tipo}`;
    toast.textContent = mensaje;
    contenedor.appendChild(toast);

    // Remover el toast después de 3 segundos
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// =============================================
// MODAL DE CONFIRMACIÓN
// =============================================

/**
 * Muestra un modal de confirmación antes de acciones destructivas.
 * Patrón para evitar eliminaciones accidentales.
 * 
 * @param {string} titulo - Título del modal
 * @param {string} mensaje - Mensaje descriptivo
 * @param {Function} callback - Función a ejecutar si el usuario confirma
 */
function mostrarModalConfirmacion(titulo, mensaje, callback) {
    document.getElementById("modalTitulo").textContent = titulo;
    document.getElementById("modalMensaje").textContent = mensaje;
    document.getElementById("modalConfirmacion").classList.remove("hidden");
    accionConfirmacion = callback;
}

/** Ejecuta la acción confirmada y cierra el modal. */
function confirmarAccion() {
    if (accionConfirmacion) {
        accionConfirmacion();
    }
    cerrarModal();
}

/** Cierra el modal sin ejecutar la acción. */
function cerrarModal() {
    document.getElementById("modalConfirmacion").classList.add("hidden");
    accionConfirmacion = null;
}

// =============================================
// ESTADÍSTICAS DEL DASHBOARD
// =============================================

/**
 * Actualiza los contadores del dashboard.
 * Hace peticiones paralelas para obtener los totales.
 */
async function actualizarEstadisticas() {
    try {
        // Peticiones en paralelo con Promise.all (más eficiente)
        const [duenos, mascotas, citas] = await Promise.all([
            obtenerDuenos(),
            obtenerMascotas(),
            obtenerCitas()
        ]);

        document.getElementById("statDuenos").textContent = duenos.length;
        document.getElementById("statMascotas").textContent = mascotas.length;

        // Contar solo citas programadas
        const citasProgramadas = citas.filter(c => c.estado === "Programada");
        document.getElementById("statCitas").textContent = citasProgramadas.length;
    } catch (error) {
        console.error("Error al actualizar estadísticas:", error);
    }
}

// =============================================
// BUSCADOR GLOBAL
// =============================================

/**
 * Busca mascotas por nombre o documento del dueño.
 * Requerimiento funcional: "filtrar mascotas por nombre o documento del dueño".
 */
async function buscarMascotaGlobal() {
    const termino = document.getElementById("buscadorGlobal").value.trim();
    const contenedor = document.getElementById("resultadosBusqueda");

    if (!termino) {
        contenedor.innerHTML = "";
        mostrarToast("Escriba un término de búsqueda", "warning");
        return;
    }

    try {
        const resultados = await buscarMascotas(termino);

        if (resultados.length === 0) {
            contenedor.innerHTML = `
                <div class="empty-state">
                    No se encontraron mascotas para "${termino}"
                </div>`;
            return;
        }

        contenedor.innerHTML = resultados.map(mascota => `
            <div class="search-result-card">
                <div>
                    <strong>${obtenerIconoEspecie(mascota.especie)} ${mascota.nombre}</strong>
                    — ${mascota.raza} · ${mascota.edad}
                </div>
                <div>
                    👤 ${mascota.duenoNombre}
                </div>
            </div>
        `).join("");
    } catch (error) {
        mostrarToast("Error en la búsqueda: " + error.message, "error");
    }
}

// =============================================
// INICIALIZACIÓN DE LA APLICACIÓN
// =============================================

/**
 * Se ejecuta cuando el DOM está completamente cargado.
 * Configura los event listeners y carga los datos iniciales.
 */
document.addEventListener("DOMContentLoaded", function () {
    // --- Event listeners de navegación ---
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (evento) {
            evento.preventDefault();
            navegarA(this.dataset.section);
        });
    });

    // --- Menú hamburguesa (móvil) ---
    document.getElementById("menuToggle").addEventListener("click", function () {
        document.getElementById("navbarMenu").classList.toggle("open");
    });

    // --- Buscador: buscar al presionar Enter ---
    document.getElementById("buscadorGlobal").addEventListener("keyup", function (evento) {
        if (evento.key === "Enter") {
            buscarMascotaGlobal();
        }
    });

    // --- Cerrar modal al hacer clic fuera ---
    document.getElementById("modalConfirmacion").addEventListener("click", function (evento) {
        if (evento.target === this) {
            cerrarModal();
        }
    });

    // --- Cargar datos iniciales del dashboard ---
    actualizarEstadisticas();
    cargarCitasDashboard();

    console.log("🐾 Huellitas Vet - Aplicación inicializada correctamente");
});
