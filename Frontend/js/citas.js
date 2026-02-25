/**
 * Módulo de gestión de Citas.
 * Controla la agenda de citas veterinarias.
 */

/**
 * Formatea una fecha ISO (YYYY-MM-DD) a formato legible en español.
 * Ejemplo: "2025-02-15" -> "15 feb 2025"
 */
function formatearFecha(fechaIso) {
    const fecha = new Date(fechaIso + "T00:00:00"); // Evitar desfase de zona horaria
    const opciones = { day: "numeric", month: "short", year: "numeric" };
    return fecha.toLocaleDateString("es-CO", opciones);
}

/**
 * Retorna la clase CSS para el badge de estado de la cita.
 */
function claseBadgeEstado(estado) {
    const clases = {
        "Programada": "badge-programada",
        "Completada": "badge-completada",
        "Cancelada": "badge-cancelada"
    };
    return clases[estado] || "badge-programada";
}

/**
 * Carga y renderiza la lista de citas en la tabla.
 */
async function cargarCitas() {
    try {
        const citas = await obtenerCitas();
        const tabla = document.getElementById("tablaCitas");

        if (citas.length === 0) {
            tabla.innerHTML = `
                <tr>
                    <td colspan="7" class="empty-state">
                        No hay citas registradas. ¡Agende la primera!
                    </td>
                </tr>`;
            return;
        }

        tabla.innerHTML = citas.map(cita => `
            <tr>
                <td>${formatearFecha(cita.fecha)}</td>
                <td>${cita.hora}</td>
                <td><strong>${cita.mascotaNombre}</strong></td>
                <td class="hide-mobile">${cita.duenoNombre}</td>
                <td>${cita.motivo}</td>
                <td><span class="badge ${claseBadgeEstado(cita.estado)}">${cita.estado}</span></td>
                <td>
                    <div class="action-buttons">
                        <button class="btn-icon edit" onclick="editarCita(${cita.id})" title="Editar">✏️</button>
                        <button class="btn-icon delete" onclick="preguntarEliminarCita(${cita.id})" title="Eliminar">🗑️</button>
                    </div>
                </td>
            </tr>
        `).join("");
    } catch (error) {
        mostrarToast("Error al cargar citas: " + error.message, "error");
    }
}

/**
 * Carga la lista de mascotas en el selector del formulario de citas.
 * Muestra nombre de mascota + dueño para fácil identificación.
 */
async function cargarSelectorMascotas() {
    try {
        const mascotas = await obtenerMascotas();
        const selector = document.getElementById("citaMascota");

        selector.innerHTML = '<option value="">Seleccionar mascota...</option>';
        mascotas.forEach(mascota => {
            selector.innerHTML += `
                <option value="${mascota.id}">
                    ${obtenerIconoEspecie(mascota.especie)} ${mascota.nombre} (Dueño: ${mascota.duenoNombre})
                </option>`;
        });
    } catch (error) {
        console.error("Error al cargar selector de mascotas:", error);
    }
}

/** Muestra el formulario para agendar una nueva cita. */
function mostrarFormularioCita() {
    document.getElementById("formCita").classList.remove("hidden");
    document.getElementById("formCitaTitulo").textContent = "Agendar Nueva Cita";
    document.getElementById("citaId").value = "";
    limpiarFormularioCita();
    cargarSelectorMascotas();

    // Establecer fecha mínima como hoy (no permite fechas pasadas)
    document.getElementById("citaFecha").min = new Date().toISOString().split("T")[0];
}

/** Oculta y limpia el formulario de cita. */
function cancelarFormularioCita() {
    document.getElementById("formCita").classList.add("hidden");
    limpiarFormularioCita();
}

/** Reinicia los campos del formulario de cita. */
function limpiarFormularioCita() {
    document.getElementById("citaMascota").value = "";
    document.getElementById("citaFecha").value = "";
    document.getElementById("citaHora").value = "";
    document.getElementById("citaMotivo").value = "";
    document.getElementById("citaEstado").value = "Programada";
}

/** Guarda una cita (crear o actualizar). */
async function guardarCita(evento) {
    evento.preventDefault();

    const id = document.getElementById("citaId").value;
    const datos = {
        mascotaId: parseInt(document.getElementById("citaMascota").value),
        fecha: document.getElementById("citaFecha").value,
        hora: document.getElementById("citaHora").value,
        motivo: document.getElementById("citaMotivo").value,
        estado: document.getElementById("citaEstado").value
    };

    try {
        if (id) {
            await actualizarCitaApi(id, datos);
            mostrarToast("Cita actualizada exitosamente", "success");
        } else {
            await crearCita(datos);
            mostrarToast("Cita agendada exitosamente", "success");
        }

        cancelarFormularioCita();
        cargarCitas();
        actualizarEstadisticas();
    } catch (error) {
        mostrarToast(error.message, "error");
    }
}

/** Carga datos de una cita en el formulario para edición. */
async function editarCita(id) {
    try {
        const cita = await obtenerCitaPorId(id);
        await cargarSelectorMascotas();

        document.getElementById("formCita").classList.remove("hidden");
        document.getElementById("formCitaTitulo").textContent = "Editar Cita";
        document.getElementById("citaId").value = cita.id;
        document.getElementById("citaMascota").value = cita.mascotaId;
        document.getElementById("citaFecha").value = cita.fecha;
        document.getElementById("citaFecha").min = new Date().toISOString().split("T")[0];
        document.getElementById("citaHora").value = cita.hora;
        document.getElementById("citaMotivo").value = cita.motivo;
        document.getElementById("citaEstado").value = cita.estado;

        document.getElementById("formCita").scrollIntoView({ behavior: "smooth" });
    } catch (error) {
        mostrarToast("Error al cargar datos de la cita", "error");
    }
}

/** Confirmación antes de eliminar cita. */
function preguntarEliminarCita(id) {
    mostrarModalConfirmacion(
        "Eliminar Cita",
        "¿Está seguro de eliminar esta cita?",
        () => ejecutarEliminarCita(id)
    );
}

/** Ejecuta la eliminación de la cita. */
async function ejecutarEliminarCita(id) {
    try {
        await eliminarCita(id);
        mostrarToast("Cita eliminada correctamente", "success");
        cargarCitas();
        actualizarEstadisticas();
    } catch (error) {
        mostrarToast("Error al eliminar: " + error.message, "error");
    }
}

/**
 * Carga las próximas citas en el dashboard.
 * Muestra solo las citas programadas (no completadas ni canceladas).
 */
async function cargarCitasDashboard() {
    try {
        const citas = await obtenerCitas();
        const contenedor = document.getElementById("listaCitasDashboard");

        // Filtrar solo citas programadas
        const citasProgramadas = citas.filter(cita => cita.estado === "Programada");

        if (citasProgramadas.length === 0) {
            contenedor.innerHTML = '<div class="empty-state">No hay citas próximas</div>';
            return;
        }

        // Mostrar máximo 5 próximas citas
        contenedor.innerHTML = citasProgramadas.slice(0, 5).map(cita => `
            <div class="cita-preview-item">
                <div class="cita-preview-info">
                    <span class="cita-preview-date">${formatearFecha(cita.fecha)} - ${cita.hora}</span>
                    <span><strong>${cita.mascotaNombre}</strong> — ${cita.motivo}</span>
                </div>
                <span class="badge badge-programada">${cita.estado}</span>
            </div>
        `).join("");
    } catch (error) {
        console.error("Error al cargar citas del dashboard:", error);
    }
}
