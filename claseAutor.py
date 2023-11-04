class Autor():
    def __init__(self, idAutor, descripcionAutor):
        self.__idAutor = None
        self.__descripcionAutor = descripcionAutor

    def getIdAutor(self):
        return self.__idAutor
    
    def setIdAutor(self, idAutor):
        self.__idAutor = idAutor
        
    def getDescripcionAutor(self):
        return  self.__descripcionAutor
    
    def setDescripcionAutor(self, descripcionAutor):
        self.__descripcionAutor = descripcionAutor
         
    #POLIMORFISMO: 
    def __obtenerDatos(self):
        return self.getDescripcionAutor()