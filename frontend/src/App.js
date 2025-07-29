import React, { useState, useEffect } from 'react';
import './App.css';
import 'boxicons/css/boxicons.min.css';
import 'aos/dist/aos.css';
import AOS from 'aos';

// Components
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import SplashScreen from './components/SplashScreen';
import NotificationContainer from './components/NotificationContainer';
import LoadingOverlay from './components/LoadingOverlay';

// Pages
import HomePage from './pages/HomePage';
import CapteursPage from './pages/CapteursPage';
import MappingPage from './pages/MappingPage';
import GraphsPage from './pages/GraphsPage';
import StatisticsPage from './pages/StatisticsPage';
import HistoryPage from './pages/HistoryPage';
import DocumentationPage from './pages/DocumentationPage';

// Services
import { ApiService } from './services/ApiService';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [showSplash, setShowSplash] = useState(true);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Initialize AOS
    AOS.init({
      duration: 300,
      easing: 'ease-in-out',
      once: true
    });

    // Initialize API Service
    ApiService.init();

    // Hide splash screen after 3 seconds
    const timer = setTimeout(() => {
      setShowSplash(false);
    }, 3000);

    // Check system theme preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setIsDarkMode(prefersDark);

    return () => clearTimeout(timer);
  }, []);

  const navigateTo = (page) => {
    setCurrentPage(page);
    setIsMobileMenuOpen(false);
  };

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const getPageTitle = (page) => {
    const titles = {
      home: 'Accueil',
      capteurs: 'Capteurs & Fichiers',
      mapping: 'Mappage des Colonnes',
      graphs: 'Graphiques',
      statistics: 'Analyse Statistique',
      history: 'Historique',
      documentation: 'Documentation'
    };
    return titles[page] || 'ISCGraph';
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage />;
      case 'capteurs':
        return <CapteursPage />;
      case 'mapping':
        return <MappingPage />;
      case 'graphs':
        return <GraphsPage />;
      case 'statistics':
        return <StatisticsPage />;
      case 'history':
        return <HistoryPage />;
      case 'documentation':
        return <DocumentationPage />;
      default:
        return <HomePage />;
    }
  };

  if (showSplash) {
    return <SplashScreen />;
  }

  return (
    <div className={`${isDarkMode ? 'dark' : ''}`}>
      <div className="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
        <div className="flex h-screen">
          {/* Sidebar */}
          <Sidebar 
            currentPage={currentPage}
            navigateTo={navigateTo}
            isMobileMenuOpen={isMobileMenuOpen}
            toggleMobileMenu={toggleMobileMenu}
          />

          {/* Main Content */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Header */}
            <Header 
              pageTitle={getPageTitle(currentPage)}
              currentPage={currentPage}
              isDarkMode={isDarkMode}
              toggleTheme={toggleTheme}
              toggleMobileMenu={toggleMobileMenu}
            />

            {/* Content */}
            <main className="flex-1 overflow-y-auto p-6">
              <div className="page active">
                {renderCurrentPage()}
              </div>
            </main>
          </div>
        </div>
        
        {/* Global components */}
        <NotificationContainer />
        <LoadingOverlay />
      </div>
    </div>
  );
}

export default App;
