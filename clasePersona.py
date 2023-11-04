class Persona():
    def __init__(self, nombre, apellido, dni, domicilio, telefono, email):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__email = email
        self.__domicilio = domicilio
        self.__telefono = telefono

    def getNombre(self):
        return self.__nombre
    
    def setNombre(self, nombre):
        self.__nombre = nombre

    def getApellido(self):
        return self.__apellido
    
    def setApellido(self, apellido):
        self.__apellido = apellido

    def getDni(self):
        return self.__dni
    
    def setDni(self, dni):
        self.__dni = dni

    def getEmail(self):
        return self.__email
    
    def setEmail(self, email):
        self.__email = email

    def getDireccion(self):
        return self.__direccion
    
    def getDomicilio(self):
        return self.__domicilio

    def setDomicilio(self, domicilio):
        self.__domicilio = domicilio

    def getTelefono(self):
        return self.__telefono
    
    def setTelefono(self, telefono):
        self.__telefono = telefono

        
    

        