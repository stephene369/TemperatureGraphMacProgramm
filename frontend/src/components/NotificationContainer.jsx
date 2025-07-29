import React from 'react';
import { useNotification } from '../hooks/useNotification';

const NotificationContainer = () => {
  const { notifications, removeNotification } = useNotification();

  const getNotificationStyles = (type) => {
    const baseStyles = "w-full bg-white dark:bg-gray-800 shadow-xl rounded-lg pointer-events-auto ring-1 ring-gray-200 dark:ring-gray-700 overflow-hidden border";
    
    switch (type) {
      case 'success':
        return `${baseStyles} border-l-4 border-green-500 border-green-100 dark:border-green-900`;
      case 'error':
        return `${baseStyles} border-l-4 border-red-500 border-red-100 dark:border-red-900`;
      case 'warning':
        return `${baseStyles} border-l-4 border-yellow-500 border-yellow-100 dark:border-yellow-900`;
      case 'info':
      default:
        return `${baseStyles} border-l-4 border-blue-500 border-blue-100 dark:border-blue-900`;
    }
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success':
        return <i className="bx bx-check-circle text-green-500 text-xl"></i>;
      case 'error':
        return <i className="bx bx-error-circle text-red-500 text-xl"></i>;
      case 'warning':
        return <i className="bx bx-error-circle text-yellow-500 text-xl"></i>;
      case 'info':
      default:
        return <i className="bx bx-info-circle text-blue-500 text-xl"></i>;
    }
  };

  if (notifications.length === 0) return null;

  return (
    <div className="notification-container">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`notification-item ${getNotificationStyles(notification.type)}`}
        >
          <div className="p-4">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                {getNotificationIcon(notification.type)}
              </div>
              <div className="ml-3 flex-1 pt-0.5">
                <p className="text-sm font-medium text-gray-900 dark:text-gray-100 break-words">
                  {notification.message}
                </p>
              </div>
              <div className="ml-4 flex-shrink-0 flex">
                <button
                  className="bg-white dark:bg-gray-800 rounded-md inline-flex text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 p-1"
                  onClick={() => removeNotification(notification.id)}
                >
                  <span className="sr-only">Close</span>
                  <i className="bx bx-x text-lg"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default NotificationContainer;
