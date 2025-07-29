import React, { useState, useEffect } from 'react';
import { ApiService } from '../services/ApiService';
import { showNotification } from '../hooks/useNotification';
import { showLoading, hideLoading } from '../hooks/useLoading';

const HistoryPage = () => {
  const [historyEntries, setHistoryEntries] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await ApiService.getHistory();
      
      if (response.success) {
        setHistoryEntries(response.history);
      } else {
        showNotification(response.message || 'Erreur lors du chargement de l\'historique', 'error');
      }
    } catch (error) {
      showNotification('Erreur de communication avec l\'API', 'error');
      console.error('API error:', error);
    }
  };

  const exportHistory = async () => {
    showLoading('Exportation de l\'historique...');
    
    try {
      const response = await ApiService.exportHistory();
      hideLoading();
      
      if (response.success) {
        showNotification('Historique exporté avec succès', 'success');
      } else {
        showNotification(response.message || 'Erreur lors de l\'exportation de l\'historique', 'error');
      }
    } catch (error) {
      hideLoading();
      showNotification('Erreur de communication avec l\'API', 'error');
      console.error('API error:', error);
    }
  };

  const formatDetails = (entry) => {
    if (!entry.details) return '-';
    
    let details = '';
    
    if (entry.details.file_path) {
      const filePath = entry.details.file_path.split('/').pop().split('\\').pop();
      details += `Fichier: ${filePath}<br>`;
    }
    
    if (entry.details.columns) {
      details += 'Colonnes: ';
      const columns = [];
      if (entry.details.columns.date) columns.push(`Date=${entry.details.columns.date}`);
      if (entry.details.columns.temperature) columns.push(`Temp=${entry.details.columns.temperature}`);
      if (entry.details.columns.humidity) columns.push(`Hum=${entry.details.columns.humidity}`);
      details += columns.join(', ');
    }
    
    if (entry.details.format) {
      details += `Format: ${entry.details.format}`;
    }
    
    if (entry.details.graph_type) {
      details += `Type de graphique: ${entry.details.graph_type}`;
    }
    
    return details || '-';
  };

  // Trier l'historique par date (du plus récent au plus ancien)
  const sortedHistory = [...historyEntries].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  return (
    <div>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4">🕓 Historique</h3>
        <p className="mb-6">Consultez l'historique des opérations effectuées dans l'application.</p>
        
        <div className="mb-6">
          <button 
            className="btn-secondary"
            onClick={exportHistory}
          >
            <span className="icon">📤</span> Exporter l'historique
          </button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
            <thead>
              <tr className="bg-gray-100 dark:bg-gray-700">
                <th className="py-2 px-4 border-b text-left">Date</th>
                <th className="py-2 px-4 border-b text-left">Action</th>
                <th className="py-2 px-4 border-b text-left">Capteur</th>
                <th className="py-2 px-4 border-b text-left">Détails</th>
              </tr>
            </thead>
            <tbody>
              {sortedHistory.length === 0 ? (
                <tr>
                  <td colSpan="4" className="py-4 px-4 text-center text-gray-500 dark:text-gray-400">
                    Aucune opération enregistrée dans l'historique.
                  </td>
                </tr>
              ) : (
                sortedHistory.map((entry, index) => {
                  const date = new Date(entry.timestamp);
                  const formattedDate = date.toLocaleString();
                  
                  return (
                    <tr key={index} className="border-b border-gray-200 dark:border-gray-700">
                      <td className="py-2 px-4">{formattedDate}</td>
                      <td className="py-2 px-4">{entry.action}</td>
                      <td className="py-2 px-4">{entry.capteur_nom || '-'}</td>
                      <td 
                        className="py-2 px-4"
                        dangerouslySetInnerHTML={{ __html: formatDetails(entry) }}
                      />
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
          <li>L'historique enregistre toutes les opérations importantes effectuées dans l'application.</li>
          <li>Vous pouvez exporter l'historique au format CSV pour le conserver ou l'analyser.</li>
          <li>L'historique est conservé localement sur votre ordinateur.</li>
        </ul>
      </div>
    </div>
  );
};

export default HistoryPage;
