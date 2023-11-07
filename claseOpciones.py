from config import db
#Clase base o clase padre de Autor, Editorial y Género. Dichas clases sirven para representar diferentes aspectos del libro.
class Opciones():
    def __init__(self, idOpcion=None, descripcionOpcion=None, nombreColeccion=None):
        self.__idOpcion = idOpcion
        self.__descripcionOpcion = descripcionOpcion
        self.__nombreColeccion = nombreColeccion

    #ENCAPSULAMIENTO Y ABSTRACCIÓN
    def getIdOpcion(self):
        return self.__idOpcion

    def setIdOpcion(self, idOpcion):
        self.__idOpcion = idOpcion

    def getDescripcionOpcion(self):
        return self.__descripcionOpcion

    def setDescripcionOpcion(self, descripcionOpcion):
        self.__descripcionOpcion = descripcionOpcion

    #Con las opciones se realiza un CRUD de las mismas. 
    def agregarOpcion(self):
        #se agrega una opcion a la colección elegida, ya sea autores, editoriales o generos.
        opcionesRef = db.collection(self.__nombreColeccion)
        opcionesRef.add({f'descripcion{self.__nombreColeccion.capitalize()}': self.__descripcionOpcion})

    def modificarOpcion(self):
        #se modifica la opción obteniendo el id de la misma
        if self.__idOpcion is not None:
            db.collection(self.__nombreColeccion).document(self.__idOpcion).update({
                f'descripcion{self.__nombreColeccion.capitalize()}': self.__descripcionOpcion,
            })
        else:
            print(f"No se proporcionó un identificador de {self.__nombreColeccion} para la modificación.")

    def eliminarOpcion(self):
        #se elimina la opción con el id de la misma. 
        if self.__idOpcion is not None:
            db.collection(self.__nombreColeccion).document(self.__idOpcion).delete()
        else:
            print(f"No se proporcionó un identificador de {self.__nombreColeccion} para la eliminación.")
    
    def mostrarOpciones(self, nombreColeccion):
        #lista de las opciones
        opcionesRef = db.collection(nombreColeccion)
        listaOpciones = [{"id": doc.id, "descripcionOpcion": doc.to_dict()[f'descripcion{nombreColeccion.capitalize()}']} for doc in opcionesRef.stream()]
        return listaOpciones

    def obtenerDescripcionesOpcion(self):
        #mediante el id de la opción se obtiene su descripción. 
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

    def listarOpciones(self, nombreColeccion, tipoOpcion, filtro):
        descripciones = []  #Lista para almacenar las descripciones

        #Realiza una consulta a la base de datos para obtener las opciones del tipo deseado
        if tipoOpcion == "autor":
            opciones_ref = db.collection(nombreColeccion)
            opciones_query = opciones_ref.where("descripcionAutor", ">=", filtro).where("descripcionAutor", "<", filtro + u'\uf8ff')
            opciones_docs = opciones_query.stream()
            for opcion_doc in opciones_docs:
                opcion = {
                    "id": opcion_doc.id,  # ID de la opción
                    "descripcion": opcion_doc.to_dict()["descripcionAutor"]  # Descripción de la opción
                }
                descripciones.append(opcion)
        elif tipoOpcion == "genero":
            opciones_ref = db.collection(nombreColeccion)
            opciones_query = opciones_ref.where("descripcionGenero", ">=", filtro).where("descripcionGenero", "<", filtro + u'\uf8ff')
            opciones_docs = opciones_query.stream()
            for opcion_doc in opciones_docs:
                opcion = {
                    "id": opcion_doc.id,  # ID de la opción
                    "descripcion": opcion_doc.to_dict()["descripcionGenero"]  #Descripción de la opción
                }
                descripciones.append(opcion)
        elif tipoOpcion == "editorial":
            opciones_ref = db.collection(nombreColeccion)
            opciones_query = opciones_ref.where("descripcionEditorial", ">=", filtro).where("descripcionEditorial", "<", filtro + u'\uf8ff')
            opciones_docs = opciones_query.stream()
            for opcion_doc in opciones_docs:
                opcion = {
                    "id": opcion_doc.id,  # ID de la opción
                    "descripcion": opcion_doc.to_dict()["descripcionEditorial"]  #Descripción de la opción
                }
                descripciones.append(opcion)
        return descripciones
    
    #MISMOS MÉTODOS PERO CON PARÁMETROS SIN INSTANCIAR A LAS CLASES (futura implementación: arreglar para que estos métodos se puedan unificar y ser reutilizados en distintas acciones. )
    def listarOpcionesGeneral(self, nombreColeccion):
        opcionesRef = db.collection(nombreColeccion)
        listaOpciones = [{"id": doc.id, "descripcionOpcion": doc.to_dict()[f'descripcion{nombreColeccion.capitalize()}']} for doc in opcionesRef.stream()]
        return listaOpciones
        
    def obtenerDescripcionOpcion(self, nombreColeccion=None, variableId=None):
        if variableId is not None:
                opcion_ref = db.collection(nombreColeccion).document(variableId)
                opcion_doc = opcion_ref.get()
                if opcion_doc.exists:
                    descripcion = opcion_doc.to_dict()[f'descripcion{nombreColeccion.capitalize()}']
                else:
                    descripcion = (f"{nombreColeccion.capitalize()} no encontrado para ID: {variableId}")
        return descripcion
    
    def eliminarOpcionGeneral(self, nombreColeccion, variableId):
        if variableId is not None:
            doc_ref = db.collection(nombreColeccion).document(variableId)
            if doc_ref.get().exists:
                doc_ref.delete()
            else:
                print(f"No se encontró el documento con el ID {variableId} en la colección {nombreColeccion}.")

    def modificarOpcionGeneral(self, nombreColeccion, idOpcion, descripcionNueva):
        if idOpcion is not None:
            db.collection(nombreColeccion).document(idOpcion).update({
                f'descripcion{nombreColeccion.capitalize()}': descripcionNueva,
            })
        else:
            print(f"No se proporcionó un identificador de {nombreColeccion} para la modificación.")
    
    def agregarOpcionGeneral(self, nombreColeccion, descripcionOpcion):
        opcionesRef = db.collection(nombreColeccion)
        opcionesRef.add({f'descripcion{nombreColeccion.capitalize()}':descripcionOpcion})

