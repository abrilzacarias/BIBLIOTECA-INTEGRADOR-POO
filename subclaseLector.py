from clasePersona import Persona
from firebase_admin import db

class Lector(Persona):
    def __init__(self, nombre, apellido, dni, domicilio, telefono, email):
        super().__init__(nombre, apellido, dni, domicilio, telefono, email)
        self.__idLector = None

    def getIdLector(self):
        return self.__idLector
    
    def setIdLector(self, idLector):
        self.__idLector = idLector
