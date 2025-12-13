import React from 'react';

const Header = ({ pageTitle, currentPage, isDarkMode, toggleTheme, toggleMobileMenu }) => {
  const getHeaderActions = () => {
    switch (currentPage) {
      case 'graphs':
        return (
          <button className="btn-primary">
            <i className="bx bx-download"></i>
            Télécharger tout
          </button>
        );
      case 'history':
        return (
          <button className="btn-secondary">
            <i className="bx bx-export"></i>
            Exporter l'historique
          </button>
        );
      case 'capteurs':
        return (
          <button className="btn-primary">
            <i className="bx bx-plus"></i>
            Ajouter un capteur
          </button>
        );
      default:
        return null;
    }
  };

  return (
    <header className="bg-white dark:bg-gray-800 shadow-md border-b border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between p-4">
        {/* Left side */}
        <div className="flex items-center gap-4">
          {/* Mobile menu button */}
          <button
            id="mobile-menu-btn"
            className="md:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            onClick={toggleMobileMenu}
          >
            <i className="bx bx-menu text-xl"></i>
          </button>
          
          {/* Page title */}
          <h1 id="page-title" className="text-2xl font-bold">
            {pageTitle}
          </h1>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-4">

          {/* Theme toggle */}
          <button
            id="theme-toggle"
            className="btn-icon text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            onClick={toggleTheme}
            title={isDarkMode ? 'Mode clair' : 'Mode sombre'}
          >
            <i className={`bx ${isDarkMode ? 'bx-sun' : 'bx-moon'} text-xl`}></i>
          </button>

        </div>
      </div>
    </header>
  );
};

export default Header;
