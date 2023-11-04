function listarOpciones(nombreColeccion, idResultados) {
    $.ajax({
        url: '/listarOpciones',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ nombreColeccion: nombreColeccion }),
        success: function(data) {
            const resultados = document.getElementById(idResultados);
            resultados.innerHTML = '';

            data.forEach(opcion => {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = nombreColeccion;  // El nombre del checkbox es el mismo que el de la colección
                checkbox.value = opcion.id;  // El valor del checkbox es el ID de la opción
            
                const label = document.createElement('label');
                label.textContent = opcion.descripcionOpcion;
            
                resultados.appendChild(checkbox);
                resultados.appendChild(label);
                resultados.appendChild(document.createElement('br'));
            });
        }
    });
}
