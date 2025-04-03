// Variables globales
let historyEntries = [];

// Chargement de la page d'historique
function loadHistoryPage() {
    showLoading('Chargement de l\'historique...');
    
    pywebview.api.get_history().then(response => {
        hideLoading();
        
        if (response.success) {
            updateHistoryUI(response.history);
        } else {
            showNotification(response.message || 'Erreur lors du chargement de l\'historique', 'error');
        }
    }).catch(error => {
        hideLoading();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Mise à jour de l'interface d'historique
function updateHistoryUI(history) {
    const historyPage = document.getElementById('history-page');
    
    // Générer le contenu HTML
    let html = `
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
            <h3 class="text-lg font-semibold mb-4">🕓 Historique</h3>
            <p class="mb-6">Consultez l'historique des opérations effectuées dans l'application.</p>
            
            <div class="mb-6">
                <button class="btn-secondary" onclick="exportHistory()">
                    <span class="icon">📤</span> Exporter l'historique
                </button>
            </div>
            
            <div class="overflow-x-auto">
                <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                    <thead>
                        <tr class="bg-gray-100 dark:bg-gray-700">
                            <th class="py-2 px-4 border-b text-left">Date</th>
                            <th class="py-2 px-4 border-b text-left">Action</th>
                            <th class="py-2 px-4 border-b text-left">Capteur</th>
                            <th class="py-2 px-4 border-b text-left">Détails</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    if (history.length === 0) {
        html += `
            <tr>
                <td colspan="4" class="py-4 px-4 text-center text-gray-500 dark:text-gray-400">
                    Aucune opération enregistrée dans l'historique.
                </td>
            </tr>
        `;
    } else {
        // Trier l'historique par date (du plus récent au plus ancien)
        history.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        history.forEach(entry => {
            // Formater la date
            const date = new Date(entry.timestamp);
            const formattedDate = date.toLocaleString();
            
            // Formater les détails
            let details = '';
            if (entry.details) {
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
            }
            
            html += `
                <tr class="border-b border-gray-200 dark:border-gray-700">
                    <td class="py-2 px-4">${formattedDate}</td>
                    <td class="py-2 px-4">${entry.action}</td>
                    <td class="py-2 px-4">${entry.capteur_nom || '-'}</td>
                    <td class="py-2 px-4">${details || '-'}</td>
                </tr>
            `;
        });
    }
    
    html += `
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h3 class="text-lg font-semibold mb-4">💬 Remarques</h3>
            <ul class="list-disc list-inside space-y-2 ml-4 text-gray-700 dark:text-gray-300">
                <li>L'historique enregistre toutes les opérations importantes effectuées dans l'application.</li>
                <li>Vous pouvez exporter l'historique au format CSV pour le conserver ou l'analyser.</li>
                <li>L'historique est conservé localement sur votre ordinateur.</li>
            </ul>
        </div>
    `;
    
    // Mettre à jour le contenu de la page
    historyPage.innerHTML = html;
}

// Afficher les détails d'une entrée d'historique
function showHistoryDetails(entryId) {
    const entry = historyEntries.find(e => e.id === entryId);
    if (!entry) return;
    
    let detailsContent = '';
    
    // Générer le contenu en fonction du type d'action
    switch (entry.action) {
        case 'Ajout capteur':
            detailsContent = `
                <p><strong>Capteur:</strong> ${entry.capteur_nom}</p>
                <p><strong>Date:</strong> ${new Date(entry.timestamp).toLocaleString()}</p>
            `;
            break;
        case 'Association fichier':
            detailsContent = `
                <p><strong>Capteur:</strong> ${entry.capteur_nom}</p>
                <p><strong>Fichier:</strong> ${entry.details.file_path.split('/').pop().split('\\').pop()}</p>
                <p><strong>Date:</strong> ${new Date(entry.timestamp).toLocaleString()}</p>
            `;
            break;
        case 'Mappage colonnes':
            detailsContent = `
                <p><strong>Capteur:</strong> ${entry.capteur_nom}</p>
                <p><strong>Colonnes mappées:</strong></p>
                <ul class="list-disc list-inside ml-4">
                    <li>Date: ${entry.details.columns.date || '-'}</li>
                    <li>Température: ${entry.details.columns.temperature || '-'}</li>
                    <li>Humidité: ${entry.details.columns.humidity || '-'}</li>
                </ul>
                <p><strong>Date:</strong> ${new Date(entry.timestamp).toLocaleString()}</p>
            `;
            break;
        case 'Génération graphique':
            detailsContent = `
                <p><strong>Type de graphique:</strong> ${entry.details.graph_type}</p>
                <p><strong>Capteurs inclus:</strong> ${entry.details.capteurs.join(', ')}</p>
                <p><strong>Date:</strong> ${new Date(entry.timestamp).toLocaleString()}</p>
            `;
            break;
        case 'Export graphique':
            detailsContent = `
                <p><strong>Fichier:</strong> ${entry.details.file_path.split('/').pop().split('\\').pop()}</p>
                <p><strong>Format:</strong> ${entry.details.format.toUpperCase()}</p>
                <p><strong>Date:</strong> ${new Date(entry.timestamp).toLocaleString()}</p>
            `;
            break;
        default:
            detailsContent = `
                <p><strong>Action:</strong> ${entry.action}</p>
                <p><strong>Date:</strong> ${new Date(entry.timestamp).toLocaleString()}</p>
                <pre class="bg-gray-100 dark:bg-gray-700 p-2 rounded mt-2 overflow-auto">${JSON.stringify(entry.details, null, 2)}</pre>
            `;
    }
    
    const actions = [
        {
            text: 'Fermer',
            class: 'btn-primary',
            onClick: hideModal
        }
    ];
    
    showModal(`Détails - ${entry.action}`, detailsContent, actions);
}

// Exporter l'historique
function exportHistory() {
    showLoading('Exportation de l\'historique...');
    
    pywebview.api.export_history().then(response => {
        hideLoading();
        
        if (response.success) {
            showNotification('Historique exporté avec succès', 'success');
        } else {
            showNotification(response.message || 'Erreur lors de l\'exportation de l\'historique', 'error');
        }
    }).catch(error => {
        hideLoading();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}
