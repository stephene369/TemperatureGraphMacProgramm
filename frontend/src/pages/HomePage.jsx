import React, { useEffect, useState } from 'react';
import { ApiService } from '../services/ApiService';
import TestNotifications from '../components/TestNotifications';

const HomePage = ({ navigateTo }) => {
  const [stats, setStats] = useState({
    capteurs: 0,
    graphiques: 0,
    fichiers: 0
  });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await ApiService.getCapteurs();
      if (response.success) {
        setStats(prev => ({
          ...prev,
          capteurs: response.capteurs.length,
          fichiers: response.capteurs.filter(c => c.file_path).length
        }));
      }
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const quickActions = [
    {
      title: 'Ajouter un capteur',
      description: 'Créez un nouveau capteur pour vos données',
      icon: 'bx-plus-circle',
      color: 'blue',
      action: () => navigateTo?.('capteurs')
    },
    {
      title: 'Importer des données',
      description: 'Associez des fichiers à vos capteurs',
      icon: 'bx-upload',
      color: 'green',
      action: () => navigateTo?.('capteurs')
    },
    {
      title: 'Générer un graphique',
      description: 'Créez des visualisations de vos données',
      icon: 'bx-bar-chart-alt-2',
      color: 'purple',
      action: () => navigateTo?.('graphs')
    },
    {
      title: 'Voir l\'historique',
      description: 'Consultez les opérations récentes',
      icon: 'bx-history',
      color: 'orange',
      action: () => navigateTo?.('history')
    }
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-8 text-white">
        <h2 className="text-2xl font-bold mb-2">Bienvenue dans ISCGraph</h2>
        <p className="text-blue-100 text-sm">
          Votre outil d'analyse de données climatiques et de température
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-full">
              <i className="bx bxs-chip text-2xl text-blue-600 dark:text-blue-400"></i>
            </div>
            <div className="ml-4">
              <h3 className="text-2xl font-bold">{stats.capteurs}</h3>
              <p className="text-gray-500 dark:text-gray-400">Capteurs</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 bg-green-100 dark:bg-green-900 rounded-full">
              <i className="bx bxs-file text-2xl text-green-600 dark:text-green-400"></i>
            </div>
            <div className="ml-4">
              <h3 className="text-2xl font-bold">{stats.fichiers}</h3>
              <p className="text-gray-500 dark:text-gray-400">Fichiers liés</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-6">Actions rapides</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {quickActions.map((action, index) => (
            <div
              key={index}
              className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
              onClick={action.action}
            >
              <div className="flex items-start">
                <div className={`p-2 bg-${action.color}-100 dark:bg-${action.color}-900 rounded-lg`}>
                  <i className={`bx ${action.icon} text-xl text-${action.color}-600 dark:text-${action.color}-400`}></i>
                </div>
                <div className="ml-3">
                  <h4 className="font-semibold text-gray-900 dark:text-gray-100">
                    {action.title}
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {action.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Getting Started */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-4">Pour commencer</h3>
        <div className="space-y-4">
          {[
            {
              step: 1,
              title: 'Ajoutez vos capteurs',
              desc: 'Créez des capteurs pour organiser vos données de température et d\'humidité'
            },
            {
              step: 2,
              title: 'Associez vos fichiers',
              desc: 'Importez vos fichiers Excel (.xlsx, .xls), CSV contenant les données'
            },
            {
              step: 3,
              title: 'Configurez le mappage',
              desc: 'Définissez quelles colonnes correspondent aux dates, températures et autres données'
            },
            {
              step: 4,
              title: 'Générez vos graphiques',
              desc: 'Créez des visualisations personnalisées de vos données climatiques'
            }
          ].map(item => (
            <div className="flex items-start" key={item.step}>
              <span className="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-sm font-semibold">
                {item.step}
              </span>
              <div className="ml-3">
                <h4 className="font-semibold">{item.title}</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Test des notifications */}
      {/* <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-4">Test des notifications</h3>
        <TestNotifications />
      </div> */}
    </div>
  );
};

export default HomePage;
