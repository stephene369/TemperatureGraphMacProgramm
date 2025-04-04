// Navigation entre les pages
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            navigateTo(page);
        });
    });
}



function navigateTo(page) {
    // Mettre à jour les éléments de navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        if (item.getAttribute('data-page') === page) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Mettre à jour le titre de la page
    const pageTitle = document.getElementById('page-title');
    switch (page) {
        case 'home':
            pageTitle.textContent = 'Accueil';
            break;
        case 'capteurs':
            pageTitle.textContent = 'Capteurs & Fichiers';
            break;
        case 'mapping':
            pageTitle.textContent = 'Mappage des Colonnes';
            break;
        case 'graphs':
            pageTitle.textContent = 'Graphiques';
            break;
        case 'history':
            pageTitle.textContent = 'Historique';
            break;
    }
    
    // Trouver la page actuellement active
    const currentActivePage = document.querySelector('.page.active');
    const newPage = document.getElementById(`${page}-page`);
    
    if (!newPage) {
        console.error(`Page ${page}-page not found`);
        return;
    }
    
    // Si c'est déjà la page active, ne rien faire
    if (currentActivePage && currentActivePage.id === newPage.id) {
        return;
    }
    
    if (currentActivePage) {
        currentActivePage.classList.add('page-exit');
        
        setTimeout(() => {
            currentActivePage.classList.remove('active');
            currentActivePage.classList.remove('page-exit');
            
            newPage.classList.add('active');
            newPage.classList.add('page-enter');
            
            loadPageContent(page);
            
            // Mettre à jour les actions du header
            updateHeaderActions(page);
            
            // Retirer la classe d'animation après qu'elle soit terminée
            setTimeout(() => {
                newPage.classList.remove('page-enter');
            }, 50);
        }, 50); // Durée de l'animation de sortie
    } else {
        // Aucune page active, afficher directement la nouvelle page avec animation
        newPage.classList.add('active');
        newPage.classList.add('page-enter');
        
        // Charger le contenu de la page si nécessaire
        loadPageContent(page);
        
        // Mettre à jour les actions du header
        updateHeaderActions(page);
        
        // Retirer la classe d'animation après qu'elle soit terminée
        setTimeout(() => {
            newPage.classList.remove('page-enter');
        }, 50);
    }
}



function loadPageContent(page) {
    // Vérifier si le contenu est déjà chargé
    const pageElement = document.getElementById(`${page}-page`);
    if (pageElement.innerHTML.trim() === '') {
        // Afficher le chargement
        showLoading(`Chargement de la page ${page}...`);
        
        // Charger le contenu en fonction de la page
        let contentLoaded = false;
        
        switch (page) {
            case 'capteurs':
                loadCapteursPage(() => {
                    contentLoaded = true;
                    // Utiliser hideLoadingWithDelay au lieu de hideLoading
                    hideLoadingWithDelay();
                });
                break;
            case 'mapping':
                loadMappingPage(() => {
                    contentLoaded = true;
                    hideLoadingWithDelay();
                });
                break;
            case 'graphs':
                loadGraphsPage(() => {
                    contentLoaded = true;
                    hideLoadingWithDelay();
                });
                break;
            case 'history':
                loadHistoryPage(() => {
                    contentLoaded = true;
                    hideLoadingWithDelay();
                });
                break;
            default:
                // Si aucune page spécifique n'est chargée, simplement attendre 2 secondes
                hideLoadingWithDelay();
                break;
        }
        
        // Sécurité : si après 5 secondes le contenu n'est toujours pas chargé, masquer le loading
        setTimeout(() => {
            if (!contentLoaded) {
                hideLoading();
                showNotification("Le chargement a pris plus de temps que prévu.", "warning");
            }
        }, 5000);
    }
}








function updateHeaderActions(page) {
    const headerActions = document.getElementById('header-actions');
    headerActions.innerHTML = '';
    
    switch (page) {
        case 'capteurs':
            const addButton = document.createElement('button');
            addButton.className = 'btn-primary';
            addButton.innerHTML = '<span class="icon">➕</span> Ajouter un capteur';
            addButton.onclick = showAddCapteurModal;
            headerActions.appendChild(addButton);
            break;
        case 'graphs':
            const exportButton = document.createElement('button');
            exportButton.className = 'btn-primary';
            exportButton.innerHTML = '<span class="icon">💾</span> Exporter';
            exportButton.onclick = exportCurrentGraph;
            headerActions.appendChild(exportButton);
            break;
    }
}

// Variable pour suivre le moment où le loading a commencé
let loadingStartTime = 0;

// Fonctions utilitaires pour l'interface
function showLoading(message = 'Chargement en cours...') {
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    
    // Enregistrer le moment où le loading a commencé
    loadingStartTime = Date.now();
    
    // Afficher le message de chargement
    loadingText.textContent = message;
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    // Calculer combien de temps s'est écoulé depuis le début du chargement
    const elapsedTime = Date.now() - loadingStartTime;
    const minLoadingTime = 2000; // 2 secondes minimum
    
    if (elapsedTime >= minLoadingTime) {
        // Si au moins 2 secondes se sont écoulées, masquer immédiatement
        const loadingOverlay = document.getElementById('loading-overlay');
        loadingOverlay.classList.add('hidden');
    } else {
        // Sinon, attendre que le temps minimum soit écoulé
        const remainingTime = minLoadingTime - elapsedTime;
        setTimeout(() => {
            const loadingOverlay = document.getElementById('loading-overlay');
            loadingOverlay.classList.add('hidden');
        }, remainingTime);
    }
}

// Fonction utilitaire pour garantir un temps de chargement minimum
function hideLoadingWithDelay(callback = null) {
    const elapsedTime = Date.now() - loadingStartTime;
    const minLoadingTime = 500; // 2 secondes minimum
    
    if (elapsedTime >= minLoadingTime) {
        // Si au moins 2 secondes se sont écoulées, exécuter immédiatement
        hideLoading();
        if (callback) callback();
    } else {
        // Sinon, attendre que le temps minimum soit écoulé
        const remainingTime = minLoadingTime - elapsedTime;
        setTimeout(() => {
            hideLoading();
            if (callback) callback();
        }, remainingTime);
    }
}


function showNotification(message, type = 'info', duration = 3000) {
    const container = document.getElementById('notification-container');
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    let icon = '💬';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';
    if (type === 'warning') icon = '⚠️';
    
    notification.innerHTML = `
        <span class="notification-icon">${icon}</span>
        <span class="notification-message">${message}</span>
    `;
    
    container.appendChild(notification);
    
    // Animation d'entrée
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Suppression après la durée spécifiée
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, duration);
}

function showModal(title, content, actions = []) {
    const modalContainer = document.getElementById('modal-container');
    const modalContent = document.getElementById('modal-content');
    
    // Créer le contenu du modal
    modalContent.innerHTML = `
        <div class="modal-header p-4 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-semibold">${title}</h3>
            <button class="modal-close">×</button>
        </div>
        <div class="modal-body p-4">
            ${content}
        </div>
        <div class="modal-footer p-4 border-t border-gray-200 dark:border-gray-700 flex justify-end space-x-2">
            ${actions.map(action => `
                <button class="${action.class || 'btn-secondary'}" id="${action.id || ''}">${action.text}</button>
            `).join('')}
        </div>
    `;
    
    // Ajouter les gestionnaires d'événements
    const closeButton = modalContent.querySelector('.modal-close');
    closeButton.addEventListener('click', hideModal);
    
    // Ajouter les gestionnaires pour les boutons d'action
    actions.forEach(action => {
        if (action.id) {
            const button = modalContent.querySelector(`#${action.id}`);
            if (button && action.onClick) {
                button.addEventListener('click', action.onClick);
            }
        }
    });
    
    // Afficher le modal
    modalContainer.classList.remove('hidden');
}

function hideModal() {
    const modalContainer = document.getElementById('modal-container');
    modalContainer.classList.add('hidden');
}
