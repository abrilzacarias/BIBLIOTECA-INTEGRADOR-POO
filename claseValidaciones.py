import re
import datetime

class Validaciones:
    def __init__(self):
        self.__caracteresDireccion = "áéíóúabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789. "
        self.__caracteresEmail = r'^[\w\.-]+@[\w\.-]+\.\w+'

    def getCaracteresDireccion(self):
        return self.__caracteresDireccion
    
    def getCaracteresEmail(self):
        return self.__caracteresEmail
        
    def validarDNI(self, dni):
        #Valida el número de DNI, debe tener 8 o menos caracteres y DEBEN SER NUMÉRICOS.
        if not re.match(r'^\d{1,8}$', str(dni)):
            return "El DNI ingresado es incorrecto. El DNI debe tener 8 o menos caracteres numéricos. "
        return ''
    
    def validarNombre(self, nombre):
        #Valida el campo del nombre del cliente, NO DEBE TENER NUMEROS y debe tener DOS LETRAS O MÁS.
        if any(caracter.isdigit() for caracter in nombre):
            return "El nombre no puede tener números."
        if len(nombre) < 2:
            return "El nombre debe tener 2 letras o más."
        return ''
                
    def validarApellido(self, apellido):
        #Valida el campo del apellido del cliente con los mismo requisitos que el nombre.
        if any(caracter.isdigit() for caracter in apellido):
            return "El apellido no puede tener números."
        if len(apellido) < 2:
            return "El apellido debe tener 2 letras o más."   
        return ''

    def validarDomicilio(self, domicilio):
        #Valida el campo del domicilio del cliente permitiendo solo ciertos caracteres, especificados en 'caracteresDireccion'
        for caracter in domicilio:
            if caracter not in self.getCaracteresDireccion():
                return "El domicilio posee caracteres inválidos. Intente nuevamente. "
        return ''  

    def validarTelefono(self, telefono):
        #Valida el número de teléfono del cliente, valida que tenga como máximo 10 caracteres.
        if len(str(telefono)) > 10:
            return "El número ingresado es incorrecto. Debe tener 10 caracteres o menos. "
        return ''
                
    def validarMail(self, email):
        #Valida la dirección de correo electrónico del cliente, permitiendo solo ciertos caracteres, especificados en 'caracteresEmail'.
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
    
    def validarFechaDevolucionPrestamo(self, fechaDevolucionPrestamo):
        fechaDevolucion = datetime.datetime.strptime(fechaDevolucionPrestamo, '%Y-%m-%d').date()
        fechaActual = datetime.date.today()
        if fechaDevolucion < fechaActual:  
            return False
        else:
            return True
    
    def obtenerFechaActualStr(self):
        fechaActual = datetime.date.today().strftime('%Y-%m-%d')
        return fechaActual
    
    def obtenerFechaActual(self):
        fechaActual = datetime.date.today()
        return fechaActual
    
    def verificarEstadoDevolucion(self, fechaDevolucionPrestamo):
        # Obtener la fecha actual
        fechaActual = self.obtenerFechaActual()
        fechaDevolucion = self.convertirFechaAFormatoFecha(fechaDevolucionPrestamo)

        # Comparar la fecha actual con la fecha de devolución
        if fechaActual > fechaDevolucion:
            return "LIBRO NO DEVUELTO"
        else:
            return True
        
    def convertirFechaAFormatoFecha(self, fecha):
        fechaDevolucion = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        return fechaDevolucion

