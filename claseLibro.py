from subClaseAutor import Autor
from subClaseEditorial import Editorial
from subClaseGenero import Genero
from config import db, bucket
from google.cloud import storage
storage_client = storage.Client()

class Libro(): 
    def __init__(self, idLibro=None, isbn=None, titulo=None, portada=None, idAutor=None, idEditorial=None, idGenero=None, cantidad=None):
        self.__idLibro = idLibro
        self.__isbn = isbn
        self.__titulo = titulo
        self.__portada = portada
        self.__idAutor = idAutor  
        self.__idEditorial = idEditorial  
        self.__idGenero = idGenero  
        self.__cantidad = cantidad
        
    #Setters y getters para acceder y modificar los atributos del cliente
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
        
    # Método privado que devuelve los datos del libro, incluyendo información adicional sobre el libro.
    def __obtenerDatos(self):
        return f'''Titulo: {self.getTitulo()} 
        Autor: {self.getAutor().getDescripcionAutor()}
        Editorial: {self.getEditorial().getDescripcionEditorial()}
        Genero: {self.getGenero().getDescripcionGenero()}
        ISBN: {self.getIsbn()}
        Cantidad: {self.getCantidad()}'''

    def listarLibros(self):
        librosRef = db.collection("libros")
        listaLibros = []

        for libro in librosRef.stream():
            datosLibros = libro.to_dict()
            isbn = datosLibros.get('isbn')
            titulo = datosLibros.get('titulo')
            portada = datosLibros.get('portada')
            cantidad = datosLibros.get('cantidad')

            idAutores = datosLibros.get('idAutor', [])
            idGeneros = datosLibros.get('idGenero', [])
            idEditoriales = datosLibros.get('idEditorial', [])

            # Obtener descripciones de autores
            autorDescripciones = [Autor(idOpcion=[id]).obtenerDescripcionesOpcion()[0] for id in idAutores]

            # Obtener descripciones de géneros
            generoDescripciones = [Genero(idOpcion=[id]).obtenerDescripcionesOpcion()[0] for id in idGeneros]

            # Obtener descripciones de editoriales
            editorialDescripciones = [Editorial(idOpcion=[id]).obtenerDescripcionesOpcion()[0] for id in idEditoriales]

            # Unir las descripciones en una sola cadena separada por comas
            autorDescripciones = "\n".join(autorDescripciones)
            generoDescripciones = "\n".join(generoDescripciones)
            editorialDescripciones = "\n".join(editorialDescripciones)

            datosLibros['idLibro'] = libro.id
            datosLibros['titulo'] = titulo
            datosLibros['isbn'] = isbn
            datosLibros['portada'] = portada
            datosLibros['autor'] = autorDescripciones
            datosLibros['editorial'] = editorialDescripciones
            datosLibros['genero'] = generoDescripciones
            datosLibros['cantidad'] = cantidad

            listaLibros.append(datosLibros)

        return listaLibros

    
    def generar_url_firmada(self, nombre_archivo, bucket_name):
        # Obtener un objeto Blob que representa tu archivo en Firebase Storage
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(nombre_archivo)

        # Generar una URL firmada válida (con la firma en base64)
        signed_url = blob.generate_signed_url(
                    version="v4",
                    expiration=604800 ,  # 1 hora en segundos
                    method="GET"
                )


        return signed_url

    def agregarLibro(self, isbn, titulo, portada, idAutor, idEditorial, idGenero, cantidad):
            #print(f'idAutor en la funcion: {idAutor} ')
            # 1. Subir la imagen de la portada a Firebase Storage
            blob = bucket.blob("portadasLibros/" + portada.filename)
            blob.upload_from_string(portada.read(), content_type=portada.content_type)

            # 2. Obtener la URL de la imagen cargada
            portadaUrl = self.generar_url_firmada("portadasLibros/" + portada.filename, "biblioteca-1d610.appspot.com")

            cantidad = int(cantidad)
            # 3. Almacenar la URL de la imagen en Firestore junto con otros datos del libro
            libro_data = {
                'isbn': isbn,
                'titulo': titulo,
                'portada': portadaUrl,  # URL de la imagen firmada
                'idAutor': idAutor,
                'idEditorial': idEditorial,
                'idGenero': idGenero,
                'cantidad': cantidad,
            }
            #print(libro_data)
            creacionLibro = db.collection('libros').add(libro_data)
            idLibro = creacionLibro[1].id
            # Obtén el ID del documento creado
            #print(f"ID del libro: {idLibro}")  # Agrega una impresión para verificar el ID del libro
            return idLibro  # Devuelve solo el ID del libro como resultado
        

    def actualizarLibro(self, idLibro, isbn, titulo, portada, idAutor, idEditorial, idGenero, cantidad):
        # 1. Subir la imagen de la portada a Firebase Storage si es necesario
        if portada is not None:
            blob = bucket.blob("portadasLibros/" + portada.filename)
            blob.upload_from_string(portada.read(), content_type=portada.content_type)
            portadaUrl = self.generar_url_firmada("portadasLibros/" + portada.filename, "biblioteca-1d610.appspot.com")
        else:
            # Si la portada no cambió, conserva la URL existente
            existing_data = db.collection('libros').document(idLibro).get()
            portadaUrl = existing_data.get('portada')

        # 2. Actualizar los datos del libro en Firestore
        libro_data = {
            'isbn': isbn,
            'titulo': titulo,
            'portada': portadaUrl,  # URL de la imagen firmada
            'idAutor': idAutor,
            'idEditorial': idEditorial,
            'idGenero': idGenero,
            'cantidad': cantidad,
        }
        db.collection('libros').document(idLibro).set(libro_data, merge=True)

        # Devuelve el ID del libro actualizado
        return idLibro

    def eliminarLibro(self, idLibro):
            if idLibro is not None:
                # Elimina el libro de la base de datos usando su identificador (__idLibro)
                db.collection("libros").document(idLibro).delete()
            else:
                print("No se proporcionó un identificador de libro para la eliminación.")
            
    def obtenerLibroPorId(self, idLibro):
        if idLibro is not None:
            # Realiza una consulta para obtener los datos del libro por su ID
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


    def buscarPorAutor(self, descripcion):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener autores cuya descripción coincide
        autoresRef = db.collection('autor').where('descripcionAutor', '>=', descripcion).where('descripcionAutor', '<=', descripcion + '\uf8ff').stream()

        for autor in autoresRef:
            # Obtenemos el ID del autor y su descripción
            idAutor = autor.id
            #descripcionAutor = autor.to_dict().get('descripcionAutor')

            # Ahora busca los libros que tengan el ID del autor en su lista de autores
            librosRef = db.collection('libros').where('idAutor', 'array_contains', idAutor).stream()

            for libro in librosRef:
                libro_data = libro.to_dict()
                idLibro = libro.id
                
                # Obtiene las descripciones de género y editorial utilizando la función obtenerDescripcionOpcion
                idGenero = libro_data.get('idGenero')
                idEditorial = libro_data.get('idEditorial')
                idAutor = libro_data.get('idAutor')
                descripcionAutor = Autor(idOpcion=idAutor).obtenerDescripcionesOpcion()
                descripcionGenero = Genero(idOpcion=idGenero).obtenerDescripcionesOpcion()
                descripcionEditorial = Editorial(idOpcion=idEditorial).obtenerDescripcionesOpcion()
                titulo = libro_data.get('titulo')
                
                # Agrega los resultados a la lista, incluyendo las descripciones de género y editorial
                resultados.append({
                    "idLibro": idLibro,
                    "autor": descripcionAutor,
                    "libro": libro_data,
                    "genero": descripcionGenero,
                    "editorial": descripcionEditorial
                })

        return resultados


    def buscarPorGenero(self, descripcion):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener géneros cuya descripción coincide
        generoRef = db.collection('genero').where('descripcionGenero', '>=', descripcion).where('descripcionGenero', '<=', descripcion + '\uf8ff').stream()

        for genero in generoRef:
            # Obtenemos el ID del género y su descripción
            idGenero = genero.id
            #descripcionGenero = genero.to_dict().get('descripcionGenero')

            # Ahora busca los libros que tengan el ID del género
            librosRef = db.collection('libros').where('idGenero', 'array_contains', idGenero).stream()

            for libro in librosRef:
                libro_data = libro.to_dict()

                idLibro = libro.id
                # Obtiene las descripciones de autor y editorial utilizando la función obtenerDescripcionOpcion
                idAutor = libro_data.get('idAutor')
                idEditorial = libro_data.get('idEditorial')
                idGenero = libro_data.get('idGenero')
                descripcionAutor = Autor(idOpcion=idAutor).obtenerDescripcionesOpcion()
                descripcionEditorial = Editorial(idOpcion=idEditorial).obtenerDescripcionesOpcion()
                descripcionGenero = Genero(idOpcion=idGenero).obtenerDescripcionesOpcion()

                # Agrega los resultados a la lista, incluyendo las descripciones de autor y editorial
                resultados.append({
                    "idLibro": idLibro,
                    "genero": descripcionGenero,
                    "libro": libro_data,
                    "autor": descripcionAutor,
                    "editorial": descripcionEditorial
                })

        return resultados

    
    def buscarPorEditorial(self, descripcion):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener editoriales cuya descripción coincide
        editorialRef = db.collection('editorial').where('descripcionEditorial', '>=', descripcion).where('descripcionEditorial', '<=', descripcion + '\uf8ff').stream()

        for editorial in editorialRef:
            # Obtenemos el ID de la editorial y su descripción
            idEditorial = editorial.id
            #descripcionEditorial = editorial.to_dict().get('descripcionEditorial')

            # Ahora busca los libros que tengan el ID de la editorial
            librosRef = db.collection('libros').where('idEditorial', 'array_contains', idEditorial).stream()

            for libro in librosRef:
                libro_data = libro.to_dict()

                idLibro = libro.id
                # Obtiene las descripciones de autor y género utilizando la función obtenerDescripcionOpcion
                idAutor = libro_data.get('idAutor')
                idGenero = libro_data.get('idGenero')
                idEditorial = libro_data.get('idEditorial')
                descripcionAutor = Autor(idOpcion=idAutor).obtenerDescripcionesOpcion()
                descripcionGenero = Genero(idOpcion=idGenero).obtenerDescripcionesOpcion()
                descripcionEditorial = Editorial(idOpcion=idEditorial).obtenerDescripcionesOpcion()
                
                # Agrega los resultados a la lista, incluyendo las descripciones de autor y género
                resultados.append({
                    "idLibro": idLibro,
                    "editorial": descripcionEditorial,
                    "libro": libro_data,
                    "autor": descripcionAutor,
                    "genero": descripcionGenero
                })

        return resultados

        
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