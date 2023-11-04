from firebase_admin import auth
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Registro:
    def __init__(self):
        self.apikey = 'AIzaSyA6v-toj9qDZnDf6agwprWam2uc8JFElVw'
        pass

    def __verificarEmail(self, user):
        try:
            linkVerificacion = auth.generate_email_verification_link(user.email)
            smtpServer = "smtp.gmail.com"
            smtpUsername = "bibliotecapizarnik@gmail.com"
            smtpPassword = "arei bpwi hsxq njex"

            msg = MIMEMultipart()
            msg['From'] = smtpUsername
            msg['To'] = user.email
            msg['Subject'] = 'Verificación de correo electrónico de BIBLIOTECA PIZARNIK'

            # Agrega una parte de texto al mensaje
            text = f'Por favor, haz clic en el siguiente enlace para verificar tu correo: {linkVerificacion}'
            msg.attach(MIMEText(text, 'plain'))

            # Configura el servidor SMTP y envía el mensaje
            server = smtplib.SMTP(smtpServer, 587)
            server.starttls()
            server.login(smtpUsername, smtpPassword)
            server.sendmail(smtpUsername, user.email, msg.as_string())
            server.quit()
            return ("Correo de verificación enviado con éxito.")
        except Exception as e:
            return ("Error al enviar el correo:", e)
    
    def getVerificarEmail(self, email):
        return self.__verificarEmail(email)
    
    def registrarUsuario(self, email, password):
        try:
            user = auth.create_user(
                email=email,
                password=password,
                email_verified=False  # Asegúrate de que el correo no esté verificado al crear el usuario.
            )

            resultadoVerificacion = self.getVerificarEmail(user)

            return resultadoVerificacion
        except Exception as e:
            print(f"Error al enviar correo de verificación: {e}")
        return user

    
