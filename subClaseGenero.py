from claseOpciones import Opciones
from config import db

# Ejemplo de uso para Genero
class Genero(Opciones):
    def __init__(self, idOpcion=None, descripcionOpcion=None):
        super().__init__(idOpcion, descripcionOpcion, "genero")

