import firebase_admin
from flask import Flask
from firebase_admin import credentials, firestore, storage
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'mysecretkey'

# Carga del certificado del proyecto
cred = credentials.Certificate("credentials\credBiblioteca.json")

# Inicializa la aplicación Firebase con las credenciales
firebase_app = firebase_admin.initialize_app(cred, {'storageBucket': 'biblioteca-1d610.appspot.com'})
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials\credBiblioteca.json"
# Inicializa el cliente de Firestore
db = firestore.client()

# Inicializa el bucket de almacenamiento
bucket = storage.bucket(app=firebase_app)