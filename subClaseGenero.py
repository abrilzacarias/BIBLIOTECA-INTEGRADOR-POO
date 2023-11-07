from claseOpciones import Opciones
from config import db

#HERENCIA: género es un herencia de la clase Opciones
class Genero(Opciones):
    def __init__(self, idOpcion=None, descripcionOpcion=None):
        super().__init__(idOpcion, descripcionOpcion, "genero")

