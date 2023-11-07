from flask import render_template, redirect, url_for, request, jsonify, session
from config import app, db
from firebase_admin import auth
from claseRegistro import Registro
from claseValidaciones import Validaciones
from claseInicioSesion import InicioSesion
from subclaseBibliotecario import Bibliotecario
from subclaseLector import Lector
from claseLibro import Libro
from claseOpciones import Opciones
import datetime

registroUsuario = Registro()
validador = Validaciones()
inicioSesionUsuario = InicioSesion()
bibliotecario = Bibliotecario()
opciones = Opciones()
libro = Libro()

@app.route ('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    error_message = ''
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            dni = request.form['dni']
            domicilio = request.form['domicilio']
            telefono = request.form['telefono']
            email = request.form['email']
            password = request.form['password']
            
            if error_message:
                error_message += " "  # Agrega espacio si hay un error
            error_message += validador.validarNombre(nombre)
            error_message += validador.validarApellido(apellido)
            error_message += validador.validarDNI(dni)
            error_message += validador.validarDomicilio(domicilio)
            error_message += validador.validarTelefono(telefono)
            error_message += validador.validarMail(email)
            error_message += validador.validarContrasena(password)
            

            if not error_message:  # Si no hay mensajes de error, procede a registrar al usuario
                registroUsuario.registrarUsuario(email, password)
                #registroUsuario.cargarDatos(nombre, apellido, dni, email, domicilio, telefono, password)

                return redirect(url_for('login'))
        except Exception as e:
            # Registro fallido, muestra un mensaje de error.
            error_message = f'El registro falló. Inténtalo de nuevo. Error: {e}'
            return render_template('login/registro.html', error_message=error_message)
    return render_template('login/registro.html', error_message=error_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        response = inicioSesionUsuario.verificarInicioSesion(email, password)
        # Procesa la respuesta
        if response.status_code == 200:
            respuestaVerificacion = inicioSesionUsuario.verificarConfirmacionMail(email)
            if respuestaVerificacion == True:
                user_data = response.json()
                user_id = user_data['localId']
                print(user_id)
                return redirect(url_for('listarLibros'))
            else:
                error_message = 'No se ha verificado su correo electrónico. Por favor, revise su correo.'
                return render_template('login/login.html', error_message=error_message)
        else:
            error_message = 'Email o contraseña incorrectas. Por favor, intente nuevamente.'
            return render_template('login/login.html', error_message=error_message)
    return render_template('login/login.html', error_message=error_message)


@app.route('/inicio')
def inicio():
    # Página de inicio después de iniciar sesión.
    return render_template('libros/vistaLibros.html')

@app.route('/resetPassword', methods=['GET','POST'])
def resetPassword():
    email = request.form.get('email')
    if request.method == 'POST':
        try:
            user = auth.get_user_by_email(email)
            inicioSesionUsuario.resetPass(email, user)
            message = 'Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico.'
            return render_template('login/resetPass.html', message=message)
        except auth.UserNotFoundError:
            message = 'No se ha encontrado su correo electronico'
            return render_template('login/resetPass.html', message=message)
    return render_template('login/resetPass.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/listarSeleccion', methods=['GET', 'POST'])
#listarSeleccion depende de la eleccion de visualizar autor, editorial o genero. En caso de elegir alguno, se 
#utiliza la misma plantilla html para listar cada uno de ellos, sin neecesidad de crear una plantilla individual para cada uno. 
def listarSeleccion(): 
    nombreColeccion = request.args.get('nombreColeccion')
    if nombreColeccion:
        variableLista = opciones.listarOpcionesGeneral(nombreColeccion)
        return render_template('libros/listarColeccion.html', variableLista=variableLista, nombreColeccion=nombreColeccion)
    else:
        if request.method == 'POST':
            nombreColeccion = request.form['nombreColeccion']
            variableLista = opciones.listarOpcionesGeneral(nombreColeccion)
            
            return render_template('libros/listarColeccion.html', variableLista=variableLista, nombreColeccion=nombreColeccion)
        else:
            return render_template('libros/listarColeccion.html')

@app.route('/eliminarVariable/<nombreColeccion>/<variableId>', methods=['GET', 'POST'])
def eliminarVariable(nombreColeccion, variableId): 
    opciones.eliminarOpcionGeneral(nombreColeccion, variableId)
    return redirect(url_for('listarSeleccion', nombreColeccion=nombreColeccion))

@app.route('/actualizarVariable/<nombreColeccion>/<variableId>', methods=['GET', 'POST'])
def actualizarVariable(nombreColeccion, variableId): 
    seleccion = opciones.obtenerDescripcionOpcion(nombreColeccion, variableId)

    if request.method == 'POST':
        descripcionNueva = request.form['descripcionNueva']

        if seleccion:
            opciones.modificarOpcionGeneral(nombreColeccion, variableId, descripcionNueva)
            return redirect(url_for('listarSeleccion', nombreColeccion=nombreColeccion))
        else:
            error_message = 'No se ha podido modificar correctamente'
            return render_template('libros/actualizarVariable.html', error_message=error_message)
    return render_template('libros/actualizarVariable.html', descripcionActual=seleccion, nombreColeccion=nombreColeccion, variableId=variableId)

@app.route('/agregarVariable/<nombreColeccion>', methods=['GET', 'POST'])
def agregarVariable(nombreColeccion): 
    if request.method == 'POST':
        nuevoDoc = request.form['nuevoDoc']

        if nuevoDoc:
            opciones.agregarOpcionGeneral(nombreColeccion, nuevoDoc)
            return redirect(url_for('listarSeleccion', nombreColeccion=nombreColeccion))
        else:
            error_message = 'No se ha podido modificar correctamente'
            return render_template('libros/agregarVariable.html', error_message=error_message)
    return render_template('libros/agregarVariable.html', nombreColeccion=nombreColeccion)

@app.route('/agregarLector', methods=['GET', 'POST'])
def agregarLector():
    error_message = ''
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            dni = request.form['dni']
            domicilio = request.form['domicilio']
            telefono = request.form['telefono']
            email = request.form['email']
            

            if error_message:
                error_message += " "  # Agrega espacio si hay un error
            error_message += validador.validarNombre(nombre)
            error_message += validador.validarApellido(apellido)
            error_message += validador.validarDNI(dni)
            error_message += validador.validarDomicilio(domicilio)
            error_message += validador.validarTelefono(telefono)
            error_message += validador.validarMail(email)
            
            

            if not error_message:  # Si no hay mensajes de error, procede a registrar al usuario
                print(f'nombre{nombre}, ape{apellido}, dni{dni}, dom{domicilio}, tel{telefono}, email{email}')
                bibliotecario.agregarLector(nombre, apellido, dni, domicilio, telefono, email)
                lector = Lector(nombre, apellido, dni, domicilio, telefono, email)
                

                return redirect(url_for('verLectores'))
        except Exception as e:
            # Registro fallido, muestra un mensaje de error.
            error_message = f'El registro falló. Inténtalo de nuevo. Error: {e}'
            return render_template('lectores/agregarLector.html', error_message=error_message)
    return render_template('lectores/agregarLector.html', error_message=error_message)

@app.route('/verLectores')
def verLectores():
    lectores = bibliotecario.mostrarLectores()
    return render_template('lectores/verLectores.html', lectores=lectores)

@app.route('/ActualizarLector/<lectorId>', methods=['GET', 'POST'])
def ActualizarLector(lectorId):
    lector = bibliotecario.obtenerLectorPorId(lectorId)
    print('hola')
    if request.method == 'POST':
        print('hola')
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        domicilio = request.form['domicilio']
        telefono = request.form['telefono']
        email = request.form['email']
        bibliotecario.actualizarLector(lectorId, nombre, apellido, dni, domicilio, telefono, email)
        return redirect(url_for('verLectores'))
    else:
        return render_template('lectores/actualizarLector.html', lector=lector, lectorId=lectorId)

@app.route('/EliminarLector/<lectorId>', methods=['GET', 'POST'])
def EliminarLector(lectorId):
    bibliotecario.eliminarLector(lectorId)
    return redirect(url_for('verLectores'))

@app.route('/verPrestamos')
def verPrestamos():
    prestamos = bibliotecario.mostrarPrestamos()
    
    return render_template('prestamos/verPrestamos.html', prestamos=prestamos)

@app.route('/cambiarEstadoPrestamo/<prestamoId>/<idLibro>', methods=['POST'])
def cambiarEstadoPrestamo(prestamoId, idLibro):
    try:
        bibliotecario.cambiarEstadoPrestamo(prestamoId, idLibro)
        return redirect(url_for('verPrestamos'))
    except Exception as e:
        return f"Error al cambiar el estado del préstamo: {str(e)}"


@app.route('/realizarPrestamo', methods=['GET', 'POST'])
def realizarPrestamo():
    #libros = libro.listarLibros()
    lectores = bibliotecario.mostrarLectores()
    if request.method == 'POST':
        dniLector = request.form['DNILector']
        idLibro = request.form['idLibro']
        cantidad = int(request.form['cantidad'])  # Convertir la cantidad a entero
        fechaDevolucion = request.form['fechaDevolucion']
        estado = "PRESTADO"

        fechaActual = validador.obtenerFechaActualStr()

        if validador.validarFechaDevolucionPrestamo(fechaDevolucion) == False:
            error = "La fecha de devolución no puede ser anterior a la fecha actual."
            return render_template('prestamos/registroPrestamo.html', error=error, lectores=lectores)  
        else:
            prestamo = bibliotecario.realizarPrestamo(dniLector, idLibro, cantidad, fechaActual, fechaDevolucion, estado)
            if prestamo == False:
                error = "La cantidad de libros en stock no es suficiente para realizar el préstamo."
                return render_template('prestamos/registroPrestamo.html', lectores=lectores, error=error)
            else:
                prestamos = bibliotecario.mostrarPrestamos()
                return render_template('prestamos/verPrestamos.html', prestamos=prestamos)
    
    return render_template('prestamos/registroPrestamo.html', lectores=lectores)
    
@app.route('/buscarPrestamos', methods=['POST'])
def buscarPrestamos():
    nombreLectorLibro = request.form['nombreLectorLibro']
    resultadoNombreLibro = bibliotecario.buscarPrestamosPorNombreLibro(nombreLectorLibro)
    resultadosNombreLector = bibliotecario.buscarPrestamosPorNombreLector(nombreLectorLibro)
    print(resultadoNombreLibro)
    print(f'LIBRO {resultadoNombreLibro}')
    # Combina las dos listas eliminando duplicados
    resultadosPrestamos = resultadoNombreLibro + resultadosNombreLector

    return render_template('prestamos/verPrestamos.html', prestamos=resultadosPrestamos)

@app.route('/listarLibros')
def listarLibros():
    libro = Libro()  # Crea una instancia de la clase Libro
    listaLibros = libro.listarLibros()
  # Agrega esta línea para verificar la lista de libros
    return render_template('libros/vistaLibros.html', libros=listaLibros)

@app.route('/agregarLibro', methods=["GET", "POST"])
def agregarLibro():
    if request.method == 'POST':
        # Obtén los datos de la solicitud JSON
        isbn = request.form["isbn"]
        titulo = request.form["titulo"]
        portada = request.files["portada"]
        idAutor = request.form.getlist('autor')  # Recibe una lista de IDs de autores
        idEditorial = request.form.getlist('editorial')  
        idGenero = request.form.getlist('genero') 
        cantidad = request.form["cantidad"]
        
        # Convierte la lista de autores en una lista de diccionarios
        #print(f'Autores: {idAutor}')
        #print(f'NOMBRE EN ROUTES: {titulo}')
        #print(f'NOMBRE EN ROUTES: {idAutor} {idEditorial} {idGenero}')
        nuevoLibro = Libro()
        idLibro = nuevoLibro.agregarLibro(isbn, titulo, portada, idAutor, idEditorial, idGenero, cantidad)
 
        # Comprueba si se ha seleccionado al menos una opción para cada campo
        if not idAutor or not idEditorial or not idGenero:
            error='Debes seleccionar al menos una opción para Autor, Editorial y Género.'
            return render_template("libros/agregarLibro.html", error_message = error)   
        
        if idLibro:
            # El libro se agregó con éxito, redirige a la vista listarLibros
            return redirect(url_for('listarLibros'))
        else:
            # Hubo un error al agregar el libro, muestra el mensaje de error
            return "Error al agregar el libro"
    else:
        return render_template("libros/agregarLibro.html")

@app.route('/obtenerLibroPorId/<string:idLibro>', methods=['GET'])
def obtenerLibroPorId(idLibro):
    if idLibro is not None:
        # Aquí puedes utilizar tu método obtenerLibroPorId para obtener los datos del libro
        libro = Libro()  # Crea una instancia de la clase Libro
        datosLibro = libro.obtenerLibroPorId(idLibro)

        if datosLibro is not None:
            # Obtén los IDs de autores, editoriales y géneros seleccionados en el libro
            idAutoresSeleccionados = datosLibro.get('idAutoresSeleccionados', [])
            idEditorialesSeleccionadas = datosLibro.get('idEditorialesSeleccionadas', [])
            idGenerosSeleccionados = datosLibro.get('idGenerosSeleccionados', [])

            #print(idAutoresSeleccionados)
            
            # Agrega estos IDs a los datos del libro
            datosLibro['idAutoresSeleccionados'] = idAutoresSeleccionados
            datosLibro['idEditorialesSeleccionadas'] = idEditorialesSeleccionadas
            datosLibro['idGenerosSeleccionados'] = idGenerosSeleccionados

            return jsonify(datosLibro)  # Devuelve los datos del libro con los IDs seleccionados como JSON
        else:
            return jsonify({'error': 'El libro no existe en la base de datos'}), 404
    else:
        return jsonify({'error': 'ID de libro no válido'}), 400


@app.route('/actualizarLibro/<idLibro>', methods=['POST'])
def actualizarLibro(idLibro):
    try:
        isbn = request.form['isbn']
        titulo = request.form['titulo']
        cantidad = request.form['cantidad']
        
        autores = request.form.getlist('autor[]')
        editoriales = request.form.getlist('editorial[]')
        generos = request.form.getlist('genero[]')

        
        portada_file = request.files.get('portadaFile')

        print(f'ISBN: {isbn}')
        print(f'Título: {titulo}')
        print(f'Cantidad: {cantidad}')
        print(f'Autores: {autores}')
        print(f'Editoriales: {editoriales}')
        print(f'Géneros: {generos}')

        if portada_file:
            print(f'Portada (FileStorage): {portada_file.filename}')
        else:
            print('No se proporcionó una nueva portada')

        libro = Libro()

        # Llama al método actualizarLibro con los argumentos apropiados
        libro.actualizarLibro(idLibro, isbn, titulo, portada_file, autores, editoriales, generos, cantidad)

        return jsonify({'message': 'Libro actualizado con éxito'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/eliminarLibro/<idLibro>', methods=['GET', 'POST'])
def eliminarLibro(idLibro): 
    libro= Libro()
    #print(idLibro)
    libro.eliminarLibro(idLibro)
    return redirect(url_for('listarLibros'))

@app.route('/listarOpciones', methods=['POST'])
def listarOpciones():
    nombreColeccion = request.json['nombreColeccion']
    tipoOpcion = request.json['tipoOpcion']  # Tipo de opción a listar (por ejemplo, "autor", "genero" o "editorial")
    filtro = request.json['filtro']  # Filtro de búsqueda (por ejemplo, "a" para autores que comienzan con "a")
    
    print(nombreColeccion)
    print(tipoOpcion)
    print(filtro)
    opciones = Opciones()

    resultados = opciones.listarOpciones(nombreColeccion, tipoOpcion, filtro)
    print(resultados)
    
    return jsonify(resultados)

@app.route('/mostrarOpciones', methods=['POST'])
def mostrarOpciones():
    nombreColeccion = request.json['nombreColeccion']
    #print(nombreColeccion) # Verificar el valor en la consola del servidor
    
    opciones = Opciones()
    resultados = opciones.mostrarOpciones(nombreColeccion)
    #print(resultados) # Verificar los resultados en la consola del servidor
    
    return jsonify(resultados)

@app.route('/buscarPorAutor', methods=['POST'])
def buscarPorAutor():
    data = request.get_json()
    descripcion = data['descripcion']
    
    # Instancia la clase Libro
    libro = Libro()
    
    # Llama al método buscarPorAutor
    resultados = libro.buscarPorAutor(descripcion)
    
    return jsonify({"resultados": resultados})

@app.route('/buscarPorEditorial', methods=['POST'])
def buscarPorEditorial():
    data = request.get_json()
    descripcion = data['descripcion']
    
    # Instancia la clase Libro
    libro = Libro()
    
    # Llama al método buscarPorEditorial
    resultados = libro.buscarPorEditorial(descripcion)
    
    return jsonify({"resultados": resultados})

@app.route('/buscarPorGenero', methods=['POST'])
def buscarPorGenero():
    data = request.get_json()
    descripcion = data['descripcion']
    # Instancia la clase Libro
    libro = Libro()
    # Llama al método buscarPorGenero
    resultados = libro.buscarPorGenero(descripcion)
    
    return jsonify({"resultados": resultados})


@app.route('/buscarPorTitulo', methods=['POST'])
def buscarPorTitulo():
    data = request.get_json()
    titulo = data['titulo']
    
    # Instancia la clase Libro
    libro = Libro()
    
    # Llama al método buscarPorTitulo en la instancia de Libro
    resultados = libro.buscarPorTitulo(titulo)
    
    return jsonify({"resultados": resultados})

#Ruta encargada de gestionar la busqueda de lectores por nombre o DNI
@app.route('/buscarLectores', methods=['POST'])
def buscarLectores():
    #Se hace un request para obtener el valor que se desea buscar
    nombreLectorDni = request.form['buscarNombreLectorDni']
    #se recuperan las busquedas a través de métodos de bibliotecario
    resultadoLectorNombre = bibliotecario.buscarLectoresPorNombre(nombreLectorDni)
    resultadosLectorDni = bibliotecario.buscarLectoresPorDni(nombreLectorDni)
    resultadosLectorApellido = bibliotecario.buscarLectoresPorApellido(nombreLectorDni)
    #se combinan las dos listas retornadas
    resultadosLectores = resultadoLectorNombre + resultadosLectorDni + resultadosLectorApellido
    #se renderiza la vista con los resultados
    return render_template('lectores/verLectores.html', lectores=resultadosLectores)

