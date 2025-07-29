import { useState, useCallback } from 'react';

let loadingInstance = null;

export const useLoading = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');

  // Store the loading instance globally
  if (!loadingInstance) {
    loadingInstance = {
      isLoading,
      setIsLoading,
      loadingMessage,
      setLoadingMessage
    };
  } else {
    loadingInstance.setIsLoading = setIsLoading;
    loadingInstance.setLoadingMessage = setLoadingMessage;
    loadingInstance.isLoading = isLoading;
    loadingInstance.loadingMessage = loadingMessage;
  }

  const showLoading = useCallback((message = 'Chargement...') => {
    setLoadingMessage(message);
    setIsLoading(true);
  }, []);

  const hideLoading = useCallback(() => {
    setIsLoading(false);
    setLoadingMessage('');
  }, []);

  return {
    isLoading,
    loadingMessage,
    showLoading,
    hideLoading
  };
};

// Global loading functions for compatibility with original code
export const showLoading = (message = 'Chargement...') => {
  if (loadingInstance) {
    loadingInstance.setLoadingMessage(message);
    loadingInstance.setIsLoading(true);
  }
};

export const hideLoading = () => {
  if (loadingInstance) {
    loadingInstance.setIsLoading(false);
    loadingInstance.setLoadingMessage('');
  }
};
