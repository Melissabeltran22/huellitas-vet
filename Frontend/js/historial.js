/**
 * Módulo de gestión del Historial Clínico (Valor Agregado).
 * Muestra los registros médicos en formato timeline para fácil lectura.
 * Permite filtrar por mascota para ver su expediente completo.
 */

/**
 * Carga y renderiza el historial clínico en formato timeline.
 * El timeline es más visual que una tabla para registros médicos.
 */
async function cargarHistorial() {
    try {
        const registros = await obtenerHistorial();
        const timeline = document.getElementById("timelineHistorial");
        await cargarSelectorFiltroMascotas();

        if (registros.length === 0) {
            timeline.innerHTML = `
                <div class="empty-state">
                    <p>No hay registros clínicos. ¡Registre el primero!</p>
                </div>`;
            return;
        }

        renderizarTimeline(registros, timeline);
    } catch (error) {
        mostrarToast("Error al cargar historial: " + error.message, "error");
    }
}

/**
 * Renderiza los registros en formato timeline visual.
 * Cada registro se muestra como una tarjeta con fecha, diagnóstico y tratamiento.
 */
function renderizarTimeline(registros, contenedor) {
    contenedor.innerHTML = registros.map(registro => `
        <div class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-card">
                <div class="timeline-header">
                    <div class="timeline-date">
                        <span class="timeline-fecha">${formatearFecha(registro.fecha)}</span>
                        <span class="timeline-vet">🩺 ${registro.veterinario}</span>
                    </div>
                    <div class="action-buttons">
                        <button class="btn-icon edit" onclick="editarHistorial(${registro.id})" title="Editar">✏️</button>
                        <button class="btn-icon delete" onclick="preguntarEliminarHistorial(${registro.id})" title="Eliminar">🗑️</button>
                    </div>
                </div>
                <div class="timeline-mascota">
                    ${obtenerIconoEspecie(registro.mascotaNombre ? "" : "")} 
                    <strong>${registro.mascotaNombre}</strong>
                    <span class="timeline-dueno">— Dueño: ${registro.duenoNombre}</span>
                    ${registro.pesoEnConsulta ? `<span class="badge badge-programada">${registro.pesoEnConsulta} kg</span>` : ""}
                </div>
                <div class="timeline-body">
                    <div class="timeline-detail">
                        <span class="timeline-label">Diagnóstico</span>
                        <p>${registro.diagnostico}</p>
                    </div>
                    <div class="timeline-detail">
                        <span class="timeline-label">Tratamiento</span>
                        <p>${registro.tratamiento}</p>
                    </div>
                    ${registro.medicamentos ? `
                    <div class="timeline-detail">
                        <span class="timeline-label">💊 Medicamentos</span>
                        <p>${registro.medicamentos}</p>
                    </div>` : ""}
                    ${registro.observaciones ? `
                    <div class="timeline-detail">
                        <span class="timeline-label">📝 Observaciones</span>
                        <p>${registro.observaciones}</p>
                    </div>` : ""}
                </div>
            </div>
        </div>
    `).join("");
}

/**
 * Carga mascotas en el selector de filtro del historial.
 */
async function cargarSelectorFiltroMascotas() {
    try {
        const mascotas = await obtenerMascotas();
        const selector = document.getElementById("historialFiltroMascota");

        selector.innerHTML = '<option value="">Todas las mascotas</option>';
        mascotas.forEach(mascota => {
            selector.innerHTML += `
                <option value="${mascota.id}">
                    ${obtenerIconoEspecie(mascota.especie)} ${mascota.nombre} (${mascota.duenoNombre})
                </option>`;
        });
    } catch (error) {
        console.error("Error al cargar selector de filtro:", error);
    }
}

/**
 * Filtra el historial clínico por mascota seleccionada.
 * Si no se selecciona ninguna, muestra todos los registros.
 */
async function filtrarHistorialPorMascota() {
    const mascotaId = document.getElementById("historialFiltroMascota").value;
    const timeline = document.getElementById("timelineHistorial");

    try {
        if (mascotaId) {
            // Obtener historial de una mascota específica
            const resultado = await obtenerHistorialPorMascota(mascotaId);
            if (resultado.historial.length === 0) {
                timeline.innerHTML = `
                    <div class="empty-state">
                        <p>No hay registros clínicos para esta mascota.</p>
                    </div>`;
                return;
            }
            renderizarTimeline(resultado.historial, timeline);
        } else {
            // Mostrar todos los registros
            cargarHistorial();
        }
    } catch (error) {
        mostrarToast("Error al filtrar historial: " + error.message, "error");
    }
}

/**
 * Carga mascotas en el selector del formulario de historial.
 */
async function cargarSelectorMascotasHistorial() {
    try {
        const mascotas = await obtenerMascotas();
        const selector = document.getElementById("historialMascota");

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

/** Muestra el formulario para un nuevo registro clínico. */
function mostrarFormularioHistorial() {
    document.getElementById("formHistorial").classList.remove("hidden");
    document.getElementById("formHistorialTitulo").textContent = "Nuevo Registro Clínico";
    document.getElementById("historialId").value = "";
    limpiarFormularioHistorial();
    cargarSelectorMascotasHistorial();

    // Fecha por defecto: hoy
    document.getElementById("historialFecha").value = new Date().toISOString().split("T")[0];
    document.getElementById("historialFecha").max = new Date().toISOString().split("T")[0];
}

/** Oculta y limpia el formulario. */
function cancelarFormularioHistorial() {
    document.getElementById("formHistorial").classList.add("hidden");
    limpiarFormularioHistorial();
}

/** Reinicia los campos del formulario. */
function limpiarFormularioHistorial() {
    document.getElementById("historialMascota").value = "";
    document.getElementById("historialFecha").value = "";
    document.getElementById("historialVeterinario").value = "";
    document.getElementById("historialPeso").value = "";
    document.getElementById("historialDiagnostico").value = "";
    document.getElementById("historialTratamiento").value = "";
    document.getElementById("historialMedicamentos").value = "";
    document.getElementById("historialObservaciones").value = "";
}

/** Guarda un registro clínico (crear o actualizar). */
async function guardarHistorial(evento) {
    evento.preventDefault();

    const id = document.getElementById("historialId").value;
    const datos = {
        mascotaId: parseInt(document.getElementById("historialMascota").value),
        fecha: document.getElementById("historialFecha").value,
        veterinario: document.getElementById("historialVeterinario").value,
        pesoEnConsulta: parseFloat(document.getElementById("historialPeso").value) || null,
        diagnostico: document.getElementById("historialDiagnostico").value,
        tratamiento: document.getElementById("historialTratamiento").value,
        medicamentos: document.getElementById("historialMedicamentos").value,
        observaciones: document.getElementById("historialObservaciones").value
    };

    try {
        if (id) {
            await actualizarRegistroClinico(id, datos);
            mostrarToast("Registro clínico actualizado", "success");
        } else {
            await crearRegistroClinico(datos);
            mostrarToast("Registro clínico creado exitosamente", "success");
        }

        cancelarFormularioHistorial();
        cargarHistorial();
    } catch (error) {
        mostrarToast(error.message, "error");
    }
}

/** Carga datos de un registro para edición. */
async function editarHistorial(id) {
    try {
        const registro = await obtenerRegistroPorId(id);
        await cargarSelectorMascotasHistorial();

        document.getElementById("formHistorial").classList.remove("hidden");
        document.getElementById("formHistorialTitulo").textContent = "Editar Registro Clínico";
        document.getElementById("historialId").value = registro.id;
        document.getElementById("historialMascota").value = registro.mascotaId;
        document.getElementById("historialFecha").value = registro.fecha;
        document.getElementById("historialFecha").max = new Date().toISOString().split("T")[0];
        document.getElementById("historialVeterinario").value = registro.veterinario;
        document.getElementById("historialPeso").value = registro.pesoEnConsulta || "";
        document.getElementById("historialDiagnostico").value = registro.diagnostico;
        document.getElementById("historialTratamiento").value = registro.tratamiento;
        document.getElementById("historialMedicamentos").value = registro.medicamentos || "";
        document.getElementById("historialObservaciones").value = registro.observaciones || "";

        document.getElementById("formHistorial").scrollIntoView({ behavior: "smooth" });
    } catch (error) {
        mostrarToast("Error al cargar registro clínico", "error");
    }
}

/** Confirmación antes de eliminar. */
function preguntarEliminarHistorial(id) {
    mostrarModalConfirmacion(
        "Eliminar Registro Clínico",
        "¿Está seguro de eliminar este registro del historial? Esta acción no se puede deshacer.",
        () => ejecutarEliminarHistorial(id)
    );
}

/** Ejecuta la eliminación del registro. */
async function ejecutarEliminarHistorial(id) {
    try {
        await eliminarRegistroClinico(id);
        mostrarToast("Registro clínico eliminado", "success");
        cargarHistorial();
    } catch (error) {
        mostrarToast("Error al eliminar: " + error.message, "error");
    }
}
