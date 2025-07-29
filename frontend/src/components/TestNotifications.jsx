import React from 'react';
import { showNotification } from '../hooks/useNotification';

const TestNotifications = () => {
  const testNotifications = () => {
    showNotification('Ceci est un test de notification de succès', 'success');
    
    setTimeout(() => {
      showNotification('Ceci est un test de notification d\'erreur avec un message plus long pour voir le comportement', 'error');
    }, 1000);
    
    setTimeout(() => {
      showNotification('Notification d\'avertissement', 'warning');
    }, 2000);
    
    setTimeout(() => {
      showNotification('Information importante', 'info');
    }, 3000);
  };

  return (
    <div className="p-4">
      <button 
        onClick={testNotifications}
        className="btn-primary"
      >
        <i className="bx bx-bell mr-2"></i>
        Tester les notifications
      </button>
    </div>
  );
};

export default TestNotifications;
