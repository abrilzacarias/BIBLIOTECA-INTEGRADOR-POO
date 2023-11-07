class Editorial():
    #Constructor de la clase editorial, inicializa los atributos del mismo.  
    #Cada vez que se añade una nueva editorial al sistema se crea una clase de la misma. 
    def __init__(self, idEditorial, descripcionEditorial):
        self.__idEditorial = None
        self.__descripcionEditorial = descripcionEditorial

    #ENCAPSULAMIENTO Y ABSTRACCIÓN
    def getIdEditorial(self):
        return self.__idEditorial
    
    def setIdEditorial(self, idEditorial):
        self.__idEditorial = idEditorial
        
    def getDescripcionEditorial(self):
        return  self.__descripcionEditorial
    
    def setDescripcionEditorial(self, descripcionEditorial):
        self.__descripcionEditorial = descripcionEditorial
         
    #POLIMORFISMO: se aplica el polimorfismo al haber métodos con nombres iguales pero con distinto comportamiento.
    def __obtenerDatos(self):
        return self.getDescripcionEditorial()