class Editorial():
    def __init__(self, idEditorial, descripcionEditorial):
        self.__idEditorial = None
        self.__descripcionEditorial = descripcionEditorial

    def getIdEditorial(self):
        return self.__idEditorial
    
    def setIdEditorial(self, idEditorial):
        self.__idEditorial = idEditorial
        
    def getDescripcionEditorial(self):
        return  self.__descripcionEditorial
    
    def setDescripcionEditorial(self, descripcionEditorial):
        self.__descripcionEditorial = descripcionEditorial
         
    #POLIMORFISMO: 
    def __obtenerDatos(self):
        return self.getDescripcionEditorial()