class Genero():
    #Constructor de la clase genero, inicializa los atributos del mismo.  
    #Cada vez que se añade un nuevo genero al sistema se crea una clase de la misma. 
    def __init__(self, idGenero, descripcionGenero):
        self.__idGenero = None
        self.__descripcionGenero = descripcionGenero

    #ENCAPSULAMIENTO Y ABSTRACCIÓN
    def getIdGenero(self):
        return self.__idGenero
    
    def setIdGenero(self, idGenero):
        self.__idGenero = idGenero
        
    def getDescripcionGenero(self):
        return  self.__descripcionGenero
    
    def setDescripcionGenero(self, descripcionGenero):
        self.__descripcionGenero = descripcionGenero
         
    #POLIMORFISMO: se aplica el polimorfismo al haber métodos con nombres iguales pero con distinto comportamiento.
    def __obtenerDatos(self):
        return self.getDescripcionGenero()