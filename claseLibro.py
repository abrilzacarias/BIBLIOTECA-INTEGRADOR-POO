from subClaseAutor import Autor # Importar la clase 'Autor' desde el módulo 'subClaseAutor'
from subClaseEditorial import Editorial # Importar la clase 'Editorial' desde el módulo 'subClaseEditorial'
from subClaseGenero import Genero # Importar la clase 'Genero' desde el módulo 'subClaseGenero'
from config import db, bucket # Importar los objetos 'db' y 'bucket' desde el módulo 'config'
from google.cloud import storage  # Importar la clase 'Client' desde el módulo 'storage' de la biblioteca 'google.cloud'


storageCliente = storage.Client()  # Crear una instancia del cliente de almacenamiento de Google Cloud

class Libro(): 
    # Constructor de la clase 'Libro' con parámetros opcionales
    def __init__(self, idLibro=None, isbn=None, titulo=None, portada=None, idAutor=None, idEditorial=None, idGenero=None, cantidad=None):
        self.__idLibro = idLibro
        self.__isbn = isbn
        self.__titulo = titulo
        self.__portada = portada
        self.__idAutor = idAutor  
        self.__idEditorial = idEditorial  
        self.__idGenero = idGenero  
        self.__cantidad = cantidad
        
    #ENCAPSULAMIENTO Y ABSTRACCIÓN
    #Setters y getters para acceder y modificar los atributos del libro
    def getIdLibro(self):
        return self.__idLibro

    def setIdLibro(self, idLibro):
        self.__idLibro = idLibro

    def getTitulo(self):
        return self.__titulo

    def setTitulo(self, titulo):
        self.__titulo = titulo
        
    def getPortada(self):
        return self.__portada

    def setPortada(self, portada):
        self.__portada = portada
        
    def getIsbn(self):
        return self.__isbn

    def setIsbn(self, isbn):
        self.__isbn = isbn
        
    def getCantidad(self):
        return self.__cantidad

    def setCantidad(self, cantidad):
        self.__cantidad = cantidad
        
    # Método privado que devuelve los datos del libro
    #POLIMORFISMO
    def __obtenerDatos(self):
        return f'''Titulo: {self.getTitulo()} 
        Autor: {self.getAutor().getDescripcionAutor()}
        Editorial: {self.getEditorial().getDescripcionEditorial()}
        Genero: {self.getGenero().getDescripcionGenero()}
        ISBN: {self.getIsbn()}
        Cantidad: {self.getCantidad()}'''

    # Método público para listar libros
    def listarLibros(self):
        # Obtener una referencia a la colección 'libros' en la base de datos
        librosRef = db.collection("libros")
        listaLibros = []
        
        # Extraer información específica del libro, como ISBN, título, portada y cantidad
        for libro in librosRef.stream():
            datosLibros = libro.to_dict()
            isbn = datosLibros.get('isbn')
            titulo = datosLibros.get('titulo')
            portada = datosLibros.get('portada')
            cantidad = datosLibros.get('cantidad')

            idAutores = datosLibros.get('idAutor', [])
            idGeneros = datosLibros.get('idGenero', [])
            idEditoriales = datosLibros.get('idEditorial', [])

            # Obtener descripciones de autores, como es una lista recorre y si no encuentra ningun valor devuelve "SIN AUTOR"
            autorDescripciones = [Autor(idOpcion=[id]).obtenerDescripcionesOpcion()[0] for id in idAutores]
            autorDescripciones = "\n".join(autorDescripciones) if autorDescripciones else "SIN AUTOR"

            # Obtener descripciones de géneros, como es una lista recorre ysi no encuentra ningun valor devuelve "SIN GENERO"
            generoDescripciones = [Genero(idOpcion=[id]).obtenerDescripcionesOpcion()[0] for id in idGeneros]
            generoDescripciones = "\n".join(generoDescripciones) if generoDescripciones else "SIN GÉNERO"

            # Obtener descripciones de editoriales como es una lista recorre ysi no encuentra ningun valor devuelve "SIN EDITORIAL"
            editorialDescripciones = [Editorial(idOpcion=[id]).obtenerDescripcionesOpcion()[0] for id in idEditoriales]
            editorialDescripciones = "\n".join(editorialDescripciones) if editorialDescripciones else "SIN EDITORIAL"

            # Actualizar el diccionario de datos del libro con la información adicional
            datosLibros['idLibro'] = libro.id
            datosLibros['titulo'] = titulo
            datosLibros['isbn'] = isbn
            datosLibros['portada'] = portada
            datosLibros['autor'] = autorDescripciones
            datosLibros['editorial'] = editorialDescripciones
            datosLibros['genero'] = generoDescripciones
            datosLibros['cantidad'] = cantidad

            # Agregar el diccionario de datos del libro a la lista de libros
            listaLibros.append(datosLibros)
        # Devolver la lista de libros con información detallada
        return listaLibros
    
    # Método público para generar la url de la imagen que se almacena en Storage
    def generarUrlFirmada(self, nombreArchivo, bucketName):
        # Obtener un objeto Blob que representa el archivo en Firebase Storage
        bucket = storageCliente.get_bucket(bucketName)
        blob = bucket.blob(nombreArchivo)

        # Crear una URL firmada para acceso de lectura a un recurso en Google Cloud Storage
        signedUrl = blob.generate_signed_url(
                    version="v4",  # Versión de la URL firmada
                    expiration=604800 ,   # Tiempo de expiración en segundos (una semana en este caso)
                    method="GET"      # Método HTTP permitido (en este caso, una solicitud GET)
                )
        return signedUrl

    # Método público para agregar libros
    def agregarLibro(self, isbn, titulo, portada, idAutor, idEditorial, idGenero, cantidad):
            # Subir la imagen de la portada a Firebase Storage
            blob = bucket.blob("portadasLibros/" + portada.filename)
            blob.upload_from_string(portada.read(), content_type=portada.content_type)

            # Obtener la URL de la imagen cargada
            portadaUrl = self.generarUrlFirmada("portadasLibros/" + portada.filename, "biblioteca-1d610.appspot.com")

            cantidad = int(cantidad)
            
            # Almacenar la URL de la imagen en Firestore junto con otros datos del libro
            libroData = {
                'isbn': isbn,
                'titulo': titulo,
                'portada': portadaUrl,  # URL de la imagen firmada
                'idAutor': idAutor,
                'idEditorial': idEditorial,
                'idGenero': idGenero,
                'cantidad': cantidad,
            }
            #print(libro_data)
            creacionLibro = db.collection('libros').add(libroData)
            idLibro = creacionLibro[1].id # Obtén el ID del documento creado
            return idLibro  # Devuelve solo el ID del libro como resultado
        
    # Método público para actualizar libros
    def actualizarLibro(self, idLibro, isbn, titulo, portada, idAutor, idEditorial, idGenero, cantidad):
        # Subir la imagen de la portada a Firebase Storage si es necesario
        if portada is not None:
            blob = bucket.blob("portadasLibros/" + portada.filename)
            blob.upload_from_string(portada.read(), content_type=portada.content_type)
            portadaUrl = self.generarUrlFirmada("portadasLibros/" + portada.filename, "biblioteca-1d610.appspot.com")
        else:
            # Si la portada no cambió, conserva la URL existente
            existing_data = db.collection('libros').document(idLibro).get()
            portadaUrl = existing_data.get('portada')

        # Actualizar los datos del libro en Firestore
        libroData = {
            'isbn': isbn,
            'titulo': titulo,
            'portada': portadaUrl,  # URL de la imagen firmada
            'idAutor': idAutor,
            'idEditorial': idEditorial,
            'idGenero': idGenero,
            'cantidad': cantidad,
        }
        db.collection('libros').document(idLibro).set(libroData, merge=True)

        # Devuelve el ID del libro actualizado
        return idLibro
    
    # Método público para eliminar libros por id
    def eliminarLibro(self, idLibro):
            if idLibro is not None:
                # Elimina el libro de la base de datos usando su identificador (__idLibro)
                db.collection("libros").document(idLibro).delete()
            else:
                print("No se proporcionó un identificador de libro para la eliminación.")
    
    # Método público para obtener la información detallada del libro mediante su id    
    def obtenerLibroPorId(self, idLibro):
        if idLibro is not None:
            # Realiza una consulta para obtener los datos del libro por su id
            libroRef = db.collection("libros").document(idLibro)
            libroDoc = libroRef.get()

            # Verifica si el libro existe en la base de datos
            if libroDoc.exists:
                datosLibro = libroDoc.to_dict()
                isbn = datosLibro.get('isbn')
                titulo = datosLibro.get('titulo')
                portada = datosLibro.get('portada')
                cantidad = datosLibro.get('cantidad')

                # Obtener descripciones de autor, editorial y género
                idAutores = datosLibro.get('idAutor', [])
                idGeneros = datosLibro.get('idGenero', [])
                idEditoriales = datosLibro.get('idEditorial', [])

                # Obtener descripciones de autores
                autorDescripciones = [Autor(idOpcion=[id]).obtenerDescripcionesOpcion()[0] for id in idAutores]

                # Obtener descripciones de géneros
                generoDescripciones = [Genero(idOpcion=[id]).obtenerDescripcionesOpcion()[0] for id in idGeneros]

                # Obtener descripciones de editoriales
                editorialDescripciones = [Editorial(idOpcion=[id]).obtenerDescripcionesOpcion()[0] for id in idEditoriales]

                # Unir las descripciones en una sola cadena separada por comas
                autorDescripciones = ", ".join(autorDescripciones)
                generoDescripciones = ", ".join(generoDescripciones)
                editorialDescripciones = ", ".join(editorialDescripciones)

                # Crear un diccionario con los datos del libro
                datosLibro = {
                    'idLibro': idLibro,
                    'isbn': isbn,
                    'titulo': titulo,
                    'portada': portada,
                    'autor': autorDescripciones,
                    'idAutoresSeleccionados': idAutores,  # Agregar los IDs
                    'editorial': editorialDescripciones,
                    'idEditorialesSeleccionadas': idEditoriales,  # Agregar los IDs
                    'genero': generoDescripciones,
                    'idGenerosSeleccionados': idGeneros,  # Agregar los IDs
                    'cantidad': cantidad
                }
                print('Datos del libro:', datosLibro)
                return datosLibro
            
            else:
                return None  # El libro no existe en la base de datos
        else:
            return None  # No se proporcionó un ID de libro válido

    # Metodo publico para buscar libros teniendo en cuenta el 'autor'
    def buscarPorAutor(self, descripcion):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener autores cuya descripción coincide
        autoresRef = db.collection('autor').where('descripcionAutor', '>=', descripcion).where('descripcionAutor', '<=', descripcion + '\uf8ff').stream()

        for autor in autoresRef:
            # Obtoene el id del autor 
            idAutor = autor.id
            #descripcionAutor = autor.to_dict().get('descripcionAutor')

            # Ahora busca los libros que tengan el id del autor en su lista de autores
            librosRef = db.collection('libros').where('idAutor', 'array_contains', idAutor).stream()

            for libro in librosRef:
                libroData = libro.to_dict()
                idLibro = libro.id
                
                # Obtiene las descripciones de autor, género y editorial utilizando la función obtenerDescripcionOpcion de la clase 'opciones'
                idGenero = libroData.get('idGenero')
                idEditorial = libroData.get('idEditorial')
                idAutor = libroData.get('idAutor')
                descripcionAutor = Autor(idOpcion=idAutor).obtenerDescripcionesOpcion()
                descripcionGenero = Genero(idOpcion=idGenero).obtenerDescripcionesOpcion()
                descripcionEditorial = Editorial(idOpcion=idEditorial).obtenerDescripcionesOpcion()
                titulo = libroData.get('titulo')
                
                # Agrega los resultados a la lista, incluyendo las descripciones de género y editorial
                resultados.append({
                    "idLibro": idLibro,
                    "autor": descripcionAutor,
                    "libro": libroData,
                    "genero": descripcionGenero,
                    "editorial": descripcionEditorial
                })

        return resultados

    # Metodo publico para buscar libros teniendo en cuenta el 'genero'
    def buscarPorGenero(self, descripcion):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener géneros cuya descripción coincide
        generoRef = db.collection('genero').where('descripcionGenero', '>=', descripcion).where('descripcionGenero', '<=', descripcion + '\uf8ff').stream()

        for genero in generoRef:
            # Obtiene el id del género 
            idGenero = genero.id
            #descripcionGenero = genero.to_dict().get('descripcionGenero')

            # Ahora busca los libros que tengan el id  del género
            librosRef = db.collection('libros').where('idGenero', 'array_contains', idGenero).stream()

            for libro in librosRef:
                libroData = libro.to_dict()

                idLibro = libro.id
                # Obtiene las descripciones de autor, género y editorial utilizando la función obtenerDescripcionOpcion de la clase 'opciones'
                idAutor = libroData.get('idAutor')
                idEditorial = libroData.get('idEditorial')
                idGenero = libroData.get('idGenero')
                descripcionAutor = Autor(idOpcion=idAutor).obtenerDescripcionesOpcion()
                descripcionEditorial = Editorial(idOpcion=idEditorial).obtenerDescripcionesOpcion()
                descripcionGenero = Genero(idOpcion=idGenero).obtenerDescripcionesOpcion()

                # Agrega los resultados a la lista, incluyendo las descripciones de autor y editorial
                resultados.append({
                    "idLibro": idLibro,
                    "genero": descripcionGenero,
                    "libro": libroData,
                    "autor": descripcionAutor,
                    "editorial": descripcionEditorial
                })

        return resultados

    # Metodo publico para buscar libros teniendo en cuenta el 'editorial'
    def buscarPorEditorial(self, descripcion):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener editoriales cuya descripción coincide
        editorialRef = db.collection('editorial').where('descripcionEditorial', '>=', descripcion).where('descripcionEditorial', '<=', descripcion + '\uf8ff').stream()

        for editorial in editorialRef:
            # Obtenemos el id de la editorial 
            idEditorial = editorial.id
            #descripcionEditorial = editorial.to_dict().get('descripcionEditorial')

            # Ahora busca los libros que tengan el ID de la editorial
            librosRef = db.collection('libros').where('idEditorial', 'array_contains', idEditorial).stream()

            for libro in librosRef:
                libroData = libro.to_dict()

                idLibro = libro.id
                # Obtiene las descripciones de autor, género y editorial utilizando la función obtenerDescripcionOpcion de la clase 'opciones'
                idAutor = libroData.get('idAutor')
                idGenero = libroData.get('idGenero')
                idEditorial = libroData.get('idEditorial')
                descripcionAutor = Autor(idOpcion=idAutor).obtenerDescripcionesOpcion()
                descripcionGenero = Genero(idOpcion=idGenero).obtenerDescripcionesOpcion()
                descripcionEditorial = Editorial(idOpcion=idEditorial).obtenerDescripcionesOpcion()
                
                # Agrega los resultados a la lista, incluyendo las descripciones de autor y género
                resultados.append({
                    "idLibro": idLibro,
                    "editorial": descripcionEditorial,
                    "libro": libroData,
                    "autor": descripcionAutor,
                    "genero": descripcionGenero
                })

        return resultados

    # Metodo publico para buscar libros teniendo en cuenta el 'titulo'    
    def buscarPorTitulo(self, titulo):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener los libros cuyo título comience con el título proporcionado
        librosRef = db.collection('libros').where('titulo', '>=', titulo).where('titulo', '<=', titulo + '\uf8ff').stream()

        for libro in librosRef:
            # Obtenemos el título del libro y otros datos si es necesario
            datosLibro = libro.to_dict()

            idLibro = libro.id
            # Obtén las descripciones de autor, género y editorial utilizando las clases correspondientes
            idAutor = datosLibro.get('idAutor')
            idGenero = datosLibro.get('idGenero')
            idEditorial = datosLibro.get('idEditorial')
            
            # Obtiene las descripciones de autor, género y editorial utilizando la función obtenerDescripcionOpcion de la clase 'opciones'
            descripcionAutor = Autor(idOpcion=idAutor).obtenerDescripcionesOpcion()
            descripcionGenero = Genero(idOpcion=idGenero).obtenerDescripcionesOpcion()
            descripcionEditorial = Editorial(idOpcion=idEditorial).obtenerDescripcionesOpcion()

            # Agrega los resultados a la lista, incluyendo las descripciones
            resultados.append({
                "libro": datosLibro,
                "idLibro": idLibro,
                "titulo": datosLibro.get('titulo'),
                "autor": descripcionAutor,
                "genero": descripcionGenero,
                "editorial": descripcionEditorial
            })

        return resultados