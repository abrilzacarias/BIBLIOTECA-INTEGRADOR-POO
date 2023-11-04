from claseOpciones import Opciones
from config import db

class Autor(Opciones):
    def __init__(self, idOpcion=None, descripcionOpcion=None):
        super().__init__(idOpcion, descripcionOpcion, "autor")
        
def agregarAutor(nombre):
    # Busca al autor en la base de datos
    autor = db.collection('autores').where('nombre', '==', nombre).get()

    # Si el autor ya existe, devuelve su ID
    if autor:
        return autor[0].id

    # Si el autor no existe, crea uno nuevo y devuelve su ID
    else:
        nuevo_autor = db.collection('autores').add({'nombre': nombre})
        return nuevo_autor.id

