// Variables globales
let capteursPourGraphs = [];
let graphTypes = [];
let currentChart = null;
let currentGraphData = null;

// Chargement de la page des graphiques
function loadGraphsPage() {
    showLoading('Chargement des données...');
    
    // Charger les capteurs disponibles pour les graphiques
    pywebview.api.get_capteurs_for_graphs().then(response => {
        if (response.success) {
            capteursPourGraphs = response.capteurs;
            
            // Charger les types de graphiques
            return pywebview.api.get_graph_types();
        } else {
            throw new Error(response.message || 'Erreur lors du chargement des capteurs');
        }
    }).then(response => {
        hideLoading();
        
        if (response.success) {
            graphTypes = response.types;
            updateGraphsUI();
        } else {
            throw new Error(response.message || 'Erreur lors du chargement des types de graphiques');
        }
    }).catch(error => {
        hideLoading();
        showNotification(error.message || 'Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Mise à jour de l'interface des graphiques
function updateGraphsUI() {
    const graphsPage = document.getElementById('graphs-page');
    
    // Générer le contenu HTML
    let html = `
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
            <h3 class="text-lg font-semibold mb-4">📊 Graphiques</h3>
            <p class="mb-6">Générez des graphiques à partir de vos données climatiques.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div class="mb-4">
                    <label for="graph-type" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Type de graphique
                    </label>
                    <select id="graph-type" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                        <option value="">-- Sélectionnez un type --</option>
    `;
    
    // Ajouter les types de graphiques
    graphTypes.forEach(type => {
        html += `<option value="${type.id}">${type.name}</option>`;
    });
    
    html += `
                    </select>
                    <p id="graph-description" class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        Sélectionnez un type de graphique pour voir sa description.
                    </p>
                </div>
                
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Capteurs à inclure
                    </label>
                    <div class="max-h-40 overflow-y-auto border border-gray-300 dark:border-gray-600 rounded-md p-2 bg-white dark:bg-gray-700">
    `;
    
    if (capteursPourGraphs.length === 0) {
        html += `
                        <p class="text-gray-500 dark:text-gray-400 p-2">
                            Aucun capteur disponible. Veuillez d'abord ajouter des capteurs, leur associer des fichiers et mapper les colonnes.
                        </p>
                    </div>
                </div>
            </div>
        `;
    } else {
        capteursPourGraphs.forEach(capteur => {
            html += `
                        <div class="flex items-center mb-2">
                            <input type="checkbox" id="capteur-${capteur.id}" class="capteur-checkbox mr-2" value="${capteur.id}">
                            <label for="capteur-${capteur.id}" class="text-gray-900 dark:text-gray-100">${capteur.nom}</label>
                        </div>
            `;
        });
        
        html += `
                    </div>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        Sélectionnez les capteurs à inclure dans le graphique.
                    </p>
                </div>
            </div>
            
            <div class="flex justify-end mb-6">
                <button id="generate-graph-btn" class="btn-primary" onclick="generateGraph()">
                    Générer le graphique
                </button>
            </div>
            
            <div id="graph-container" class="hidden">
                <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-inner mb-4">
                    <h4 id="graph-title" class="text-lg font-semibold mb-4 text-center"></h4>
                    <div class="aspect-w-16 aspect-h-9">
                        <canvas id="graph-canvas"></canvas>
                    </div>
                </div>
                
                <div class="flex justify-end space-x-4">
                    <button id="export-png-btn" class="btn-secondary" onclick="exportGraph('png')">
                        Exporter en PNG
                    </button>
                    <button id="export-pdf-btn" class="btn-secondary" onclick="exportGraph('pdf')">
                        Exporter en PDF
                    </button>
                </div>
            </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h3 class="text-lg font-semibold mb-4">💬 Remarques</h3>
            <ul class="list-disc list-inside space-y-2 ml-4 text-gray-700 dark:text-gray-300">
                <li>Les graphiques sont générés à partir des données des capteurs sélectionnés.</li>
                <li>Certains types de graphiques nécessitent des données spécifiques (température, humidité, etc.).</li>
                <li>Vous pouvez exporter les graphiques en PNG ou PDF pour les inclure dans vos rapports.</li>
                <li>Pour de meilleurs résultats, assurez-vous que les données des capteurs couvrent la même période.</li>
            </ul>
        </div>
    `;
    }
    
    // Mettre à jour le contenu de la page
    graphsPage.innerHTML = html;
    
    // Ajouter l'écouteur d'événement pour le changement de type de graphique
    const graphTypeSelect = document.getElementById('graph-type');
    if (graphTypeSelect) {
        graphTypeSelect.addEventListener('change', updateGraphDescription);
    }
}

// Mise à jour de la description du graphique
function updateGraphDescription() {
    const graphTypeSelect = document.getElementById('graph-type');
    const graphDescription = document.getElementById('graph-description');
    
    const selectedType = graphTypes.find(type => type.id === graphTypeSelect.value);
    
    if (selectedType) {
        graphDescription.textContent = selectedType.description;
    } else {
        graphDescription.textContent = 'Sélectionnez un type de graphique pour voir sa description.';
    }
}

// Générer un graphique
function generateGraph() {
    // Récupérer le type de graphique sélectionné
    const graphTypeSelect = document.getElementById('graph-type');
    const graphType = graphTypeSelect.value;
    
    if (!graphType) {
        showNotification('Veuillez sélectionner un type de graphique', 'warning');
        return;
    }
    
    // Récupérer les capteurs sélectionnés
    const selectedCapteurs = [];
    document.querySelectorAll('.capteur-checkbox:checked').forEach(checkbox => {
        selectedCapteurs.push(checkbox.value);
    });
    
    if (selectedCapteurs.length === 0) {
        showNotification('Veuillez sélectionner au moins un capteur', 'warning');
        return;
    }
    
    // Désactiver le bouton pendant le traitement
    const generateButton = document.getElementById('generate-graph-btn');
    generateButton.disabled = true;
    generateButton.textContent = 'Génération...';
    
    showLoading('Génération du graphique...');
    
    // Générer le graphique
    pywebview.api.generate_graph(graphType, selectedCapteurs).then(response => {
        hideLoading();
        generateButton.disabled = false;
        generateButton.textContent = 'Générer le graphique';
        
        if (response.success) {
            currentGraphData = response.data;
            displayGraph(response.data);
        } else {
            showNotification(response.message || 'Erreur lors de la génération du graphique', 'error');
        }
    }).catch(error => {
        hideLoading();
        generateButton.disabled = false;
        generateButton.textContent = 'Générer le graphique';
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Afficher un graphique
function displayGraph(data) {
    // Afficher le conteneur du graphique
    const graphContainer = document.getElementById('graph-container');
    graphContainer.classList.remove('hidden');
    
    // Mettre à jour le titre du graphique
    document.getElementById('graph-title').textContent = data.title;
    
    // Récupérer le canvas
    const canvas = document.getElementById('graph-canvas');
    const ctx = canvas.getContext('2d');
    
    // Détruire le graphique existant s'il y en a un
    if (currentChart) {
        currentChart.destroy();
    }
    
    // Créer la configuration du graphique
    let config = {
        type: data.type,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {}
        }
    };
    
    // Configurer les données en fonction du type de graphique
    if (data.type === 'scatter') {
        config.data = {
            datasets: data.datasets
        };
        
        // Configurer les axes pour le graphique de dispersion
        config.options.scales = {
            x: {
                title: {
                    display: true,
                    text: data.x_axis
                }
            },
            y: {
                title: {
                    display: true,
                    text: data.y_axis
                }
            }
        };
    } else {
        config.data = {
            labels: data.labels,
            datasets: data.datasets
        };
        
        // Configurer les axes pour les autres types de graphiques
        config.options.scales = {
            x: {
                title: {
                    display: true,
                    text: data.x_axis
                }
            },
            y: {
                title: {
                    display: true,
                    text: data.y_axis
                }
            }
        };
    }
    
    // Créer le graphique
    currentChart = new Chart(ctx, config);
    
    // Faire défiler jusqu'au graphique
    graphContainer.scrollIntoView({ behavior: 'smooth' });
}

// Exporter un graphique
function exportGraph(format) {
    if (!currentChart) {
        showNotification('Aucun graphique à exporter', 'warning');
        return;
    }
    
    // Récupérer l'image du graphique
    const canvas = document.getElementById('graph-canvas');
    const imageData = canvas.toDataURL('image/png');
    
    // Demander le nom du fichier
    const title = document.getElementById('graph-title').textContent;
    const defaultFilename = title.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    
    const content = `
        <div class="mb-4">
            <label for="export-filename" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nom du fichier
            </label>
            <input type="text" id="export-filename" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" value="${defaultFilename}">
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Le fichier sera exporté au format ${format.toUpperCase()}.
            </p>
        </div>
    `;
    
    const actions = [
        {
            text: 'Annuler',
            class: 'btn-secondary',
            onClick: hideModal
        },
        {
            text: 'Exporter',
            class: 'btn-primary',
            id: 'export-btn',
            onClick: () => {
                const filename = document.getElementById('export-filename').value.trim() || defaultFilename;
                doExportGraph(imageData, filename, format);
            }
        }
    ];
    
    showModal(`Exporter en ${format.toUpperCase()}`, content, actions);
}

// Effectuer l'export du graphique
function doExportGraph(imageData, filename, format) {
    // Désactiver le bouton pendant le traitement
    const exportButton = document.getElementById('export-btn');
    exportButton.disabled = true;
    exportButton.textContent = 'Exportation...';
    
    // Envoyer la demande d'export à l'API
    pywebview.api.export_graph(imageData, filename, format).then(response => {
        hideModal();
        
        if (response.success) {
            showNotification(`Graphique exporté avec succès en ${format.toUpperCase()}`, 'success');
        } else {
            showNotification(response.message || `Erreur lors de l'export en ${format.toUpperCase()}`, 'error');
        }
    }).catch(error => {
        hideModal();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}
