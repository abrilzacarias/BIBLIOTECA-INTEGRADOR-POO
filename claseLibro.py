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
            autorDescripciones = ", ".join(autorDescripciones)
            generoDescripciones = ", ".join(generoDescripciones)
            editorialDescripciones = ", ".join(editorialDescripciones)

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
        
            print(f'idAutor en la funcion: {idAutor} ')
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
            print(libro_data)
            creacionLibro = db.collection('libros').add(libro_data)
            idLibro = creacionLibro[1].id
              # Obtén el ID del documento creado
            print(f"ID del libro: {idLibro}")  # Agrega una impresión para verificar el ID del libro
            return idLibro  # Devuelve solo el ID del libro como resultado
        

    def modificarLibro(self):
        if self.__idLibro is not None:
            # Actualiza el libro en la base de datos usando su identificador (__idLibro)
            db.collection("libros").document(self.__idLibro).update({
                'titulo': self.__titulo,
                'isbn': self.__isbn,
                'portada': self.__portada,
                'autor': self.__autor.getDescripcionAutor(),
                'editorial': self.__editorial.getDescripcionEditorial(),
                'genero': self.__genero.getDescripcionGenero(),
                'cantidad': self.__cantidad
            })
        else:
            print("No se proporcionó un identificador de libro para la modificación.")

    def eliminarLibro(self, idLibro):
        if idLibro is not None:
            # Elimina el libro de la base de datos usando su identificador (__idLibro)
            db.collection("libros").document(idLibro).delete()
        else:
            print("No se proporcionó un identificador de libro para la eliminación.")

    def buscarPorAutor(self, descripcion):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener los autores cuya descripción comience con la descripción proporcionada
        autoresRef = db.collection('autor').where('descripcionAutor', '>=', descripcion).where('descripcionAutor', '<=', descripcion + '\uf8ff').stream()

        for autor in autoresRef:
            # Obtenemos el ID del autor
            idAutor = autor.id

            # Ahora buscamos los libros por el ID del autor en la colección de libros
            librosRef = db.collection('libros').where('idAutor', '==', idAutor).stream()

            for libro in librosRef:
                datosLibro = libro.to_dict()
                idEditorial = datosLibro.get("idEditorial")

                # Obtén la descripción completa de la editorial usando la clase Editorial
                editorialDescripcion = Editorial(idOpcion=idEditorial).obtenerDescripcionOpcion()

                # Agrega los resultados a la lista
                resultados.append({
                    "autor": autor.to_dict()['descripcionAutor'],
                    "editorial": editorialDescripcion,
                })

        return resultados

    
    def buscarPorEditorial(self, descripcion):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener los géneros cuya descripción comience con la descripción proporcionada
        editorialRef = db.collection('editorial').where('descripcionEditorial', '>=', descripcion).where('descripcionEditorial', '<=', descripcion + '\uf8ff').stream()

        for editorial in editorialRef:
            # Obtenemos el ID del genero
            idEditorial = editorial.id

            # Ahora buscamos los libros por el ID del genero en la colección de libros
            librosRef = db.collection('libros').where('idEditorial', '==', idEditorial).stream()

            for libro in librosRef:
                # Agrega los resultados a la lista
                resultados.append({
                    "editorial": editorial.to_dict()['descripcionEditorial'],
                })

        return resultados
        
    def buscarPorGenero(self, descripcion):
        # Crea una lista vacía para almacenar los resultados
        resultados = []

        # Realiza una consulta para obtener los géneros cuya descripción comience con la descripción proporcionada
        generosRef = db.collection('genero').where('descripcionGenero', '>=', descripcion).where('descripcionGenero', '<=', descripcion + '\uf8ff').stream()

        for genero in generosRef:
            # Obtenemos el ID del genero
            idGenero = genero.id

            # Ahora buscamos los libros por el ID del genero en la colección de libros
            librosRef = db.collection('libros').where('idGenero', '==', idGenero).stream()

            for libro in librosRef:
                # Agrega los resultados a la lista
                resultados.append({
                    "genero": genero.to_dict()['descripcionGenero'],
                })

        return resultados
    
    #def buscarPorTitulo():
