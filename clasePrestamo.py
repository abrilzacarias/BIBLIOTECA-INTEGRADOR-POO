#la clase Prestamo se utiliza para realizar los préstamos a los lectores registrados en el sistema. 
class Prestamo:
    def __init__(self, lectorNombre, libroNombre, idLibro, cantidad, fechaEntrega, fechaDevolucion, estado):
        #se inicializan los atributos para el préstamos
        self.__lectorNombre = lectorNombre #el nombre del lector al que se va a realizar el préstamos
        self.__libroNombre = libroNombre #el nombre del libro que se prestará
        self.__idLibro = idLibro #el id del libro a prestar
        self.__cantidad = cantidad #la cantidad de ejemplares a prestar
        self.__fechaEntrega = fechaEntrega #le fecha de entrega es la fecha en la cual el bibliotecario le entrega el libro al lector.
        self.__fechaDevolucion = fechaDevolucion #la fecha de devolución es la fecha estimada que el lector debe devolver el libro. 
        self.__estado = estado #los estados son: prestado, devuelvo, no devuelto

    #ENCAPSULAMIENTO Y ABSTRACCIÓN
    def getLectorNombre(self):
        return self.__lectorNombre

    def setLectorNombre(self, lectorNombre):
        self.__lectorNombre = lectorNombre
        
    def getLibroNombre(self):
        return self.__libroNombre

    def setLibroNombre(self, libroNombre):
        self.__libroNombre = libroNombre

    def getIdLibro(self):
        return self.__idLibro

    def setIdLibro(self, idLibro):
        self.__idLibro = idLibro
        
    def getLibroEditorial(self):
        return self.__libroEditorial

    def setLibroEditorial(self, libroEditorial):
        self.__libroEditorial = libroEditorial

    def getCantidad(self):
        return self.__cantidad

    def setCantidad(self, cantidad):
        self.__cantidad = cantidad

    def getFechaEntrega(self):
        return self.__fechaEntrega

    def setFechaEntrega(self, fechaEntrega):
        self.__fechaEntrega = fechaEntrega

    def getFechaDevolucion(self):
        return self.__fechaDevolucion

    def setFechaDevolucion(self, fechaDevolucion):
        self.__fechaDevolucion = fechaDevolucion
        
    def getEstado(self):
        return self.__estado

    def setEstado(self, estado):
        self.__estado = estado

