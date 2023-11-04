// Configura la información de Firebase
const firebaseConfig = {
  apiKey: "AIzaSyA6v-toj9qDZnDf6agwprWam2uc8JFElVw",
  authDomain: "biblioteca-1d610.firebaseapp.com",
  projectId: "biblioteca-1d610",
};

// Inicializa Firebase con la configuración
firebase.initializeApp(firebaseConfig);

// Esta función manejará el registro con Google
function registroConGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  firebase.auth()
    .signInWithPopup(provider)
    .then((result) => {
      // El usuario ha sido registrado con éxito
      console.log(result.user);
    })
    .catch((error) => {
      // Ha ocurrido un error durante el registro
      console.error(error);
    });
}

