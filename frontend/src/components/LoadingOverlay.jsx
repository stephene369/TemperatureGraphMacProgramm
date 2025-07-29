import React from 'react';
import { useLoading } from '../hooks/useLoading';

const LoadingOverlay = () => {
  const { isLoading, loadingMessage } = useLoading();

  if (!isLoading) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-xl">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <span className="text-gray-900 dark:text-gray-100 font-medium">
            {loadingMessage}
          </span>
        </div>
      </div>
    </div>
  );
};

export default LoadingOverlay;
