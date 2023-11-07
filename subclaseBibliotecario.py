#Estas líneas importan las clases y módulos necesarios.
from clasePersona import Persona
from clasePrestamo import Prestamo
from claseValidaciones import Validaciones
from config import db

#La clase Bibliotecario hereda de la clase Persona. Se trata de HERENCIA
class Bibliotecario(Persona):
    #Inicializa una instancia de Bibliotecario con atributos. Si no se proporcionan valores, se les asigna el valor predeterminado None.
    def __init__(self, nombre=None, apellido=None, dni=None, domicilio=None, telefono=None, email=None, password=None):
        #Esta línea llama al constructor de la clase base Persona para inicializar los atributos de persona heredados.
        super().__init__(nombre, apellido, dni, domicilio, email, telefono)
        self.__password = password
        self.__idBibliotecario = None

    #Metodos setters y getters. ABSTRACCIÓN Y ENCAPSULAMIENTO
    def getPassword(self):
        return self.__password
    
    def setPassword(self, password):
        self.__password = password
        
    def getIdBibliotecario(self):
        return self.__idBibliotecario
    
    def setIdBibliotecario(self, idBibliotecario):
        self.__idBibliotecario = idBibliotecario

    #Método encargado de obtener los datos de un lector por su ID
    def obtenerLectorPorId(self, idLector):
        #se obtiene una referencia a la colección de lectores en la base de datos
        lectoresRef = db.collection('lectores')
        #se busca un documento en la colección de lectores que coincida con el ID proporcionado
        lectorDoc = lectoresRef.document(idLector).get()

        # se verifica si el documento del lector existe en la base de datos
        if lectorDoc.exists:
            # si existe, se recuperan los datos del lector del documento
            datosLector = lectorDoc.to_dict()
            return datosLector
        else:
            #el lector no fue encontrado
            return None
    
    # Método encargado de buscar un libro por su nombre en la base de datos
    def buscarLibroPorNombre(self, nombreLibro):
        librosRef = db.collection('libros')
        # se crea una consulta para buscar libros cuyo título esté en el rango [nombreLibro, nombreLibro + '\uf8ff']
        consulta = librosRef.where('titulo', '>=', nombreLibro).where('titulo', '<=', nombreLibro + '\uf8ff').get()
        # se itera a través de los resultados de la consulta
        for libro in consulta:
            # se recuperan los datos del libro y se almacenan en un diccionario
            datosLibro = libro.to_dict()
            # se devuelven los datos del libro
            return datosLibro
        return None
    
    # Método encargado de buscar el nombre de un lector por su ID
    def buscarNombreLectorPorID(self, idLector):
        #se obtiene una referencia al documento del lector por su ID en la colección 'lectores'
        lectoresRef = db.collection('lectores').document(idLector)
        documento = lectoresRef.get()
        if documento.exists:
            datosLector = documento.to_dict()
            #se recuperan el nombre y el apellido del lector
            nombre = datosLector.get('nombre', '')
            apellido = datosLector.get('apellido', '')
            return f"{nombre} {apellido}"
        else:
            return None

    # Método encargado de buscar el nombre de un lector por su ID
    #procedimiento similar a  buscarNombreLectorPorID() pero en la busqueda de un libro
    def buscarNombreLibroPorID(self, idLibro):
        librosRef = db.collection('libros').document(idLibro)
        documento = librosRef.get()
        if documento.exists:
            return documento.get('titulo')
        else:
            return None

    # Método encargado de buscar el nombre de un lector por su DNI en la base de datos
    def buscarNombreLectorPorDni(self, dniLector):
        # Se realiza una consulta en la colección 'lectores' para buscar un lector con el DNI especificado
        lectores = db.collection('lectores').where('dni', '==', dniLector).stream()
        for lector in lectores:
            # Se recuperan los datos del lector actual como un diccionario
            datosLector = lector.to_dict()
            # Se recupera el nombre y el apellido del lector, si están disponibles
            nombre = datosLector.get('nombre', '')
            apellido = datosLector.get('apellido', '')
            print(f"Nombre del lector: {nombre} {apellido}")
            # Se combina el nombre y el apellido en un solo string y se devuelve
            return f"{nombre} {apellido}"
        return None

    #Método encargado de agregar un nuevo lector a la base de datos
    def agregarLector(self, nombre, apellido, dni, domicilio, telefono, email):
        # Se crea un diccionario con los datos del nuevo lector, utilizando capitalize() para poner en mayuscula la primera letra de nombre y apellido.
        lectoresData = {
            'nombre': nombre.capitalize(),
            'apellido': apellido.capitalize(),
            'dni' : dni ,
            'email' : email ,
            'domicilio' : domicilio.capitalize() ,
            'telefono' : telefono 
        }
        print(lectoresData)
        # Se agrega el nuevo lector a la colección 'lectores' en la base de datos
        creacion = db.collection('lectores').add(lectoresData)
        # Se obtiene la nueva clave única generada para el lector
        claveUnica = creacion[1].id
        # Se devuelve la clave única como resultado de la operación
        return claveUnica
    
    # Método encargado de recuperar y mostrar la lista de lectores desde la base de datos
    def mostrarLectores(self):
        #Lee todos los documentos en la colección 'lectores'.
        lectoresRef = db.collection("lectores")
        lectores = lectoresRef.stream()
        listaLectores = []
        # Se itera a través de los documentos de los lectores
        for lector in lectores:
            # Se convierten los datos del lector en un diccionario
            datosLector = lector.to_dict()
            docId = lector.id  # Acceso al ID del documento
            # Se crea un diccionario con los datos del lector
            lectorDic = {
                'id': docId,
                'nombre': datosLector['nombre'],
                'apellido': datosLector['apellido'],
                'dni' : datosLector['dni'],
                'email': datosLector['email'],
                'domicilio': datosLector['domicilio'],
                'telefono': datosLector['telefono']
            }
            # Se agrega el diccionario del lector a la lista de lectores
            listaLectores.append(lectorDic)
        return listaLectores

    # Método encargado de actualizar los datos de un lector en la base de datos
    def actualizarLector(self, lectorId, nombre, apellido, dni, domicilio, telefono, email):
        # Se obtiene una referencia a la colección 'lectores' en la base de datos
        lectores = db.collection("lectores")
        lectorRef = lectores.document(lectorId)
        # Se verifica si el lector existe en la base de datos
        if lectorRef.get().exists:
            # Si el lector existe, se actualizan sus datos con los valores proporcionados
            lectorRef.update({
                'nombre': nombre,
                'apellido': apellido,
                'dni': dni,
                'domicilio': domicilio,
                'telefono': telefono,
                'email': email
            })
        else:
            print("Cliente no encontrado. No se pudieron actualizar los datos.")
    
    # Método encargado de eliminar un lector de la base de datos
    def eliminarLector(self, lectorId):
        lectores = db.collection("lectores")
        lectorRef = lectores.document(lectorId)
        # Se verifica si el lector existe en la base de datos
        if lectorRef.get().exists:
            lectorRef.delete()
        else:
            print("Cliente no encontrado. No se pudo eliminar.")
    
    # Método encargado de mostrar la lista de préstamos registrados
    def mostrarPrestamos(self):
        prestamosRef = db.collection("prestamos")
        prestamos = prestamosRef.stream()
        # Se verifica el estado de los préstamos
        self.verificarEstadoPrestamos()
        listaPrestamos = []
        for prestamo in prestamos:
            datosPrestamo = prestamo.to_dict()
            docId = prestamo.id
            # Se crea un diccionario con los datos del préstamo
            prestamoDic = {
                'id': docId,
                'titulo': datosPrestamo['libroNombre'],
                'lector': datosPrestamo['lectorNombre'],
                'cantidad': datosPrestamo['cantidad'],
                #CAMBIAR
                'fechaEntrega': datosPrestamo['fechaEntrega'],
                'fechaDevolucion': datosPrestamo['fechaDevolucion'],
                'estado': datosPrestamo['estado'],
                'idLibro': datosPrestamo['idLibro']
            }
            # Se agrega el diccionario a la lista de préstamos
            listaPrestamos.append(prestamoDic)
        # Se retorna la lista de préstamos
        return listaPrestamos
    
    # Método encargado de cambiar el estado de un préstamo y actualizar la cantidad de libros disponibles
    def cambiarEstadoPrestamo(self, prestamoId, idLibro):
        try:
            prestamosRef = db.collection("prestamos")
            prestamo = prestamosRef.document(prestamoId)

            # Se verifica si el préstamo existe
            if prestamo.get().exists:
                prestamoData = prestamo.get().to_dict()
                print(f"prestamoData: {prestamoData}")
                # Se actualiza el estado del préstamo a 'DEVUELTO'
                prestamo.update({'estado': 'DEVUELTO'})

                # Se obtiene una referencia al documento del libro relacionado al préstamo
                libroRef = db.collection('libros').document(idLibro)
                libroData = libroRef.get().to_dict()

                if libroData:
                    cantidadDisponibleActual = libroData['cantidad']
                    cantidadLibrosPrestados = prestamoData.get('cantidad')
                    cantidadDisponibleNueva = cantidadDisponibleActual + cantidadLibrosPrestados
                    # Se actualiza la cantidad de libros disponibles en elstock de libros
                    libroRef.update({'cantidad': cantidadDisponibleNueva})
                return "EXITO AL CAMBIAR EL ESTADO DEL PRESTAMO"
                
            return "ERROR AL CAMBIAR EL ESTADO DEL PRESTAMO"
        except Exception as e:
            return False
      
    def realizarPrestamo(self, dniLector, idLibro, cantidad, fechaEntrega, fechaDevolucion, estado="PRESTADO"):
        nombreLector = self.buscarNombreLectorPorDni(dniLector)
        nombreLibro = self.buscarNombreLibroPorID(idLibro)
        print(f'nombreLector {nombreLector}, nombreLibro {nombreLibro}')
        if nombreLector and nombreLibro:
            lectorNombre = nombreLector
            libroNombre = nombreLibro
            cantidad = int(cantidad)

            libro = self.buscarLibroPorNombre(libroNombre)
            if libro:
                cantidadDisponible = int(libro["cantidad"])

                if cantidad <= cantidadDisponible:
                    prestamo = Prestamo(lectorNombre, libroNombre, idLibro, cantidad, fechaEntrega, fechaDevolucion, estado)

                    prestamosRef = db.collection('prestamos')
                    nuevoPrestamo = {
                        'lectorNombre': prestamo.getLectorNombre(),
                        'libroNombre': prestamo.getLibroNombre(),
                        'idLibro': idLibro,
                        'cantidad': prestamo.getCantidad(),
                        'fechaEntrega': prestamo.getFechaEntrega(),
                        'fechaDevolucion': prestamo.getFechaDevolucion(),
                        'estado': prestamo.getEstado()
                    }
                    prestamosRef.add(nuevoPrestamo)

                    cantidadDisponible -= cantidad
                    libroRef = db.collection('libros').document(idLibro)
                    libroRef.update({'cantidad': cantidadDisponible})

                    print("Préstamo registrado con éxito.")
                    return True
                else:
                    print("No hay suficientes copias disponibles de ese libro.")
                    return False
            else:
                print("Libro no encontrado por nombre.")
        else:
            print("Lector o libro no encontrado por ID.")

    def buscarPrestamosPorNombreLector(self, inicioNombreLector):
        prestamosRef = db.collection("prestamos")
        prestamos_query = prestamosRef.where("lectorNombre", ">=", inicioNombreLector).where("lectorNombre", "<", inicioNombreLector + u'\uf8ff').stream()
        listaPrestamos = []

        for prestamo in prestamos_query:
            datosPrestamo = prestamo.to_dict()
            docId = prestamo.id
            prestamoDic = {
                'id': docId,
                'titulo': datosPrestamo['libroNombre'],
                'lector': datosPrestamo['lectorNombre'],
                'cantidad': datosPrestamo['cantidad'],
                'fechaEntrega': datosPrestamo['fechaEntrega'],
                'fechaDevolucion': datosPrestamo['fechaDevolucion'],
                'estado': datosPrestamo['estado']
            }
            listaPrestamos.append(prestamoDic)

        return listaPrestamos

    def buscarPrestamosPorNombreLibro(self, inicioNombreLibro):
        prestamosRef = db.collection("prestamos")
        prestamos_query = prestamosRef.where("libroNombre", ">=", inicioNombreLibro).where("libroNombre", "<", inicioNombreLibro + u'\uf8ff').stream()
        listaPrestamos = []

        for prestamo in prestamos_query:
            datosPrestamo = prestamo.to_dict()
            docId = prestamo.id
            prestamoDic = {
                'id': docId,
                'titulo': datosPrestamo['libroNombre'],
                'lector': datosPrestamo['lectorNombre'],
                'cantidad': datosPrestamo['cantidad'],
                'fechaEntrega': datosPrestamo['fechaEntrega'],
                'fechaDevolucion': datosPrestamo['fechaDevolucion'],
                'estado': datosPrestamo['estado']
            }
            listaPrestamos.append(prestamoDic)

        return listaPrestamos


    def actualizarLector(self, lectorId, nombre, apellido, dni, domicilio, telefono, email):
        # Actualiza un cliente existente
        lectores = db.collection("lectores")
        lectorRef = lectores.document(lectorId)
        if lectorRef.get().exists:
            lectorRef.update({
                'nombre': nombre,
                'apellido': apellido,
                'dni': dni,
                'domicilio': domicilio,
                'telefono': telefono,
                'email': email
            })
        else:
            print("Cliente no encontrado. No se pudieron actualizar los datos.")
            
    def eliminarLector(self, lectorId):
        lectores = db.collection("lectores")
        lectorRef = lectores.document(lectorId)
        if lectorRef.get().exists:
            lectorRef.delete()
        else:
            print("Cliente no encontrado. No se pudo eliminar.")

    def verificarEstadoPrestamos(self):
        # Consulta todos los préstamos (reemplaza "prestamos" con la colección real)
        prestamosRef = db.collection('prestamos').stream()

        for prestamo in prestamosRef:
            datosPrestamo = prestamo.to_dict()
            fechaDevolucion = datosPrestamo.get('fechaDevolucion')
            estado = datosPrestamo.get('estado')
            print(estado)
            if estado != 'DEVUELTO':
                estado = Validaciones().verificarEstadoDevolucion(fechaDevolucion)

                print(f"ID del préstamo: {prestamo.id}, Estado: {estado}")
                if estado == "LIBRO NO DEVUELTO":
                    # Cambia el estado del préstamo a "NO DEVUELTO" en la base de datos
                    db.collection('prestamos').document(prestamo.id).update({'estado': 'NO DEVUELTO'})
    
    def buscarLectoresPorNombre(self, inicioNombre):
        lectoresRef = db.collection("lectores")
        lectores = lectoresRef.where("nombre", ">=", inicioNombre).where("nombre", "<", inicioNombre + u'\uf8ff').stream()
        listaLectores = []

        for prestamo in lectores:
            datosLector = prestamo.to_dict()
            docId = prestamo.id
            prestamoDic = {
                'id': docId,
                'nombre': datosLector['nombre'],
                'apellido': datosLector['apellido'],
                'dni' : datosLector['dni'],
                'email': datosLector['email'],
                'domicilio': datosLector['domicilio'],
                'telefono': datosLector['telefono']
            }
            listaLectores.append(prestamoDic)
        return listaLectores
    
    def buscarLectoresPorDni(self, inicioDni):
        lectoresRef = db.collection("lectores")
        lectores = lectoresRef.where("dni", ">=", inicioDni).where("dni", "<", inicioDni + u'\uf8ff').stream()
        listaLectores = []

        for prestamo in lectores:
            datosLector = prestamo.to_dict()
            docId = prestamo.id
            prestamoDic = {
                'id': docId,
                'nombre': datosLector['nombre'],
                'apellido': datosLector['apellido'],
                'dni' : datosLector['dni'],
                'email': datosLector['email'],
                'domicilio': datosLector['domicilio'],
                'telefono': datosLector['telefono']
            }
            listaLectores.append(prestamoDic)
        return listaLectores
    
    def buscarLectoresPorApellido(self, inicioApellido):
        lectoresRef = db.collection("lectores")
        lectores = lectoresRef.where("apellido", ">=", inicioApellido).where("apellido", "<", inicioApellido + u'\uf8ff').stream()
        listaLectores = []

        for prestamo in lectores:
            datosLector = prestamo.to_dict()
            docId = prestamo.id
            prestamoDic = {
                'id': docId,
                'nombre': datosLector['nombre'],
                'apellido': datosLector['apellido'],
                'dni' : datosLector['dni'],
                'email': datosLector['email'],
                'domicilio': datosLector['domicilio'],
                'telefono': datosLector['telefono']
            }
            listaLectores.append(prestamoDic)
        return listaLectores