import React, { useState, useEffect } from 'react';
import { ApiService } from '../services/ApiService';
import { showNotification } from '../hooks/useNotification';
import { showLoading, hideLoading } from '../hooks/useLoading';

const StatisticsPageMultiple = () => {
  const [capteurs, setCapteurs] = useState([]);
  const [selectedCapteurs, setSelectedCapteurs] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [statistics, setStatistics] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    loadAvailableCapteurs();
  }, []);

  const loadAvailableCapteurs = async () => {
    try {
      showLoading('Chargement des capteurs...');
      const response = await ApiService.getAvailableCapteursForStatistics();
      
      if (response.success) {
        setCapteurs(response.capteurs);
      } else {
        showNotification(response.message || 'Erreur lors du chargement des capteurs', 'error');
      }
    } catch (error) {
      showNotification('Erreur de communication avec l\'API', 'error');
      console.error('Error loading capteurs:', error);
    } finally {
      hideLoading();
    }
  };

  const handleCapteurChange = (capteurId) => {
    setSelectedCapteurs(prev => {
      if (prev.includes(capteurId)) {
        return prev.filter(id => id !== capteurId);
      } else {
        return [...prev, capteurId];
      }
    });
  };

  const selectAllCapteurs = () => {
    if (selectedCapteurs.length === capteurs.length) {
      setSelectedCapteurs([]);
    } else {
      setSelectedCapteurs(capteurs.map(c => c.id));
    }
  };

  const analyzeStatistics = async () => {
    if (selectedCapteurs.length === 0) {
      showNotification('Veuillez sélectionner au moins un capteur', 'warning');
      return;
    }

    setIsAnalyzing(true);
    try {
      showLoading('Analyse des données en cours...');
      const response = await ApiService.getDataStatistics(selectedCapteurs, startDate || null, endDate || null);
      
      if (response.success) {
        setStatistics(response);
        showNotification('Analyse terminée avec succès', 'success');
      } else {
        showNotification(response.message || 'Erreur lors de l\'analyse', 'error');
        setStatistics(null);
      }
    } catch (error) {
      showNotification('Erreur lors de l\'analyse des données', 'error');
      console.error('Error analyzing statistics:', error);
      setStatistics(null);
    } finally {
      setIsAnalyzing(false);
      hideLoading();
    }
  };

  const exportToExcel = async () => {
    if (selectedCapteurs.length === 0) {
      showNotification('Veuillez sélectionner au moins un capteur', 'warning');
      return;
    }

    try {
      showLoading('Export en cours...');
      const response = await ApiService.exportStatisticsToExcel(selectedCapteurs, startDate || null, endDate || null);
      
      if (response.success) {
        showNotification(`Export réussi: ${response.filename}`, 'success');
      } else {
        showNotification(response.message || 'Erreur lors de l\'export', 'error');
      }
    } catch (error) {
      showNotification('Erreur lors de l\'export', 'error');
      console.error('Error exporting statistics:', error);
    } finally {
      hideLoading();
    }
  };

  const renderCapteurCard = (capteur) => {
    const isSelected = selectedCapteurs.includes(capteur.id);
    
    return (
      <div
        key={capteur.id}
        className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
          isSelected
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
        }`}
        onClick={() => handleCapteurChange(capteur.id)}
      >
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center mb-2">
              <input
                type="checkbox"
                checked={isSelected}
                onChange={() => handleCapteurChange(capteur.id)}
                className="mr-3 w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                onClick={(e) => e.stopPropagation()}
              />
              <h4 className="font-semibold text-gray-900 dark:text-gray-100">
                {capteur.nom}
              </h4>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Types: {capteur.available_data_types.join(', ')}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500">
              {capteur.file_path?.split(/[/\\]/).pop()}
            </p>
          </div>
        </div>
      </div>
    );
  };

  const renderStatisticsSummary = () => {
    if (!statistics || !statistics.results) return null;

    return (
      <div className="space-y-6">
        {/* Résumé général */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 flex items-center">
            <i className="bx bx-bar-chart-alt text-green-500 mr-2"></i>
            Résumé de l'analyse
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {statistics.results.filter(r => r.success).length}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">Capteurs analysés</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                {statistics.results.filter(r => r.success && r.statistiques.temperature && !r.statistiques.temperature.error).length}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">Données température</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {statistics.results.filter(r => r.success && r.statistiques.humidity && !r.statistiques.humidity.error).length}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">Données humidité</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                {statistics.results.filter(r => r.success && r.statistiques.dew_point && !r.statistiques.dew_point.error).length}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">Données point de rosée</p>
            </div>
          </div>
        </div>

        {/* Tableau de synthèse */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 flex items-center">
            <i className="bx bx-table text-blue-500 mr-2"></i>
            Tableau de synthèse
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Capteur
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Temp. Min/Max (°C)
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    HR Min/Max (%)
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    % HR &gt; 65%
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    % HR &lt; 55%
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Point Rosée (°C)
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {statistics.results.filter(r => r.success).map((result) => (
                  <tr key={result.capteur_id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100">
                      {result.capteur_info.nom}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {result.statistiques.temperature && !result.statistiques.temperature.error
                        ? `${result.statistiques.temperature.temperature_minimale} / ${result.statistiques.temperature.temperature_maximale}`
                        : 'N/A'
                      }
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {result.statistiques.humidity && !result.statistiques.humidity.error
                        ? `${result.statistiques.humidity.humidite_minimale} / ${result.statistiques.humidity.humidite_maximale}`
                        : 'N/A'
                      }
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {result.statistiques.humidity && !result.statistiques.humidity.error
                        ? `${result.statistiques.humidity.pourcentage_au_dessus_65}%`
                        : 'N/A'
                      }
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {result.statistiques.humidity && !result.statistiques.humidity.error
                        ? `${result.statistiques.humidity.pourcentage_au_dessous_55}%`
                        : 'N/A'
                      }
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {result.statistiques.dew_point && !result.statistiques.dew_point.error
                        ? `${result.statistiques.dew_point.point_rosee_minimal} / ${result.statistiques.dew_point.point_rosee_maximal}`
                        : 'N/A'
                      }
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-500 to-blue-600 rounded-lg p-8 text-white">
        <h2 className="text-3xl font-bold mb-2">Analyse Statistique Multi-Capteurs</h2>
        <p className="text-green-100 text-lg">
          Extraction de données et tableaux de synthèse pour plusieurs capteurs
        </p>
      </div>

      {/* Configuration */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-6 flex items-center">
          <i className="bx bx-cog text-blue-500 mr-2"></i>
          Configuration de l'analyse
        </h3>

        {/* Sélection des capteurs */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <label className="block text-sm font-medium">Capteurs à analyser</label>
            <button
              onClick={selectAllCapteurs}
              className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
            >
              {selectedCapteurs.length === capteurs.length ? 'Désélectionner tout' : 'Sélectionner tout'}
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {capteurs.map(renderCapteurCard)}
          </div>
          
          {selectedCapteurs.length > 0 && (
            <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
              <p className="text-sm text-blue-700 dark:text-blue-300">
                <i className="bx bx-info-circle mr-1"></i>
                {selectedCapteurs.length} capteur(s) sélectionné(s)
              </p>
            </div>
          )}
        </div>

        {/* Filtres dates */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-2">Date de début (optionnelle)</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Date de fin (optionnelle)</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              min={startDate}
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-4">
          <button
            onClick={analyzeStatistics}
            disabled={selectedCapteurs.length === 0 || isAnalyzing}
            className="btn-primary flex items-center"
          >
            <i className="bx bx-bar-chart-alt mr-2"></i>
            {isAnalyzing ? 'Analyse en cours...' : 'Analyser'}
          </button>
          
          <button
            onClick={exportToExcel}
            disabled={selectedCapteurs.length === 0}
            className="btn-secondary flex items-center"
          >
            <i className="bx bx-download mr-2"></i>
            Exporter Tableau Excel
          </button>
        </div>
      </div>

      {/* Résultats */}
      {statistics && renderStatisticsSummary()}

      {/* Message d'aide */}
      {capteurs.length === 0 && (
        <div className="bg-yellow-50 dark:bg-yellow-900/30 p-6 rounded-lg border-l-4 border-yellow-500">
          <h4 className="font-semibold mb-2 text-yellow-700 dark:text-yellow-300">
            <i className="bx bx-info-circle mr-2"></i>
            Aucun capteur disponible
          </h4>
          <p className="text-yellow-600 dark:text-yellow-400">
            Pour utiliser cette fonctionnalité, vous devez d'abord:
          </p>
          <ol className="list-decimal list-inside mt-2 text-yellow-600 dark:text-yellow-400">
            <li>Ajouter des capteurs dans la section "Capteurs & Fichiers"</li>
            <li>Associer des fichiers de données à vos capteurs</li>
            <li>Configurer le mappage des colonnes</li>
          </ol>
        </div>
      )}
    </div>
  );
};

export default StatisticsPageMultiple;
