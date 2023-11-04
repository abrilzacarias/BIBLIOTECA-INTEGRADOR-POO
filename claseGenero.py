class Genero():
    def __init__(self, idGenero, descripcionGenero):
        self.__idGenero = None
        self.__descripcionGenero = descripcionGenero

    def getIdGenero(self):
        return self.__idGenero
    
    def setIdGenero(self, idGenero):
        self.__idGenero = idGenero
        
    def getDescripcionGenero(self):
        return  self.__descripcionGenero
    
    def setDescripcionGenero(self, descripcionGenero):
        self.__descripcionGenero = descripcionGenero
         
    #POLIMORFISMO: 
    def __obtenerDatos(self):
        return self.getDescripcionGenero()