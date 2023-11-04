from clasePersona import Persona
from clasePrestamo import Prestamo
from config import db

class Bibliotecario(Persona):
    def __init__(self, nombre=None, apellido=None, dni=None, domicilio=None, telefono=None, email=None, password=None):
        super().__init__(nombre, apellido, dni, domicilio, email, telefono)
        self.__password = password
        self.__idBibliotecario = None

    def getPassword(self):
        return self.__password
    
    def setPassword(self, password):
        self.__password = password
        
    def getIdBibliotecario(self):
        return self.__idBibliotecario
    
    def setIdBibliotecario(self, idBibliotecario):
        self.__idBibliotecario = idBibliotecario
   

    #Método encargado de obtener los datos de un cliente por su ID
    def obtenerLectorPorId(self, idLector):
    # Obtener un cliente por su ID
        lectores_ref = db.collection('lectores')
        lector_doc = lectores_ref.document(idLector).get()

        if lector_doc.exists:
            # El documento del cliente existe, y puedes acceder a sus datos
            datos_lector = lector_doc.to_dict()
            return datos_lector
        else:
            # El cliente no fue encontrado
            return None
        
    def buscarLibroPorNombre(self, nombreLibro):
        librosRef = db.collection('libros')
        query = librosRef.where('titulo', '>=', nombreLibro).where('titulo', '<=', nombreLibro + '\uf8ff').get()
        for libro in query:
            datosLibro = libro.to_dict()
            return datosLibro
        return None
    
  
    def buscarNombreLectorPorID(self,idLector):
        lectoresRef = db.collection('lectores').document(idLector)
        documento = lectoresRef.get()
        if documento.exists:
            datos_lector = documento.to_dict()
            nombre = datos_lector.get('nombre', '')
            apellido = datos_lector.get('apellido', '')
            return f"{nombre} {apellido}"
        else:
            return None

    
    def buscarNombreLibroPorID(self,idLibro):
        librosRef = db.collection('libros').document(idLibro)
        documento = librosRef.get()
        if documento.exists:
            return documento.get('titulo')
        else:
            return None

    #Método encargado de actualizar los datos de un cliente
    def agregarLector(self, nombre, apellido, dni, domicilio, telefono, email):
        print(nombre)
        lectoresRef = db.collection("lectores")
        lectores_data = {
            'nombre': nombre.capitalize(),
            'apellido': apellido.capitalize(),
            'dni' : dni ,
            'email' : email ,
            'domicilio' : domicilio.capitalize() ,
            'telefono' : telefono 
        }
        print(lectores_data)
        creacion = db.collection('lectores').add(lectores_data)
        nueva_clave_unica = creacion[1].id
        return nueva_clave_unica
    
    def mostrarLectores(self):
        #Lee todos los documentos en la colección 'clientes' y los convierte en una lista de diccionarios.
        lectoresRef = db.collection("lectores")
        lectores = lectoresRef.stream()
        listaLectores = []
        for lector in lectores:
            datosLector = lector.to_dict()
            docId = lector.id  # Acceso al ID del documento
            lectorDic = {
                'id': docId,
                'nombre': datosLector['nombre'],
                'apellido': datosLector['apellido'],
                'dni' : datosLector['dni'],
                'email': datosLector['email'],
                'domicilio': datosLector['domicilio'],
                'telefono': datosLector['telefono']
            }
            listaLectores.append(lectorDic)
        return listaLectores

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
            
    def mostrarPrestamos(self):
        prestamosRef = db.collection("prestamos")
        prestamos = prestamosRef.stream()
        listaPrestamos = []
        for prestamo in prestamos:
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
    
    def cambiarEstadoPrestamo(self, prestamoId):
        try:
            prestamosRef = db.collection("prestamos")
            prestamo = prestamosRef.document(prestamoId)

            if prestamo.get().exists:
                prestamo.update({'estado': 'Devuelto'})
                return True
            else:
                return False
        except Exception as e:
            return False 
      
    def realizarPrestamo(self, idLector, idLibro, cantidad, fechaEntrega, fechaDevolucion, estado="PRESTADO"):
        nombreLector = self.buscarNombreLectorPorID(idLector)
        nombreLibro = self.buscarNombreLibroPorID(idLibro)

        if nombreLector and nombreLibro:
            lectorNombre = nombreLector
            libroNombre = nombreLibro
            cantidad = int(cantidad)

            libro = self.buscarLibroPorNombre(libroNombre)
            if libro:
                cantidadDisponible = int(libro["cantidad"])

                if cantidad <= cantidadDisponible:
                    prestamo = Prestamo(lectorNombre, libroNombre, cantidad, fechaEntrega, fechaDevolucion, estado)

                    prestamosRef = db.collection('prestamos')
                    nuevoPrestamo = {
                        'lectorNombre': prestamo.getLectorNombre(),
                        'libroNombre': prestamo.getLibroNombre(),
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
                else:
                    print("No hay suficientes copias disponibles de ese libro.")
            else:
                print("Libro no encontrado por nombre.")
        else:
            print("Lector o libro no encontrado por ID.")
    
    from firebase_admin import firestore

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
    
       
    '''def realizarPrestamo(self, idLector, idLibro, cantidad, fechaEntrega, fechaDevolucion, estado="PRESTADO"):
        bibliotecario = Bibliotecario()
        nombreLector = bibliotecario.buscarNombreLectorPorID(idLector)
        nombreLibro = bibliotecario.buscarNombreLibroPorID(idLibro)

        if nombreLector and nombreLibro:
            lectorNombre = nombreLector
            libroNombre = nombreLibro

            libro = bibliotecario.buscarLibroPorNombre(libroNombre)
            if libro:
                cantidadDisponible = libro["cantidad"]


                prestamo = Prestamo(lectorNombre, libroNombre, cantidad, fechaEntrega, fechaDevolucion, estado)

                prestamosRef = db.collection('prestamos')
                nuevoPrestamo = {
                    'lectorNombre': prestamo.getLectorNombre(),
                    'libroNombre': prestamo.getLibroNombre(),
                    'cantidad': prestamo.getCantidad(),
                    'fechaEntrega': prestamo.getFechaEntrega(),
                    'fechaDevolucion': prestamo.getFechaDevolucion(),
                    'estado': prestamo.getEstado()
                }

                prestamosRef.add(nuevoPrestamo)
                print("Préstamo registrado con éxito.")
            else:
                print("No hay suficientes copias disponibles de ese libro.")
        else:
            print("Lector o libro no encontrado por ID.")'''
            

'''idLector = "2it3rKmV7LPveYJbDDp9"  # Reemplaza con un ID válido
idLibro = "qPpR5pGmWHE2E3VHyuzO"    # Reemplaza con un ID válido
cantidad = 2
fechaEntrega = "2023-11-03"  # Reemplaza con una fecha válida
fechaDevolucion = "2023-11-10"  # Reemplaza con una fecha válida
estado = "PRESTADO"
bibliotecario = Bibliotecario()  # Crea una instancia de la clase Bibliotecario

bibliotecario.realizarPrestamo(idLector, idLibro, cantidad, fechaEntrega, fechaDevolucion,estado)'''

#Bibliotecario.realizarPrestamo(idLector, idLibro, cantidad, fechaEntrega, fechaDevolucion, estado)

'''bibliotecario = Bibliotecario()  # Crea una instancia de la clase Bibliotecario
resultados = bibliotecario.buscarLibroPorNombre("HOLAABRIL")
if resultados:
    for clave, valor in resultados.items():
        print(f"{clave}: {valor}")  # Imprimir clave y valor
else:
    print("No se encontraron libros con ese nombre.")'''
'''    
bibliotecario = Bibliotecario()

# Llama al método mostrarPrestamos para obtener la lista de préstamos
lista_prestamos = bibliotecario.mostrarPrestamos()

# Comprueba si se obtuvieron préstamos y los imprime
if lista_prestamos:
    for prestamo in lista_prestamos:
        print("ID:", prestamo["id"])
        print("Título del Libro:", prestamo["titulo"])
        print("Nombre del Lector:", prestamo["lector"])
        print("Cantidad:", prestamo["cantidad"])
        print("Fecha de Entrega:", prestamo["fechaEntrega"])
        print("Fecha de Devolución:", prestamo["fechaDevolucion"])
        print("Estado:", prestamo["estado"])
        print("------------")
else:
    print("No se encontraron préstamos.")
'''   