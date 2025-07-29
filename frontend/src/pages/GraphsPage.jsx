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

  return (
    <div className="space-y-6">
      {/* Configuration des graphiques */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">📊 Graphiques</h3>
        <p className="mb-6">Générez des graphiques à partir de vos données climatiques.</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Sélection du type de graphique */}
          <div className="space-y-4">
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
            
            {/* Sélection des capteurs */}
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
                  Sélectionnez un ou plusieurs capteurs à inclure dans le graphique.
                </p>
              )}
            </div>
          </div>
          
          {/* Sélection des dates */}
          <div className="space-y-4">
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
        
        <div className="flex justify-end mt-6">
          <button
            onClick={generateGraph}
            className="btn-primary"
            disabled={selectedCapteurs.length === 0}
          >
            Générer le graphique
          </button>
        </div>
      </div>

      {/* Affichage des graphiques générés */}
      {showGraphContainer && generatedGraphs.length > 0 && (
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
