#Se importan los modulos necesarios
import re
import datetime

# Clase que contiene métodos para realizar validaciones en el sistema bibliotecario, como validar datos de bibliotecarios/clientes 
# o fechas de devolución de prestamos
class Validaciones:
    def __init__(self):
        # Define caracteres permitidos en una dirección.
        self.__caracteresDireccion = "áéíóúabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789. "
        # Define caracteres para validar direcciones de correo electrónico.
        self.__caracteresEmail = r'^[\w\.-]+@[\w\.-]+\.\w+'

    # Métodos para obtener los caracteres permitidos en una dirección y la expresión regular para un correo electrónico.
    #ABSTRACCION Y ENCAPSULAMIENTO
    def getCaracteresDireccion(self):
        return self.__caracteresDireccion
    
    def getCaracteresEmail(self):
        return self.__caracteresEmail
    
    # Valida un número de DNI, debe tener 8 o menos caracteres y ser numérico.
    def validarDNI(self, dni):
        #Valida el número de DNI, debe tener 8 o menos caracteres y DEBEN SER NUMÉRICOS.
        if not re.match(r'^\d{1,8}$', str(dni)):
            return "El DNI ingresado es incorrecto. El DNI debe tener 8 o menos caracteres numéricos. "
        return ''
    
    # Valida el nombre pasado como parametro, no debe contener números y debe tener al menos 2 letras.
    def validarNombre(self, nombre):
        #Valida el campo del nombre, NO DEBE TENER NUMEROS y debe tener DOS LETRAS O MÁS.
        if any(caracter.isdigit() for caracter in nombre):
            return "El nombre no puede tener números."
        if len(nombre) < 2:
            return "El nombre debe tener 2 letras o más."
        return ''
                
    def validarApellido(self, apellido):
        #Valida el campo del apellido con los mismo requisitos que el nombre.
        if any(caracter.isdigit() for caracter in apellido):
            return "El apellido no puede tener números."
        if len(apellido) < 2:
            return "El apellido debe tener 2 letras o más."   
        return ''

    def validarDomicilio(self, domicilio):
        #Valida el campo del domicilio ingresadp permitiendo solo ciertos caracteres, especificados en 'caracteresDireccion'
        for caracter in domicilio:
            if caracter not in self.getCaracteresDireccion():
                return "El domicilio posee caracteres inválidos. Intente nuevamente. "
        return ''  

    def validarTelefono(self, telefono):
        #Valida el número de teléfono pasado como parametro, valida que tenga como máximo 10 caracteres.
        if len(str(telefono)) > 10:
            return "El número ingresado es incorrecto. Debe tener 10 caracteres o menos. "
        return ''
                
    def validarMail(self, email):
        #Valida la dirección de correo electrónico ingresada, permitiendo solo ciertos caracteres, especificados en 'caracteresEmail'.
        if re.match(self.getCaracteresEmail(), email):
            return ''
        else: 
            return "El email no es válido. "
        
    def validarContrasena(self, contrasena):
    # Requisitos: al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial
        if len(contrasena) < 8:
            return "La contraseña debe tener al menos 8 caracteres. "
        
        if not re.search(r'[A-Z]', contrasena):
            return "La contraseña debe contener al menos una letra mayúscula. "
        
        if not re.search(r'[a-z]', contrasena):
            return "La contraseña debe contener al menos una letra minúscula. "
        
        if not re.search(r'\d', contrasena):
            return "La contraseña debe contener al menos un número. "
        
        if not re.search(r'[!@#$%^&*]', contrasena):
            return "La contraseña debe contener al menos un carácter especial: !@#$%^&*. "
        
        return ''  # La contraseña es válida
    
    # Valida la fecha de devolución de un préstamo, asegurando que sea una fecha futura.
    #Se utiliza el modulo datetime
    def validarFechaDevolucionPrestamo(self, fechaDevolucionPrestamo):
        fechaDevolucion = datetime.datetime.strptime(fechaDevolucionPrestamo, '%Y-%m-%d').date()
        fechaActual = datetime.date.today()
        if fechaDevolucion < fechaActual:  
            return False
        else:
            return True
    
    # Obtiene la fecha actual en formato de cadena (YYYY-MM-DD).
    def obtenerFechaActualStr(self):
        fechaActual = datetime.date.today().strftime('%Y-%m-%d')
        return fechaActual
    
    # Obtiene la fecha actual como un objeto de fecha.
    def obtenerFechaActual(self):
        fechaActual = datetime.date.today()
        return fechaActual
    
    # Verifica el estado de devolución de un libro en función de la fecha de devolución.
    def verificarEstadoDevolucion(self, fechaDevolucionPrestamo):
        # Obtener la fecha actual
        fechaActual = self.obtenerFechaActual()
        fechaDevolucion = self.convertirFechaAFormatoFecha(fechaDevolucionPrestamo)

        # Comparar la fecha actual con la fecha de devolución
        if fechaActual > fechaDevolucion:
            return "LIBRO NO DEVUELTO"
        else:
            return True
        
    # Convierte una fecha en formato de cadena a un objeto de fecha.
    def convertirFechaAFormatoFecha(self, fecha):
        fechaDevolucion = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        return fechaDevolucion
    
    # Valida un ISBN, asegurando que tenga 13 dígitos después de eliminar espacios en blanco o guiones.
    def validarIsbn(self, isbn):
        # Elimina cualquier espacio en blanco o guiones del ISBN
        isbn = isbn.replace(" ", "").replace("-", "")

        # Comprueba si el ISBN tiene 13 dígitos
        if not isbn.isdigit() or len(isbn) != 13:
            return "El ISBN debe tener exactamente 13 dígitos."

        return ''  # ISBN válido
    
    # Convierte un título a formato capitalizado (con las palabras iniciales en mayúsculas).
    def convertirTitulo(self,titulo):
        palabras = titulo.split()
        palabras_capitalizadas = [palabra.capitalize() for palabra in palabras]
        return " ".join(palabras_capitalizadas)