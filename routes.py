#se importan los módulos necesarios. 
from flask import render_template, redirect, url_for, request, jsonify, session #se utiliza flask como servidor
from config import app, db #se importa config
from firebase_admin import auth #permite acceder y administrar proyectos de Firebase desde Python. 
#se importan las clases
from claseRegistro import Registro
from claseValidaciones import Validaciones
from claseInicioSesion import InicioSesion
from subclaseBibliotecario import Bibliotecario
from subclaseLector import Lector
from claseLibro import Libro
from claseOpciones import Opciones
import datetime

#Se realizan las instancias de las clases.
registroUsuario = Registro()
validador = Validaciones()
inicioSesionUsuario = InicioSesion()
bibliotecario = Bibliotecario()
opciones = Opciones()
libro = Libro()

# Función de verificación de sesión
def verificarSesion(fn):
    def wrapper(*args, **kwargs):
        if 'idUser' in session:
            # El bibliotecario está en sesión, permite el acceso a la ruta
            return fn(*args, **kwargs)
        else:
            # El bibliotecario no está en sesión, redirige a la página de inicio de sesión
            return redirect(url_for('login'))
    # Asigna el nombre de la función original al envoltorio
    wrapper.__name__ = fn.__name__
    return wrapper

#página principal
@app.route ('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#ruta para registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    error_message = ''
    if request.method == 'POST':
        try:
            #se obtienen los datos desde el formulario html
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            dni = request.form['dni']
            domicilio = request.form['domicilio']
            telefono = request.form['telefono']
            email = request.form['email']
            password = request.form['password']
            
            #se realizan las validaciones 
            if error_message:
                error_message += " "  # Agrega espacio si hay un error
            error_message += validador.validarNombre(nombre)
            error_message += validador.validarApellido(apellido)
            error_message += validador.validarDNI(dni)
            error_message += validador.validarDomicilio(domicilio)
            error_message += validador.validarTelefono(telefono)
            error_message += validador.validarMail(email)
            error_message += validador.validarContrasena(password)
            
            #si no se presentan incovenientes se registra al usuario. 
            if not error_message:  # Si no hay mensajes de error, procede a registrar al usuario
                registroUsuario.registrarUsuario(email, password)

                return redirect(url_for('login'))
        except Exception as e:
            #Registro fallido, muestra un mensaje de error.
            error_message = f'El registro falló. Inténtalo de nuevo. Error: {e}'
            return render_template('login/registro.html', error_message=error_message)
    return render_template('login/registro.html', error_message=error_message)

#ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    if request.method == 'POST':
        #obtiene los métodos desde el formulario html
        email = request.form['email']
        password = request.form['password']

        #ingresa a la vista del bibliotecario unicamente si el usuario se encuentra verificado. 
        response = inicioSesionUsuario.verificarInicioSesion(email, password)
        # Procesa la respuesta
        if response.status_code == 200:
            respuestaVerificacion = inicioSesionUsuario.verificarConfirmacionMail(email)
            if respuestaVerificacion == True:
                userData = response.json()
                user = userData['localId']
                if user:
                    session['idUser'] = user[0]
                return redirect(url_for('listarLibros'))
            else:
                error_message = 'No se ha verificado su correo electrónico. Por favor, revise su correo.'
                return render_template('login/login.html', error_message=error_message)
        else:
            error_message = 'Email o contraseña incorrectas. Por favor, intente nuevamente.'
            return render_template('login/login.html', error_message=error_message)
    return render_template('login/login.html', error_message=error_message)


#ruta para reestablecer la contraseña del usuario. 
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
    #limpia la sesion del usuario para el logout.
    session.clear()
    return redirect(url_for('login'))

#listarSeleccion depende de la eleccion de visualizar autor, editorial o genero. En caso de elegir alguno, se 
#utiliza la misma plantilla html para listar cada uno de ellos, sin neecesidad de crear una plantilla individual para cada uno. 
@app.route('/listarSeleccion', methods=['GET', 'POST'])
@verificarSesion
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
#se recupera al nombre de la colección y el id de la variable desde la URL 
@verificarSesion
def eliminarVariable(nombreColeccion, variableId): 
    opciones.eliminarOpcionGeneral(nombreColeccion, variableId)
    return redirect(url_for('listarSeleccion', nombreColeccion=nombreColeccion))

@app.route('/actualizarVariable/<nombreColeccion>/<variableId>', methods=['GET', 'POST'])
#se recupera al nombre de la colección y el id de la variable desde la URL 
@verificarSesion
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
#se recupera al nombre de la colección desde la URL 
@verificarSesion
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

#ruta para agregar al lector al sistema. 
@app.route('/agregarLector', methods=['GET', 'POST'])
@verificarSesion
def agregarLector():
    error_message = ''
    if request.method == 'POST':
        try:
            #se obtienen los datos del lector a través de un formulario html.
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            dni = request.form['dni']
            domicilio = request.form['domicilio']
            telefono = request.form['telefono']
            email = request.form['email']
            
            #se realizan las validaciones
            if error_message:
                error_message += " "  # Agrega espacio si hay un error
            error_message += validador.validarNombre(nombre)
            error_message += validador.validarApellido(apellido)
            error_message += validador.validarDNI(dni)
            error_message += validador.validarDomicilio(domicilio)
            error_message += validador.validarTelefono(telefono)
            error_message += validador.validarMail(email)
            
            

            if not error_message:  # Si no hay mensajes de error, procede a registrar al usuario
                bibliotecario.agregarLector(nombre, apellido, dni, domicilio, telefono, email)
                #en caso de no presentar incovenientes se agrega al lector y se crea la instancia de la clase. 
                lector = Lector(nombre, apellido, dni, domicilio, telefono, email)
                

                return redirect(url_for('verLectores'))
        except Exception as e:
            # Registro fallido, muestra un mensaje de error.
            error_message = f'El registro falló. Inténtalo de nuevo. Error: {e}'
            return render_template('lectores/agregarLector.html', error_message=error_message)
    return render_template('lectores/agregarLector.html', error_message=error_message)

#ruta vista de todos los lectores existentes con su respectiva información y las acciones a realizar. 
@app.route('/verLectores')
@verificarSesion
def verLectores():
    lectores = bibliotecario.mostrarLectores()
    return render_template('lectores/verLectores.html', lectores=lectores)

@app.route('/ActualizarLector/<lectorId>', methods=['GET', 'POST'])
#obtiene el id del lector desde la URL
@verificarSesion
def ActualizarLector(lectorId):
    lector = bibliotecario.obtenerLectorPorId(lectorId)
    if request.method == 'POST':
        #se obtienen los datos del lector a traves de un formulario html
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
#obtiene el id del lector desde la URL
@verificarSesion
def EliminarLector(lectorId):
    bibliotecario.eliminarLector(lectorId)
    return redirect(url_for('verLectores'))

@app.route('/verPrestamos')
@verificarSesion
def verPrestamos():
    #ruta a la vista de todos los prestamos que se han realizado con su respectivos datos
    prestamos = bibliotecario.mostrarPrestamos()
    
    return render_template('prestamos/verPrestamos.html', prestamos=prestamos)

#ruta al cambio de prestamo
@app.route('/cambiarEstadoPrestamo/<prestamoId>/<idLibro>', methods=['POST'])
#se obtiene el id del prestamo y el id del libro desde la URL
@verificarSesion
def cambiarEstadoPrestamo(prestamoId, idLibro):
    try:
        bibliotecario.cambiarEstadoPrestamo(prestamoId, idLibro)
        return redirect(url_for('verPrestamos'))
    except Exception as e:
        return f"Error al cambiar el estado del préstamo: {str(e)}"


#ruta a realizar prestamos donde se mostraran 2 partes, donde elige el libro a prestar y los datos del préstamo. 
@app.route('/realizarPrestamo', methods=['GET', 'POST'])
@verificarSesion
def realizarPrestamo():
    libros = libro.listarLibros()
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
                lectores = bibliotecario.mostrarLectores()
                print(lectores)
                return render_template('prestamos/registroPrestamo.html', lectores=lectores, error=error)
            else:
                prestamos = bibliotecario.mostrarPrestamos()
                return render_template('prestamos/verPrestamos.html', prestamos=prestamos)
    
    return render_template('prestamos/registroPrestamo.html', lectores=lectores, libros=libros)
    
@app.route('/buscarPrestamos', methods=['POST'])
@verificarSesion
def buscarPrestamos():
    nombreLectorLibro = request.form['nombreLectorLibro']
    #a los prestamos se los puede buscar por titulo o por nombre del lector al cual se le ha prestado el libro. 
    resultadoNombreLibro = bibliotecario.buscarPrestamosPorNombreLibro(nombreLectorLibro)
    resultadosNombreLector = bibliotecario.buscarPrestamosPorNombreLector(nombreLectorLibro)
    #Combina las dos listas eliminando duplicados
    resultadosPrestamos = resultadoNombreLibro + resultadosNombreLector
    return render_template('prestamos/verPrestamos.html', prestamos=resultadosPrestamos)

@app.route('/listarLibros')
#ruta a la primera vista del bibliotecario el cual lista los libros.
@verificarSesion
def listarLibros():
    listaLibros = libro.listarLibros()
  # Agrega esta línea para verificar la lista de libros
    return render_template('libros/vistaLibros.html', libros=listaLibros)

@app.route('/agregarLibro', methods=["GET", "POST"])
@verificarSesion
def agregarLibro():
    error_messages = []
    try:
        if request.method == 'POST':
            # Obtiene los datos de la solicitud JSON
            isbn = request.form["isbn"]
            titulo = request.form["titulo"]
            portada = request.files["portada"]
            idAutor = request.form.getlist('autor')  # Recibe una lista de IDs de autores
            idEditorial = request.form.getlist('editorial')  
            idGenero = request.form.getlist('genero') 
            cantidad = request.form["cantidad"]
            
            tituloFormateado = validador.convertirTitulo(titulo)
            
            # Valida ISBN
            isbn_error = validador.validarIsbn(isbn)
            if isbn_error:
                error_messages.append(isbn_error)

            # Valida título
            titulo_error = validador.validarNombre(titulo)
            if titulo_error:
                error_messages.append(titulo_error)

            # Comprueba si se ha seleccionado al menos una opción para Autor, Editorial y Género
            if not idAutor or not idEditorial or not idGenero:
                error_messages.append('Debes seleccionar al menos una opción para Autor, Editorial y Género.')

            if not error_messages:
                nuevoLibro = Libro()
                idLibro = nuevoLibro.agregarLibro(isbn, tituloFormateado, portada, idAutor, idEditorial, idGenero, cantidad)
                if idLibro:
                    return redirect(url_for('listarLibros'))
    except Exception as e:
        # Registro fallido, muestra un mensaje de error.
        error_messages.append(f'El registro falló. Inténtalo de nuevo. Error: {e}')
    return render_template("libros/agregarLibro.html", error_messages=error_messages)


@app.route('/obtenerLibroPorId/<string:idLibro>', methods=['GET'])
@verificarSesion
def obtenerLibroPorId(idLibro):
    if idLibro is not None:
        datosLibro = libro.obtenerLibroPorId(idLibro)

        if datosLibro is not None:
            #obtiene los IDs de autores, editoriales y géneros seleccionados en el libro
            idAutoresSeleccionados = datosLibro.get('idAutoresSeleccionados', [])
            idEditorialesSeleccionadas = datosLibro.get('idEditorialesSeleccionadas', [])
            idGenerosSeleccionados = datosLibro.get('idGenerosSeleccionados', [])
            
            #agrega los IDs
            datosLibro['idAutoresSeleccionados'] = idAutoresSeleccionados
            datosLibro['idEditorialesSeleccionadas'] = idEditorialesSeleccionadas
            datosLibro['idGenerosSeleccionados'] = idGenerosSeleccionados

            return jsonify(datosLibro)  # Devuelve los datos del libro con los IDs seleccionados como JSON
        else:
            return jsonify({'error': 'El libro no existe en la base de datos'}), 404
    else:
        return jsonify({'error': 'ID de libro no válido'}), 400


@app.route('/actualizarLibro/<idLibro>', methods=['POST'])
#se obtiene el id del Libro desde la URL
@verificarSesion
def actualizarLibro(idLibro):
    try:
        #se obtienen los datos a actualizar desde un formulario html
        isbn = request.form['isbn']
        titulo = request.form['titulo']
        cantidad = request.form['cantidad']
        
        autores = request.form.getlist('autor[]')
        editoriales = request.form.getlist('editorial[]')
        generos = request.form.getlist('genero[]')

        
        portada_file = request.files.get('portadaFile')

        if portada_file:
            print(f'Portada (FileStorage): {portada_file.filename}')
        else:
            print('No se proporcionó una nueva portada')

        #llama al método actualizarLibro con los argumentos apropiados
        libro.actualizarLibro(idLibro, isbn, titulo, portada_file, autores, editoriales, generos, cantidad)

        return jsonify({'message': 'Libro actualizado con éxito'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/eliminarLibro/<idLibro>', methods=['GET', 'POST'])
@verificarSesion
def eliminarLibro(idLibro): 
    libro= Libro()
    libro.eliminarLibro(idLibro)
    return redirect(url_for('listarLibros'))

@app.route('/listarOpciones', methods=['POST'])
@verificarSesion
def listarOpciones():
    nombreColeccion = request.json['nombreColeccion']
    tipoOpcion = request.json['tipoOpcion']  # Tipo de opción a listar (por ejemplo, "autor", "genero" o "editorial")
    filtro = request.json['filtro']  # Filtro de búsqueda (por ejemplo, "a" para autores que comienzan con "a")
    resultados = opciones.listarOpciones(nombreColeccion, tipoOpcion, filtro)
    print(resultados)
    
    return jsonify(resultados)

@app.route('/mostrarOpciones', methods=['POST'])
@verificarSesion
def mostrarOpciones():
    nombreColeccion = request.json['nombreColeccion']
    resultados = opciones.mostrarOpciones(nombreColeccion)    
    return jsonify(resultados)

@app.route('/buscarPorAutor', methods=['POST'])
@verificarSesion
def buscarPorAutor():
    data = request.get_json()
    descripcion = data['descripcion']
        
    # llama al método buscarPorAutor
    resultados = libro.buscarPorAutor(descripcion)
    
    return jsonify({"resultados": resultados})

@app.route('/buscarPorEditorial', methods=['POST'])
@verificarSesion
def buscarPorEditorial():
    data = request.get_json()
    descripcion = data['descripcion']

    # llama al método buscarPorEditorial
    resultados = libro.buscarPorEditorial(descripcion)
    
    return jsonify({"resultados": resultados})

@app.route('/buscarPorGenero', methods=['POST'])
@verificarSesion
def buscarPorGenero():
    data = request.get_json()
    descripcion = data['descripcion']
    # llama al método buscarPorGenero
    resultados = libro.buscarPorGenero(descripcion)
    
    return jsonify({"resultados": resultados})


@app.route('/buscarPorTitulo', methods=['POST'])
@verificarSesion
def buscarPorTitulo():
    data = request.get_json()
    titulo = data['titulo']
    
    # llama al método buscarPorTitulo en la instancia de Libro
    resultados = libro.buscarPorTitulo(titulo)
    
    return jsonify({"resultados": resultados})

#ruta encargada de gestionar la busqueda de lectores por nombre o DNI
@app.route('/buscarLectores', methods=['POST'])
@verificarSesion
def buscarLectores():
    #se hace un request para obtener el valor que se desea buscar
    nombreLectorDni = request.form['buscarNombreLectorDni']
    #se recuperan las busquedas a través de métodos de bibliotecario
    resultadoLectorNombre = bibliotecario.buscarLectoresPorNombre(nombreLectorDni)
    resultadosLectorDni = bibliotecario.buscarLectoresPorDni(nombreLectorDni)
    resultadosLectorApellido = bibliotecario.buscarLectoresPorApellido(nombreLectorDni)
    #se combinan las dos listas retornadas
    resultadosLectores = resultadoLectorNombre + resultadosLectorDni + resultadosLectorApellido
    #se renderiza la vista con los resultados
    return render_template('lectores/verLectores.html', lectores=resultadosLectores)

