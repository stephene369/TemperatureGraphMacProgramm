import { useState, useCallback } from 'react';

let notificationInstance = null;

export const useNotification = () => {
  const [notifications, setNotifications] = useState([]);

  // Store the notification instance globally
  if (!notificationInstance) {
    notificationInstance = {
      notifications,
      setNotifications
    };
  } else {
    notificationInstance.setNotifications = setNotifications;
    notificationInstance.notifications = notifications;
  }

  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  const showNotification = useCallback((message, type = 'info', duration = 5000) => {
    const id = Date.now() + Math.random();
    const notification = {
      id,
      message,
      type,
      timestamp: Date.now()
    };

    setNotifications(prev => [...prev, notification]);

    // Auto-remove notification after duration
    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, duration);
    }

    return id;
  }, [removeNotification]);

  const clearAllNotifications = useCallback(() => {
    setNotifications([]);
  }, []);

  return {
    notifications,
    showNotification,
    removeNotification,
    clearAllNotifications
  };
};

// Global notification functions for compatibility with original code
export const showNotification = (message, type = 'info', duration = 5000) => {
  if (notificationInstance && notificationInstance.setNotifications) {
    const id = Date.now() + Math.random();
    const notification = {
      id,
      message,
      type,
      timestamp: Date.now()
    };

    notificationInstance.setNotifications(prev => [...prev, notification]);

    if (duration > 0) {
      setTimeout(() => {
        notificationInstance.setNotifications(prev => prev.filter(n => n.id !== id));
      }, duration);
    }

    return id;
  }
};
