import React, { useState, useEffect } from 'react';
import { ApiService } from '../services/ApiService';
import { showNotification } from '../hooks/useNotification';

const MappingPage = () => {
    const [capteursPourMapping, setCapteursPourrMapping] = useState([]);
    const [selectedCapteurId, setSelectedCapteurId] = useState(null);
    const [availableColumns, setAvailableColumns] = useState([]);
    const [mapping, setMapping] = useState({
        date: '',
        temperature: '',
        humidity: '',
        dew_point: ''
    });
    const [dataPreview, setDataPreview] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [showMappingForm, setShowMappingForm] = useState(false);

    // Chargement des capteurs au montage du composant
    useEffect(() => {
        loadMappingPage();
    }, []);

    // Fonction pour charger les capteurs disponibles pour le mappage
    const loadMappingPage = async () => {
        setIsLoading(true);

        try {
            const response = await ApiService.getCapteursForMapping();

            if (response.success) {
                setCapteursPourrMapping(response.capteurs);
            } else {
                showNotification(response.message || 'Erreur lors du chargement des capteurs', 'error');
            }
        } catch (error) {
            showNotification('Erreur de communication avec l\'API', 'error');
            console.error('API error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Gestion de la sélection d'un capteur
    const onCapteurSelected = async (capteurId) => {
        if (!capteurId) {
            setShowMappingForm(false);
            setSelectedCapteurId(null);
            return;
        }

        setSelectedCapteurId(capteurId);
        setIsLoading(true);

        try {
            // Charger les colonnes disponibles
            const columnsResponse = await ApiService.getColumnsForMapping(capteurId);

            if (columnsResponse.success) {
                setAvailableColumns(columnsResponse.columns);

                // Charger les valeurs actuelles du mappage si disponibles
                const capteur = capteursPourMapping.find(c => c.id === capteurId);
                if (capteur && capteur.columns) {
                    setMapping({
                        date: capteur.columns.date || '',
                        temperature: capteur.columns.temperature || '',
                        humidity: capteur.columns.humidity || '',
                        dew_point: capteur.columns.dew_point || ''
                    });
                } else {
                    // Réinitialiser le mappage
                    setMapping({
                        date: '',
                        temperature: '',
                        humidity: '',
                        dew_point: ''
                    });
                }

                // Charger l'aperçu des données
                await loadDataPreview(capteurId);
                setShowMappingForm(true);
            } else {
                showNotification(columnsResponse.message || 'Erreur lors du chargement des colonnes', 'error');
            }
        } catch (error) {
            showNotification('Erreur de communication avec l\'API', 'error');
            console.error('API error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Charger l'aperçu des données
    const loadDataPreview = async (capteurId) => {
        try {
            const response = await ApiService.getDataPreview(capteurId);

            if (response.success) {
                setDataPreview(response.preview);
            } else {
                showNotification(response.message || 'Erreur lors du chargement de l\'aperçu', 'error');
            }
        } catch (error) {
            showNotification('Erreur de communication avec l\'API', 'error');
            console.error('API error:', error);
        }
    };

    // Gestion du changement de mappage
    const handleMappingChange = (field, value) => {
        setMapping(prev => ({
            ...prev,
            [field]: value
        }));
    };

    // Enregistrer le mappage des colonnes
    const saveMapping = async () => {
        // Vérifier que les colonnes obligatoires sont sélectionnées
        if (!mapping.date) {
            showNotification('Veuillez sélectionner une colonne de date', 'warning');
            return;
        }

        if (!mapping.temperature) {
            showNotification('Veuillez sélectionner une colonne de température', 'warning');
            return;
        }

        // Préparer le mappage
        const mappingData = {
            date: mapping.date,
            temperature: mapping.temperature
        };

        if (mapping.humidity) {
            mappingData.humidity = mapping.humidity;
        }

        if (mapping.dew_point) {
            mappingData.dew_point = mapping.dew_point;
        }

        setIsSaving(true);

        try {
            const response = await ApiService.saveColumnMapping(selectedCapteurId, mappingData);

            if (response.success) {
                showNotification('Mappage enregistré avec succès', 'success');
                await loadMappingPage(); // Recharger la page
            } else {
                showNotification(response.message || 'Erreur lors de l\'enregistrement du mappage', 'error');
            }
        } catch (error) {
            showNotification('Erreur de communication avec l\'API', 'error');
            console.error('API error:', error);
        } finally {
            setIsSaving(false);
        }
    };

    // Rendu du sélecteur de colonnes
    const renderColumnSelect = (fieldName, label, required = false, description) => (
        <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {label} {required && <span className="text-red-500">*</span>}
            </label>
            <select
                value={mapping[fieldName]}
                onChange={(e) => handleMappingChange(fieldName, e.target.value)}
                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
                <option value="">-- Sélectionnez une colonne --</option>
                {availableColumns.map(column => (
                    <option key={column} value={column}>{column}</option>
                ))}
            </select>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {description}
            </p>
        </div>
    );

    // Rendu de l'aperçu des données
    const renderDataPreview = () => {
        if (!dataPreview) {
            return (
                <p className="text-gray-500 dark:text-gray-400">
                    Sélectionnez un capteur pour voir un aperçu des données.
                </p>
            );
        }

        return (
            <div>
                <div className="overflow-x-auto">
                    <table className="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                        <thead>
                            <tr className="bg-gray-100 dark:bg-gray-700">
                                {dataPreview.columns.map(column => (
                                    <th key={column} className="py-2 px-4 border-b text-left">
                                        {column}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {dataPreview.data.map((row, index) => (
                                <tr key={index} className="border-b border-gray-200 dark:border-gray-700">
                                    {row.map((cell, cellIndex) => (
                                        <td key={cellIndex} className="py-2 px-4">
                                            {cell !== null ? cell : ''}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                    Aperçu des {dataPreview.data.length} premières lignes du fichier.
                </p>
            </div>
        );
    };

    if (isLoading) {
        return (
            <div className="space-y-6">
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                    <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                        <span className="ml-2">Chargement...</span>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
                <h3 className="text-lg font-semibold mb-4">
                    <i className='bx bx-brain' style={{ color: '#4a6cf7' }}></i> Mappage des Colonnes
                </h3>
                <p className="mb-6">
                    Définissez quelles colonnes correspondent à la date, la température, l'humidité et le point de rosée.
                </p>

                <div className="mb-6">
                    <label htmlFor="capteur-select" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Sélectionnez un capteur
                    </label>
                    <select
                        id="capteur-select"
                        value={selectedCapteurId || ''}
                        onChange={(e) => onCapteurSelected(e.target.value)}
                        className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                    >
                        <option value="">-- Sélectionnez un capteur --</option>
                        {capteursPourMapping.length === 0 ? (
                            <option disabled>Aucun capteur avec fichier disponible</option>
                        ) : (
                            capteursPourMapping.map(capteur => (
                                <option key={capteur.id} value={capteur.id}>
                                    {capteur.nom}
                                </option>
                            ))
                        )}
                    </select>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        {capteursPourMapping.length === 0
                            ? 'Veuillez d\'abord ajouter des capteurs et leur associer des fichiers.'
                            : 'Seuls les capteurs avec des fichiers associés sont affichés.'
                        }
                    </p>
                </div>

                {showMappingForm && (
                    <div id="mapping-form">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                            {renderColumnSelect(
                                'date',
                                'Colonne de date',
                                true,
                                'Colonne contenant les dates/heures des mesures.'
                            )}

                            {renderColumnSelect(
                                'temperature',
                                'Colonne de température',
                                true,
                                'Colonne contenant les valeurs de température.'
                            )}

                            {renderColumnSelect(
                                'humidity',
                                'Colonne d\'humidité (optionnelle)',
                                false,
                                'Colonne contenant les valeurs d\'humidité (si disponible).'
                            )}

                            {renderColumnSelect(
                                'dew_point',
                                'Colonne de point de rosée (optionnelle)',
                                false,
                                'Colonne contenant les valeurs de point de rosée (si disponible).'
                            )}
                        </div>

                        <div className="mb-6">
                            <h4 className="font-semibold mb-2">Aperçu des données</h4>
                            <div id="data-preview" className="overflow-x-auto">
                                {renderDataPreview()}
                            </div>
                        </div>

                        <div className="flex justify-end">
                            <button
                                id="save-mapping-btn"
                                onClick={saveMapping}
                                disabled={isSaving}
                                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isSaving ? 'Enregistrement...' : 'Enregistrer le mappage'}
                            </button>
                        </div>
                    </div>
                )}
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4">💬 Remarques</h3>
                <ul className="list-disc list-inside space-y-2 ml-4 text-gray-700 dark:text-gray-300">
                    <li>L'application tente de détecter automatiquement les colonnes, mais vous pouvez les modifier ici.</li>
                    <li>Les colonnes de date et de température sont obligatoires.</li>
                    <li>Les colonnes d'humidité et de point de rosée sont optionnelles, mais recommandées pour certains graphiques.</li>
                    <li>Une fois le mappage enregistré, vous pourrez générer des graphiques à partir de ces données.</li>
                </ul>
            </div>
        </div>
    );
};

export default MappingPage;
