// Variables globales
let capteursPourMapping = [];
let selectedCapteurId = null;
let availableColumns = [];

// Chargement de la page de mappage
function loadMappingPage() {
    showLoading('Chargement des capteurs...');
    
    pywebview.api.get_capteurs_for_mapping().then(response => {
        hideLoading();
        
        if (response.success) {
            capteursPourMapping = response.capteurs;
            updateMappingUI();
        } else {
            showNotification(response.message || 'Erreur lors du chargement des capteurs', 'error');
        }
    }).catch(error => {
        hideLoading();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Mise à jour de l'interface de mappage
function updateMappingUI() {
    const mappingPage = document.getElementById('mapping-page');
    
    // Générer le contenu HTML
    let html = `
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
            <h3 class="text-lg font-semibold mb-4"><i class='bx bx-brain' style="color: #4a6cf7;"></i>
 Mappage des Colonnes</h3>
            <p class="mb-6">Définissez quelles colonnes correspondent à la date, la température et l'humidité.</p>
            
            <div class="mb-6">
                <label for="capteur-select" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Sélectionnez un capteur
                </label>
                <select id="capteur-select" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" onchange="onCapteurSelected()">
                    <option value="">-- Sélectionnez un capteur --</option>
    `;
    
    if (capteursPourMapping.length === 0) {
        html += `
                    <option disabled>Aucun capteur avec fichier disponible</option>
                </select>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    Veuillez d'abord ajouter des capteurs et leur associer des fichiers.
                </p>
            </div>
        </div>
        `;
    } else {
        capteursPourMapping.forEach(capteur => {
            html += `<option value="${capteur.id}">${capteur.nom}</option>`;
        });
        
        html += `
                </select>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    Seuls les capteurs avec des fichiers associés sont affichés.
                </p>
            </div>
            
            <div id="mapping-form" class="hidden">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="mb-4">
                        <label for="date-column" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Colonne de date <span class="text-red-500">*</span>
                        </label>
                        <select id="date-column" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                            <option value="">-- Sélectionnez une colonne --</option>
                        </select>
                        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                            Colonne contenant les dates/heures des mesures.
                        </p>
                    </div>
                    
                    <div class="mb-4">
                        <label for="temperature-column" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Colonne de température <span class="text-red-500">*</span>
                        </label>
                        <select id="temperature-column" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                            <option value="">-- Sélectionnez une colonne --</option>
                        </select>
                        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                            Colonne contenant les valeurs de température.
                        </p>
                    </div>
                    
                    <div class="mb-4">
                        <label for="humidity-column" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Colonne d'humidité (optionnelle)
                        </label>
                        <select id="humidity-column" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                            <option value="">-- Sélectionnez une colonne --</option>
                        </select>
                        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                            Colonne contenant les valeurs d'humidité (si disponible).
                        </p>
                    </div>
                </div>
                
                <div class="mb-6">
                    <h4 class="font-semibold mb-2">Aperçu des données</h4>
                    <div id="data-preview" class="overflow-x-auto">
                        <p class="text-gray-500 dark:text-gray-400">
                            Sélectionnez un capteur pour voir un aperçu des données.
                        </p>
                    </div>
                </div>
                
                <div class="flex justify-end">
                    <button id="save-mapping-btn" class="btn-primary" onclick="saveMapping()">
                        Enregistrer le mappage
                    </button>
                </div>
            </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h3 class="text-lg font-semibold mb-4">💬 Remarques</h3>
            <ul class="list-disc list-inside space-y-2 ml-4 text-gray-700 dark:text-gray-300">
                <li>L'application tente de détecter automatiquement les colonnes, mais vous pouvez les modifier ici.</li>
                <li>Les colonnes de date et de température sont obligatoires.</li>
                <li>La colonne d'humidité est optionnelle, mais recommandée pour certains graphiques.</li>
                <li>Une fois le mappage enregistré, vous pourrez générer des graphiques à partir de ces données.</li>
            </ul>
        </div>
    `;
    }
    
    // Mettre à jour le contenu de la page
    mappingPage.innerHTML = html;
}

// Gestion de la sélection d'un capteur
function onCapteurSelected() {
    const capteurSelect = document.getElementById('capteur-select');
    const capteurId = capteurSelect.value;
    
    if (!capteurId) {
        document.getElementById('mapping-form').classList.add('hidden');
        return;
    }
    
    selectedCapteurId = capteurId;
    
    showLoading('Chargement des colonnes...');
    
    // Charger les colonnes disponibles
    pywebview.api.get_columns_for_mapping(capteurId).then(response => {
        if (response.success) {
            availableColumns = response.columns;
            updateColumnSelects();
            loadDataPreview();
        } else {
            hideLoading();
            showNotification(response.message || 'Erreur lors du chargement des colonnes', 'error');
        }
    }).catch(error => {
        hideLoading();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Mise à jour des sélecteurs de colonnes
function updateColumnSelects() {
    const dateSelect = document.getElementById('date-column');
    const temperatureSelect = document.getElementById('temperature-column');
    const humiditySelect = document.getElementById('humidity-column');
    
    // Vider les sélecteurs
    dateSelect.innerHTML = '<option value="">-- Sélectionnez une colonne --</option>';
    temperatureSelect.innerHTML = '<option value="">-- Sélectionnez une colonne --</option>';
    humiditySelect.innerHTML = '<option value="">-- Sélectionnez une colonne --</option>';
    
    // Ajouter les colonnes disponibles
    availableColumns.forEach(column => {
        dateSelect.innerHTML += `<option value="${column}">${column}</option>`;
        temperatureSelect.innerHTML += `<option value="${column}">${column}</option>`;
        humiditySelect.innerHTML += `<option value="${column}">${column}</option>`;
    });
    
    // Sélectionner les valeurs actuelles si disponibles
    const capteur = capteursPourMapping.find(c => c.id === selectedCapteurId);
    if (capteur && capteur.columns) {
        if (capteur.columns.date) {
            dateSelect.value = capteur.columns.date;
        }
        if (capteur.columns.temperature) {
            temperatureSelect.value = capteur.columns.temperature;
        }
        if (capteur.columns.humidity) {
            humiditySelect.value = capteur.columns.humidity;
        }
    }
    
    // Afficher le formulaire
    document.getElementById('mapping-form').classList.remove('hidden');
}

// Charger l'aperçu des données
function loadDataPreview() {
    pywebview.api.get_data_preview(selectedCapteurId).then(response => {
        hideLoading();
        
        if (response.success) {
            updateDataPreview(response.preview);
        } else {
            showNotification(response.message || 'Erreur lors du chargement de l\'aperçu', 'error');
        }
    }).catch(error => {
        hideLoading();
        updateDataPreview(response.preview);
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Mise à jour de l'aperçu des données
function updateDataPreview(preview) {
    const previewContainer = document.getElementById('data-preview');
    
    let html = `
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <thead>
                    <tr class="bg-gray-100 dark:bg-gray-700">
    `;
    
    // En-têtes de colonnes
    preview.columns.forEach(column => {
        html += `<th class="py-2 px-4 border-b text-left">${column}</th>`;
    });
    
    html += `
                    </tr>
                </thead>
                <tbody>
    `;
    
    // Lignes de données
    preview.data.forEach(row => {
        html += `<tr class="border-b border-gray-200 dark:border-gray-700">`;
        row.forEach(cell => {
            html += `<td class="py-2 px-4">${cell !== null ? cell : ''}</td>`;
        });
        html += `</tr>`;
    });
    
    html += `
                </tbody>
            </table>
        </div>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Aperçu des ${preview.data.length} premières lignes du fichier.
        </p>
    `;
    
    previewContainer.innerHTML = html;
}

// Enregistrer le mappage des colonnes
function saveMapping() {
    const dateColumn = document.getElementById('date-column').value;
    const temperatureColumn = document.getElementById('temperature-column').value;
    const humidityColumn = document.getElementById('humidity-column').value;
    
    // Vérifier que les colonnes obligatoires sont sélectionnées
    if (!dateColumn) {
        showNotification('Veuillez sélectionner une colonne de date', 'warning');
        return;
    }
    
    if (!temperatureColumn) {
        showNotification('Veuillez sélectionner une colonne de température', 'warning');
        return;
    }
    
    // Préparer le mappage
    const mapping = {
        date: dateColumn,
        temperature: temperatureColumn
    };
    
    if (humidityColumn) {
        mapping.humidity = humidityColumn;
    }
    
    // Désactiver le bouton pendant le traitement
    const saveButton = document.getElementById('save-mapping-btn');
    saveButton.disabled = true;
    saveButton.textContent = 'Enregistrement...';
    
    // Envoyer le mappage à l'API
    pywebview.api.save_column_mapping(selectedCapteurId, mapping).then(response => {
        saveButton.disabled = false;
        saveButton.textContent = 'Enregistrer le mappage';
        
        if (response.success) {
            showNotification('Mappage enregistré avec succès', 'success');
            loadMappingPage();  // Recharger la page
        } else {
            showNotification(response.message || 'Erreur lors de l\'enregistrement du mappage', 'error');
        }
    }).catch(error => {
        saveButton.disabled = false;
        saveButton.textContent = 'Enregistrer le mappage';
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}
