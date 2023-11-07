// Configura la información de Firebase
const firebaseConfig = {
    apiKey: "AIzaSyA6v-toj9qDZnDf6agwprWam2uc8JFElVw",
    authDomain: "biblioteca-1d610.firebaseapp.com",
    projectId: "biblioteca-1d610",
  };
  
  // Inicializa Firebase con la configuración
  firebase.initializeApp(firebaseConfig);

  function iniciarSesionConGoogle() {
    var provider = new firebase.auth.GoogleAuthProvider();
    
    firebase.auth().signInWithPopup(provider)
      .then(function(result) {
        // Autenticación exitosa, el usuario ha iniciado sesión con Google
        var user = result.user;
        console.log('Usuario autenticado con Google:', user);
        
        // Redirige a la página de inicio, o realiza cualquier otra acción que desees.
        window.location.href = '/listarLibros';  // Cambia '/listarLibros' según la URL de tu vista de listarLibros
      })
      .catch(function(error) {
        // Autenticación fallida, muestra un mensaje de error.
        console.error('Error al iniciar sesión con Google:', error);
      });
  }
  

  document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("password");
    const togglePasswordButton = document.getElementById("togglePassword");

  togglePasswordButton.addEventListener("click", function () {
      if (passwordInput.type === "password") {
          passwordInput.type = "text";  // Cambiar el tipo de campo a texto
          togglePasswordButton.innerHTML = '<i class="fas fa-eye-slash"></i>';
      } else {
          passwordInput.type = "password";  // Cambiar el tipo de campo a contraseña
          togglePasswordButton.innerHTML = '<i class="fas fa-eye"></i>';
      }
  });
});


