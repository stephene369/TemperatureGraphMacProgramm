// Variables globales
let currentPage = 'home';
let isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser le thème
    updateTheme();
    
    // Ajouter les écouteurs d'événements pour la navigation
    document.querySelectorAll('.nav-item[data-page]').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            navigateTo(this.dataset.page);
        });
    });
    
    // Écouteur pour le bouton de thème
    // document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
    
    // Écouteur pour le menu mobile
    document.getElementById('mobile-menu-btn').addEventListener('click', toggleMobileMenu);
    
    // Charger les informations de l'application
    loadAppInfo();
});

// Charger les informations de l'application
function loadAppInfo() {
    pywebview.api.get_app_info().then(response => {
        if (response.success) {
            console.log('App info:', response);
        }
    }).catch(error => {
        console.error('Error loading app info:', error);
    });
}

// Navigation
function navigateTo(page) {
    // Masquer toutes les pages
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });
    
    // Désactiver tous les liens de navigation
    document.querySelectorAll('.nav-item[data-page]').forEach(item => {
        item.classList.remove('active');
    });
    
    // Activer la page et le lien correspondants
    document.getElementById(`${page}-page`).classList.add('active');
    document.querySelector(`.nav-item[data-page="${page}"]`).classList.add('active');
    
    // Mettre à jour le titre de la page
    updatePageTitle(page);
    
    // Fermer le menu mobile si ouvert
    document.getElementById('sidebar').classList.remove('open');
    
    // Mettre à jour la page courante
    currentPage = page;
    
    // Charger le contenu spécifique à la page
    loadPageContent(page);
}

// Mettre à jour le titre de la page
function updatePageTitle(page) {
    let title = '';
    
    switch (page) {
        case 'home':
            title = 'Accueil';
            break;
        case 'capteurs':
            title = 'Capteurs & Fichiers';
            break;
        case 'mapping':
            title = 'Mappage des Colonnes';
            break;
        case 'graphs':
            title = 'Graphiques';
            break;
        case 'history':
            title = 'Historique';
            break;
        default:
            title = 'ClimaGraph';
    }
    
    document.getElementById('page-title').textContent = title;
    document.title = `ClimaGraph - ${title}`;
}

// Charger le contenu spécifique à la page
function loadPageContent(page) {
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

// Basculer le thème clair/sombre
function toggleTheme() {
    isDarkMode = !isDarkMode;
    updateTheme();
}

// Mettre à jour le thème
function updateTheme() {
    if (isDarkMode) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
}

// Basculer le menu mobile
function toggleMobileMenu() {
    document.getElementById('sidebar').classList.toggle('open');
}

// Afficher une notification
function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    
    // Créer la notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    // Icône en fonction du type
    let icon = '';
    switch (type) {
        case 'success':
            icon = '✅';
            break;
        case 'error':
            icon = '❌';
            break;
        case 'warning':
            icon = '⚠️';
            break;
        default:
            icon = 'ℹ️';
    }
    
    // Contenu de la notification
    notification.innerHTML = `
        <span class="notification-icon">${icon}</span>
        <span>${message}</span>
    `;
    
    // Ajouter au conteneur
    container.appendChild(notification);
    
    // Afficher avec animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Masquer après 5 secondes
    setTimeout(() => {
        notification.classList.remove('show');
        
        // Supprimer après l'animation
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

// Afficher un modal
function showModal(title, content, actions = []) {
    const modalContainer = document.getElementById('modal-container');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const modalFooter = document.getElementById('modal-footer');
    
    // Définir le titre et le contenu
    modalTitle.textContent = title;
    modalBody.innerHTML = content;
    
    // Ajouter les boutons d'action
    modalFooter.innerHTML = '';
    actions.forEach(action => {
        const button = document.createElement('button');
        button.textContent = action.text;
        button.className = action.class || 'btn-secondary';
        if (action.id) {
            button.id = action.id;
        }
        button.addEventListener('click', action.onClick);
        modalFooter.appendChild(button);
    });
    
    // Afficher le modal
    modalContainer.classList.remove('hidden');
}

// Masquer le modal
function hideModal() {
    document.getElementById('modal-container').classList.add('hidden');
}

// Afficher l'overlay de chargement
function showLoading(text = 'Chargement...') {
    document.getElementById('loading-text').textContent = text;
    document.getElementById('loading-overlay').classList.remove('hidden');
}

// Masquer l'overlay de chargement
function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}




