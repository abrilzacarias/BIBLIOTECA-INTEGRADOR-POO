from config import db

class Opciones():
    def __init__(self, idOpcion=None, descripcionOpcion=None, nombreColeccion=None):
        self.__idOpcion = idOpcion
        self.__descripcionOpcion = descripcionOpcion
        self.__nombreColeccion = nombreColeccion

    def getIdOpcion(self):
        return self.__idOpcion

    def setIdOpcion(self, idOpcion):
        self.__idOpcion = idOpcion

    def getDescripcionOpcion(self):
        return self.__descripcionOpcion

    def setDescripcionOpcion(self, descripcionOpcion):
        self.__descripcionOpcion = descripcionOpcion

    def listarOpciones(self, nombreColeccion):
        opcionesRef = db.collection(nombreColeccion)
        listaOpciones = [{"id": doc.id, "descripcionOpcion": doc.to_dict()[f'descripcion{nombreColeccion.capitalize()}']} for doc in opcionesRef.stream()]
        return listaOpciones

    def agregarOpcion(self, nombreColeccion, descripcionOpcion):
        opcionesRef = db.collection(nombreColeccion)
        opcionesRef.add({f'descripcion{nombreColeccion.capitalize()}':descripcionOpcion})

    def modificarOpcion(self, nombreColeccion, idOpcion, descripcionNueva):
        if idOpcion is not None:
            db.collection(nombreColeccion).document(idOpcion).update({
                f'descripcion{nombreColeccion.capitalize()}': descripcionNueva,
            })
        else:
            print(f"No se proporcionó un identificador de {nombreColeccion} para la modificación.")

    def eliminarOpcion(self, nombreColeccion, variableId):
        if variableId is not None:
            doc_ref = db.collection(nombreColeccion).document(variableId)
            if doc_ref.get().exists:
                doc_ref.delete()
            else:
                print(f"No se encontró el documento con el ID {variableId} en la colección {nombreColeccion}.")
    

    def obtenerDescripcionesOpcion(self):
        descripciones = []  # Lista para almacenar las descripciones
        if self.__idOpcion is not None:
            for id in self.__idOpcion:  # Itera a través de la lista de identificadores
                opcion_ref = db.collection(self.__nombreColeccion).document(id)
                opcion_doc = opcion_ref.get()
                if opcion_doc.exists:
                    descripcion = opcion_doc.to_dict()[f'descripcion{self.__nombreColeccion.capitalize()}']
                    descripciones.append(descripcion)
                else:
                    descripciones.append(f"{self.__nombreColeccion.capitalize()} no encontrado para ID: {id}")
        return descripciones

    def obtenerDescripcionOpcion(self, nombreColeccion=None, variableId=None):
        if variableId is not None:
                opcion_ref = db.collection(nombreColeccion).document(variableId)
                opcion_doc = opcion_ref.get()
                if opcion_doc.exists:
                    descripcion = opcion_doc.to_dict()[f'descripcion{nombreColeccion.capitalize()}']
                else:
                    descripcion = (f"{nombreColeccion.capitalize()} no encontrado para ID: {variableId}")
        return descripcion
