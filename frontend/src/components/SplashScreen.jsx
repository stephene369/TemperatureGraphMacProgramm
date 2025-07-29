import React from 'react';

const SplashScreen = () => {
  return (
    <div id="splash-screen" className="flex flex-col items-center justify-center">
      <img 
        src="/assets/img/logo.png"
        alt="ISC Graph Logo" 
        className="logo-animation"
        onError={(e) => {
          // Fallback si l'image n'est pas trouvée
          e.target.style.display = 'none';
          e.target.nextSibling.style.display = 'block';
        }}
      />
      <div style={{ display: 'none' }} className="text-4xl font-bold text-blue-600">
        ISCGraph
      </div>
    </div>
  );
};

export default SplashScreen;
