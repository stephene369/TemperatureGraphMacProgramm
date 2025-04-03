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
    
    // Afficher la page correspondante
    const pages = document.querySelectorAll('.page');
    pages.forEach(p => {
        p.classList.remove('active');
    });
    
    const currentPage = document.getElementById(`${page}-page`);
    currentPage.classList.add('active');
    
    // Charger le contenu de la page si nécessaire
    loadPageContent(page);
    
    // Mettre à jour les actions du header
    updateHeaderActions(page);
}

function loadPageContent(page) {
    // Vérifier si le contenu est déjà chargé
    const pageElement = document.getElementById(`${page}-page`);
    if (pageElement.innerHTML.trim() === '') {
        // Afficher le chargement
        showLoading(`Chargement de la page ${page}...`);
        
        // Charger le contenu en fonction de la page
        switch (page) {
            case 'capteurs':
                loadCapteursPage();
                break;
            case 'mapping':
                loadMappingPage();
                break;
            case 'graphs':
                loadGraphsPage();
                break;
            case 'history':
                loadHistoryPage();
                break;
        }
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

// Fonctions utilitaires pour l'interface
function showLoading(message = 'Chargement en cours...') {
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    
    loadingText.textContent = message;
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    const loadingOverlay = document.getElementById('loading-overlay');
    loadingOverlay.classList.add('hidden');
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
