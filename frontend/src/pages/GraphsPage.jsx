import React, { useState, useEffect } from 'react';
import { ApiService } from '../services/ApiService';
import { showNotification } from '../hooks/useNotification';
import { showLoading, hideLoading } from '../hooks/useLoading';

const GraphsPage = () => {
  const [capteurs, setCapteurs] = useState([]);
  const [graphTypes, setGraphTypes] = useState([]);
  const [selectedGraphType, setSelectedGraphType] = useState('');
  const [selectedCapteurs, setSelectedCapteurs] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [generatedGraphs, setGeneratedGraphs] = useState([]);
  const [showGraphContainer, setShowGraphContainer] = useState(false);

  // Nouveaux états pour les onglets et statistiques
  const [activeTab, setActiveTab] = useState('graphs'); // 'graphs' ou 'statistics'
  const [statistics, setStatistics] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      // Charger les capteurs disponibles pour les graphiques
      const capteursResponse = await ApiService.getCapteursForGraphs();
      if (capteursResponse.success) {
        setCapteurs(capteursResponse.capteurs);

        // Charger les types de graphiques
        const typesResponse = await ApiService.getGraphTypes();
        if (typesResponse.success) {
          setGraphTypes(typesResponse.types);
        } else {
          showNotification(
            typesResponse.message || 'Erreur lors du chargement des types de graphiques',
            'error'
          );
        }
      } else {
        showNotification(
          capteursResponse.message || 'Erreur lors du chargement des capteurs',
          'error'
        );
      }
    } catch (error) {
      showNotification('Erreur de communication avec l\'API', 'error');
      console.error('API error:', error);
    }
  };

  const updateGraphDescription = () => {
    const selectedType = graphTypes.find(type => type.id === selectedGraphType);
    return selectedType ? selectedType.description : 'Sélectionnez un type de graphique pour voir sa description.';
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

  const generateGraph = async () => {
    if (selectedCapteurs.length === 0) {
      showNotification('Veuillez sélectionner au moins un capteur', 'error');
      return;
    }

    if (selectedGraphType === 'all') {
      await generateAllGraphTypes();
      return;
    }

    if (!selectedGraphType || selectedGraphType === '') {
      showNotification('Veuillez sélectionner un type de graphique', 'error');
      return;
    }

    // Vérifier la cohérence des dates
    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
      showNotification('La date de début doit être antérieure à la date de fin', 'error');
      return;
    }

    showLoading('Génération du graphique en cours...');

    try {
      const options = {};
      if (startDate) options.start_date = startDate;
      if (endDate) options.end_date = endDate;

      const response = await ApiService.generateGraph(selectedGraphType, selectedCapteurs, options);

      hideLoading();

      if (response.success) {
        setGeneratedGraphs([{
          id: selectedGraphType,
          title: response.data.title,
          images: Array.isArray(response.image) ? response.image : [response.image],
          type: selectedGraphType
        }]);
        setShowGraphContainer(true);
        showNotification(response.data.title, 'success');
      } else {
        showNotification(response.message, 'error');
      }
    } catch (error) {
      hideLoading();
      showNotification('Erreur lors de la génération du graphique', 'error');
      console.error(error);
    }
  };

  const generateAllGraphTypes = async () => {
    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
      showNotification('La date de début doit être antérieure à la date de fin', 'error');
      return;
    }

    showLoading('Génération de tous les graphiques en cours...');

    const options = {};
    if (startDate) options.start_date = startDate;
    if (endDate) options.end_date = endDate;

    const allGraphs = [];

    try {
      // Générer chaque type de graphique séquentiellement
      for (const graphType of graphTypes) {
        try {
          const response = await ApiService.generateGraph(graphType.id, selectedCapteurs, options);

          if (response.success) {
            if (Array.isArray(response.image) && response.image.length > 1) {
              response.image.forEach((img, index) => {
                allGraphs.push({
                  id: `${graphType.id}_${index + 1}`,
                  title: `${graphType.name} ${index + 1}`,
                  images: [img],
                  type: graphType.id,
                  name: graphType.name
                });
              });
            } else {
              allGraphs.push({
                id: graphType.id,
                title: graphType.name,
                images: Array.isArray(response.image) ? response.image : [response.image],
                type: graphType.id,
                name: graphType.name
              });
            }
          }
        } catch (error) {
          console.error(`Erreur lors de la génération du graphique ${graphType.id}:`, error);
        }
      }

      setGeneratedGraphs(allGraphs);
      setShowGraphContainer(true);
      hideLoading();

    } catch (error) {
      hideLoading();
      showNotification('Erreur lors de la génération des graphiques', 'error');
      console.error(error);
    }
  };

  const downloadSingleImage = async (imageData, filename) => {
    showLoading('Préparation du téléchargement...');

    try {
      const response = await ApiService.saveImageWithDialog(imageData, filename);
      hideLoading();

      if (response.success) {
        showNotification('Image enregistrée avec succès', 'success');
      } else {
        showNotification(response.message, 'error');
      }
    } catch (error) {
      hideLoading();
      showNotification('Erreur lors du téléchargement de l\'image', 'error');
      console.error(error);
    }
  };

  const downloadAllImages = async () => {
    showLoading('Préparation du téléchargement...');

    try {
      const imagesData = generatedGraphs.flatMap(graph =>
        graph.images.map((img, index) => ({
          id: graph.images.length > 1 ? `${graph.id}_${index + 1}` : graph.id,
          name: graph.images.length > 1 ? `${graph.title}_${index + 1}` : graph.title,
          image: img
        }))
      );

      const response = await ApiService.saveAllImagesWithDialog(imagesData);
      hideLoading();

      if (response.success) {
        showNotification('Images enregistrées avec succès', 'success');
      } else {
        showNotification(response.message, 'error');
      }
    } catch (error) {
      hideLoading();
      showNotification('Erreur lors du téléchargement des graphiques', 'error');
      console.error(error);
    }
  };

  // Nouvelles fonctions pour les statistiques
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

  const renderStatisticsSummary = () => {
    if (!statistics || !statistics.results) return null;

    return (
      <div className="space-y-6">
        {/* Résumé général */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 flex items-center">
            <i className="bx bx-bar-chart-alt text-green-500 mr-2"></i>
            Résumé de l'analyse - Capteurs sélectionnés pour graphiques
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
            Tableau de synthèse - Période: {startDate || 'début'} à {endDate || 'fin'}
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

        {/* Actions pour les statistiques */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <i className="bx bx-download text-green-500 mr-2"></i>
            Export des données
          </h3>
          <div className="flex gap-4">
            <button
              onClick={exportToExcel}
              disabled={selectedCapteurs.length === 0}
              className="btn-primary flex items-center"
            >
              <i className="bx bx-download mr-2"></i>
              Exporter Tableau Excel
            </button>
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Le fichier Excel contiendra une feuille de synthèse et une feuille détaillée par capteur.
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Onglets */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md">
        <div className="border-b border-gray-200 dark:border-gray-700">
          <nav className="flex space-x-8 px-6" aria-label="Tabs">
            <button
              onClick={() => setActiveTab('graphs')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'graphs'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
            >
              <i className="bx bx-bar-chart-alt-2 mr-2"></i>
              Graphiques
            </button>
            <button
              onClick={() => setActiveTab('statistics')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'statistics'
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
            >
              <i className="bx bx-table mr-2"></i>
              Tableaux de synthèse
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'graphs' ? (
            <div>
              <h3 className="text-lg font-semibold mb-4">📊 Graphiques</h3>
              <p className="mb-6">Générez des graphiques à partir de vos données climatiques.</p>
            </div>
          ) : (
            <div>
              <h3 className="text-lg font-semibold mb-4">📊 Tableaux de synthèse</h3>
              <p className="mb-6">Analysez et exportez les statistiques des capteurs sélectionnés avec la même plage de dates que pour les graphiques.</p>

              {/* Actions pour les statistiques */}
              <div className="flex gap-4 mb-6">
                <button
                  onClick={analyzeStatistics}
                  disabled={selectedCapteurs.length === 0 || isAnalyzing}
                  className="btn-primary flex items-center"
                >
                  <i className="bx bx-bar-chart-alt mr-2"></i>
                  {isAnalyzing ? 'Analyse en cours...' : 'Analyser les capteurs sélectionnés'}
                </button>

                <button
                  onClick={exportToExcel}
                  disabled={selectedCapteurs.length === 0}
                  className="btn-secondary flex items-center"
                >
                  <i className="bx bx-download mr-2"></i>
                  Exporter Excel
                </button>
              </div>

              {/* {selectedCapteurs.length === 0 && (
                <div className="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg border-l-4 border-yellow-500 mb-6">
                  <p className="text-yellow-700 dark:text-yellow-300">
                    <i className="bx bx-info-circle mr-2"></i>
                    Sélectionnez des capteurs ci-dessous pour générer les tableaux de synthèse.
                  </p>
                </div>
              )} */}
            </div>
          )}
        </div>
      </div>


      {/* Configuration commune des capteurs et dates */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">⚙️ Configuration</h3>
        <p className="mb-6">
          Sélectionnez vos capteurs et la période d'analyse. Ces paramètres s'appliquent à la fois aux graphiques et aux tableaux de synthèse.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* Colonne gauche */}
          <div className="space-y-6">

            {/* Type de graphique */}
            {activeTab === 'graphs' && (
              <div>
                <label htmlFor="graph-type" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Type de graphique
                </label>
                <select
                  id="graph-type"
                  value={selectedGraphType}
                  onChange={(e) => setSelectedGraphType(e.target.value)}
                  className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                >
                  <option
                    value="all"
                    style={{ backgroundColor: '#4a6cf7', color: 'white', border: '2px solid #3451b2', fontWeight: 'bold' }}
                  >
                    Tous les types de graphiques
                  </option>
                  <option value="">-- Sélectionnez un type --</option>
                  {graphTypes.map(type => (
                    <option key={type.id} value={type.id}>
                      {type.name}
                    </option>
                  ))}
                </select>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  {updateGraphDescription()}
                </p>
              </div>
            )}

            {/* Choix des capteurs */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Capteurs à inclure
              </label>
              <div className="max-h-40 overflow-y-auto border border-gray-300 dark:border-gray-600 rounded-md p-2 bg-white dark:bg-gray-700">
                {capteurs.length === 0 ? (
                  <p className="text-gray-500 dark:text-gray-400 p-2">
                    Aucun capteur disponible. Veuillez d'abord ajouter des capteurs, leur associer des fichiers et mapper les colonnes.
                  </p>
                ) : (
                  capteurs.map(capteur => (
                    <div key={capteur.id} className="flex items-center mb-2">
                      <input
                        type="checkbox"
                        id={`capteur-${capteur.id}`}
                        checked={selectedCapteurs.includes(capteur.id)}
                        onChange={() => handleCapteurChange(capteur.id)}
                        className="mr-2"
                      />
                      <label htmlFor={`capteur-${capteur.id}`} className="text-gray-900 dark:text-gray-100">
                        {capteur.nom}
                      </label>
                    </div>
                  ))
                )}
              </div>
              {capteurs.length > 0 && (
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  Sélectionnez un ou plusieurs capteurs pour {activeTab === 'graphs' ? 'les graphiques' : 'l\'analyse statistique'}.
                </p>
              )}
            </div>
          </div>

          {/* Colonne droite */}
          <div className="space-y-6">
            {/* Date de début */}
            <div>
              <label htmlFor="start-date" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Date de début (optionnelle)
              </label>
              <input
                type="date"
                id="start-date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              />
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Laissez vide pour utiliser toutes les données disponibles.
              </p>
            </div>

            {/* Date de fin */}
            <div>
              <label htmlFor="end-date" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Date de fin (optionnelle)
              </label>
              <input
                type="date"
                id="end-date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              />
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Laissez vide pour utiliser toutes les données disponibles.
              </p>
            </div>
          </div>
        </div>

        {/* Bouton de génération - seulement pour l'onglet graphiques */}
        {activeTab === 'graphs' && (
          <div className="flex justify-end mt-6">
            <button
              onClick={generateGraph}
              className="btn-primary"
              disabled={selectedCapteurs.length === 0}
            >
              Générer le graphique
            </button>
          </div>
        )}
      </div>


      {/* Affichage des graphiques générés - seulement pour l'onglet graphiques */}
      {activeTab === 'graphs' && showGraphContainer && generatedGraphs.length > 0 && (
        <div className="space-y-6">
          {selectedGraphType === 'all' && generatedGraphs.length > 1 && (
            <div className="flex justify-center">
              <button
                onClick={downloadAllImages}
                className="btn-primary flex items-center justify-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                Télécharger toutes les images
              </button>
            </div>
          )}

          {generatedGraphs.map(graph => (
            <div key={graph.id} className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-inner relative">
              <div className="flex justify-between items-center mb-4">
                <h4 className="text-lg font-semibold">{graph.title}</h4>
              </div>

              <div className="grid grid-cols-1 gap-4">
                {graph.images.map((imageData, index) => (
                  <div key={index} className="relative">
                    <img
                      src={`data:image/png;base64,${imageData}`}
                      alt={`${graph.title} - Graphique ${index + 1}`}
                      className="w-full border border-gray-200 dark:border-gray-700 rounded"
                    />
                    <button
                      onClick={() => downloadSingleImage(imageData, graph.images.length > 1 ? `${graph.title}_${index + 1}` : graph.title)}
                      className="absolute top-2 right-2 bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-full shadow-md transition-colors"
                      title="Télécharger cette image"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}



      {/* Affichage des statistiques - seulement pour l'onglet statistiques */}
      {activeTab === 'statistics' && renderStatisticsSummary()}

      {/* Remarques */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">💬 Remarques</h3>
        <ul className="list-disc list-inside space-y-2 ml-4 text-gray-700 dark:text-gray-300">
          <li>Les graphiques sont générés à partir des données des capteurs sélectionnés.</li>
          <li>Certains types de graphiques nécessitent des données spécifiques (température, humidité, etc.).</li>
          <li>Vous pouvez exporter les graphiques en cliquant sur le bouton de téléchargement de chaque image.</li>
          <li>L'option "Tous les types de graphiques" générera automatiquement tous les graphiques disponibles pour les capteurs sélectionnés.</li>
          <li>Utilisez les sélecteurs de date pour limiter la période affichée sur les graphiques.</li>
        </ul>
      </div>
    </div>
  );
};

export default GraphsPage;
