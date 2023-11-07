from claseOpciones import Opciones
from config import db
#HERENCIA: editorial es una herencia de la clase Opciones
class Editorial(Opciones):
    def __init__(self, idOpcion=None, descripcionOpcion=None):
        super().__init__(idOpcion, descripcionOpcion, "editorial")