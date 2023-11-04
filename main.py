from subclaseBibliotecario import Bibliotecario

resultados = Bibliotecario.buscarLibroPorNombre("HOLAABRIL")
if resultados:
    for libro in resultados:
        print(libro)  # Imprimir información de cada libro encontrado
else:
    print("No se encontraron libros con ese nombre.")