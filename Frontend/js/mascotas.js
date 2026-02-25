/**
 * Módulo de gestión de Mascotas (Pacientes).
 * Usa tarjetas (cards) en lugar de tabla para una UI más visual.
 */

/**
 * Retorna el emoji correspondiente a la especie de la mascota.
 * Útil para hacer la interfaz más visual e intuitiva.
 */
function obtenerIconoEspecie(especie) {
    const iconos = {
        "Perro": "🐕",
        "Gato": "🐱",
        "Ave": "🐦",
        "Reptil": "🦎",
        "Otro": "🐾"
    };
    return iconos[especie] || "🐾";
}

/**
 * Carga y renderiza la lista de mascotas en formato de tarjetas.
 */
async function cargarMascotas() {
    try {
        const mascotas = await obtenerMascotas();
        const grid = document.getElementById("gridMascotas");

        if (mascotas.length === 0) {
            grid.innerHTML = `
                <div class="empty-state">
                    <p>No hay mascotas registradas. ¡Registre la primera!</p>
                </div>`;
            return;
        }

        // Renderizar tarjeta para cada mascota
        grid.innerHTML = mascotas.map(mascota => `
            <div class="pet-card">
                <div class="pet-card-header">
                    <h4>
                        <span class="especie-icon">${obtenerIconoEspecie(mascota.especie)}</span>
                        ${mascota.nombre}
                    </h4>
                    <div class="action-buttons">
                        <button class="btn-icon edit" onclick="editarMascota(${mascota.id})" title="Editar">✏️</button>
                        <button class="btn-icon delete" onclick="preguntarEliminarMascota(${mascota.id}, '${mascota.nombre}')" title="Eliminar">🗑️</button>
                    </div>
                </div>
                <div class="pet-card-body">
                    <div class="pet-detail">
                        <span>Especie</span>
                        <span>${mascota.especie}</span>
                    </div>
                    <div class="pet-detail">
                        <span>Raza</span>
                        <span>${mascota.raza}</span>
                    </div>
                    <div class="pet-detail">
                        <span>Edad</span>
                        <span>${mascota.edad}</span>
                    </div>
                    <div class="pet-detail">
                        <span>Peso</span>
                        <span>${mascota.peso ? mascota.peso + " kg" : "—"}</span>
                    </div>
                </div>
                <div class="pet-card-footer">
                    <span>👤 ${mascota.duenoNombre}</span>
                    <span>📅 ${mascota.cantidadCitas} cita${mascota.cantidadCitas !== 1 ? "s" : ""}</span>
                </div>
            </div>
        `).join("");
    } catch (error) {
        mostrarToast("Error al cargar mascotas: " + error.message, "error");
    }
}

/**
 * Carga la lista de dueños en el selector del formulario de mascotas.
 * Necesario para asignar una mascota a su dueño (Foreign Key).
 */
async function cargarSelectorDuenos() {
    try {
        const duenos = await obtenerDuenos();
        const selector = document.getElementById("mascotaDueno");

        // Mantener la primera opción (placeholder) y agregar dueños
        selector.innerHTML = '<option value="">Seleccionar dueño...</option>';
        duenos.forEach(dueno => {
            selector.innerHTML += `
                <option value="${dueno.id}">
                    ${dueno.nombre} ${dueno.apellido} (${dueno.documento})
                </option>`;
        });
    } catch (error) {
        console.error("Error al cargar selector de dueños:", error);
    }
}

/** Muestra el formulario para registrar una nueva mascota. */
function mostrarFormularioMascota() {
    document.getElementById("formMascota").classList.remove("hidden");
    document.getElementById("formMascotaTitulo").textContent = "Registrar Nueva Mascota";
    document.getElementById("mascotaId").value = "";
    limpiarFormularioMascota();
    cargarSelectorDuenos(); // Cargar dueños disponibles

    // Establecer fecha máxima como hoy (no permite fechas futuras)
    document.getElementById("mascotaFechaNacimiento").max = new Date().toISOString().split("T")[0];
}

/** Oculta y limpia el formulario de mascota. */
function cancelarFormularioMascota() {
    document.getElementById("formMascota").classList.add("hidden");
    limpiarFormularioMascota();
}

/** Reinicia los campos del formulario de mascota. */
function limpiarFormularioMascota() {
    document.getElementById("mascotaNombre").value = "";
    document.getElementById("mascotaEspecie").value = "";
    document.getElementById("mascotaRaza").value = "";
    document.getElementById("mascotaFechaNacimiento").value = "";
    document.getElementById("mascotaPeso").value = "";
    document.getElementById("mascotaDueno").value = "";
    document.getElementById("mascotaObservaciones").value = "";
}

/** Guarda una mascota (crear o actualizar). */
async function guardarMascota(evento) {
    evento.preventDefault();

    const id = document.getElementById("mascotaId").value;
    const datos = {
        nombre: document.getElementById("mascotaNombre").value,
        especie: document.getElementById("mascotaEspecie").value,
        raza: document.getElementById("mascotaRaza").value,
        fechaNacimiento: document.getElementById("mascotaFechaNacimiento").value,
        peso: parseFloat(document.getElementById("mascotaPeso").value) || null,
        duenoId: parseInt(document.getElementById("mascotaDueno").value),
        observaciones: document.getElementById("mascotaObservaciones").value
    };

    try {
        if (id) {
            await actualizarMascota(id, datos);
            mostrarToast("Mascota actualizada exitosamente", "success");
        } else {
            await crearMascota(datos);
            mostrarToast("Mascota registrada exitosamente", "success");
        }

        cancelarFormularioMascota();
        cargarMascotas();
        actualizarEstadisticas();
    } catch (error) {
        mostrarToast(error.message, "error");
    }
}

/** Carga datos de una mascota en el formulario para edición. */
async function editarMascota(id) {
    try {
        const mascota = await obtenerMascotaPorId(id);
        await cargarSelectorDuenos();

        document.getElementById("formMascota").classList.remove("hidden");
        document.getElementById("formMascotaTitulo").textContent = "Editar Mascota";
        document.getElementById("mascotaId").value = mascota.id;
        document.getElementById("mascotaNombre").value = mascota.nombre;
        document.getElementById("mascotaEspecie").value = mascota.especie;
        document.getElementById("mascotaRaza").value = mascota.raza;
        document.getElementById("mascotaFechaNacimiento").value = mascota.fechaNacimiento;
        document.getElementById("mascotaFechaNacimiento").max = new Date().toISOString().split("T")[0];
        document.getElementById("mascotaPeso").value = mascota.peso || "";
        document.getElementById("mascotaDueno").value = mascota.duenoId;
        document.getElementById("mascotaObservaciones").value = mascota.observaciones || "";

        document.getElementById("formMascota").scrollIntoView({ behavior: "smooth" });
    } catch (error) {
        mostrarToast("Error al cargar datos de la mascota", "error");
    }
}

/** Confirmación antes de eliminar mascota. */
function preguntarEliminarMascota(id, nombre) {
    mostrarModalConfirmacion(
        "Eliminar Mascota",
        `¿Está seguro de eliminar a "${nombre}"? Se eliminarán también todas sus citas.`,
        () => ejecutarEliminarMascota(id)
    );
}

/** Ejecuta la eliminación de la mascota. */
async function ejecutarEliminarMascota(id) {
    try {
        await eliminarMascota(id);
        mostrarToast("Mascota eliminada correctamente", "success");
        cargarMascotas();
        actualizarEstadisticas();
    } catch (error) {
        mostrarToast("Error al eliminar: " + error.message, "error");
    }
}
