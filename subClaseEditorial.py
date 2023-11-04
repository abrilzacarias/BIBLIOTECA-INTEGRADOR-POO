from claseOpciones import Opciones
from config import db

class Editorial(Opciones):
    def __init__(self, idOpcion=None, descripcionOpcion=None):
        super().__init__(idOpcion, descripcionOpcion, "editorial")