import React, { useState, useEffect } from 'react';
import { ApiService } from '../services/ApiService';
import { showNotification } from '../hooks/useNotification';
import { showLoading, hideLoading } from '../hooks/useLoading';

const StatisticsPage = () => {
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

  const analyzeStatistics = async () => {
    if (!selectedCapteur) {
      showNotification('Veuillez sélectionner un capteur', 'warning');
      return;
    }

    setIsAnalyzing(true);
    try {
      showLoading('Analyse des données en cours...');
      const response = await ApiService.getDataStatistics(selectedCapteur, startDate || null, endDate || null);
      
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
    if (!selectedCapteur) {
      showNotification('Veuillez sélectionner un capteur', 'warning');
      return;
    }

    try {
      showLoading('Export en cours...');
      const response = await ApiService.exportStatisticsToExcel(selectedCapteur, startDate || null, endDate || null);
      
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

  const getSelectedCapteurInfo = () => {
    return capteurs.find(c => c.id === selectedCapteur);
  };

  const renderTemperatureStats = (tempStats) => {
    if (tempStats.error) {
      return (
        <div className="text-center py-4 text-gray-500">
          <i className="bx bx-error-circle text-4xl mb-2"></i>
          <p>{tempStats.error}</p>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
          <h5 className="font-semibold mb-2 text-blue-700 dark:text-blue-300">
            <i className="bx bx-trending-up mr-2"></i>Écart maximal journalier
          </h5>
          <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {tempStats.ecart_maximal_journalier}°C
          </p>
        </div>

        <div className="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
          <h5 className="font-semibold mb-2 text-green-700 dark:text-green-300">
            <i className="bx bx-bar-chart-alt mr-2"></i>Écart moyen journalier
          </h5>
          <p className="text-2xl font-bold text-green-600 dark:text-green-400">
            {tempStats.ecart_moyen_journalier}°C
          </p>
        </div>

        <div className="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
          <h5 className="font-semibold mb-2 text-purple-700 dark:text-purple-300">
            <i className="bx bx-down-arrow-circle mr-2"></i>Température minimale
          </h5>
          <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {tempStats.temperature_minimale}°C
          </p>
        </div>

        <div className="bg-red-50 dark:bg-red-900/30 p-4 rounded-lg">
          <h5 className="font-semibold mb-2 text-red-700 dark:text-red-300">
            <i className="bx bx-up-arrow-circle mr-2"></i>Température maximale
          </h5>
          <p className="text-2xl font-bold text-red-600 dark:text-red-400">
            {tempStats.temperature_maximale}°C
          </p>
        </div>
      </div>
    );
  };

  const renderHumidityStats = (humStats) => {
    if (humStats.error) {
      return (
        <div className="text-center py-4 text-gray-500">
          <i className="bx bx-error-circle text-4xl mb-2"></i>
          <p>{humStats.error}</p>
        </div>
      );
    }

    return (
      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
            <h5 className="font-semibold mb-2 text-blue-700 dark:text-blue-300">
              <i className="bx bx-trending-up mr-2"></i>Variation max. quotidienne
            </h5>
            <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {humStats.variation_maximale_quotidienne}%
            </p>
          </div>

          <div className="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
            <h5 className="font-semibold mb-2 text-green-700 dark:text-green-300">
              <i className="bx bx-bar-chart-alt mr-2"></i>Écart moyen journalier
            </h5>
            <p className="text-2xl font-bold text-green-600 dark:text-green-400">
              {humStats.ecart_moyen_journalier}%
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-orange-50 dark:bg-orange-900/30 p-4 rounded-lg">
            <h5 className="font-semibold mb-2 text-orange-700 dark:text-orange-300">
              <i className="bx bx-up-arrow mr-2"></i>Au-dessus de 65% HR
            </h5>
            <p className="text-xl font-bold text-orange-600 dark:text-orange-400">
              {humStats.pourcentage_au_dessus_65}%
            </p>
          </div>

          <div className="bg-cyan-50 dark:bg-cyan-900/30 p-4 rounded-lg">
            <h5 className="font-semibold mb-2 text-cyan-700 dark:text-cyan-300">
              <i className="bx bx-down-arrow mr-2"></i>Au-dessous de 55% HR
            </h5>
            <p className="text-xl font-bold text-cyan-600 dark:text-cyan-400">
              {humStats.pourcentage_au_dessous_55}%
            </p>
          </div>

          <div className="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg">
            <h5 className="font-semibold mb-2 text-yellow-700 dark:text-yellow-300">
              <i className="bx bx-shuffle mr-2"></i>Fluctuations ±10%
            </h5>
            <p className="text-xl font-bold text-yellow-600 dark:text-yellow-400">
              {humStats.pourcentage_fluctuations_elevees}%
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
            <h5 className="font-semibold mb-2 text-purple-700 dark:text-purple-300">
              <i className="bx bx-down-arrow-circle mr-2"></i>Humidité minimale
            </h5>
            <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
              {humStats.humidite_minimale}%
            </p>
          </div>

          <div className="bg-red-50 dark:bg-red-900/30 p-4 rounded-lg">
            <h5 className="font-semibold mb-2 text-red-700 dark:text-red-300">
              <i className="bx bx-up-arrow-circle mr-2"></i>Humidité maximale
            </h5>
            <p className="text-2xl font-bold text-red-600 dark:text-red-400">
              {humStats.humidite_maximale}%
            </p>
          </div>
        </div>
      </div>
    );
  };

  const renderLuminosityStats = (lumStats) => {
    if (lumStats.error) {
      return (
        <div className="text-center py-4 text-gray-500">
          <i className="bx bx-error-circle text-4xl mb-2"></i>
          <p>{lumStats.error}</p>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg">
          <h5 className="font-semibold mb-2 text-yellow-700 dark:text-yellow-300">
            <i className="bx bx-sun mr-2"></i>Valeur maximale
          </h5>
          <p className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
            {lumStats.valeur_maximale_lux} lux
          </p>
        </div>

        <div className="bg-orange-50 dark:bg-orange-900/30 p-4 rounded-lg">
          <h5 className="font-semibold mb-2 text-orange-700 dark:text-orange-300">
            <i className="bx bx-time mr-2"></i>Exposition 100 lux
          </h5>
          <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
            {lumStats.duree_exposition_100_lux_minutes} min
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-500 to-blue-600 rounded-lg p-8 text-white">
        <h2 className="text-3xl font-bold mb-2">Analyse Statistique</h2>
        <p className="text-green-100 text-lg">
          Extraction de données et statistiques détaillées de vos capteurs
        </p>
      </div>

      {/* Configuration */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold mb-6 flex items-center">
          <i className="bx bx-cog text-blue-500 mr-2"></i>
          Configuration de l'analyse
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {/* Sélection du capteur */}
          <div>
            <label className="block text-sm font-medium mb-2">Capteur</label>
            <select
              value={selectedCapteur}
              onChange={(e) => setSelectedCapteur(e.target.value)}
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Sélectionner un capteur</option>
              {capteurs.map((capteur) => (
                <option key={capteur.id} value={capteur.id}>
                  {capteur.nom}
                </option>
              ))}
            </select>
          </div>

          {/* Date de début */}
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

          {/* Date de fin */}
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

          {/* Actions */}
          <div className="flex flex-col gap-2">
            <button
              onClick={analyzeStatistics}
              disabled={!selectedCapteur || isAnalyzing}
              className="btn-primary flex-1"
            >
              <i className="bx bx-bar-chart-alt mr-2"></i>
              {isAnalyzing ? 'Analyse...' : 'Analyser'}
            </button>
            
            <button
              onClick={exportToExcel}
              disabled={!selectedCapteur}
              className="btn-secondary flex-1"
            >
              <i className="bx bx-download mr-2"></i>
              Exporter Excel
            </button>
          </div>
        </div>

        {/* Informations sur le capteur sélectionné */}
        {selectedCapteur && (
          <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg border-l-4 border-blue-500">
            <h4 className="font-semibold mb-2 text-blue-700 dark:text-blue-300">
              Capteur sélectionné: {getSelectedCapteurInfo()?.nom}
            </h4>
            <p className="text-sm text-blue-600 dark:text-blue-400 mb-2">
              Types de données disponibles: {getSelectedCapteurInfo()?.available_data_types.join(', ')}
            </p>
            <p className="text-xs text-blue-500 dark:text-blue-400">
              Fichier: {getSelectedCapteurInfo()?.file_path.split(/[/\\]/).pop()}
            </p>
          </div>
        )}
      </div>

      {/* Résultats */}
      {statistics && (
        <div className="space-y-6">
          {/* Informations générales */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-4 flex items-center">
              <i className="bx bx-info-circle text-green-500 mr-2"></i>
              Informations sur l'analyse
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Capteur</p>
                <p className="font-semibold">{statistics.capteur_info.nom}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Période analysée</p>
                <p className="font-semibold">
                  {statistics.periode_analyse.debut || 'Début'} → {statistics.periode_analyse.fin || 'Fin'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Types de données</p>
                <p className="font-semibold">
                  {Object.keys(statistics.statistiques).filter(key => !statistics.statistiques[key].error).join(', ')}
                </p>
              </div>
            </div>
          </div>

          {/* Statistiques de température */}
          {statistics.statistiques.temperature && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold mb-6 flex items-center">
                <i className="bx bx-thermometer text-red-500 mr-2"></i>
                Statistiques de Température
              </h3>
              {renderTemperatureStats(statistics.statistiques.temperature)}
            </div>
          )}

          {/* Statistiques d'humidité */}
          {statistics.statistiques.humidity && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold mb-6 flex items-center">
                <i className="bx bx-droplet text-blue-500 mr-2"></i>
                Statistiques d'Humidité
              </h3>
              {renderHumidityStats(statistics.statistiques.humidity)}
            </div>
          )}

          {/* Statistiques de luminosité */}
          {statistics.statistiques.luminosity && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold mb-6 flex items-center">
                <i className="bx bx-sun text-yellow-500 mr-2"></i>
                Statistiques de Luminosité
              </h3>
              {renderLuminosityStats(statistics.statistiques.luminosity)}
            </div>
          )}
        </div>
      )}

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

export default StatisticsPage;
