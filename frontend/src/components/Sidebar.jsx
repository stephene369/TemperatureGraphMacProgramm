import React from 'react';

const Sidebar = ({ currentPage, navigateTo, isMobileMenuOpen, toggleMobileMenu }) => {
  const menuItems = [
    { id: 'home', label: 'Accueil', icon: 'bxs-home' },
    { id: 'capteurs', label: 'Capteurs & Fichiers', icon: 'bxs-folder' },
    { id: 'mapping', label: 'Mappage des Colonnes', icon: 'bxs-grid-alt' },
    { id: 'graphs', label: 'Graphiques', icon: 'bxs-bar-chart-alt-2' },
    { id: 'history', label: 'Historique', icon: 'bxs-time' },
    { id: 'documentation', label: 'Documentation', icon: 'bxs-book' }
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={toggleMobileMenu}
        />
      )}
      
      {/* Sidebar */}
      <div 
        id="sidebar" 
        className={`w-64 bg-white dark:bg-gray-800 shadow-md fixed md:relative z-50 h-full transform transition-transform duration-300 ${
          isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        {/* Header */}
        <div className="px-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold">ISCGraph</h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Analyse de données climatiques
              </p>
            </div>
            {/* Mobile close button */}
            <button 
              className="md:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              onClick={toggleMobileMenu}
            >
              <i className="bx bx-x text-xl"></i>
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-4">
          {menuItems.map((item) => (
            <a
              key={item.id}
              href="#"
              className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
              onClick={(e) => {
                e.preventDefault();
                navigateTo(item.id);
              }}
            >
              <i className={`bx ${item.icon} nav-item-icon`}></i>
              {item.label}
            </a>
          ))}
        </nav>

        {/* Footer */}
        <div className="absolute bottom-4 left-4 right-4">
          <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
            <p>ISCGraph v2.0</p>
            <p>© 2025 - ISC-Graph</p>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
