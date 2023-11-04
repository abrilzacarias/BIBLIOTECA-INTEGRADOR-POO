class Prestamo:
    def __init__(self, lectorNombre, libroNombre, cantidad, fechaEntrega, fechaDevolucion, estado):
        self.__lectorNombre = lectorNombre
        self.__libroNombre = libroNombre
        self.__cantidad = cantidad
        self.__fechaEntrega = fechaEntrega
        self.__fechaDevolucion = fechaDevolucion
        self.__estado = estado

    def getLectorNombre(self):
        return self.__lectorNombre

    def setLectorNombre(self, lectorNombre):
        self.__lectorNombre = lectorNombre
        
    def getLibroNombre(self):
        return self.__libroNombre

    def setLibroNombre(self, libroNombre):
        self.__libroNombre = libroNombre

    def getLibroAutor(self):
        return self.__libroAutor

    def setLibroAutor(self, libroAutor):
        self.__libroAutor = libroAutor
        
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


