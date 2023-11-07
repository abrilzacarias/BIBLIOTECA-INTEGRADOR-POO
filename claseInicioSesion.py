#se importa los módulos necesarios
import requests
from firebase_admin import auth
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#la clase de inicio sesion es utilizada para llevar a cabo todas las acciones que estés relacionadas con la misma.
class InicioSesion():
    def __init__(self):
        pass

    #Verifica que el usuario haya verificado su mail al momento de registrarse, en caso de no haberlo hecho, no permite
    #el inicio de sesión
    def verificarConfirmacionMail(self, userEmail):
        user = auth.get_user_by_email(userEmail)
        if user.email_verified:
            return True
        else:
            return False

    #Verifica las credenciales ingresadas por el usuario 
    def verificarInicioSesion(self, email, password):
        #Datos para autenticar mediante la REST API de Firebase
        data = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        #Realiza una solicitud POST a la API de autenticación de Firebase
        response = requests.post(
            'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyA6v-toj9qDZnDf6agwprWam2uc8JFElVw',
            json=data
        )
        print(response)
        return response
    
    #En caso de haber olvidado la contraseña, el usuario puede recuperar su cuenta con el reseteo de la misma. 
    #El usuario recibe un mail de parte de la biblioteca con un link donde puede reestablecer su contraseña.
    def resetPass(self, email, user):
        try: 
            #SMTP (Simple Mail Transfer Protocol) es un protocolo de red utilizado para enviar correos electrónicos a través de Internet.
            linkReset = auth.generate_password_reset_link(email)
            smtpServer = "smtp.gmail.com"
            smtpUsername = "bibliotecapizarnik@gmail.com"
            smtpPassword = "arei bpwi hsxq njex"

            msg = MIMEMultipart()
            msg['From'] = smtpUsername
            msg['To'] = user.email
            msg['Subject'] = 'Reestablece tu Contraseña'

            text = f'Por favor, haz clic en el siguiente enlace para reestablecer tu Contraseña: {linkReset}'
            msg.attach(MIMEText(text, 'plain'))

            # Configura el servidor SMTP y envía el mensaje
            server = smtplib.SMTP(smtpServer, 587)
            server.starttls()
            server.login(smtpUsername, smtpPassword)
            server.sendmail(smtpUsername, user.email, msg.as_string())
            server.quit()
            return ("Correo de recuperacion enviado con éxito.")
        except Exception as e:
            return ("Error al enviar el correo:", e)
        