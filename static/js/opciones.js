function listarOpciones(nombreColeccion, idResultados, tipoOpcion, filtroId) {
    console.log(filtroId);
    console.log(nombreColeccion);
    console.log(tipoOpcion);
    console.log(idResultados);
    $.ajax({
        url: '/listarOpciones',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ nombreColeccion: nombreColeccion, tipoOpcion: tipoOpcion, filtro: filtroId }),
        success: function(data) {
            const resultados = document.getElementById(idResultados);
            resultados.innerHTML = '';

            if (data.length === 0) {
                const noResultadosMensaje = document.createElement('p');
                noResultadosMensaje.textContent = 'No se encontraron resultados.';
                resultados.appendChild(noResultadosMensaje);
            } else {
                data.forEach(descripcion => {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.name = nombreColeccion;
                    checkbox.value = descripcion.id;  // ID de la opción
                    checkbox.id = descripcion.id;  // ID de la opción
                    checkbox.className = 'custom-control-input'; 

                    const label = document.createElement('label');
                    label.textContent = `${descripcion.descripcion}`;  // Muestra tanto la descripción como el ID
                    label.className = 'custom-control-label'; // Nombre de clase personalizada
                    resultados.appendChild(checkbox);
                    resultados.appendChild(label);
                    resultados.appendChild(document.createElement('br'));
                });
                    // Agregar el botón "Agregar Variable" después de los checkboxes
                    const agregarVariableBtn = document.createElement('button');
                    agregarVariableBtn.textContent = 'Agregar ' + nombreColeccion;
                    agregarVariableBtn.className = 'btn btn-primary'; // Puedes aplicar clases de Bootstrap para el estilo deseado
                    agregarVariableBtn.addEventListener('click', function() {
                        var url = '/agregarVariable/' + nombreColeccion;
                        window.location.href = url;
                    });
                    resultados.appendChild(agregarVariableBtn);
            }
        }
    });
}
//const checkbox = document.createElement('input');
//checkbox.type = 'checkbox';
//checkbox.name = nombreColeccion;  // El nombre del checkbox es el mismo que el de la colección
//checkbox.value = descripcion;  // El valor del checkbox es la descripción de la opción

//const label = document.createElement('label');
//label.textContent = descripcion;  // Establece el texto del label con la descripción

//resultados.appendChild(checkbox);
//resultados.appendChild(label);
//resultados.appendChild(document.createElement('br'));
function listarOpcionesEditar(nombreColeccion, idResultados, opcionesSeleccionadas, habilitarCheckboxes = true) {
    $.ajax({
        url: '/mostrarOpciones',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ nombreColeccion: nombreColeccion }),
        success: function(data) {
            const resultados = document.getElementById(idResultados);
            resultados.innerHTML = '';

            data.forEach(opcion => {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';

                // Configurar los nombres de los checkboxes según el tipo de colección
                if (nombreColeccion === 'autor') {
                    checkbox.name = 'idAutor[]';
                } else if (nombreColeccion === 'editorial') {
                    checkbox.name = 'idEditorial[]';
                } else if (nombreColeccion === 'genero') {
                    checkbox.name = 'idGenero[]';
                }
                checkbox.value = opcion.id;

                // Verificar si esta opción está en las opciones seleccionadas
                if (opcionesSeleccionadas && opcionesSeleccionadas.includes(opcion.id)) {
                    checkbox.checked = true;
                }

                // Habilitar o deshabilitar los checkboxes según el valor de habilitarCheckboxes
                checkbox.disabled = !habilitarCheckboxes;

                const label = document.createElement('label');
                label.textContent = opcion.descripcionOpcion;

                resultados.appendChild(checkbox);
                resultados.appendChild(label);
                resultados.appendChild(document.createElement('br'));
            });
        }
    });
}

$(document).ready(function() {
    // Utiliza eventos delegados para los botones de editar
    $(document).on('click', '.editar-libro', function() {
        const idLibro = $(this).data('id'); // Obtén el ID del libro a editar
        editarLibro(idLibro);
    });

    function editarLibro(idLibro) {
        console.log('Función editarLibro se está ejecutando');
    
        // Obtén los datos del libro correspondiente y llena el formulario
        $.ajax({
            url: '/obtenerLibroPorId/' + idLibro,
            type: 'GET',
            success: function(data) {
                if (data) {
                    // Llena los campos de entrada de texto
                    $('.editar-isbn').val(data.isbn);
                    $('.editar-titulo').val(data.titulo);
                    $('.editar-cantidad').val(data.cantidad);
                
                    // Llama a listarOpciones para generar los checkboxes
                    listarOpcionesEditar('autor', 'autores-checkboxes', data.idAutoresSeleccionados, true);
                    listarOpcionesEditar('editorial', 'editoriales-checkboxes', data.idEditorialesSeleccionadas, true);
                    listarOpcionesEditar('genero', 'generos-checkboxes', data.idGenerosSeleccionados, true);

                    // Obtén el valor del input de portada
                    var portadaFile = $('#portadaFile')[0].files[0];
                    console.log('Valor del campo de portada:', portadaFile);
                    
                    $('#modal-editar-libro').modal('show');
                } else {
                    console.log('No se pudieron obtener los datos del libro para editar.');
                }
            },
            error: function() {
                console.log('Hubo un error al obtener los datos del libro para editar.');
            }
        });
        $('#actualizar-libro').on('click', function() {
            const isbn = $('.editar-isbn').val();
            const titulo = $('.editar-titulo').val();
            const cantidad = $('.editar-cantidad').val();
        
            const autor = [];
            $('input[name="idAutor[]"]:checked').each(function() {
                autor.push($(this).val());
            });
        
            const editorial = [];
            $('input[name="idEditorial[]"]:checked').each(function() {
                editorial.push($(this).val());
            });
        
            const genero = [];
            $('input[name="idGenero[]"]:checked').each(function() {
                genero.push($(this).val());
            });
        
            var portadaFile = $('#portadaFile')[0].files[0];
        
            console.log('Valor del campo de portada:', portadaFile);
            console.log('Valor de autor:', autor);
            console.log('Valor de editorial:', editorial);
            console.log('Valor de genero:', genero);
            console.log('Valor de isb:', isbn);
            console.log('Valor de titulo:', titulo);
        
            var formData = new FormData();
            formData.append('isbn', isbn);
            formData.append('titulo', titulo);
            formData.append('cantidad', cantidad);
        
            // Agregar autor, editorial y genero como arrays
            for (let i = 0; i < autor.length; i++) {
                formData.append('autor[]', autor[i]);
            }
            
            for (let i = 0; i < editorial.length; i++) {
                formData.append('editorial[]', editorial[i]);
            }
            
            for (let i = 0; i < genero.length; i++) {
                formData.append('genero[]', genero[i]);
            }
        
            // Verificar si se proporciona una nueva portada y agregarla si es el caso
            if (portadaFile) {
                formData.append('portadaFile', portadaFile);
            }
        
            console.log('FormData:', formData);
        
            // Realizar la solicitud AJAX
            $.ajax({
                url: '/actualizarLibro/' + idLibro,
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    console.log('Libro actualizado con éxito.', response);
                    $('#modal-editar-libro').modal('hide');
                    location.reload();
                },
                error: function(response) {
                    console.log('Error en la solicitud:', response);
                }
            });
        });        
        
    }
        //Cuando se hace clic en el botón "Borrar" en la tabla
        $(document).on('click', '.borrar-libro-btn', function () {
            //Obtener el ID del libro desde el atributo data-libro-id
            const idLibro = $(this).data('id'); // Obtén el ID del libro a borrar
            console.log('ID del libro a editar:', idLibro);
    
            //Obtener el título y autor del libro que se va a eliminar desde la tabla
            var tituloLibro = $(this).closest("tr").find("td:eq(0)").text();
    
            //Configurar el título y autor en el modal de confirmación
            $("#libro-titulo").text(tituloLibro);
    
            //Mostrar el modal de confirmación de eliminación
            $("#modal-confirmacion-eliminar").modal("show");
    
            //Eliminar cualquier manejador de eventos anterior
            $("#confirmar-eliminar-libro").off("click");
    
            //Manejador de eventos para el botón "Eliminar" en el modal de confirmación
            $("#confirmar-eliminar-libro").on("click", function () {
                //Realizar una solicitud POST para eliminar el libro
                $.ajax({
                    type: "POST",
                    url: "/eliminarLibro/" + idLibro, //Ajusta la URL según tu ruta en Flask
                    success: function (data) {
                        //Manejar la respuesta del servidor (por ejemplo, mostrar un mensaje de éxito)
                        console.log("Libro eliminado con éxito: " + data.mensaje);
                        //Recargar la página después de eliminar el libro
                        location.reload();
                    },
                    error: function (error) {
                        //Manejar los errores (por ejemplo, mostrar un mensaje de error)
                        console.error("Error al eliminar el libro: " + error.responseJSON.mensaje);
                    }
                });
    
                //Ocultar el modal de confirmación de eliminación
                $("#modal-confirmacion-eliminar").modal("hide");
            });
        });
                // Cuando se hace clic en el botón "Buscar libro"
                $('#buscar-libro-btn').click(function(event) {
                    event.preventDefault();
                    var busqueda = $('#buscar-libro-input').val().trim();
                    console.log("Valor de busqueda:", busqueda);
        
                    // Validar si el campo de búsqueda está vacío
                    if (busqueda === "") {
                        alert("Por favor, ingrese un criterio de búsqueda.");
                        return;
                    }
        
                    // Realizar una solicitud AJAX para buscar libros por autor
                    $.ajax({
                        type: "POST",
                        url: "/buscarPorAutor",
                        data: JSON.stringify({ descripcion: busqueda }),
                        contentType: "application/json",
                        success: function (data) {
                            console.log("Respuesta de buscarPorAutor:", data);
                            // Limpia la tabla actual
                            $('#tabla-resultados').empty();
        
                            // Agregar resultados a la tabla
                            agregarResultadosATabla(data.resultados);
                        },
                        error: function (error) {
                            console.error("Error en la búsqueda de libros por autor:", error.responseJSON ? error.responseJSON.mensaje : "Error desconocido");
                        }
                    });
        
                    // Realizar una solicitud AJAX para buscar libros por editorial
                    $.ajax({
                        type: "POST",
                        url: "/buscarPorEditorial",
                        data: JSON.stringify({ descripcion: busqueda }),
                        contentType: "application/json",
                        success: function (data) {
                            console.log("Respuesta de buscarPorEditorial:", data);
                            // Limpia la tabla actual
                            $('#tabla-resultados').empty();
        
                            // Agregar resultados a la tabla
                            agregarResultadosATabla(data.resultados);
                        },
                        error: function (error) {
                            console.error("Error en la búsqueda de libros por editorial:", error.responseJSON ? error.responseJSON.mensaje : "Error desconocido");
                        }
                    });
        
                    // Realizar una solicitud AJAX para buscar libros por género
                    $.ajax({
                        type: "POST",
                        url: "/buscarPorGenero",
                        data: JSON.stringify({ descripcion: busqueda }),
                        contentType: "application/json",
                        success: function (data) {
                            console.log("Respuesta de buscarPorGenero:", data);
                            // Limpia la tabla actual
                            $('#tabla-resultados').empty();
        
                            // Agregar resultados a la tabla
                            agregarResultadosATabla(data.resultados);
                        },
                        error: function (error) {
                            console.error("Error en la búsqueda de libros por género:", error.responseJSON ? error.responseJSON.mensaje : "Error desconocido");
                        }
                    });
        
                    // Realizar una solicitud AJAX para buscar libros por título
                    $.ajax({
                        type: "POST",
                        url: "/buscarPorTitulo",
                        data: JSON.stringify({ titulo: busqueda }),
                        contentType: "application/json",
                        success: function (data) {
                            console.log("Respuesta de buscarPoTitulo:", data);
                            // Limpia la tabla actual
                            $('#tabla-resultados').empty();
        
                            // Agregar resultados a la tabla
                            agregarResultadosATabla(data.resultados);
                        },
                        error: function (error) {
                            console.error("Error en la búsqueda de libros por título:", error.responseJSON ? error.responseJSON.mensaje : "Error desconocido");
                        }
                    });
                });
                function agregarResultadosATabla(resultados) {
                    // Limpia la tabla actual
                    $('#tabla-resultados').empty();
            
                    if (resultados.length === 0) {
                        // Manejar el caso en que no se encuentren resultados
                        $('#tabla-resultados').append('<tr><td colspan="7">No se encontraron resultados</td></tr>');
                    } else {
                        resultados.forEach(function (resultado) {
                            var libro = resultado.libro;
            
                            // Accede a las propiedades dependiendo de la estructura de datos
                            console.log('ID del libro:', resultado.idLibro);
                            var titulo = libro.titulo;
                            var portada = libro.portada;
                            var isbn = libro.isbn;
                            var autor = resultado.autor;
                            console.log(autor)
                            var genero = resultado.genero;
                            var editorial = resultado.editorial;
                            var cantidad = libro.cantidad;
            
                            // Crear una nueva fila de tabla con los datos
                            $('#tabla-resultados').append('<tr>' +
                                '<td>' + titulo + '</td>' +
                                '<td><img src="' + portada + '" alt="Portada"></td>' +
                                '<td>' + isbn + '</td>' +
                                '<td>' + autor + '</td>' +
                                '<td>' + genero + '</td>' +
                                '<td>' + editorial + '</td>' +
                                '<td>' + cantidad + '</td>' +
                                '<td>' +
                                '<button class="btn btn-modificar editar-libro" data-target="#modal-editar-libro" data-id="' + resultado.idLibro + '"><i class="fa-solid fa-pencil"></i> ' +
                                '<button class="btn btn-eliminar borrar-libro-btn" data-id="' + resultado.idLibro + '"><i class="fa-solid fa-trash"></i></button>' +
                                '</td>' +
                                '</tr>');
                        });
                    }
                }
});