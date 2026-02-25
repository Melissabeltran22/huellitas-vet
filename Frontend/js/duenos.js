/**
 * Módulo de gestión de Dueños.
 * Controla la lógica del CRUD de dueños en la interfaz.
 */

/**
 * Carga y renderiza la lista de dueños en la tabla.
 * Se llama al navegar a la sección de dueños y después de cada operación CRUD.
 */
async function cargarDuenos() {
    try {
        const duenos = await obtenerDuenos();
        const tabla = document.getElementById("tablaDuenos");

        if (duenos.length === 0) {
            tabla.innerHTML = `
                <tr>
                    <td colspan="6" class="empty-state">
                        No hay dueños registrados. ¡Registre el primero!
                    </td>
                </tr>`;
            return;
        }

        // Generar filas de la tabla con los datos de cada dueño
        tabla.innerHTML = duenos.map(dueno => `
            <tr>
                <td><strong>${dueno.nombre} ${dueno.apellido}</strong></td>
                <td>${dueno.documento}</td>
                <td>${dueno.telefono}</td>
                <td>${dueno.correo || "—"}</td>
                <td class="hide-mobile">
                    <span class="badge badge-programada">${dueno.cantidadMascotas}</span>
                </td>
                <td>
                    <div class="action-buttons">
                        <button class="btn-icon edit" onclick="editarDueno(${dueno.id})" title="Editar">✏️</button>
                        <button class="btn-icon delete" onclick="preguntarEliminarDueno(${dueno.id}, '${dueno.nombre} ${dueno.apellido}')" title="Eliminar">🗑️</button>
                    </div>
                </td>
            </tr>
        `).join("");
    } catch (error) {
        mostrarToast("Error al cargar dueños: " + error.message, "error");
    }
}

/** Muestra el formulario para registrar un nuevo dueño. */
function mostrarFormularioDueno() {
    document.getElementById("formDueno").classList.remove("hidden");
    document.getElementById("formDuenoTitulo").textContent = "Registrar Nuevo Dueño";
    document.getElementById("duenoId").value = "";
    limpiarFormularioDueno();
}

/** Oculta y limpia el formulario de dueño. */
function cancelarFormularioDueno() {
    document.getElementById("formDueno").classList.add("hidden");
    limpiarFormularioDueno();
}

/** Reinicia todos los campos del formulario. */
function limpiarFormularioDueno() {
    document.getElementById("duenoNombre").value = "";
    document.getElementById("duenoApellido").value = "";
    document.getElementById("duenoDocumento").value = "";
    document.getElementById("duenoTelefono").value = "";
    document.getElementById("duenoCorreo").value = "";
    document.getElementById("duenoDireccion").value = "";
}

/**
 * Guarda un dueño (crear o actualizar según si tiene ID).
 * El formulario usa onsubmit para prevenir el envío por defecto.
 */
async function guardarDueno(evento) {
    evento.preventDefault(); // Evitar recarga de página

    const id = document.getElementById("duenoId").value;
    const datos = {
        nombre: document.getElementById("duenoNombre").value,
        apellido: document.getElementById("duenoApellido").value,
        documento: document.getElementById("duenoDocumento").value,
        telefono: document.getElementById("duenoTelefono").value,
        correo: document.getElementById("duenoCorreo").value,
        direccion: document.getElementById("duenoDireccion").value
    };

    try {
        if (id) {
            // Actualizar dueño existente (PUT)
            await actualizarDueno(id, datos);
            mostrarToast("Dueño actualizado exitosamente", "success");
        } else {
            // Crear nuevo dueño (POST)
            await crearDueno(datos);
            mostrarToast("Dueño registrado exitosamente", "success");
        }

        cancelarFormularioDueno();
        cargarDuenos();
        actualizarEstadisticas(); // Actualizar contador del dashboard
    } catch (error) {
        mostrarToast(error.message, "error");
    }
}

/**
 * Carga los datos de un dueño en el formulario para edición.
 * Hace un GET al servidor para obtener los datos actualizados.
 */
async function editarDueno(id) {
    try {
        const dueno = await obtenerDuenoPorId(id);

        document.getElementById("formDueno").classList.remove("hidden");
        document.getElementById("formDuenoTitulo").textContent = "Editar Dueño";
        document.getElementById("duenoId").value = dueno.id;
        document.getElementById("duenoNombre").value = dueno.nombre;
        document.getElementById("duenoApellido").value = dueno.apellido;
        document.getElementById("duenoDocumento").value = dueno.documento;
        document.getElementById("duenoTelefono").value = dueno.telefono;
        document.getElementById("duenoCorreo").value = dueno.correo || "";
        document.getElementById("duenoDireccion").value = dueno.direccion || "";

        // Scroll al formulario para que sea visible
        document.getElementById("formDueno").scrollIntoView({ behavior: "smooth" });
    } catch (error) {
        mostrarToast("Error al cargar datos del dueño", "error");
    }
}

/** Muestra el modal de confirmación antes de eliminar un dueño. */
function preguntarEliminarDueno(id, nombre) {
    mostrarModalConfirmacion(
        "Eliminar Dueño",
        `¿Está seguro de eliminar a "${nombre}"? Se eliminarán también todas sus mascotas y citas asociadas.`,
        () => ejecutarEliminarDueno(id)
    );
}

/** Ejecuta la eliminación del dueño tras confirmación. */
async function ejecutarEliminarDueno(id) {
    try {
        await eliminarDueno(id);
        mostrarToast("Dueño eliminado correctamente", "success");
        cargarDuenos();
        actualizarEstadisticas();
    } catch (error) {
        mostrarToast("Error al eliminar: " + error.message, "error");
    }
}
