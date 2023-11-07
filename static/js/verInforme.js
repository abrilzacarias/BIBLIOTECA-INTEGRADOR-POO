function mostrarVistaPrevia() {
    var element = document.querySelector('.table'); // Elemento que deseas convertir a PDF

    // Obtén los estilos CSS relacionados con la tabla
    var styles = document.head.innerHTML;

    html2pdf()
        .from(element)
        .set({
            html2canvas: { scale: 2 }, // Ajusta la escala para mejorar la calidad
            margin: 10, // Márgenes
            jsPDF: { format: 'a4', orientation: 'portrait' } // Formato y orientación del PDF
        })
        .outputPdf()
        .then(function(pdf) {
            // Crea un objeto Blob a partir del PDF
            var pdfBlob = new Blob([pdf], { type: 'application/pdf' });

            // Crea un enlace de descarga para el PDF
            var link = document.createElement('a');
            link.href = URL.createObjectURL(pdfBlob);
            link.download = 'tabla.pdf'; // Nombre del archivo PDF
            link.style.display = 'none';

            // Agrega los estilos CSS al documento de la ventana de vista previa
            var nuevaVentana = window.open('', 'VER INFORMES PRESTAMOS');
            nuevaVentana.document.write('<html><head><style>' + styles + '</style></head><body>');
            nuevaVentana.document.write(element.outerHTML);
            nuevaVentana.document.write('</body></html>');
            nuevaVentana.document.close();

            // Espera a que se carguen los estilos y luego imprime el PDF
            nuevaVentana.onload = function() {
                nuevaVentana.print();
                nuevaVentana.close();
            };
        });
}