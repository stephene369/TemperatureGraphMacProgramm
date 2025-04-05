// Animations Lottie pour le splash screen
try {
  document.addEventListener("DOMContentLoaded", function() {
    try {
      const lottieAnimations = [

        "lotties/onMASlImNg.lottie"
        // "https://lottie.host/feae722c-0a85-4fbb-acdb-debe06e26ef9/8vr4dMpNX1.lottie",
        // "https://lottie.host/18a34c71-0d92-4e05-ae83-e9281702aa6d/ne6UxpW4xy.lottie",
      //   "https://lottie.host/e6972592-361b-4e15-8ede-5e9bf3c062e3/MOKWNpsqcr.lottie"
      ];
      
      const randomAnimation = lottieAnimations[Math.floor(Math.random() * lottieAnimations.length)];
      
      const lottieContainer = document.getElementById('lottie-container');
      const lottiePlayer = document.createElement('dotlottie-player');
      
      lottiePlayer.setAttribute('src', randomAnimation);
      lottiePlayer.setAttribute('background', 'transparent');
      lottiePlayer.setAttribute('speed', '1');
      lottiePlayer.setAttribute('style', 'width: 250px; height: 250px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);');
      lottiePlayer.setAttribute('loop', '');
      lottiePlayer.setAttribute('autoplay', '');
      
      lottieContainer.appendChild(lottiePlayer);      
      setTimeout(function() {
        try {
          const splashScreen = document.getElementById('splash-screen');
          splashScreen.classList.add('hidden');
            
        } catch (error) {
          console.error("Erreur lors de la gestion du splash screen:", error);
        }
      }, 2500);
    } catch (error) {
      console.error("Erreur lors de l'initialisation de l'animation:", error);
    }
  });
} catch (error) {
  console.error("Erreur lors de l'ajout de l'écouteur DOMContentLoaded:", error);
}