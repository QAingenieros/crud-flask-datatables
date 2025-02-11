/**
 * Inicializa la aplicación cuando el documento está listo.
 * Carga los datos iniciales y configura la tabla.
 */
$(document).ready(async function() {
    const keys = await obtenerKeys('/api/datos');
    const datos = await obtenerDatos('/api/datos');
    inicializarTabla(keys, datos);
});

/**
 * Obtiene las claves (columnas) disponibles desde el endpoint especificado.
 * @param {string} url - URL del endpoint para obtener las claves.
 * @returns {Promise<Array>} Array con las claves disponibles.
 */
async function obtenerKeys(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.data && data.data.length > 0) {
            const keys = Object.keys(data.data[0]);
            console.log('Keys disponibles:', keys);
            return keys;
        } else {
            console.log('No hay datos disponibles');
            return [];
        }
    } catch (error) {
        console.error('Error al obtener las keys:', error);
        return [];
    }
}

/**
 * Obtiene los datos desde el endpoint especificado.
 * @param {string} url - URL del endpoint para obtener los datos.
 * @returns {Promise<Array>} Array con los datos obtenidos.
 */
async function obtenerDatos(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.data && data.data.length > 0) {
            console.log('Datos obtenidos:', data.data);
            return data.data;
        } else {
            console.log('No hay datos disponibles');
            return [];
        }
    } catch (error) {
        console.error('Error al obtener los datos:', error);
        return [];
    }
}

/**
 * Inicializa la tabla DataTable con las columnas y datos especificados.
 * @param {Array} keys - Array con las claves para las columnas.
 * @param {Array} datos - Array con los datos para la tabla.
 */
function inicializarTabla(keys, datos) {
    // Reordenar las keys para que 'id' sea la primera
    const keysOrdenadas = ['id', ...keys.filter(key => key !== 'id')];

    // Generar columnas asegurando que ID es la primera
    const columnas = keysOrdenadas.map(key => ({
        data: key,
        title: key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' ')
    }));

    console.log('Columnas generadas:', columnas);

    if ($.fn.DataTable.isDataTable('#tablaDatos')) {
        $('#tablaDatos').DataTable().destroy();
        $('#tablaDatos').empty();
    }

    $('#tablaDatos').DataTable({
        data: datos,
        columns: columnas.concat([
            {
                data: null,
                render: function(data, type, row) {
                    return `
                        <button onclick="editarRegistro(this)" class="btn btn-primary btn-sm">
                            <i class="fa fa-edit"></i>
                        </button>
                        <button onclick="eliminarRegistro(this)" class="btn btn-danger btn-sm">
                            <i class="fa fa-trash"></i>
                        </button>
                    `;
                },
                title: 'Acciones'
            }
        ]),
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
        },
        order: [[0, 'asc']] // Ordenar por ID de forma ascendente por defecto
    });
}

/**
 * Cambia los datos mostrados en la tabla según el endpoint especificado.
 * @param {string} url - URL del endpoint para obtener los nuevos datos.
 */
async function changeDatatables(url) {
    const keys = await obtenerKeys(url);
    const datos = await obtenerDatos(url);
    inicializarTabla(keys, datos);

    // Actualizar el título
    const endpoint = url.split('/').pop();
    $('#tituloTabla').text(endpoint.charAt(0).toUpperCase() + endpoint.slice(1));
}

/**
 * Muestra el modal para editar un registro existente.
 * @param {HTMLElement} btn - Botón que disparó el evento.
 */
function editarRegistro(btn) {
    const tabla = $('#tablaDatos').DataTable();
    const data = tabla.row($(btn).parents('tr')).data();
    const columnas = tabla.settings().init().columns;

    // Limpiar el formulario
    $('#formEdicion').empty();

    // Cambiar el título del modal
    $('#modalEdicionLabel').text('Editar Registro');

    // Generar campos del formulario dinámicamente
    columnas.forEach((columna, index) => {
        if (columna.data && columna.data !== null) {
            const valor = data[columna.data];
            const campo = generarCampoFormulario(columna.data, columna.title, valor);
            $('#formEdicion').append(campo);
        }
    });

    // Guardar el ID del registro actual
    $('#formEdicion').data('id', data.id);

    // Cambiar el botón de guardar
    const btnGuardar = $('.modal-footer .btn-primary');
    btnGuardar.attr('onclick', 'guardarCambios()');

    // Mostrar el modal
    const modal = new bootstrap.Modal(document.getElementById('modalEdicion'));
    modal.show();
}

/**
 * Genera un campo de formulario HTML basado en los parámetros proporcionados.
 * @param {string} name - Nombre del campo.
 * @param {string} label - Etiqueta para el campo.
 * @param {*} value - Valor inicial del campo.
 * @returns {string} HTML del campo de formulario.
 */
function generarCampoFormulario(name, label, value) {
    // Determinar el tipo de input basado en el nombre del campo o el valor
    let tipo = 'text';
    if (name.includes('fecha')) {
        tipo = 'date';
    } else if (typeof value === 'number') {
        tipo = 'number';
    } else if (name.includes('email')) {
        tipo = 'email';
    }

    return `
        <div class="mb-3">
            <label for="${name}" class="form-label">${label}</label>
            <input type="${tipo}"
                   class="form-control"
                   id="${name}"
                   name="${name}"
                   value="${value || ''}"
                   ${tipo === 'number' ? 'step="any"' : ''}>
        </div>
    `;
}

/**
 * Guarda los cambios realizados en un registro existente.
 * Envía una petición PUT al servidor y actualiza la tabla.
 */
async function guardarCambios() {
    const formData = new FormData(document.getElementById('formEdicion'));
    const datos = Object.fromEntries(formData.entries());
    const id = $('#formEdicion').data('id');

    try {
        // Obtener el endpoint actual
        const endpoint = obtenerEndpointActual();

        // Realizar la petición PUT
        const response = await fetch(`/api/${endpoint}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error al actualizar el registro');
        }

        // Cerrar el modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalEdicion'));
        modal.hide();

        // Recargar la tabla
        const keys = await obtenerKeys(`/api/${endpoint}`);
        const datosNuevos = await obtenerDatos(`/api/${endpoint}`);
        inicializarTabla(keys, datosNuevos);

        // Mostrar mensaje de éxito
        alert('Registro actualizado exitosamente');

    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    }
}

/**
 * Elimina un registro de la base de datos.
 * Envía una petición DELETE al servidor y actualiza la tabla.
 * @param {HTMLElement} btn - Botón que disparó el evento.
 */
async function eliminarRegistro(btn) {
    if (confirm('¿Está seguro de eliminar este registro?')) {
        const tabla = $('#tablaDatos').DataTable();
        const data = tabla.row($(btn).parents('tr')).data();
        const endpoint = obtenerEndpointActual();

        try {
            const response = await fetch(`/api/${endpoint}/${data.id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error al eliminar el registro');
            }

            // Recargar la tabla
            const keys = await obtenerKeys(`/api/${endpoint}`);
            const datosNuevos = await obtenerDatos(`/api/${endpoint}`);
            inicializarTabla(keys, datosNuevos);

            // Mostrar mensaje de éxito
            alert('Registro eliminado exitosamente');

        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    }
}

/**
 * Muestra el modal para agregar un nuevo registro.
 * Genera los campos del formulario dinámicamente según las columnas actuales.
 */
function showAddRegistroModal() {
    const tabla = $('#tablaDatos').DataTable();
    const columnas = tabla.settings().init().columns;

    // Limpiar el formulario
    $('#formEdicion').empty();

    // Cambiar el título del modal
    $('#modalEdicionLabel').text('Nuevo Registro');

    // Generar campos del formulario dinámicamente
    columnas.forEach((columna, index) => {
        if (columna.data && columna.data !== null && columna.data !== 'id') { // Excluir la columna de acciones y el ID
            const campo = generarCampoFormulario(columna.data, columna.title, '');
            $('#formEdicion').append(campo);
        }
    });

    // Cambiar el botón de guardar
    const btnGuardar = $('.modal-footer .btn-primary');
    btnGuardar.attr('onclick', 'guardarNuevoRegistro()');

    // Mostrar el modal
    const modal = new bootstrap.Modal(document.getElementById('modalEdicion'));
    modal.show();
}

/**
 * Guarda un nuevo registro en la base de datos.
 * Envía una petición POST al servidor y actualiza la tabla.
 */
async function guardarNuevoRegistro() {
    const formData = new FormData(document.getElementById('formEdicion'));
    const datos = Object.fromEntries(formData.entries());

    try {
        // Obtener el endpoint actual
        const endpoint = obtenerEndpointActual();

        // Realizar la petición POST
        const response = await fetch(`/api/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });

        if (!response.ok) {
            throw new Error('Error al crear el registro');
        }

        // Cerrar el modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalEdicion'));
        modal.hide();

        // Recargar la tabla
        const keys = await obtenerKeys(`/api/${endpoint}`);
        const datosNuevos = await obtenerDatos(`/api/${endpoint}`);
        inicializarTabla(keys, datosNuevos);

        // Mostrar mensaje de éxito
        alert('Registro creado exitosamente');

    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear el registro');
    }
}

/**
 * Obtiene el endpoint actual basado en el título de la tabla.
 * @returns {string} Nombre del endpoint actual en minúsculas.
 */
function obtenerEndpointActual() {
    // Obtener el título actual de la tabla y convertirlo a endpoint
    const titulo = $('#tituloTabla').text().toLowerCase();
    return titulo;
}





