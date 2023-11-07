#La clase Persona actúa como la clase padre o ABSTRACTA ya que no se la puede instanciar directamente. 
#Hereda a la clase Bibliotecario todos sus atributos.
class Persona():
    #Constructor, se inicializan los atributos. 
    def __init__(self, nombre, apellido, dni, domicilio, telefono, email):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__email = email
        self.__domicilio = domicilio
        self.__telefono = telefono

    #ENCAPSULAMIENTO Y ABSTRACCIÓN
    def getNombre(self): #obtiene nombre
        return self.__nombre
    
    def setNombre(self, nombre): #establece nombre 
        self.__nombre = nombre

    def getApellido(self): #obtiene apellido
        return self.__apellido
    
    def setApellido(self, apellido): #establece apellido
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

        
    

        