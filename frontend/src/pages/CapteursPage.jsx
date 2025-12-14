import React, { useState, useEffect } from 'react';
import { ApiService } from '../services/ApiService';
import { showNotification } from '../hooks/useNotification';
import { showLoading, hideLoading } from '../hooks/useLoading';

import AddCapteurModal from '../components/modals/AddCapteurModal';
import EditCapteurModal from '../components/modals/EditCapteurModal';
import DeleteCapteurModal from '../components/modals/DeleteCapteurModal';

const CapteursPage = () => {
  const [capteurs, setCapteurs] = useState([]);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedCapteur, setSelectedCapteur] = useState(null);

  useEffect(() => {
    loadCapteursPage();
  }, []);

  const loadCapteursPage = async () => {
    try {
      const response = await ApiService.getCapteurs();
      hideLoading();
      
      if (response.success) {
        setCapteurs(response.capteurs);
      } else {
        showNotification(response.message || 'Erreur lors du chargement des capteurs', 'error');
      }
    } catch (error) {
      hideLoading();
      showNotification('Erreur de communication avec l\'API', 'error');
      console.error('API error:', error);
    }
  };

  const handleAddCapteur = async (nom) => {
    try {
      const response = await ApiService.addCapteur(nom);
      
      if (response.success) {
        showNotification(`Capteur "${nom}" ajouté avec succès`, 'success');
        setIsAddModalOpen(false);
        loadCapteursPage();
      } else {
        showNotification(response.message || 'Erreur lors de l\'ajout du capteur', 'error');
      }
    } catch (error) {
      showNotification('Erreur de communication avec l\'API', 'error');
      console.error('API error:', error);
    }
  };

  const handleEditCapteur = async (id, nom) => {
    try {
      const response = await ApiService.editCapteur(id, nom);
      
      if (response.success) {
        showNotification('Capteur modifié avec succès', 'success');
        setIsEditModalOpen(false);
        setSelectedCapteur(null);
        loadCapteursPage();
      } else {
        showNotification(response.message || 'Erreur lors de la modification du capteur', 'error');
      }
    } catch (error) {
      showNotification('Erreur de communication avec l\'API', 'error');
      console.error('API error:', error);
    }
  };

  const handleDeleteCapteur = async (id) => {
    try {
      const response = await ApiService.deleteCapteur(id);
      
      if (response.success) {
        showNotification('Capteur supprimé avec succès', 'success');
        setIsDeleteModalOpen(false);
        setSelectedCapteur(null);
        loadCapteursPage();
      } else {
        showNotification(response.message || 'Erreur lors de la suppression du capteur', 'error');
      }
    } catch (error) {
      showNotification('Erreur de communication avec l\'API', 'error');
      console.error('API error:', error);
    }
  };

  const handleSelectFile = async (capteurId) => {
    showLoading('Sélection du fichier...');
    
    try {
      const response = await ApiService.selectFile(capteurId);
      hideLoading();
      
      if (response.success) {
        showNotification('Fichier associé avec succès', 'success');
        
        if (response.needs_mapping) {
          showNotification('Veuillez mapper les colonnes pour ce fichier', 'info');
          // TODO: Implement navigation to mapping page when available
          // navigateTo('mapping');
        } else {
          loadCapteursPage();
        }
      } else {
        showNotification(response.message || 'Erreur lors de l\'association du fichier', 'error');
      }
    } catch (error) {
      hideLoading();
      showNotification('Erreur de communication avec l\'API', 'error');
      console.error('API error:', error);
    }
  };

  const showEditCapteurModal = (capteurId) => {
    const capteur = capteurs.find(c => c.id === capteurId);
    if (!capteur) {
      showNotification('Capteur non trouvé', 'error');
      return;
    }
    setSelectedCapteur(capteur);
    setIsEditModalOpen(true);
  };

  const showDeleteCapteurModal = (capteurId) => {
    const capteur = capteurs.find(c => c.id === capteurId);
    if (!capteur) {
      showNotification('Capteur non trouvé', 'error');
      return;
    }
    setSelectedCapteur(capteur);
    setIsDeleteModalOpen(true);
  };

  const getColonnesStatus = (capteur) => {
    let colonnesStatus = 'Non mappées';
    let colonnesClass = 'text-red-500 dark:text-red-400';
    
    if (capteur.columns) {
      if (capteur.columns.date && capteur.columns.temperature) {
        colonnesStatus = 'Mappées';
        colonnesClass = 'text-green-500 dark:text-green-400';
      } else {
        colonnesStatus = 'Partiellement mappées';
        colonnesClass = 'text-yellow-500 dark:text-yellow-400';
      }
    }
    
    return { colonnesStatus, colonnesClass };
  };

  const getFichierStatus = (capteur) => {
    let fichierStatus = capteur.file_path ? 
      capteur.file_path.split('/').pop().split('\\').pop() : 
      'Non associé';
    let fichierClass = capteur.file_path ? 
      'text-green-500 dark:text-green-400' : 
      'text-red-500 dark:text-red-400';
    
    return { fichierStatus, fichierClass };
  };

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4">Capteurs & Fichiers</h3>
        <p className="mb-6">Ajoutez vos capteurs et associez-leur des fichiers de données.</p>
        
        <button 
          className="btn-primary mb-6" 
          onClick={() => setIsAddModalOpen(true)}
        >
          <span className="icon">➕</span> Ajouter un capteur
        </button>
        
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
            <thead>
              <tr className="bg-gray-100 dark:bg-gray-700">
                <th className="py-2 px-4 border-b text-left">Nom</th>
                <th className="py-2 px-4 border-b text-left">Fichier</th>
                <th className="py-2 px-4 border-b text-left">Colonnes mappées</th>
                <th className="py-2 px-4 border-b text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {capteurs.length === 0 ? (
                <tr>
                  <td colSpan="4" className="py-4 px-4 text-center text-gray-500 dark:text-gray-400">
                    Aucun capteur ajouté. Cliquez sur "Ajouter un capteur" pour commencer.
                  </td>
                </tr>
              ) : (
                capteurs.map(capteur => {
                  const { colonnesStatus, colonnesClass } = getColonnesStatus(capteur);
                  const { fichierStatus, fichierClass } = getFichierStatus(capteur);
                  
                  return (
                    <tr key={capteur.id} className="border-b border-gray-200 dark:border-gray-700">
                      <td className="py-2 px-4">{capteur.nom}</td>
                      <td className={`py-2 px-4 ${fichierClass}`}>{fichierStatus}</td>
                      <td className={`py-2 px-4 ${colonnesClass}`}>{colonnesStatus}</td>
                      <td className="py-2 px-4">
                        <div className="flex space-x-2">
                          <button 
                            className="btn-icon text-blue-500" 
                            onClick={() => showEditCapteurModal(capteur.id)}
                            title="Modifier"
                          >
                            ✏️
                          </button>
                          <button 
                            className="btn-icon text-green-500" 
                            onClick={() => handleSelectFile(capteur.id)}
                            title="Sélectionner un fichier"
                          >
                            📄
                          </button>
                          <button 
                            className="btn-icon text-red-500" 
                            onClick={() => showDeleteCapteurModal(capteur.id)}
                            title="Supprimer"
                          >
                            🗑️
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
      
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">💬 Remarques</h3>
        <ul className="list-disc list-inside space-y-2 ml-4 text-gray-700 dark:text-gray-300">
          <li>Un capteur correspond à un point de mesure.</li>
          <li>Les fichiers peuvent être en .xlsx, .xls</li>
          <li>L'application tentera de détecter automatiquement les colonnes de date, température et humidité.</li>
          <li>Si la détection automatique échoue, vous serez redirigé vers la page de mappage des colonnes.</li>
        </ul>
      </div>

      {/* Modals */}
      <AddCapteurModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onAdd={handleAddCapteur}
      />

      <EditCapteurModal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setSelectedCapteur(null);
        }}
        onEdit={handleEditCapteur}
        capteur={selectedCapteur}
      />

      <DeleteCapteurModal
        isOpen={isDeleteModalOpen}
        onClose={() => {
          setIsDeleteModalOpen(false);
          setSelectedCapteur(null);
        }}
        onDelete={handleDeleteCapteur}
        capteur={selectedCapteur}
      />
    </div>
  );
};

export default CapteursPage;
