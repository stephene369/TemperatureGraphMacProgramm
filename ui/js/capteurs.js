// Variables globales
let capteurs = [];

// Chargement de la page des capteurs
function loadCapteursPage() {
    // showLoading('Chargement des capteurs...');
    pywebview.api.get_capteurs().then(response => {
        hideLoading();
        
        if (response.success) {
            capteurs = response.capteurs;
            updateCapteursUI();
        } else {
            showNotification(response.message || 'Erreur lors du chargement des capteurs', 'error');
        }
    }).catch(error => {
        hideLoading();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Mise à jour de l'interface des capteurs
function updateCapteursUI() {
    const capteursPage = document.getElementById('capteurs-page');
    
    // Générer le contenu HTML
    let html = `
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
            <h3 class="text-lg font-semibold mb-4">📁 Capteurs & Fichiers</h3>
            <p class="mb-6">Ajoutez vos capteurs et associez-leur des fichiers de données.</p>
            
            <button class="btn-primary mb-6" onclick="showAddCapteurModal()">
                <span class="icon">➕</span> Ajouter un capteur
            </button>
            
            <div class="overflow-x-auto">
                <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                    <thead>
                        <tr class="bg-gray-100 dark:bg-gray-700">
                            <th class="py-2 px-4 border-b text-left">Nom</th>
                            <th class="py-2 px-4 border-b text-left">Fichier</th>
                            <th class="py-2 px-4 border-b text-left">Colonnes mappées</th>
                            <th class="py-2 px-4 border-b text-left">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    if (capteurs.length === 0) {
        html += `
            <tr>
                <td colspan="4" class="py-4 px-4 text-center text-gray-500 dark:text-gray-400">
                    Aucun capteur ajouté. Cliquez sur "Ajouter un capteur" pour commencer.
                </td>
            </tr>
        `;
    } else {
        capteurs.forEach(capteur => {
            // Déterminer le statut des colonnes
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
            
            // Déterminer le statut du fichier
            let fichierStatus = capteur.file_path ? 
                capteur.file_path.split('/').pop().split('\\').pop() : 
                'Non associé';
            let fichierClass = capteur.file_path ? 
                'text-green-500 dark:text-green-400' : 
                'text-red-500 dark:text-red-400';
            
            html += `
                <tr class="border-b border-gray-200 dark:border-gray-700">
                    <td class="py-2 px-4">${capteur.nom}</td>
                    <td class="py-2 px-4 ${fichierClass}">${fichierStatus}</td>
                    <td class="py-2 px-4 ${colonnesClass}">${colonnesStatus}</td>
                    <td class="py-2 px-4">
                        <div class="flex space-x-2">
                            <button class="btn-icon text-blue-500" onclick="showEditCapteurModal('${capteur.id}')">
                                ✏️
                            </button>
                            <button class="btn-icon text-green-500" onclick="selectFile('${capteur.id}')">
                                📄
                            </button>
                            <button class="btn-icon text-red-500" onclick="showDeleteCapteurModal('${capteur.id}')">
                                🗑️
                            </button>
                        </div>
                    </td>
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
                <li>Un capteur correspond à un point de mesure.</li>
                <li>Les fichiers peuvent être en .xlsx, .xls ou .hobo.</li>
                <li>L'application tentera de détecter automatiquement les colonnes de date, température et humidité.</li>
                <li>Si la détection automatique échoue, vous serez redirigé vers la page de mappage des colonnes.</li>
            </ul>
        </div>
    `;
    
    // Mettre à jour le contenu de la page
    capteursPage.innerHTML = html;
}

// Afficher le modal d'ajout de capteur
function showAddCapteurModal() {
    const content = `
        <div class="mb-4">
            <label for="capteur-nom" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nom du capteur
            </label>
            <input type="text" id="capteur-nom" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Exemple : "Nord", "Sud-Est", "Extérieur", etc.
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
            text: 'Ajouter',
            class: 'btn-primary',
            id: 'add-capteur-btn',
            onClick: addCapteur
        }
    ];
    
    showModal('Ajouter un capteur', content, actions);
    
    // Focus sur le champ de nom
    setTimeout(() => {
        document.getElementById('capteur-nom').focus();
    }, 100);
}

// Ajouter un capteur
function addCapteur() {
    const nomInput = document.getElementById('capteur-nom');
    const nom = nomInput.value.trim();
    
    if (!nom) {
        showNotification('Veuillez saisir un nom pour le capteur', 'warning');
        nomInput.focus();
        return;
    }
    
    // Désactiver le bouton pendant le traitement
    const addButton = document.getElementById('add-capteur-btn');
    addButton.disabled = true;
    addButton.textContent = 'Ajout en cours...';
    
    pywebview.api.add_capteur(nom).then(response => {
        hideModal();
        
        if (response.success) {
            showNotification(`Capteur "${nom}" ajouté avec succès`, 'success');
            loadCapteursPage();  // Recharger la liste des capteurs
        } else {
            showNotification(response.message || 'Erreur lors de l\'ajout du capteur', 'error');
        }
    }).catch(error => {
        hideModal();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Afficher le modal de modification de capteur
function showEditCapteurModal(capteurId) {
    const capteur = capteurs.find(c => c.id === capteurId);
    
    if (!capteur) {
        showNotification('Capteur non trouvé', 'error');
        return;
    }
    
    const content = `
        <div class="mb-4">
            <label for="capteur-nom-edit" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nom du capteur
            </label>
            <input type="text" id="capteur-nom-edit" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" value="${capteur.nom}">
        </div>
    `;
    
    const actions = [
        {
            text: 'Annuler',
            class: 'btn-secondary',
            onClick: hideModal
        },
        {
            text: 'Enregistrer',
            class: 'btn-primary',
            id: 'edit-capteur-btn',
            onClick: () => updateCapteur(capteurId)
        }
    ];
    
    showModal('Modifier le capteur', content, actions);
    
    // Focus sur le champ de nom
    setTimeout(() => {
        document.getElementById('capteur-nom-edit').focus();
    }, 100);
}

// Mettre à jour un capteur
function updateCapteur(capteurId) {
    const nomInput = document.getElementById('capteur-nom-edit');
    const nom = nomInput.value.trim();
    
    if (!nom) {
        showNotification('Veuillez saisir un nom pour le capteur', 'warning');
        nomInput.focus();
        return;
    }
    
    // Désactiver le bouton pendant le traitement
    const editButton = document.getElementById('edit-capteur-btn');
    editButton.disabled = true;
    editButton.textContent = 'Enregistrement...';
    
    pywebview.api.update_capteur(capteurId, nom).then(response => {
        hideModal();
        
        if (response.success) {
            showNotification(`Capteur modifié avec succès`, 'success');
            loadCapteursPage();  // Recharger la liste des capteurs
        } else {
            showNotification(response.message || 'Erreur lors de la modification du capteur', 'error');
        }
    }).catch(error => {
        hideModal();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Afficher le modal de suppression de capteur
function showDeleteCapteurModal(capteurId) {
    const capteur = capteurs.find(c => c.id === capteurId);
    
    if (!capteur) {
        showNotification('Capteur non trouvé', 'error');
        return;
    }
    
    const content = `
        <p class="mb-4">Êtes-vous sûr de vouloir supprimer le capteur "${capteur.nom}" ?</p>
        <p class="text-red-500 dark:text-red-400">Cette action est irréversible.</p>
    `;
    
    const actions = [
        {
            text: 'Annuler',
            class: 'btn-secondary',
            onClick: hideModal
        },
        {
            text: 'Supprimer',
            class: 'btn-danger',
            id: 'delete-capteur-btn',
            onClick: () => deleteCapteur(capteurId)
        }
    ];
    
    showModal('Supprimer le capteur', content, actions);
}

// Supprimer un capteur
function deleteCapteur(capteurId) {
    // Désactiver le bouton pendant le traitement
    const deleteButton = document.getElementById('delete-capteur-btn');
    deleteButton.disabled = true;
    deleteButton.textContent = 'Suppression...';
    
    pywebview.api.delete_capteur(capteurId).then(response => {
        hideModal();
        
        if (response.success) {
            showNotification(`Capteur supprimé avec succès`, 'success');
            loadCapteursPage();  // Recharger la liste des capteurs
        } else {
            showNotification(response.message || 'Erreur lors de la suppression du capteur', 'error');
        }
    }).catch(error => {
        hideModal();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}

// Sélectionner un fichier pour un capteur
function selectFile(capteurId) {
    showLoading('Sélection du fichier...');
    
    pywebview.api.select_file(capteurId).then(response => {
        hideLoading();
        
        if (response.success) {
            showNotification('Fichier associé avec succès', 'success');
            
            // Si le mappage est nécessaire, rediriger vers la page de mappage
            if (response.needs_mapping) {
                showNotification('Veuillez mapper les colonnes pour ce fichier', 'info');
                navigateTo('mapping');
            } else {
                loadCapteursPage();  // Recharger la liste des capteurs
            }
        } else {
            showNotification(response.message || 'Erreur lors de l\'association du fichier', 'error');
        }
    }).catch(error => {
        hideLoading();
        showNotification('Erreur de communication avec l\'API', 'error');
        console.error('API error:', error);
    });
}
